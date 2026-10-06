from dataclasses import dataclass
from typing import Optional


@dataclass
class Course:
    id: Optional[int]
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row):
        return cls(
            row["id"],
            row["title"],
            row["description"],
            row["category"],
            row["created_at"],
        )

    @classmethod
    def create(cls, conn, title, description=None, category=None):
        cur = conn.execute(
            "INSERT INTO course (title, description, category) VALUES (?, ?, ?)",
            (title, description, category),
        )
        conn.commit()
        return cls.get_by_id(conn, cur.lastrowid)

    @classmethod
    def get_all(cls, conn):
        rows = conn.execute(
            "SELECT * FROM course ORDER BY title COLLATE NOCASE"
        ).fetchall()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def get_by_id(cls, conn, course_id):
        row = conn.execute(
            "SELECT * FROM course WHERE id = ?", (course_id,)
        ).fetchone()
        return cls.from_row(row) if row else None

    @classmethod
    def update(cls, conn, course_id, title, description=None, category=None):
        cur = conn.execute(
            "UPDATE course SET title = ?, description = ?, category = ? WHERE id = ?",
            (title, description, category, course_id),
        )
        conn.commit()
        return cur.rowcount > 0

    @classmethod
    def delete(cls, conn, course_id):
        cur = conn.execute("DELETE FROM course WHERE id = ?", (course_id,))
        conn.commit()
        return cur.rowcount > 0