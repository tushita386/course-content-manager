import re
from tests.conftest import register_instructor, add_student, login, logout


def _setup_logged_in_student(client, semester=3):
    register_instructor(client)
    add_student(client)
    logout(client)
    login(client, 'priya@test.com', 'pass123')
    client.post('/select-semester', data={'semester': str(semester)})


def test_semester_selection_auto_creates_courses(client):
    _setup_logged_in_student(client, semester=3)
    response = client.get('/courses')
    # Semester 3 has 9 subjects in the seeded VTU curriculum.
    # Count the opening card tag exactly, since 'course-card' alone would
    # also match inside 'course-card-actions' further down the same card.
    assert response.data.count(b'<li class="course-card">') == 9


def test_student_can_create_a_course(client):
    _setup_logged_in_student(client)
    response = client.post('/courses/new', data={
        'title': 'My Custom Course', 'description': '', 'subject': '', 'semester': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'My Custom Course' in response.data


def test_course_without_title_is_rejected(client):
    _setup_logged_in_student(client)
    response = client.post('/courses/new', data={
        'title': '', 'description': '', 'subject': '', 'semester': ''
    })
    assert response.status_code == 400


def test_student_can_edit_own_course(client):
    _setup_logged_in_student(client)
    client.post('/courses/new', data={'title': 'Original', 'description': '', 'subject': '', 'semester': ''})

    response = client.get('/courses')
    course_id = re.findall(rb'/courses/(\d+)', response.data)[0].decode()

    response = client.post(f'/courses/{course_id}/edit', data={
        'title': 'Renamed', 'description': '', 'subject': '', 'semester': ''
    }, follow_redirects=True)
    assert b'Renamed' in response.data


def test_student_can_delete_own_course(client):
    _setup_logged_in_student(client)
    client.post('/courses/new', data={'title': 'To Delete', 'description': '', 'subject': '', 'semester': ''})

    response = client.get('/courses')
    course_id = re.findall(rb'/courses/(\d+)', response.data)[0].decode()

    response = client.post(f'/courses/{course_id}/delete', follow_redirects=True)
    assert b'To Delete' not in response.data


def test_student_cannot_edit_another_students_course(client):
    _setup_logged_in_student(client)
    response = client.get('/courses')
    course_id = re.findall(rb'/courses/(\d+)', response.data)[0].decode()

    # Add and log in as a second student under the same instructor
    logout(client)
    login(client, 'rao@test.com', 'pass123')
    add_student(client, name='Second', email='second@test.com')
    logout(client)
    login(client, 'second@test.com', 'pass123')

    response = client.get(f'/courses/{course_id}/edit')
    assert response.status_code == 403


def test_search_filters_courses_by_title(client):
    _setup_logged_in_student(client, semester=3)
    response = client.get('/courses?q=Operating')
    assert response.data.count(b'<li class="course-card">') == 1
    assert b'Operating Systems' in response.data
