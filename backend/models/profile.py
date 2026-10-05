from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    email: str
    id: int = 1

    @classmethod
    def from_row(cls, row):
        return cls(row["name"], row["email"], row["id"])