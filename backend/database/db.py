import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent
DATABASE_PATH = DB_DIR / "course_content.db"
SCHEMA_PATH = DB_DIR / "schema.sql"


def get_connection():
    """Open a SQLite connection with foreign keys enforced."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the tables from schema.sql if they do not exist."""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()