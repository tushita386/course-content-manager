from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import Instructor, Student, Course, Task, VALID_STATUSES, email_exists

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

    if role == 'instructor':
        instructor = Instructor.get_by_id(session['user_id'])
        name = instructor.name if instructor else None
    elif role == 'student':
        student = Student.get_by_id(session['user_id'])
        name = student.name if student else None

    return render_template('home.html', role=role, name=name)


@main.route('/register/instructor', methods=['GET', 'POST'])
def register_instructor():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or not password:
            return "All fields are required.", 400

        if email_exists(email):
            return "An account with this email already exists.", 400

        instructor = Instructor.create(name, email, password)
        session['user_id'] = instructor.id
        session['role'] = 'instructor'
        return redirect(url_for('main.home'))

    return render_template('register_instructor.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        instructor = Instructor.get_by_email(email)
        if instructor and instructor.verify_password(password):
            session['user_id'] = instructor.id
            session['role'] = 'instructor'
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


@main.route('/instructor/add-student', methods=['GET', 'POST'])
@login_required(role='instructor')
def add_student():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or not password:
            return "All fields are required.", 400

        if email_exists(email):
            return "An account with this email already exists.", 400

        instructor_id = session['user_id']
        Student.create(name, email, password, instructor_id)
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

    search = request.args.get('q', '').strip() or None
    semester_raw = request.args.get('semester', '')
    semester = int(semester_raw) if semester_raw.isdigit() else None

    courses = Course.get_by_student(student_id, search=search, semester=semester)

    progress = {}
    for course in courses:
        course_tasks = Task.get_by_course(course.id)
        total = len(course_tasks)
        completed = sum(1 for t in course_tasks if t.status == 'Completed')
        progress[course.id] = (completed, total)

    return render_template(
        'courses.html',
        courses=courses,
        student=student,
        search=search or '',
        selected_semester=semester,
        progress=progress
    )


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

    status_filter = request.args.get('status') or None
    tasks = Task.get_by_course(course_id, status=status_filter)
    return render_template(
        'course_detail.html',
        course=course,
        tasks=tasks,
        status_filter=status_filter or ''
    )


@main.route('/courses/<int:course_id>/tasks/new', methods=['GET', 'POST'])
@login_required(role='student')
def new_task(course_id):
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
            return "Task title is required.", 400

        if status not in VALID_STATUSES:
            return "Invalid status value.", 400

        Task.create(title, notes, status, due_date, course_id, created_by='student')
        return redirect(url_for('main.course_detail', course_id=course_id))

    return render_template('task_form.html', course=course, task=None, restricted=False)


@main.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required(role='student')
def edit_task(task_id):
    task = Task.get_by_id(task_id)

    if task is None:
        return "Task not found.", 404

    course = Course.get_by_id(task.course_id)

    if course is None or course.student_id != session['user_id']:
        return "Access denied.", 403

    # A student can only change the status of a task the instructor assigned —
    # title, notes and due_date stay locked, since the instructor authored them.
    restricted = (task.created_by == 'instructor')

    if request.method == 'POST':
        status = request.form.get('status', 'Not Started')

        if status not in VALID_STATUSES:
            return "Invalid status value.", 400

        if restricted:
            task.update_status(status)
            return redirect(url_for('main.course_detail', course_id=course.id))

        title = request.form.get('title', '').strip()
        notes = request.form.get('notes', '').strip()
        due_date = request.form.get('due_date') or None

        if not title:
            return "Task title is required.", 400

        task.update(title, notes, status, due_date)
        return redirect(url_for('main.course_detail', course_id=course.id))

    return render_template('task_form.html', course=course, task=task, restricted=restricted)


@main.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required(role='student')
def delete_task(task_id):
    task = Task.get_by_id(task_id)

    if task is None:
        return "Task not found.", 404

    course = Course.get_by_id(task.course_id)

    if course is None or course.student_id != session['user_id']:
        return "Access denied.", 403

    if task.created_by == 'instructor':
        return "You can't delete a task assigned by your instructor.", 403

    course_id = course.id
    task.delete()
    return redirect(url_for('main.course_detail', course_id=course_id))


@main.route('/instructor/students')
@login_required(role='instructor')
def instructor_students():
    students = Student.get_by_instructor(session['user_id'])
    return render_template('instructor_students.html', students=students)


@main.route('/instructor/students/<int:student_id>/courses')
@login_required(role='instructor')
def instructor_student_courses(student_id):
    student = Student.get_by_id(student_id)

    if student is None or student.instructor_id != session['user_id']:
        return "Access denied.", 403

    courses = Course.get_by_student(student_id)
    return render_template('instructor_student_courses.html', student=student, courses=courses)


@main.route('/instructor/courses/<int:course_id>/assign-task', methods=['GET', 'POST'])
@login_required(role='instructor')
def assign_task(course_id):
    course = Course.get_by_id(course_id)

    if course is None:
        return "Course not found.", 404

    student = Student.get_by_id(course.student_id)

    if student is None or student.instructor_id != session['user_id']:
        return "Access denied.", 403

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        notes = request.form.get('notes', '').strip()
        due_date = request.form.get('due_date') or None

        if not title:
            return "Task title is required.", 400

        Task.create(title, notes, 'Not Started', due_date, course_id, created_by='instructor')
        return redirect(url_for('main.instructor_student_courses', student_id=student.id))

    return render_template('assign_task.html', course=course, student=student)
