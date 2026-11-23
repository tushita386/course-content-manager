from pathlib import Path

from flask import Flask, abort, g, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException

from backend import validation
from backend.database.db import DATABASE_PATH, get_connection, init_db
from backend.models.content_item import ContentItem
from backend.models.course import Course
from backend.models.dashboard import get_dashboard
from backend.models.profile import Profile
from backend.models.search import search

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "frontend" / "templates"),
    static_folder=str(BASE_DIR / "frontend" / "static"),
)
app.config["DATABASE"] = str(DATABASE_PATH)

_initialized = set()


def get_db():
    """One database connection per request, closed automatically afterwards."""
    if "db" not in g:
        g.db = get_connection(app.config["DATABASE"])
    return g.db


@app.before_request
def ensure_database():
    path = app.config["DATABASE"]
    if path not in _initialized:
        init_db(path)
        _initialized.add(path)


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ---------------------------------------------------------------- dashboard

@app.route("/")
def dashboard():
    db = get_db()
    return render_template("dashboard.html", data=get_dashboard(db), profile=Profile.get(db))


# ------------------------------------------------------------------ profile

@app.route("/profile", methods=["GET", "POST"])
def profile():
    db = get_db()
    if request.method == "POST":
        values, errors = validation.validate_profile(request.form)
        if not errors:
            Profile.save(db, values["name"], values["email"])
            return redirect(url_for("profile", saved=1))
        return render_template("profile.html", values=values, errors=errors, saved=False), 400
    current = Profile.get(db)
    values = {"name": current.name, "email": current.email} if current else {"name": "", "email": ""}
    return render_template("profile.html", values=values, errors={}, saved=bool(request.args.get("saved")))


# ------------------------------------------------------------------ courses

@app.route("/courses")
def course_list():
    db = get_db()
    stats = {row["course_id"]: row for row in get_dashboard(db)["per_course"]}
    return render_template("courses.html", courses=Course.get_all(db), stats=stats)


@app.route("/courses/new", methods=["GET", "POST"])
def course_new():
    if request.method == "POST":
        values, errors = validation.validate_course(request.form)
        if not errors:
            course = Course.create(
                get_db(), values["title"], values["description"] or None, values["category"] or None
            )
            return redirect(url_for("course_detail", course_id=course.id))
        return render_template("course_form.html", heading="Add course", values=values, errors=errors), 400
    values = {"title": "", "description": "", "category": ""}
    return render_template("course_form.html", heading="Add course", values=values, errors={})


@app.route("/courses/<int:course_id>")
def course_detail(course_id):
    db = get_db()
    course = Course.get_by_id(db, course_id) or abort(404)
    selected_type = validation.clean_filter(request.args.get("type"), ContentItem.TYPES)
    selected_status = validation.clean_filter(request.args.get("status"), ContentItem.STATUSES)
    items = ContentItem.get_by_course(db, course_id, selected_type, selected_status)
    all_items = ContentItem.get_by_course(db, course_id)
    done = sum(1 for item in all_items if item.status == "Completed")
    return render_template(
        "course_detail.html",
        course=course,
        items=items,
        total=len(all_items),
        done=done,
        types=ContentItem.TYPES,
        statuses=ContentItem.STATUSES,
        selected_type=selected_type,
        selected_status=selected_status,
    )


@app.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
def course_edit(course_id):
    db = get_db()
    course = Course.get_by_id(db, course_id) or abort(404)
    if request.method == "POST":
        values, errors = validation.validate_course(request.form)
        if not errors:
            Course.update(db, course_id, values["title"], values["description"] or None,
                          values["category"] or None)
            return redirect(url_for("course_detail", course_id=course_id))
        return render_template("course_form.html", heading="Edit course", values=values, errors=errors), 400
    values = {"title": course.title, "description": course.description or "", "category": course.category or ""}
    return render_template("course_form.html", heading="Edit course", values=values, errors={})


@app.route("/courses/<int:course_id>/delete", methods=["POST"])
def course_delete(course_id):
    if not Course.delete(get_db(), course_id):
        abort(404)
    return redirect(url_for("course_list"))


# ------------------------------------------------------------------ content

@app.route("/courses/<int:course_id>/content/new", methods=["GET", "POST"])
def content_new(course_id):
    db = get_db()
    course = Course.get_by_id(db, course_id) or abort(404)
    if request.method == "POST":
        values, errors = validation.validate_content(request.form)
        if not errors:
            ContentItem.create(db, course_id, values["title"], values["content_type"],
                               values["link_or_description"] or None, values["status"])
            return redirect(url_for("course_detail", course_id=course_id))
        return render_template("content_form.html", heading="Add content", course=course, values=values,
                               errors=errors, types=ContentItem.TYPES, statuses=ContentItem.STATUSES), 400
    values = {"title": "", "content_type": ContentItem.TYPES[0], "link_or_description": "",
              "status": ContentItem.STATUSES[0]}
    return render_template("content_form.html", heading="Add content", course=course, values=values,
                           errors={}, types=ContentItem.TYPES, statuses=ContentItem.STATUSES)


@app.route("/content/<int:item_id>/edit", methods=["GET", "POST"])
def content_edit(item_id):
    db = get_db()
    item = ContentItem.get_by_id(db, item_id) or abort(404)
    course = Course.get_by_id(db, item.course_id) or abort(404)
    if request.method == "POST":
        values, errors = validation.validate_content(request.form)
        if not errors:
            ContentItem.update(db, item_id, values["title"], values["content_type"],
                               values["link_or_description"] or None, values["status"])
            return redirect(url_for("course_detail", course_id=item.course_id))
        return render_template("content_form.html", heading="Edit content", course=course, values=values,
                               errors=errors, types=ContentItem.TYPES, statuses=ContentItem.STATUSES), 400
    values = {"title": item.title, "content_type": item.content_type,
              "link_or_description": item.link_or_description or "", "status": item.status}
    return render_template("content_form.html", heading="Edit content", course=course, values=values,
                           errors={}, types=ContentItem.TYPES, statuses=ContentItem.STATUSES)


@app.route("/content/<int:item_id>/delete", methods=["POST"])
def content_delete(item_id):
    db = get_db()
    item = ContentItem.get_by_id(db, item_id) or abort(404)
    ContentItem.delete(db, item_id)
    return redirect(url_for("course_detail", course_id=item.course_id))


# ------------------------------------------------------------------- search

@app.route("/search")
def search_page():
    keyword = validation.clean_keyword(request.args.get("q"))
    results = search(get_db(), keyword)
    return render_template("search.html", keyword=keyword, results=results)


# ------------------------------------------------------------------- errors

ERROR_TEXT = {
    405: ("Action not allowed", "That action is not available for this page."),
}


@app.errorhandler(HTTPException)
def http_error(error):
    if error.code == 404:
        return render_template("404.html"), 404
    title, message = ERROR_TEXT.get(error.code, ("Something went wrong", "The request could not be completed."))
    return render_template("error.html", code=error.code, title=title, message=message), error.code


@app.errorhandler(Exception)
def unexpected_error(error):
    # Details go to the console only; the user sees a friendly page (never a raw database error).
    app.logger.exception("Unexpected error")
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
