from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import Mentor, Student, email_exists

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
    return "Course Content Manager is running!"


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