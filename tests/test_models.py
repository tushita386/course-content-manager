import sqlite3
import unittest

from backend.database.db import get_connection
from backend.models.content_item import ContentItem
from backend.models.course import Course
from backend.models.dashboard import get_dashboard
from backend.models.profile import Profile
from backend.models.search import search
from tests.helpers import AppTestCase, memory_db


class ProfileModelTests(unittest.TestCase):
    def setUp(self):
        self.conn = memory_db()
        self.addCleanup(self.conn.close)

    def test_get_before_save(self):
        """TC-M01 | FR-02 | There is no profile until one is saved"""
        self.assertIsNone(Profile.get(self.conn))

    def test_save_creates(self):
        """TC-M02 | FR-01, FR-02 | Saving creates the profile and it can be read back"""
        saved = Profile.save(self.conn, "Test User", "test@example.com")
        self.assertEqual(saved, Profile("Test User", "test@example.com", 1))
        self.assertEqual(Profile.get(self.conn), saved)

    def test_save_replaces(self):
        """TC-M03 | FR-01 | Saving again replaces the profile and keeps a single row"""
        Profile.save(self.conn, "A", "a@b.co")
        Profile.save(self.conn, "B", "b@b.co")
        self.assertEqual(Profile.get(self.conn).name, "B")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM profile").fetchone()[0], 1)

    def test_second_profile_rejected(self):
        """TC-M04 | FR-01 | The database rejects a second profile (id other than 1)"""
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("INSERT INTO profile (id, name, email) VALUES (2, 'x', 'y')")


class CourseModelTests(unittest.TestCase):
    def setUp(self):
        self.conn = memory_db()
        self.addCleanup(self.conn.close)

    def test_create_and_list(self):
        """TC-M05 | FR-03, FR-04 | Courses are created and listed in alphabetical order"""
        Course.create(self.conn, "dbms", "Relational", "Core")
        Course.create(self.conn, "Algorithms")
        titles = [c.title for c in Course.get_all(self.conn)]
        self.assertEqual(titles, ["Algorithms", "dbms"])

    def test_get_by_id(self):
        """TC-M06 | FR-05 | A course is found by id and a missing id returns None"""
        course = Course.create(self.conn, "DBMS", "About", "Core")
        found = Course.get_by_id(self.conn, course.id)
        self.assertEqual((found.title, found.description, found.category), ("DBMS", "About", "Core"))
        self.assertIsNone(Course.get_by_id(self.conn, 999))

    def test_update(self):
        """TC-M07 | FR-06 | Updating a course changes its fields"""
        course = Course.create(self.conn, "DBMS")
        self.assertTrue(Course.update(self.conn, course.id, "DBMS Advanced", "New", "Core"))
        found = Course.get_by_id(self.conn, course.id)
        self.assertEqual((found.title, found.description, found.category), ("DBMS Advanced", "New", "Core"))
        self.assertFalse(Course.update(self.conn, 999, "x"))

    def test_delete_cascades(self):
        """TC-M08 | FR-07, NFR-04 | Deleting a course also deletes its content, leaving no orphans"""
        course = Course.create(self.conn, "DBMS")
        ContentItem.create(self.conn, course.id, "Notes", "Note")
        self.assertTrue(Course.delete(self.conn, course.id))
        self.assertIsNone(Course.get_by_id(self.conn, course.id))
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM content_item").fetchone()[0], 0)

    def test_delete_missing(self):
        """TC-M09 | FR-07 | Deleting a course that does not exist returns False"""
        self.assertFalse(Course.delete(self.conn, 999))


class ContentModelTests(unittest.TestCase):
    def setUp(self):
        self.conn = memory_db()
        self.addCleanup(self.conn.close)
        self.course = Course.create(self.conn, "DBMS")

    def test_create_defaults(self):
        """TC-M10 | FR-08, FR-11 | New content starts as Not started and counts as pending"""
        item = ContentItem.create(self.conn, self.course.id, "Notes", "Note")
        self.assertEqual(item.status, "Not started")
        self.assertTrue(item.is_pending)

    def test_update_status(self):
        """TC-M11 | FR-09, FR-11 | Updating content changes its fields and status"""
        item = ContentItem.create(self.conn, self.course.id, "Notes", "Note")
        self.assertTrue(ContentItem.update(self.conn, item.id, "Notes v2", "Link", "https://example.com", "Completed"))
        found = ContentItem.get_by_id(self.conn, item.id)
        self.assertEqual((found.title, found.content_type, found.status), ("Notes v2", "Link", "Completed"))
        self.assertFalse(found.is_pending)

    def test_delete(self):
        """TC-M12 | FR-10 | Deleting content removes it; a missing id returns False"""
        item = ContentItem.create(self.conn, self.course.id, "Notes", "Note")
        self.assertTrue(ContentItem.delete(self.conn, item.id))
        self.assertIsNone(ContentItem.get_by_id(self.conn, item.id))
        self.assertFalse(ContentItem.delete(self.conn, 999))

    def test_database_rejects_invalid_status(self):
        """TC-M13 | FR-16 | The database itself rejects an invalid status or type"""
        with self.assertRaises(sqlite3.IntegrityError):
            ContentItem.create(self.conn, self.course.id, "Bad", "Note", None, "Finished")
        with self.assertRaises(sqlite3.IntegrityError):
            ContentItem.create(self.conn, self.course.id, "Bad", "Video")

    def test_content_belongs_to_course(self):
        """TC-M14 | FR-05 | Content is listed only under its own course, oldest first"""
        other = Course.create(self.conn, "Algorithms")
        ContentItem.create(self.conn, self.course.id, "First", "Note")
        ContentItem.create(self.conn, self.course.id, "Second", "Link")
        ContentItem.create(self.conn, other.id, "Elsewhere", "Note")
        titles = [i.title for i in ContentItem.get_by_course(self.conn, self.course.id)]
        self.assertEqual(titles, ["First", "Second"])


class SearchFilterTests(unittest.TestCase):
    def setUp(self):
        self.conn = memory_db()
        self.addCleanup(self.conn.close)
        self.dbms = Course.create(self.conn, "DBMS")
        self.algo = Course.create(self.conn, "Algorithms")
        ContentItem.create(self.conn, self.dbms.id, "Normalization notes", "Note", None, "Completed")
        ContentItem.create(self.conn, self.dbms.id, "SQL practice sheet", "Assignment resource", None, "In progress")
        ContentItem.create(self.conn, self.dbms.id, "ER diagram link", "Link")
        ContentItem.create(self.conn, self.algo.id, "Sorting notes", "Note")

    def titles(self, **filters):
        return [i.title for i in ContentItem.get_by_course(self.conn, self.dbms.id, **filters)]

    def test_search_content_titles(self):
        """TC-M15 | FR-12 | Search finds content titles and shows the course each belongs to"""
        result = search(self.conn, "notes")
        self.assertEqual(result["courses"], [])
        self.assertEqual([(i.title, c) for i, c in result["content"]],
                         [("Sorting notes", "Algorithms"), ("Normalization notes", "DBMS")])

    def test_search_course_titles_case_insensitive(self):
        """TC-M16 | FR-12 | Search finds course titles regardless of letter case"""
        result = search(self.conn, "dbms")
        self.assertEqual([c.title for c in result["courses"]], ["DBMS"])
        self.assertEqual(result["content"], [])

    def test_search_empty_keyword(self):
        """TC-M17 | FR-12 | An empty keyword returns no results"""
        self.assertEqual(search(self.conn, "   "), {"courses": [], "content": []})
        self.assertEqual(search(self.conn, None), {"courses": [], "content": []})

    def test_search_wildcards_are_literal(self):
        """TC-M18 | FR-12 | The characters % and _ are searched literally, not as wildcards"""
        self.assertEqual(search(self.conn, "%")["content"], [])
        self.assertEqual(search(self.conn, "_")["content"], [])
        ContentItem.create(self.conn, self.dbms.id, "100% done", "Note")
        self.assertEqual([i.title for i, _ in search(self.conn, "100%")["content"]], ["100% done"])

    def test_filters(self):
        """TC-M19 | FR-13 | Content can be filtered by type, by status and by both"""
        self.assertEqual(len(self.titles()), 3)
        self.assertEqual(self.titles(content_type="Note"), ["Normalization notes"])
        self.assertEqual(self.titles(status="In progress"), ["SQL practice sheet"])
        self.assertEqual(self.titles(content_type="Link", status="Not started"), ["ER diagram link"])
        self.assertEqual(self.titles(content_type="Note", status="Not started"), [])

    def test_unknown_filter_values_ignored(self):
        """TC-M20 | FR-13 | Unknown filter values are treated as All"""
        self.assertEqual(len(self.titles(content_type="All", status="Finished")), 3)


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.conn = memory_db()
        self.addCleanup(self.conn.close)
        self.dbms = Course.create(self.conn, "DBMS")
        self.algo = Course.create(self.conn, "Algorithms")
        self.empty = Course.create(self.conn, "Embedded Systems")
        ContentItem.create(self.conn, self.dbms.id, "Notes", "Note", None, "Completed")
        ContentItem.create(self.conn, self.dbms.id, "SQL sheet", "Assignment resource", None, "In progress")
        self.er = ContentItem.create(self.conn, self.dbms.id, "ER link", "Link")
        ContentItem.create(self.conn, self.algo.id, "Sorting notes", "Note", None, "Completed")

    @staticmethod
    def totals(d):
        return (d["total_courses"], d["total_content"], d["completed"], d["pending"])

    def test_totals(self):
        """TC-M21 | FR-14 | Dashboard totals count courses, content, completed and pending (D-04)"""
        self.assertEqual(self.totals(get_dashboard(self.conn)), (3, 4, 2, 2))

    def test_per_course_progress(self):
        """TC-M22 | FR-15 | Per-course progress shows completed/total, including courses with no content"""
        rows = [(p["title"], p["completed"], p["total"]) for p in get_dashboard(self.conn)["per_course"]]
        self.assertEqual(rows, [("Algorithms", 1, 1), ("DBMS", 1, 3), ("Embedded Systems", 0, 0)])

    def test_dashboard_follows_changes(self):
        """TC-M23 | FR-14 | Dashboard totals follow status changes and course deletion"""
        ContentItem.update(self.conn, self.er.id, "ER link", "Link", None, "Completed")
        self.assertEqual(self.totals(get_dashboard(self.conn)), (3, 4, 3, 1))
        Course.delete(self.conn, self.algo.id)
        self.assertEqual(self.totals(get_dashboard(self.conn)), (2, 3, 2, 1))

    def test_empty_database(self):
        """TC-M24 | FR-14 | An empty database gives all-zero totals"""
        conn = memory_db()
        self.addCleanup(conn.close)
        self.assertEqual(get_dashboard(conn),
                         {"total_courses": 0, "total_content": 0, "completed": 0, "pending": 0, "per_course": []})


class SafetyTests(AppTestCase):
    def test_sql_text_is_stored_literally(self):
        """TC-M25 | NFR-05 | SQL-looking text is stored as plain text and the tables stay intact"""
        conn = self.db()
        tricky = "x'); DROP TABLE course;--"
        course = Course.create(conn, tricky)
        ContentItem.create(conn, course.id, tricky, "Note")
        self.assertEqual(Course.get_by_id(conn, course.id).title, tricky)
        self.assertEqual([i.title for i in ContentItem.get_by_course(conn, course.id)], [tricky])
        self.assertEqual(len(search(conn, "DROP TABLE")["courses"]), 1)

    def test_foreign_keys_enabled(self):
        """TC-M26 | NFR-04 | Every connection from the helper has foreign keys switched on"""
        conn = get_connection(self.db_path)
        self.addCleanup(conn.close)
        self.assertEqual(conn.execute("PRAGMA foreign_keys").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
