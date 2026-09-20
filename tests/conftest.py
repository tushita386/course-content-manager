import os
import tempfile
import pytest

# Ensure the app package can be imported when pytest is run from the
# project root (standard convention — pytest adds the rootdir automatically,
# but we set this explicitly so it isn't dependent on how it's invoked).
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app import database


@pytest.fixture
def client():
    """
    Gives each test function a completely fresh database and a Flask test
    client. Using a temporary file per test (rather than the real
    course_content_manager.db) means tests never interfere with each other,
    and never touch your actual development data.
    """
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    # Point the app's database module at this temporary file instead of the
    # real one, for the duration of this one test.
    original_path = database.DATABASE_PATH
    database.DATABASE_PATH = db_path

    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        database.init_db()

    with app.test_client() as test_client:
        yield test_client

    # Clean up: restore the real path and delete the temp file.
    database.DATABASE_PATH = original_path
    os.close(db_fd)
    os.unlink(db_path)


def register_instructor(client, name='Dr. Rao', email='rao@test.com', password='pass123'):
    return client.post('/register/instructor', data={
        'name': name, 'email': email, 'password': password
    }, follow_redirects=True)


def add_student(client, name='Priya', email='priya@test.com', password='pass123'):
    return client.post('/instructor/add-student', data={
        'name': name, 'email': email, 'password': password
    }, follow_redirects=True)


def login(client, email, password):
    return client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)


def logout(client):
    return client.get('/logout')
