"""Input validation (design: section 18.1 of the master document).

Every validate_* function takes form-like data (anything with .get) and returns
(values, errors):
  values - the trimmed input, so a failed form can be shown again with what the user typed
  errors - {field: message}; empty when the input is valid
"""
import re

from backend.models.content_item import ContentItem

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

LIMITS = {
    "name": 100,
    "email": 254,
    "course_title": 150,
    "description": 1000,
    "category": 50,
    "content_title": 150,
    "link_or_description": 1000,
}


def _text(form, key):
    return (form.get(key) or "").strip()


def _check_required(values, errors, key, label, limit):
    value = values[key]
    if not value:
        errors[key] = f"{label} is required."
    elif len(value) > limit:
        errors[key] = f"{label} must be {limit} characters or fewer."


def _check_optional(values, errors, key, label, limit):
    if len(values[key]) > limit:
        errors[key] = f"{label} must be {limit} characters or fewer."


def validate_profile(form):
    values = {"name": _text(form, "name"), "email": _text(form, "email")}
    errors = {}
    _check_required(values, errors, "name", "Name", LIMITS["name"])
    _check_required(values, errors, "email", "Email", LIMITS["email"])
    if "email" not in errors and not EMAIL_PATTERN.match(values["email"]):
        errors["email"] = "Enter a valid email address, for example name@example.com."
    return values, errors


def validate_course(form):
    values = {
        "title": _text(form, "title"),
        "description": _text(form, "description"),
        "category": _text(form, "category"),
    }
    errors = {}
    _check_required(values, errors, "title", "Title", LIMITS["course_title"])
    _check_optional(values, errors, "description", "Description", LIMITS["description"])
    _check_optional(values, errors, "category", "Category", LIMITS["category"])
    return values, errors


def validate_content(form):
    values = {
        "title": _text(form, "title"),
        "content_type": _text(form, "content_type"),
        "link_or_description": _text(form, "link_or_description"),
        "status": _text(form, "status"),
    }
    errors = {}
    _check_required(values, errors, "title", "Title", LIMITS["content_title"])
    _check_optional(values, errors, "link_or_description", "Link or description",
                    LIMITS["link_or_description"])
    if values["content_type"] not in ContentItem.TYPES:
        errors["content_type"] = "Choose a content type from the list."
    if values["status"] not in ContentItem.STATUSES:
        errors["status"] = "Choose a status from the list."
    return values, errors


def clean_filter(value, allowed):
    """A filter value if it is one of the allowed values, otherwise "" (meaning All)."""
    return value if value in allowed else ""


def clean_keyword(value):
    """The search keyword with surrounding whitespace removed."""
    return (value or "").strip()
