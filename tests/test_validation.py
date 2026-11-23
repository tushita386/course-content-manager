import unittest

from backend import validation
from backend.models.content_item import ContentItem


class ValidationTests(unittest.TestCase):
    def test_profile_valid(self):
        """TC-V01 | FR-16 | A profile with a name and a valid email is accepted"""
        values, errors = validation.validate_profile({"name": " Test User ", "email": "test@example.com"})
        self.assertEqual(errors, {})
        self.assertEqual(values["name"], "Test User")

    def test_profile_empty_name(self):
        """TC-V02 | FR-16 | An empty or whitespace-only profile name is rejected"""
        for name in ("", "   ", None):
            _, errors = validation.validate_profile({"name": name, "email": "a@b.co"})
            self.assertIn("name", errors)

    def test_profile_bad_email(self):
        """TC-V03 | FR-16 | Invalid email addresses are rejected"""
        for email in ("", "plain", "a@b", "@b.co", "a@.co", "a b@c.co", "a@b@c.co"):
            _, errors = validation.validate_profile({"name": "A", "email": email})
            self.assertIn("email", errors, email)

    def test_profile_good_emails(self):
        """TC-V04 | FR-16 | Reasonable email addresses are accepted"""
        for email in ("a@b.co", "first.last@example.com", "x+tag@mail.example.org"):
            _, errors = validation.validate_profile({"name": "A", "email": email})
            self.assertEqual(errors, {}, email)

    def test_profile_length_limits(self):
        """TC-V05 | FR-16 | Profile name over 100 and email over 254 characters are rejected"""
        _, errors = validation.validate_profile({"name": "n" * 100, "email": "a@b.co"})
        self.assertEqual(errors, {})
        _, errors = validation.validate_profile({"name": "n" * 101, "email": "a@b.co"})
        self.assertIn("name", errors)
        long_email = "a" * 250 + "@b.co"
        _, errors = validation.validate_profile({"name": "A", "email": long_email})
        self.assertIn("email", errors)

    def test_course_empty_title(self):
        """TC-V06 | FR-16 | An empty or whitespace-only course title is rejected"""
        for title in ("", "   ", None):
            _, errors = validation.validate_course({"title": title})
            self.assertIn("title", errors)

    def test_course_trimmed(self):
        """TC-V07 | FR-16 | Course input is trimmed and optional fields may be empty"""
        values, errors = validation.validate_course({"title": "  DBMS  "})
        self.assertEqual(errors, {})
        self.assertEqual(values, {"title": "DBMS", "description": "", "category": ""})

    def test_course_length_limits(self):
        """TC-V08 | FR-16 | Course title (150), description (1000) and category (50) limits are enforced"""
        _, errors = validation.validate_course({"title": "t" * 150, "description": "d" * 1000, "category": "c" * 50})
        self.assertEqual(errors, {})
        _, errors = validation.validate_course({"title": "t" * 151, "description": "d" * 1001, "category": "c" * 51})
        self.assertEqual(set(errors), {"title", "description", "category"})

    def test_content_invalid_type(self):
        """TC-V09 | FR-16 | A content type outside the allowed list is rejected"""
        _, errors = validation.validate_content({"title": "x", "content_type": "Video", "status": "Completed"})
        self.assertIn("content_type", errors)

    def test_content_invalid_status(self):
        """TC-V10 | FR-16, FR-11 | A status outside the allowed list is rejected"""
        _, errors = validation.validate_content({"title": "x", "content_type": "Note", "status": "Finished"})
        self.assertIn("status", errors)

    def test_content_all_allowed_values(self):
        """TC-V11 | FR-16, FR-11 | Every allowed content type and status is accepted"""
        for content_type in ContentItem.TYPES:
            for status in ContentItem.STATUSES:
                _, errors = validation.validate_content(
                    {"title": "x", "content_type": content_type, "status": status})
                self.assertEqual(errors, {}, (content_type, status))

    def test_content_title_rules(self):
        """TC-V12 | FR-16 | Content title is required (max 150) and link/description is limited to 1000"""
        base = {"content_type": "Note", "status": "Completed"}
        _, errors = validation.validate_content(dict(base, title=""))
        self.assertIn("title", errors)
        _, errors = validation.validate_content(dict(base, title="t" * 151))
        self.assertIn("title", errors)
        _, errors = validation.validate_content(dict(base, title="ok", link_or_description="l" * 1001))
        self.assertIn("link_or_description", errors)

    def test_clean_filter(self):
        """TC-V13 | FR-13 | Unknown or empty filter values are treated as All"""
        self.assertEqual(validation.clean_filter("Note", ContentItem.TYPES), "Note")
        for value in ("All", "", None, "Finished", "note"):
            self.assertEqual(validation.clean_filter(value, ContentItem.TYPES), "")

    def test_clean_keyword(self):
        """TC-V14 | FR-12 | The search keyword is trimmed and None becomes empty"""
        self.assertEqual(validation.clean_keyword("  notes "), "notes")
        self.assertEqual(validation.clean_keyword(None), "")


if __name__ == "__main__":
    unittest.main()
