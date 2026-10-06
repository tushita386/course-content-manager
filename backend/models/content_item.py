from dataclasses import dataclass
from typing import Optional


@dataclass
class ContentItem:
    TYPES = ("Note", "Link", "PDF reference", "Assignment resource")
    STATUSES = ("Not started", "In progress", "Completed")
    PENDING_STATUSES = ("Not started", "In progress")

    id: Optional[int]
    course_id: int
    title: str
    content_type: str
    link_or_description: Optional[str] = None
    status: str = "Not started"
    created_at: Optional[str] = None

    @property
    def is_pending(self):
        return self.status in self.PENDING_STATUSES

    @classmethod
    def from_row(cls, row):
        return cls(
            row["id"],
            row["course_id"],
            row["title"],
            row["content_type"],
            row["link_or_description"],
            row["status"],
            row["created_at"],
        )

    @classmethod
    def create(cls, conn, course_id, title, content_type,
               link_or_description=None, status="Not started"):
        cur = conn.execute(
            "INSERT INTO content_item "
            "(course_id, title, content_type, link_or_description, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (course_id, title, content_type, link_or_description, status),
        )
        conn.commit()
        return cls.get_by_id(conn, cur.lastrowid)

    @classmethod
    def get_by_id(cls, conn, item_id):
        row = conn.execute(
            "SELECT * FROM content_item WHERE id = ?", (item_id,)
        ).fetchone()
        return cls.from_row(row) if row else None

    @classmethod
    def get_by_course(cls, conn, course_id):
        rows = conn.execute(
            "SELECT * FROM content_item WHERE course_id = ? ORDER BY created_at, id",
            (course_id,),
        ).fetchall()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def update(cls, conn, item_id, title, content_type,
               link_or_description=None, status="Not started"):
        cur = conn.execute(
            "UPDATE content_item SET title = ?, content_type = ?, "
            "link_or_description = ?, status = ? WHERE id = ?",
            (title, content_type, link_or_description, status, item_id),
        )
        conn.commit()
        return cur.rowcount > 0

    @classmethod
    def delete(cls, conn, item_id):
        cur = conn.execute("DELETE FROM content_item WHERE id = ?", (item_id,))
        conn.commit()
        return cur.rowcount > 0