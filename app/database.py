import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'course_content_manager.db')


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, like a dictionary
    conn.execute("PRAGMA foreign_keys = ON")  # enforce foreign key constraints
    return conn


def init_db():
    conn = get_connection()
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized successfully.")
