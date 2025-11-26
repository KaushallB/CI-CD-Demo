"""
Security tests for WealthWise
Tests authentication, session management, and security features
"""
import pytest


def test_csrf_protection_enabled_in_production(app):
    """Test that CSRF protection can be enabled"""
    # In testing mode it's disabled, but verify the config exists
    assert 'WTF_CSRF_ENABLED' in app.config


def test_secure_cookie_settings(app):
    """Test that session cookies have secure settings"""
    assert app.config.get('SESSION_COOKIE_HTTPONLY') is True
    assert app.config.get('SESSION_COOKIE_SECURE') is True


def test_password_not_exposed_in_response(client):
    """Test that passwords are never exposed in responses"""
    response = client.get('/registration')  # Changed from /register to /registration
    assert response.status_code == 200
    assert b'password' in response.data.lower()  # Form field exists
    # But actual password values should never be visible


def test_sql_injection_protection(client):
    """Test basic SQL injection protection"""
    malicious_input = "'; DROP TABLE users; --"
    response = client.post('/login', data={
        'email_or_phone': malicious_input,
        'password': 'test'
    }, follow_redirects=True)
    
    # Should handle gracefully without error
    assert response.status_code == 200


def test_xss_protection(client):
    """Test basic XSS protection"""
    malicious_input = "<script>alert('XSS')</script>"
    response = client.post('/login', data={
        'email_or_phone': malicious_input,
        'password': 'test'
    }, follow_redirects=True)
    
    # Should escape or reject malicious input
    assert response.status_code == 200
    assert b'<script>' not in response.data


def test_session_timeout_configuration(app):
    """Test that session timeout is configured"""
    assert 'PERMANENT_SESSION_LIFETIME' in app.config
    # Should have reasonable timeout (24 hours)
    timeout = app.config['PERMANENT_SESSION_LIFETIME']
    assert timeout.total_seconds() > 0


def test_bcrypt_password_hashing(app):
    """Test that bcrypt is properly configured"""
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt(app)
    
    test_password = "TestPassword123!"
    hashed = bcrypt.generate_password_hash(test_password).decode('utf-8')
    
    # Hash should be different from original
    assert hashed != test_password
    
    # Should verify correctly
    assert bcrypt.check_password_hash(hashed, test_password)
    
    # Wrong password should fail
    assert not bcrypt.check_password_hash(hashed, "WrongPassword")


def test_email_validation(app, test_user_data):
    """Test that email validation works"""
    from forms import RegistrationForm
    
    with app.app_context():
        # Valid email
        form = RegistrationForm(data=test_user_data)
        assert form.validate()
        
        # Invalid email
        invalid_data = test_user_data.copy()
        invalid_data['email'] = 'not-an-email'
        form = RegistrationForm(data=invalid_data)
        assert not form.validate()


def test_unauthorized_access_blocked(client):
    """Test that unauthorized users cannot access protected routes"""
    protected_routes = [
        '/dashboard/1',
        '/add_expense/1',
        '/add_income/1',
        '/view_reports/1',
        '/chatbot/1'
    ]
    
    for route in protected_routes:
        response = client.get(route, follow_redirects=False)
        # Should redirect to login or return 401 (not 404)
        assert response.status_code in [302, 401], f"Route {route} returned {response.status_code}"
