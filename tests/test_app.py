"""
Basic application tests for WealthWise
Tests core Flask functionality and routing
"""
import pytest


def test_app_exists(app):
    """Test that the Flask app exists"""
    assert app is not None


def test_app_is_testing(app):
    """Test that the app is in testing mode"""
    assert app.config['TESTING'] is True


def test_index_route_redirects_to_login(client):
    """Test that the root route redirects to login"""
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302 
    assert '/login' in response.location


def test_login_page_loads(client):
    """Test that the login page loads successfully"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data or b'login' in response.data


def test_registration_page_loads(client):
    """Test that the registration page loads successfully"""
    response = client.get('/registration')
    assert response.status_code == 200
    assert b'register' in response.data.lower() or b'sign up' in response.data.lower()


def test_forgot_password_page_loads(client):
    """Test that forgot password page loads"""
    response = client.get('/forgot_password')
    assert response.status_code == 200
    assert b'forgot' in response.data.lower() or b'email' in response.data.lower()


def test_dashboard_requires_authentication(client):
    """Test that dashboard requires login"""
    response = client.get('/dashboard/1', follow_redirects=False)
    assert response.status_code in [302, 401]  # Should redirect or deny


def test_add_expense_requires_authentication(client):
    """Test that add expense requires login"""
    response = client.get('/add_expense/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_add_income_requires_authentication(client):
    """Test that add income requires login"""
    response = client.get('/add_income/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_chatbot_requires_authentication(client):
    """Test that chatbot requires login"""
    response = client.get('/chatbot/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_view_reports_requires_authentication(client):
    """Test that view reports requires login"""
    response = client.get('/view_reports/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_static_files_accessible(client):
    """Test that static CSS files are accessible"""
    response = client.get('/static/css/style.css')
    assert response.status_code == 200


def test_404_error(client):
    """Test that 404 errors are handled properly"""
    response = client.get('/nonexistent-page-12345-xyz')
    assert response.status_code == 404


def test_csrf_disabled_in_testing(app):
    """Verify CSRF is disabled during testing"""
    assert app.config['WTF_CSRF_ENABLED'] is False


def test_mail_suppressed_in_testing(app):
    """Verify email sending is suppressed during testing"""
    assert app.config['MAIL_SUPPRESS_SEND'] is True


def test_secret_key_configured(app):
    """Test that secret key is set"""
    assert app.config['SECRET_KEY'] is not None
    assert app.config['SECRET_KEY'] != ''
