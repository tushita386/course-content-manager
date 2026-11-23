import html as htmllib
import re
import sqlite3
import time
from unittest import mock

from tests.helpers import AppTestCase


class DashboardAndProfileRouteTests(AppTestCase):
    def test_dashboard_shows_totals(self):
        """TC-R01 | FR-14, FR-15 | The dashboard shows totals and per-course progress"""
        course = self.make_course("DBMS")
        self.make_content(course, "Notes", status="Completed")
        self.make_content(course, "Sheet", "Assignment resource", status="In progress")
        self.make_content(course, "Link", "Link")
        html = self.page("/")
        self.assertIn("Progress by course", html)
        self.assertIn("1 / 3", html)
        self.assertRegex(html, r'<span class="num">1</span><span>Courses</span>')
        self.assertRegex(html, r'<span class="num">3</span><span>Content items</span>')
        self.assertRegex(html, r'<span class="num">1</span><span>Completed</span>')
        self.assertRegex(html, r'<span class="num">2</span><span>Pending</span>')

    def test_dashboard_empty(self):
        """TC-R02 | FR-14 | The dashboard works with no data and invites the user to add a course"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Add your first course", response.get_data(as_text=True))

    def test_profile_save_and_view(self):
        """TC-R03 | FR-01, FR-02 | A profile can be saved and is shown again on the profile page"""
        response = self.client.post("/profile", data={"name": "Test User", "email": "test@example.com"})
        self.assertEqual(response.status_code, 302)
        html = self.page("/profile?saved=1")
        self.assertIn("Profile saved.", html)
        self.assertIn('value="Test User"', html)
        self.assertIn('value="test@example.com"', html)
        self.client.post("/profile", data={"name": "Changed", "email": "c@example.com"})
        self.assertIn('value="Changed"', self.page("/profile"))

    def test_profile_invalid_input(self):
        """TC-R04 | FR-16 | An invalid profile shows messages, keeps the input and saves nothing"""
        response = self.client.post("/profile", data={"name": "", "email": "not-an-email"})
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Name is required.", html)
        self.assertIn("valid email", html)
        self.assertIn('value="not-an-email"', html)
        self.assertNotIn('value="Test', self.page("/profile"))

    def test_dashboard_greets_profile_name(self):
        """TC-R05 | FR-02 | The dashboard greets the user by the saved profile name"""
        self.assertNotIn("Welcome back", self.page("/"))
        self.client.post("/profile", data={"name": "Tushita", "email": "t@example.com"})
        self.assertIn("Welcome back, Tushita", self.page("/"))


class CourseRouteTests(AppTestCase):
    def test_create_redirects_to_detail(self):
        """TC-R06 | FR-03 | Saving a new course opens that course's detail page (D-04)"""
        response = self.client.post("/courses/new", data={"title": "DBMS", "category": "Core"})
        self.assertEqual(response.status_code, 302)
        self.assertRegex(response.headers["Location"], r"/courses/\d+$")
        self.assertIn("DBMS", self.page(response.headers["Location"]))

    def test_course_list(self):
        """TC-R07 | FR-04 | The course list shows each course with its number of content items"""
        first = self.make_course("DBMS", category="Core")
        self.make_course("Algorithms")
        self.make_content(first, "Notes")
        self.make_content(first, "Link", "Link")
        html = self.page("/courses")
        self.assertIn("DBMS", html)
        self.assertIn("Algorithms", html)
        self.assertIn("2 items", html)
        self.assertIn("0 items", html)
        self.assertLess(html.index("Algorithms"), html.index("DBMS"))

    def test_create_validation_error(self):
        """TC-R08 | FR-16 | An empty course title shows a message, keeps the input and saves nothing"""
        response = self.client.post("/courses/new", data={"title": "   ", "category": "Core", "description": "keep me"})
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Title is required.", html)
        self.assertIn("keep me", html)
        self.assertIn('value="Core"', html)
        self.assertIn("No courses yet", self.page("/courses"))

    def test_detail_shows_content_and_badges(self):
        """TC-R09 | FR-05 | The detail page shows the course, its content, types, status badges and progress"""
        course = self.make_course("DBMS", description="Relational databases")
        self.make_content(course, "Normalization notes", "Note", "Completed")
        self.make_content(course, "SQL sheet", "Assignment resource", "In progress")
        html = self.page(f"/courses/{course}")
        self.assertIn("Relational databases", html)
        self.assertIn("Normalization notes", html)
        self.assertIn("Assignment resource", html)
        self.assertIn("badge-completed", html)
        self.assertIn("badge-in-progress", html)
        self.assertIn("1 of 2 completed", html)

    def test_edit_course(self):
        """TC-R10 | FR-06 | Editing a course saves the change and returns to its detail page"""
        course = self.make_course("DBMS")
        self.assertIn('value="DBMS"', self.page(f"/courses/{course}/edit"))
        response = self.client.post(f"/courses/{course}/edit", data={"title": "DBMS 2", "category": "Core", "description": ""})
        self.assertEqual(response.status_code, 302)
        self.assertIn("DBMS 2", self.page(f"/courses/{course}"))
        bad = self.client.post(f"/courses/{course}/edit", data={"title": ""})
        self.assertEqual(bad.status_code, 400)
        self.assertIn("DBMS 2", self.page(f"/courses/{course}"))

    def test_delete_course(self):
        """TC-R11 | FR-07 | Deleting a course removes it and its content; the delete URL does not accept GET"""
        course = self.make_course("DBMS")
        self.make_content(course, "Notes")
        self.assertEqual(self.client.get(f"/courses/{course}/delete").status_code, 405)
        self.assertEqual(self.client.get(f"/courses/{course}").status_code, 200)
        response = self.client.post(f"/courses/{course}/delete")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(f"/courses/{course}").status_code, 404)
        self.assertEqual(self.db().execute("SELECT COUNT(*) FROM content_item").fetchone()[0], 0)


class ContentRouteTests(AppTestCase):
    def setUp(self):
        super().setUp()
        self.course = self.make_course("DBMS")

    def item_id(self, title):
        return self.db().execute("SELECT id FROM content_item WHERE title = ?", (title,)).fetchone()[0]

    def test_add_content(self):
        """TC-R12 | FR-08 | Adding content returns to the course page where the new item is listed"""
        response = self.client.post(
            f"/courses/{self.course}/content/new",
            data={"title": "Normalization notes", "content_type": "Note", "status": "Not started",
                  "link_or_description": "chapter 3"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith(f"/courses/{self.course}"))
        html = self.page(f"/courses/{self.course}")
        self.assertIn("Normalization notes", html)
        self.assertIn("chapter 3", html)

    def test_edit_content_status(self):
        """TC-R13 | FR-09, FR-11 | Editing content changes its fields and its status"""
        self.make_content(self.course, "Notes")
        item = self.item_id("Notes")
        self.assertIn('value="Notes"', self.page(f"/content/{item}/edit"))
        self.client.post(f"/content/{item}/edit",
                         data={"title": "Notes v2", "content_type": "Link", "status": "Completed",
                               "link_or_description": "https://example.com"})
        html = self.page(f"/courses/{self.course}")
        self.assertIn("Notes v2", html)
        self.assertIn("badge-completed", html)
        self.assertNotIn("badge-not-started", html)

    def test_delete_content(self):
        """TC-R14 | FR-10 | Deleting content removes it from the course page"""
        self.make_content(self.course, "Notes")
        item = self.item_id("Notes")
        self.assertEqual(self.client.get(f"/content/{item}/delete").status_code, 405)
        self.assertEqual(self.client.post(f"/content/{item}/delete").status_code, 302)
        self.assertNotIn("Notes", self.page(f"/courses/{self.course}").split("Learning content")[1])

    def test_invalid_content_rejected(self):
        """TC-R15 | FR-16 | Invalid content shows messages, keeps the input and saves nothing"""
        response = self.client.post(
            f"/courses/{self.course}/content/new",
            data={"title": "", "content_type": "Video", "status": "Finished", "link_or_description": "keep this"},
        )
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Title is required.", html)
        self.assertIn("Choose a content type", html)
        self.assertIn("Choose a status", html)
        self.assertIn("keep this", html)
        self.assertEqual(self.db().execute("SELECT COUNT(*) FROM content_item").fetchone()[0], 0)

    def test_filters_via_query_string(self):
        """TC-R16 | FR-13 | The course page filters content by type and status; unknown values show everything"""
        self.make_content(self.course, "Notes A", "Note", "Completed")
        self.make_content(self.course, "Site B", "Link", "In progress")
        self.make_content(self.course, "Sheet C", "Assignment resource", "Not started")
        by_status = self.page(f"/courses/{self.course}?status=In+progress")
        self.assertIn("Site B", by_status)
        self.assertNotIn("Notes A", by_status)
        by_type = self.page(f"/courses/{self.course}?type=Note")
        self.assertIn("Notes A", by_type)
        self.assertNotIn("Site B", by_type)
        none = self.page(f"/courses/{self.course}?type=Note&status=In+progress")
        self.assertIn("No content matches this filter.", none)
        everything = self.page(f"/courses/{self.course}?type=All&status=Finished")
        for title in ("Notes A", "Site B", "Sheet C"):
            self.assertIn(title, everything)

    def test_filter_selection_is_kept(self):
        """TC-R17 | FR-13 | The filter drop-downs keep the selected values"""
        html = self.page(f"/courses/{self.course}?type=Link&status=Completed")
        self.assertRegex(html, r'<option value="Link"\s+selected')
        self.assertRegex(html, r'<option value="Completed"\s+selected')


class SearchRouteTests(AppTestCase):
    def test_search_results_grouped(self):
        """TC-R18 | FR-12 | Search results list matching courses and matching content with their course"""
        notes_course = self.make_course("Notes Workshop")
        dbms = self.make_course("DBMS")
        self.make_content(dbms, "Normalization notes")
        html = self.page("/search?q=notes")
        self.assertIn("Notes Workshop", html)
        self.assertIn("Normalization notes", html)
        self.assertIn(f"/courses/{dbms}", html)
        self.assertIn(f"/courses/{notes_course}", html)

    def test_search_empty_and_no_match(self):
        """TC-R19 | FR-12 | An empty keyword asks for one, and no match says so"""
        self.make_course("DBMS")
        self.assertIn("Enter a keyword", self.page("/search?q="))
        self.assertIn("Enter a keyword", self.page("/search"))
        self.assertIn("No results found", self.page("/search?q=zzzz"))

    def test_search_is_case_insensitive(self):
        """TC-R20 | FR-12 | Searching in a different letter case finds the same course"""
        self.make_course("Database Systems")
        self.assertIn("Database Systems", self.page("/search?q=DATABASE"))
        self.assertIn("Database Systems", self.page("/search?q=systems"))


class ErrorHandlingTests(AppTestCase):
    def test_missing_records_show_friendly_page(self):
        """TC-R21 | FR-17, NFR-03 | Missing courses or content show a friendly not-found page, not a crash"""
        for url in ("/courses/999", "/courses/999/edit", "/courses/999/content/new", "/content/999/edit",
                    "/courses/abc", "/no-such-page"):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404, url)
            self.assertIn("Page not found", response.get_data(as_text=True), url)
        self.assertEqual(self.client.post("/courses/999/delete").status_code, 404)
        self.assertEqual(self.client.post("/content/999/delete").status_code, 404)

    def test_custom_404_page(self):
        """TC-R22 | FR-17 | The 404 page is the custom page with a way back to the app"""
        html = self.page("/courses/999")
        self.assertIn(">404<", html)
        self.assertIn("Back to the dashboard", html)
        self.assertIn('href="/courses"', html)

    def test_unexpected_error_is_friendly(self):
        """TC-R23 | FR-17, NFR-03 | An unexpected database error shows the custom 500 page without technical details"""
        with mock.patch("backend.app.Course.get_all", side_effect=sqlite3.OperationalError("secret detail")):
            with self.assertLogs("backend.app", level="ERROR"):
                response = self.client.get("/courses")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn(">500<", html)
        self.assertIn("Something went wrong", html)
        self.assertNotIn("secret detail", html)
        self.assertNotIn("OperationalError", html)
        self.assertNotIn("Traceback", html)


class QualityTests(AppTestCase):
    def test_html_is_escaped(self):
        """TC-R24 | NFR-05 | User text containing HTML is shown as text, not run"""
        course = self.make_course("<script>alert(1)</script>", description="<b>bold</b>")
        self.make_content(course, "<img src=x onerror=alert(1)>")
        for url in (f"/courses/{course}", "/courses", "/", "/search?q=script"):
            html = self.page(url)
            self.assertNotIn("<script>alert(1)</script>", html, url)
            self.assertNotIn("<img src=x", html, url)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", self.page("/courses"))

    def test_unsafe_link_is_not_clickable(self):
        """TC-R25 | NFR-05 | Only http and https links become clickable links"""
        course = self.make_course("DBMS")
        self.make_content(course, "Bad link", "Link", link_or_description="javascript:alert(1)")
        self.make_content(course, "Good link", "Link", link_or_description="https://example.com/page")
        html = self.page(f"/courses/{course}")
        self.assertNotIn('href="javascript:', html)
        self.assertIn('href="https://example.com/page"', html)

    def test_navigation_on_every_page(self):
        """TC-R26 | NFR-01 | Every main page offers links to the dashboard, courses and profile, and search"""
        course = self.make_course("DBMS")
        self.make_content(course, "Notes")
        urls = ["/", "/courses", "/courses/new", f"/courses/{course}", f"/courses/{course}/edit",
                f"/courses/{course}/content/new", "/profile", "/search?q=x", "/courses/999"]
        for url in urls:
            html = self.page(url)
            for target in ('href="/"', 'href="/courses"', 'href="/profile"', 'action="/search"'):
                self.assertIn(target, html, f"{target} missing on {url}")

    def test_every_link_works(self):
        """TC-R27 | NFR-01, FR-17 | Every internal link on the main pages leads to a working page"""
        course = self.make_course("DBMS", description="About")
        self.make_content(course, "Notes", "Note", "Completed")
        self.make_content(course, "Site", "Link", link_or_description="https://example.com")
        self.client.post("/profile", data={"name": "A", "email": "a@b.co"})
        pages = ["/", "/courses", "/courses/new", f"/courses/{course}", f"/courses/{course}/edit",
                 f"/courses/{course}/content/new", "/content/1/edit", "/profile", "/search?q=notes"]
        checked = set()
        for url in pages:
            for href in re.findall(r'href="(/[^"#]*)"', self.page(url)):
                href = htmllib.unescape(href)
                if href in checked:
                    continue
                checked.add(href)
                self.assertEqual(self.client.get(href).status_code, 200, f"{href} (linked from {url})")
        self.assertGreater(len(checked), 8)

    def test_forms_post_to_existing_routes(self):
        """TC-R28 | NFR-01 | Every form on the main pages submits to a route that exists"""
        course = self.make_course("DBMS")
        self.make_content(course, "Notes")
        pages = ["/courses/new", f"/courses/{course}", f"/courses/{course}/edit",
                 f"/courses/{course}/content/new", "/content/1/edit", "/profile"]
        for url in pages:
            for form in re.findall(r"<form[^>]*>", self.page(url)):
                method = re.search(r'method="(\w+)"', form)
                action = re.search(r'action="([^"]*)"', form)
                target = htmllib.unescape(action.group(1)) if action else url
                if not (method and method.group(1).lower() == "post"):
                    continue
                if target.endswith("/delete"):
                    # Deleting would remove data the next forms need. The route exists if GET is "method not allowed".
                    self.assertEqual(self.client.get(target).status_code, 405, f"{target} from {url}")
                else:
                    # Posting nothing must give a handled response, never a crash or a missing route.
                    status = self.client.post(target, data={}).status_code
                    self.assertIn(status, (302, 400), f"POST {target} from {url} gave {status}")

    def test_pages_are_fast_with_many_records(self):
        """TC-R29 | NFR-02 | With 300 courses and 900 content items the main pages respond in under 2 seconds"""
        conn = self.db()
        conn.executemany("INSERT INTO course (title, category) VALUES (?, ?)",
                         [(f"Course {i}", "Bulk") for i in range(300)])
        ids = [row[0] for row in conn.execute("SELECT id FROM course")]
        conn.executemany(
            "INSERT INTO content_item (course_id, title, content_type, status) VALUES (?, ?, 'Note', ?)",
            [(cid, f"Item {n}", status) for cid in ids for n, status in
             enumerate(("Not started", "In progress", "Completed"))],
        )
        conn.commit()
        for url in ("/", "/courses", f"/courses/{ids[0]}", "/search?q=Item"):
            started = time.perf_counter()
            response = self.client.get(url)
            elapsed = time.perf_counter() - started
            self.assertEqual(response.status_code, 200, url)
            self.assertLess(elapsed, 2.0, f"{url} took {elapsed:.2f}s")
