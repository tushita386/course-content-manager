from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_connection


class Mentor:
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
            "INSERT INTO mentors (name, email, password_hash) VALUES (?, ?, ?)",
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
            "SELECT * FROM mentors WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['name'], row['email'], row['password_hash'])

    @classmethod
    def get_by_id(cls, mentor_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM mentors WHERE id = ?", (mentor_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['name'], row['email'], row['password_hash'])

    @classmethod
    def get_all(cls):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM mentors").fetchall()
        conn.close()
        return [cls(row['id'], row['name'], row['email'], row['password_hash']) for row in rows]

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student:
    def __init__(self, id, name, email, password_hash, mentor_id, current_semester=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.mentor_id = mentor_id
        self.current_semester = current_semester

    @classmethod
    def create(cls, name, email, password, mentor_id):
        password_hash = generate_password_hash(password)
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO students (name, email, password_hash, mentor_id) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, mentor_id)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return cls(new_id, name, email, password_hash, mentor_id, None)

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
                    row['mentor_id'], row['current_semester'])

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
                    row['mentor_id'], row['current_semester'])

    @classmethod
    def get_by_mentor(cls, mentor_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM students WHERE mentor_id = ?", (mentor_id,)
        ).fetchall()
        conn.close()
        return [cls(row['id'], row['name'], row['email'], row['password_hash'],
                     row['mentor_id'], row['current_semester']) for row in rows]

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
    return Mentor.get_by_email(email) is not None or Student.get_by_email(email) is not None


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
    def get_by_student(cls, student_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM courses WHERE student_id = ?", (student_id,)
        ).fetchall()
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


class Content:
    def __init__(self, id, title, notes, status, due_date, updated_at, course_id):
        self.id = id
        self.title = title
        self.notes = notes
        self.status = status
        self.due_date = due_date
        self.updated_at = updated_at
        self.course_id = course_id

    @classmethod
    def create(cls, title, notes, status, due_date, course_id):
        updated_at = datetime.utcnow().isoformat()
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO content (title, notes, status, due_date, updated_at, course_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (title, notes, status, due_date, updated_at, course_id)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return cls(new_id, title, notes, status, due_date, updated_at, course_id)

    @classmethod
    def get_by_course(cls, course_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM content WHERE course_id = ? ORDER BY due_date IS NULL, due_date",
            (course_id,)
        ).fetchall()
        conn.close()
        return [cls(row['id'], row['title'], row['notes'], row['status'],
                     row['due_date'], row['updated_at'], row['course_id']) for row in rows]

    @classmethod
    def get_by_id(cls, content_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM content WHERE id = ?", (content_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['title'], row['notes'], row['status'],
                    row['due_date'], row['updated_at'], row['course_id'])

    def update(self, title, notes, status, due_date):
        updated_at = datetime.utcnow().isoformat()
        conn = get_connection()
        conn.execute(
            "UPDATE content SET title = ?, notes = ?, status = ?, due_date = ?, updated_at = ? "
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

    def delete(self):
        conn = get_connection()
        conn.execute("DELETE FROM content WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
