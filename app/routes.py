from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import Mentor, Student, Course, Content, VALID_STATUSES, email_exists

main = Blueprint('main', __name__)


def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('main.login'))
            if role and session.get('role') != role:
                return "Access denied.", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@main.route('/')
def home():
    role = session.get('role')
    name = None

    if role == 'mentor':
        mentor = Mentor.get_by_id(session['user_id'])
        name = mentor.name if mentor else None
    elif role == 'student':
        student = Student.get_by_id(session['user_id'])
        name = student.name if student else None

    return render_template('home.html', role=role, name=name)


@main.route('/register/mentor', methods=['GET', 'POST'])
def register_mentor():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or not password:
            return "All fields are required.", 400

        if email_exists(email):
            return "An account with this email already exists.", 400

        mentor = Mentor.create(name, email, password)
        session['user_id'] = mentor.id
        session['role'] = 'mentor'
        return redirect(url_for('main.home'))

    return render_template('register_mentor.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        mentor = Mentor.get_by_email(email)
        if mentor and mentor.verify_password(password):
            session['user_id'] = mentor.id
            session['role'] = 'mentor'
            return redirect(url_for('main.home'))

        student = Student.get_by_email(email)
        if student and student.verify_password(password):
            session['user_id'] = student.id
            session['role'] = 'student'
            if student.current_semester is None:
                return redirect(url_for('main.select_semester'))
            return redirect(url_for('main.home'))

        return "Invalid email or password.", 401

    return render_template('login.html')


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))


@main.route('/mentor/add-student', methods=['GET', 'POST'])
@login_required(role='mentor')
def add_student():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or not password:
            return "All fields are required.", 400

        if email_exists(email):
            return "An account with this email already exists.", 400

        mentor_id = session['user_id']
        Student.create(name, email, password, mentor_id)
        return redirect(url_for('main.home'))

    return render_template('add_student.html')


@main.route('/select-semester', methods=['GET', 'POST'])
@login_required(role='student')
def select_semester():
    student = Student.get_by_id(session['user_id'])

    if request.method == 'POST':
        semester = request.form.get('semester')

        if not semester:
            return "Please select a semester.", 400

        semester = int(semester)
        student.update_semester(semester)
        Course.auto_create_for_semester(student.id, semester)
        return redirect(url_for('main.list_courses'))

    return render_template('select_semester.html', current_semester=student.current_semester)


@main.route('/courses')
@login_required(role='student')
def list_courses():
    student_id = session['user_id']
    student = Student.get_by_id(student_id)
    courses = Course.get_by_student(student_id)
    return render_template('courses.html', courses=courses, student=student)


@main.route('/courses/new', methods=['GET', 'POST'])
@login_required(role='student')
def new_course():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        subject = request.form.get('subject', '').strip()
        semester = request.form.get('semester') or None

        if not title:
            return "Course title is required.", 400

        Course.create(title, description, subject, semester, session['user_id'])
        return redirect(url_for('main.list_courses'))

    return render_template('course_form.html', course=None)


@main.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required(role='student')
def edit_course(course_id):
    course = Course.get_by_id(course_id)

    if course is None:
        return "Course not found.", 404

    if course.student_id != session['user_id']:
        return "Access denied.", 403

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        subject = request.form.get('subject', '').strip()
        semester = request.form.get('semester') or None

        if not title:
            return "Course title is required.", 400

        course.update(title, description, subject, semester)
        return redirect(url_for('main.list_courses'))

    return render_template('course_form.html', course=course)


@main.route('/courses/<int:course_id>/delete', methods=['POST'])
@login_required(role='student')
def delete_course(course_id):
    course = Course.get_by_id(course_id)

    if course is None:
        return "Course not found.", 404

    if course.student_id != session['user_id']:
        return "Access denied.", 403

    course.delete()
    return redirect(url_for('main.list_courses'))


@main.route('/courses/<int:course_id>')
@login_required(role='student')
def course_detail(course_id):
    course = Course.get_by_id(course_id)

    if course is None:
        return "Course not found.", 404

    if course.student_id != session['user_id']:
        return "Access denied.", 403

    content_items = Content.get_by_course(course_id)
    return render_template('course_detail.html', course=course, content_items=content_items)


@main.route('/courses/<int:course_id>/content/new', methods=['GET', 'POST'])
@login_required(role='student')
def new_content(course_id):
    course = Course.get_by_id(course_id)

    if course is None:
        return "Course not found.", 404

    if course.student_id != session['user_id']:
        return "Access denied.", 403

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        notes = request.form.get('notes', '').strip()
        status = request.form.get('status', 'Not Started')
        due_date = request.form.get('due_date') or None

        if not title:
            return "Content title is required.", 400

        if status not in VALID_STATUSES:
            return "Invalid status value.", 400

        Content.create(title, notes, status, due_date, course_id)
        return redirect(url_for('main.course_detail', course_id=course_id))

    return render_template('content_form.html', course=course, content=None)


@main.route('/content/<int:content_id>/edit', methods=['GET', 'POST'])
@login_required(role='student')
def edit_content(content_id):
    content = Content.get_by_id(content_id)

    if content is None:
        return "Content not found.", 404

    course = Course.get_by_id(content.course_id)

    if course is None or course.student_id != session['user_id']:
        return "Access denied.", 403

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        notes = request.form.get('notes', '').strip()
        status = request.form.get('status', 'Not Started')
        due_date = request.form.get('due_date') or None

        if not title:
            return "Content title is required.", 400

        if status not in VALID_STATUSES:
            return "Invalid status value.", 400

        content.update(title, notes, status, due_date)
        return redirect(url_for('main.course_detail', course_id=course.id))

    return render_template('content_form.html', course=course, content=content)


@main.route('/content/<int:content_id>/delete', methods=['POST'])
@login_required(role='student')
def delete_content(content_id):
    content = Content.get_by_id(content_id)

    if content is None:
        return "Content not found.", 404

    course = Course.get_by_id(content.course_id)

    if course is None or course.student_id != session['user_id']:
        return "Access denied.", 403

    course_id = course.id
    content.delete()
    return redirect(url_for('main.course_detail', course_id=course_id))
