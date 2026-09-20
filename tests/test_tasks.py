import re
from tests.conftest import register_instructor, add_student, login, logout


def _setup_course(client, semester=3):
    register_instructor(client)
    add_student(client)
    logout(client)
    login(client, 'priya@test.com', 'pass123')
    client.post('/select-semester', data={'semester': str(semester)})
    response = client.get('/courses')
    course_id = re.findall(rb'/courses/(\d+)', response.data)[0].decode()
    return course_id


def test_task_without_title_is_rejected(client):
    course_id = _setup_course(client)
    response = client.post(f'/courses/{course_id}/tasks/new', data={
        'title': '', 'notes': '', 'status': 'Not Started', 'due_date': ''
    })
    assert response.status_code == 400


def test_task_with_invalid_status_is_rejected(client):
    course_id = _setup_course(client)
    response = client.post(f'/courses/{course_id}/tasks/new', data={
        'title': 'Valid Title', 'notes': '', 'status': 'NOT_A_REAL_STATUS', 'due_date': ''
    })
    assert response.status_code == 400


def test_student_can_create_and_complete_own_task(client):
    course_id = _setup_course(client)
    client.post(f'/courses/{course_id}/tasks/new', data={
        'title': 'My Note', 'notes': '', 'status': 'Not Started', 'due_date': ''
    })

    response = client.get(f'/courses/{course_id}')
    task_id = re.search(rb'/tasks/(\d+)/edit', response.data).group(1).decode()

    response = client.post(f'/tasks/{task_id}/edit', data={
        'title': 'My Note', 'notes': '', 'status': 'Completed', 'due_date': ''
    }, follow_redirects=True)
    assert b'Completed' in response.data


def test_instructor_assigned_task_shows_correct_badge(client):
    course_id = _setup_course(client)
    logout(client)
    login(client, 'rao@test.com', 'pass123')

    response = client.get('/instructor/students')
    student_id = re.findall(rb'/instructor/students/(\d+)/courses', response.data)[0].decode()
    client.get(f'/instructor/students/{student_id}/courses')

    client.post(f'/instructor/courses/{course_id}/assign-task', data={
        'title': 'Submit Assignment 1', 'notes': '', 'due_date': ''
    })

    logout(client)
    login(client, 'priya@test.com', 'pass123')
    response = client.get(f'/courses/{course_id}')
    assert b'Assigned by Instructor' in response.data


def test_student_can_update_status_of_assigned_task(client):
    course_id = _setup_course(client)
    logout(client)
    login(client, 'rao@test.com', 'pass123')
    client.post(f'/instructor/courses/{course_id}/assign-task', data={
        'title': 'Assigned Task', 'notes': '', 'due_date': ''
    })

    logout(client)
    login(client, 'priya@test.com', 'pass123')
    response = client.get(f'/courses/{course_id}')
    task_id = re.search(rb'/tasks/(\d+)/edit', response.data).group(1).decode()

    response = client.post(f'/tasks/{task_id}/edit', data={'status': 'In Progress'}, follow_redirects=True)
    assert b'In Progress' in response.data


def test_student_cannot_delete_assigned_task(client):
    course_id = _setup_course(client)
    logout(client)
    login(client, 'rao@test.com', 'pass123')
    client.post(f'/instructor/courses/{course_id}/assign-task', data={
        'title': 'Assigned Task', 'notes': '', 'due_date': ''
    })

    logout(client)
    login(client, 'priya@test.com', 'pass123')
    response = client.get(f'/courses/{course_id}')
    task_id = re.search(rb'/tasks/(\d+)/edit', response.data).group(1).decode()

    response = client.post(f'/tasks/{task_id}/delete')
    assert response.status_code == 403


def test_student_cannot_retitle_assigned_task(client):
    course_id = _setup_course(client)
    logout(client)
    login(client, 'rao@test.com', 'pass123')
    client.post(f'/instructor/courses/{course_id}/assign-task', data={
        'title': 'Original Title', 'notes': '', 'due_date': ''
    })

    logout(client)
    login(client, 'priya@test.com', 'pass123')
    response = client.get(f'/courses/{course_id}')
    task_id = re.search(rb'/tasks/(\d+)/edit', response.data).group(1).decode()

    # Attempt to tamper with the title via a direct request — should be ignored
    client.post(f'/tasks/{task_id}/edit', data={'title': 'Hacked Title', 'status': 'In Progress'})
    response = client.get(f'/courses/{course_id}')
    assert b'Original Title' in response.data
    assert b'Hacked Title' not in response.data
