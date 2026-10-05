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