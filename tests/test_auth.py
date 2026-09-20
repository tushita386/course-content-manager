from tests.conftest import register_instructor, add_student, login, logout


def test_instructor_can_register(client):
    response = register_instructor(client)
    assert response.status_code == 200
    assert b'My Students' in response.data


def test_duplicate_email_is_rejected(client):
    register_instructor(client, email='same@test.com')
    logout(client)
    # Try registering a second instructor with the same email
    response = register_instructor(client, name='Someone Else', email='same@test.com')
    assert response.status_code == 400
    assert b'already exists' in response.data


def test_login_with_wrong_password_is_rejected(client):
    register_instructor(client, email='rao@test.com', password='correct123')
    logout(client)
    response = login(client, 'rao@test.com', 'wrongpassword')
    assert response.status_code == 401
    assert b'Invalid email or password' in response.data


def test_login_with_unknown_email_is_rejected(client):
    response = login(client, 'nobody@test.com', 'whatever')
    assert response.status_code == 401


def test_logged_out_user_redirected_from_protected_page(client):
    response = client.get('/courses', follow_redirects=True)
    # Should land on the login page, not the protected page
    assert b'Login' in response.data or b'Log in' in response.data


def test_student_cannot_access_instructor_only_page(client):
    register_instructor(client)
    add_student(client)
    logout(client)
    login(client, 'priya@test.com', 'pass123')

    response = client.get('/instructor/students')
    assert response.status_code == 403


def test_instructor_cannot_access_student_only_page(client):
    register_instructor(client)
    response = client.get('/courses')
    assert response.status_code == 403
