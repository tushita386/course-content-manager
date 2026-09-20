from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_connection


class Instructor:
    def __init__(self, id, name, email, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def create(cls, name, email, password):
        password_hash = generate_password_hash(password)
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO instructors (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return cls(new_id, name, email, password_hash)

    @classmethod
    def get_by_email(cls, email):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM instructors WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['name'], row['email'], row['password_hash'])

    @classmethod
    def get_by_id(cls, instructor_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM instructors WHERE id = ?", (instructor_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['name'], row['email'], row['password_hash'])

    @classmethod
    def get_all(cls):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM instructors").fetchall()
        conn.close()
        return [cls(row['id'], row['name'], row['email'], row['password_hash']) for row in rows]

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student:
    def __init__(self, id, name, email, password_hash, instructor_id, current_semester=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.instructor_id = instructor_id
        self.current_semester = current_semester

    @classmethod
    def create(cls, name, email, password, instructor_id):
        password_hash = generate_password_hash(password)
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO students (name, email, password_hash, instructor_id) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, instructor_id)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return cls(new_id, name, email, password_hash, instructor_id, None)

    @classmethod
    def get_by_email(cls, email):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM students WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['name'], row['email'], row['password_hash'],
                    row['instructor_id'], row['current_semester'])

    @classmethod
    def get_by_id(cls, student_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['name'], row['email'], row['password_hash'],
                    row['instructor_id'], row['current_semester'])

    @classmethod
    def get_by_instructor(cls, instructor_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM students WHERE instructor_id = ?", (instructor_id,)
        ).fetchall()
        conn.close()
        return [cls(row['id'], row['name'], row['email'], row['password_hash'],
                     row['instructor_id'], row['current_semester']) for row in rows]

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_semester(self, semester):
        conn = get_connection()
        conn.execute(
            "UPDATE students SET current_semester = ? WHERE id = ?",
            (semester, self.id)
        )
        conn.commit()
        conn.close()
        self.current_semester = semester


def email_exists(email):
    """Cross-table uniqueness check — used during registration."""
    return Instructor.get_by_email(email) is not None or Student.get_by_email(email) is not None


class Course:
    def __init__(self, id, title, description, subject, semester, student_id):
        self.id = id
        self.title = title
        self.description = description
        self.subject = subject
        self.semester = semester
        self.student_id = student_id

    @classmethod
    def create(cls, title, description, subject, semester, student_id):
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO courses (title, description, subject, semester, student_id) VALUES (?, ?, ?, ?, ?)",
            (title, description, subject, semester, student_id)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return cls(new_id, title, description, subject, semester, student_id)

    @classmethod
    def get_by_student(cls, student_id, search=None, semester=None):
        query = "SELECT * FROM courses WHERE student_id = ?"
        params = [student_id]

        if search:
            query += " AND (title LIKE ? OR subject LIKE ?)"
            like_pattern = f"%{search}%"
            params.extend([like_pattern, like_pattern])

        if semester:
            query += " AND semester = ?"
            params.append(semester)

        query += " ORDER BY semester, title"

        conn = get_connection()
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [cls(row['id'], row['title'], row['description'], row['subject'],
                     row['semester'], row['student_id']) for row in rows]

    @classmethod
    def get_by_id(cls, course_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM courses WHERE id = ?", (course_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['title'], row['description'], row['subject'],
                    row['semester'], row['student_id'])

    @classmethod
    def auto_create_for_semester(cls, student_id, semester):
        """
        Looks up every subject in vtu_subjects for the given semester and
        creates a Course for each one the student doesn't already have
        (matched by title, within that same semester) — so calling this
        again later (e.g. re-visiting the semester page) never duplicates
        courses that already exist.
        """
        conn = get_connection()

        existing = conn.execute(
            "SELECT title FROM courses WHERE student_id = ? AND semester = ?",
            (student_id, semester)
        ).fetchall()
        existing_titles = {row['title'] for row in existing}

        subjects = conn.execute(
            "SELECT subject_name FROM vtu_subjects WHERE semester = ?",
            (semester,)
        ).fetchall()

        for row in subjects:
            subject_name = row['subject_name']
            if subject_name not in existing_titles:
                conn.execute(
                    "INSERT INTO courses (title, description, subject, semester, student_id) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (subject_name, '', '', semester, student_id)
                )

        conn.commit()
        conn.close()

    def update(self, title, description, subject, semester):
        conn = get_connection()
        conn.execute(
            "UPDATE courses SET title = ?, description = ?, subject = ?, semester = ? WHERE id = ?",
            (title, description, subject, semester, self.id)
        )
        conn.commit()
        conn.close()
        self.title = title
        self.description = description
        self.subject = subject
        self.semester = semester

    def delete(self):
        conn = get_connection()
        conn.execute("DELETE FROM courses WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()


VALID_STATUSES = ('Not Started', 'In Progress', 'Completed')


class Task:
    def __init__(self, id, title, notes, status, due_date, updated_at, created_by, course_id):
        self.id = id
        self.title = title
        self.notes = notes
        self.status = status
        self.due_date = due_date
        self.updated_at = updated_at
        self.created_by = created_by
        self.course_id = course_id

    @classmethod
    def create(cls, title, notes, status, due_date, course_id, created_by='student'):
        updated_at = datetime.utcnow().isoformat()
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO tasks (title, notes, status, due_date, updated_at, created_by, course_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, notes, status, due_date, updated_at, created_by, course_id)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return cls(new_id, title, notes, status, due_date, updated_at, created_by, course_id)

    @classmethod
    def get_by_course(cls, course_id, status=None):
        query = "SELECT * FROM tasks WHERE course_id = ?"
        params = [course_id]

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY due_date IS NULL, due_date"

        conn = get_connection()
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [cls(row['id'], row['title'], row['notes'], row['status'], row['due_date'],
                     row['updated_at'], row['created_by'], row['course_id']) for row in rows]

    @classmethod
    def get_by_id(cls, task_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['title'], row['notes'], row['status'], row['due_date'],
                    row['updated_at'], row['created_by'], row['course_id'])

    def update(self, title, notes, status, due_date):
        """Full update — used for the student's own tasks, and by the instructor
        editing a task they assigned. Not used for a student updating an
        instructor-assigned task; see update_status() for that restricted case."""
        updated_at = datetime.utcnow().isoformat()
        conn = get_connection()
        conn.execute(
            "UPDATE tasks SET title = ?, notes = ?, status = ?, due_date = ?, updated_at = ? "
            "WHERE id = ?",
            (title, notes, status, due_date, updated_at, self.id)
        )
        conn.commit()
        conn.close()
        self.title = title
        self.notes = notes
        self.status = status
        self.due_date = due_date
        self.updated_at = updated_at

    def update_status(self, status):
        """Restricted update — a student can only change the status of a task
        the instructor assigned to them; title/notes/due_date stay locked."""
        updated_at = datetime.utcnow().isoformat()
        conn = get_connection()
        conn.execute(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
            (status, updated_at, self.id)
        )
        conn.commit()
        conn.close()
        self.status = status
        self.updated_at = updated_at

    def delete(self):
        conn = get_connection()
        conn.execute("DELETE FROM tasks WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
