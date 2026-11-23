"""User account operations for teacher/student authentication."""
from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str

    @classmethod
    def from_row(cls, row):
        return cls(row["id"], row["username"], row["password_hash"], row["role"])

    @classmethod
    def get_by_id(cls, db, user_id):
        row = db.execute(
            "SELECT id, username, password_hash, role FROM app_user WHERE id = ?", (user_id,)
        ).fetchone()
        return cls.from_row(row) if row else None

    @classmethod
    def get_by_username(cls, db, username):
        row = db.execute(
            "SELECT id, username, password_hash, role FROM app_user WHERE username = ? COLLATE NOCASE",
            (username,),
        ).fetchone()
        return cls.from_row(row) if row else None

    @classmethod
    def get_by_role(cls, db, role):
        row = db.execute("SELECT id FROM app_user WHERE role = ? LIMIT 1", (role,)).fetchone()
        return row

    @classmethod
    def create(cls, db, username, password_hash, role):
        cursor = db.execute(
            "INSERT INTO app_user (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role),
        )
        db.commit()
        return cls.get_by_id(db, cursor.lastrowid)

    @classmethod
    def get_all_students(cls, db):
        rows = db.execute(
            "SELECT id, username, password_hash, role FROM app_user "
            "WHERE role = 'student' ORDER BY username COLLATE NOCASE"
        ).fetchall()
        return [cls.from_row(row) for row in rows]
