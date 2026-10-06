from backend.models.content_item import ContentItem
from backend.models.course import Course


def _like_pattern(keyword):
    """Escape % and _ so the keyword is matched literally."""
    escaped = keyword.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return "%" + escaped + "%"


def search(conn, keyword):
    """Search course titles and content titles (case-insensitive for English letters).

    Returns {"courses": [Course, ...], "content": [(ContentItem, course_title), ...]}.
    An empty keyword returns no results.
    """
    keyword = (keyword or "").strip()
    if not keyword:
        return {"courses": [], "content": []}
    pattern = _like_pattern(keyword)
    course_rows = conn.execute(
        "SELECT * FROM course WHERE title LIKE ? ESCAPE '\\' "
        "ORDER BY title COLLATE NOCASE",
        (pattern,),
    ).fetchall()
    content_rows = conn.execute(
        "SELECT content_item.*, course.title AS course_title "
        "FROM content_item JOIN course ON course.id = content_item.course_id "
        "WHERE content_item.title LIKE ? ESCAPE '\\' "
        "ORDER BY course.title COLLATE NOCASE, content_item.created_at, content_item.id",
        (pattern,),
    ).fetchall()
    return {
        "courses": [Course.from_row(row) for row in course_rows],
        "content": [(ContentItem.from_row(row), row["course_title"]) for row in content_rows],
    }