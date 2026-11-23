from pathlib import Path

import os
from functools import wraps
from getpass import getpass

import click
from flask import Flask, abort, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import HTTPException

from backend import validation
from backend.database.db import DATABASE_PATH, get_connection, init_db
from backend.models.content_item import ContentItem
from backend.models.course import Course
from backend.models.dashboard import get_dashboard
from backend.models.profile import Profile
from backend.models.search import search
from backend.models.user import User

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "frontend" / "templates"),
    static_folder=str(BASE_DIR / "frontend" / "static"),
)
app.config["DATABASE"] = str(DATABASE_PATH)
# Set FLASK_SECRET_KEY to a long random value outside local development.
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "local-development-key-change-before-deployment")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

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


# -------------------------------------------------------------- authentication

def current_user():
    if "current_user" not in g:
        user_id = session.get("user_id")
        g.current_user = User.get_by_id(get_db(), user_id) if user_id else None
    return g.current_user


@app.context_processor
def inject_user():
    # Keep the friendly 500 page renderable even if the database itself failed.
    try:
        return {"current_user": current_user()}
    except Exception:
        return {"current_user": None}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def teacher_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if not user:
            return redirect(url_for("login", next=request.path))
        if user.role != "teacher":
            abort(403)
        return view(*args, **kwargs)
    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.get_by_username(get_db(), username)
        from werkzeug.security import check_password_hash
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            destination = request.args.get("next") or request.form.get("next")
            if not destination or not destination.startswith("/") or destination.startswith("//"):
                destination = url_for("dashboard")
            return redirect(destination)
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/students", methods=["GET", "POST"])
@teacher_required
def students():
    db = get_db()
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or len(username) > 80:
            error = "Enter a username (up to 80 characters)."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif User.get_by_username(db, username):
            error = "That username is already in use."
        else:
            User.create(db, username, generate_password_hash(password), "student")
            return redirect(url_for("students", created=1))
    return render_template("students.html", students=User.get_all_students(db),
                           error=error, created=request.args.get("created"))


@app.cli.command("create-teacher")
def create_teacher():
    """Create the initial teacher account (run once from the terminal)."""
    init_db(app.config["DATABASE"])
    db = get_connection(app.config["DATABASE"])
    try:
        if User.get_by_role(db, "teacher"):
            raise click.ClickException("A teacher account already exists.")
        username = click.prompt("Teacher username").strip()
        if not username or len(username) > 80:
            raise click.ClickException("Username must contain 1 to 80 characters.")
        password = getpass("Teacher password (minimum 8 characters): ")
        confirm = getpass("Confirm password: ")
        if len(password) < 8 or password != confirm:
            raise click.ClickException("Passwords must match and contain at least 8 characters.")
        User.create(db, username.strip(), generate_password_hash(password), "teacher")
        click.echo("Teacher account created. Log in through the application.")
    finally:
        db.close()


# ---------------------------------------------------------------- dashboard

@app.route("/")
@login_required
def dashboard():
    db = get_db()
    return render_template("dashboard.html", data=get_dashboard(db), profile=Profile.get(db))


# ------------------------------------------------------------------ profile

@app.route("/profile", methods=["GET", "POST"])
@teacher_required
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
@login_required
def course_list():
    db = get_db()
    stats = {row["course_id"]: row for row in get_dashboard(db)["per_course"]}
    return render_template("courses.html", courses=Course.get_all(db), stats=stats)


@app.route("/courses/new", methods=["GET", "POST"])
@teacher_required
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
@login_required
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
@teacher_required
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
@teacher_required
def course_delete(course_id):
    if not Course.delete(get_db(), course_id):
        abort(404)
    return redirect(url_for("course_list"))


# ------------------------------------------------------------------ content

@app.route("/courses/<int:course_id>/content/new", methods=["GET", "POST"])
@teacher_required
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
@teacher_required
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
@teacher_required
def content_delete(item_id):
    db = get_db()
    item = ContentItem.get_by_id(db, item_id) or abort(404)
    ContentItem.delete(db, item_id)
    return redirect(url_for("course_detail", course_id=item.course_id))


# ------------------------------------------------------------------- search

@app.route("/search")
@login_required
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
