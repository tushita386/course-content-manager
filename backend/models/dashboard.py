from backend.models.content_item import ContentItem

COMPLETED_STATUS = "Completed"  # one of ContentItem.STATUSES (FR-11)


def get_dashboard(conn):
    """Totals (FR-14) and per-course progress (FR-15).

    Pending means Not started or In progress (D-04).
    """
    total_courses = conn.execute("SELECT COUNT(*) FROM course").fetchone()[0]
    total_content = conn.execute("SELECT COUNT(*) FROM content_item").fetchone()[0]
    completed = conn.execute(
        "SELECT COUNT(*) FROM content_item WHERE status = ?", (COMPLETED_STATUS,)
    ).fetchone()[0]
    placeholders = ",".join("?" for _ in ContentItem.PENDING_STATUSES)
    pending = conn.execute(
        "SELECT COUNT(*) FROM content_item WHERE status IN (" + placeholders + ")",
        ContentItem.PENDING_STATUSES,
    ).fetchone()[0]
    rows = conn.execute(
        "SELECT course.id AS course_id, course.title AS title, "
        "COUNT(content_item.id) AS total, "
        "COALESCE(SUM(CASE WHEN content_item.status = ? THEN 1 ELSE 0 END), 0) AS completed "
        "FROM course LEFT JOIN content_item ON content_item.course_id = course.id "
        "GROUP BY course.id ORDER BY course.title COLLATE NOCASE",
        (COMPLETED_STATUS,),
    ).fetchall()
    per_course = [
        {
            "course_id": row["course_id"],
            "title": row["title"],
            "completed": row["completed"],
            "total": row["total"],
        }
        for row in rows
    ]
    return {
        "total_courses": total_courses,
        "total_content": total_content,
        "completed": completed,
        "pending": pending,
        "per_course": per_course,
    }
