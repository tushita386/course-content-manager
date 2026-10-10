from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    email: str
    id: int = 1

    @classmethod
    def from_row(cls, row):
        return cls(row["name"], row["email"], row["id"])

    @classmethod
    def get(cls, conn):
        """Return the saved profile, or None if it does not exist."""
        row = conn.execute(
            "SELECT * FROM profile WHERE id = 1"
        ).fetchone()
        return cls.from_row(row) if row else None

    @classmethod
    def save(cls, conn, name, email):
        """Create or replace the single profile."""
        conn.execute(
            "INSERT OR REPLACE INTO profile (id, name, email) VALUES (1, ?, ?)",
            (name, email),
        )
        conn.commit()
        return cls.get(conn)
