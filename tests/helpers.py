"""Shared helpers for the automated tests."""
import os
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path

from backend.app import app
from backend.database.db import SCHEMA_PATH, get_connection, init_db
from backend.models.user import User
from werkzeug.security import generate_password_hash


def memory_db():
    """A fresh in-memory database with the real schema and foreign keys on."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(Path(SCHEMA_PATH).read_text(encoding="utf-8"))
    return conn


class AppTestCase(unittest.TestCase):
    """Runs the Flask app against a temporary database file for each test.

    The real development database is never touched.
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmpdir, "test.db")
        self.previous_db = app.config["DATABASE"]
        app.config["DATABASE"] = self.db_path
        app.config["TESTING"] = True
        self.client = app.test_client()
        init_db(self.db_path)
        conn = get_connection(self.db_path)
        User.create(conn, "testteacher", generate_password_hash("teacherpass123"), "teacher")
        conn.close()
        self.client.post("/login", data={"username": "testteacher", "password": "teacherpass123"})

    def tearDown(self):
        app.config["DATABASE"] = self.previous_db
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def db(self):
        """A direct connection to this test's database, closed automatically."""
        init_db(self.db_path)
        conn = get_connection(self.db_path)
        self.addCleanup(conn.close)
        return conn

    def page(self, url):
        return self.client.get(url).get_data(as_text=True)

    def make_course(self, title="DBMS", category="Core", description=""):
        response = self.client.post(
            "/courses/new", data={"title": title, "category": category, "description": description}
        )
        self.assertEqual(response.status_code, 302)
        return int(response.headers["Location"].rstrip("/").split("/")[-1])

    def make_content(self, course_id, title="Notes", content_type="Note",
                     status="Not started", link_or_description=""):
        response = self.client.post(
            f"/courses/{course_id}/content/new",
            data={"title": title, "content_type": content_type, "status": status,
                  "link_or_description": link_or_description},
        )
        self.assertEqual(response.status_code, 302)
