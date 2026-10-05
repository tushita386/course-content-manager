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