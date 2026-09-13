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
    def get_all(cls):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM mentors").fetchall()
        conn.close()
        return [cls(row['id'], row['name'], row['email'], row['password_hash']) for row in rows]

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student:
    def __init__(self, id, name, email, password_hash, mentor_id):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.mentor_id = mentor_id

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
        return cls(new_id, name, email, password_hash, mentor_id)

    @classmethod
    def get_by_email(cls, email):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM students WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return cls(row['id'], row['name'], row['email'], row['password_hash'], row['mentor_id'])

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


def email_exists(email):
    """Cross-table uniqueness check — used during registration."""
    return Mentor.get_by_email(email) is not None or Student.get_by_email(email) is not None