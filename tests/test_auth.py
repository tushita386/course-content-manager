import sqlite3
from werkzeug.security import generate_password_hash
from tests.helpers import AppTestCase
from backend.models.user import User


class AuthenticationAndRoleTests(AppTestCase):
    def test_login_rejects_invalid_credentials(self):
        self.client.post("/logout")
        response = self.client.post("/login", data={"username": "testteacher", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid username or password.", response.get_data(as_text=True))

    def test_login_and_logout(self):
        self.client.post("/logout")
        response = self.client.post("/login", data={"username": "testteacher", "password": "teacherpass123"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get("/").status_code, 200)
        self.client.post("/logout")
        self.assertEqual(self.client.get("/").status_code, 302)

    def test_teacher_can_create_student(self):
        response = self.client.post("/students", data={"username": "student1", "password": "studentpass123"})
        self.assertEqual(response.status_code, 302)
        student = User.get_by_username(self.db(), "student1")
        self.assertIsNotNone(student)
        self.assertEqual(student.role, "student")
        self.assertNotEqual(student.password_hash, "studentpass123")

    def test_teacher_cannot_create_short_password_or_duplicate(self):
        short = self.client.post("/students", data={"username": "student2", "password": "short"})
        self.assertEqual(short.status_code, 200)
        self.assertIn("at least 8 characters", short.get_data(as_text=True))
        self.client.post("/students", data={"username": "student1", "password": "studentpass123"})
        duplicate = self.client.post("/students", data={"username": "student1", "password": "studentpass456"})
        self.assertIn("already in use", duplicate.get_data(as_text=True))

    def test_student_can_read_but_cannot_mutate(self):
        conn = self.db()
        User.create(conn, "student1", generate_password_hash("studentpass123"), "student")
        course = self.make_course("DBMS")
        self.make_content(course, "Normalization notes")
        self.client.post("/logout")
        self.client.post("/login", data={"username": "student1", "password": "studentpass123"})
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/courses").status_code, 200)
        self.assertEqual(self.client.get(f"/courses/{course}").status_code, 200)
        self.assertEqual(self.client.get("/search?q=notes").status_code, 200)
        self.assertEqual(self.client.get("/students").status_code, 403)
        self.assertEqual(self.client.get("/profile").status_code, 403)
        self.assertEqual(self.client.get("/courses/new").status_code, 403)
        self.assertEqual(self.client.post("/courses/new", data={"title": "Injected"}).status_code, 403)
        self.assertEqual(self.client.post(f"/courses/{course}/delete").status_code, 403)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM course").fetchone()[0], 1)

    def test_unauthenticated_users_are_redirected_to_login(self):
        self.client.post("/logout")
        for path in ("/", "/courses", "/search?q=dbms", "/students"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login", response.headers["Location"])

    def test_students_cannot_register_or_assign_themselves_teacher(self):
        response = self.client.post("/register", data={"username": "evil", "password": "password123", "role": "teacher"})
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(User.get_by_username(self.db(), "evil"))
