"""
Route and endpoint tests for WealthWise
Tests all major routes and their responses
"""
import pytest


def test_login_page_accessible(client):
    """Test that login page is accessible"""
    response = client.get('/login')
    assert response.status_code == 200


def test_registration_page_accessible(client):
    """Test that registration page is accessible"""
    response = client.get('/registration')
    assert response.status_code == 200


def test_forgot_password_accessible(client):
    """Test that forgot password page loads"""
    response = client.get('/forgot_password')
    assert response.status_code == 200


def test_dashboard_requires_login(client):
    """Test that dashboard redirects when not authenticated"""
    response = client.get('/dashboard/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_add_expense_requires_login(client):
    """Test that add expense requires authentication"""
    response = client.get('/add_expense/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_add_income_requires_login(client):
    """Test that add income requires authentication"""
    response = client.get('/add_income/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_view_reports_requires_login(client):
    """Test that view reports requires authentication"""
    response = client.get('/view_reports/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_chatbot_requires_login(client):
    """Test that chatbot requires authentication"""
    response = client.get('/chatbot/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_visualize_requires_login(client):
    """Test that visualize page requires authentication"""
    response = client.get('/visualize/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_download_reports_requires_login(client):
    """Test that download reports requires authentication"""
    response = client.get('/download_reports/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_all_transactions_requires_login(client):
    """Test that all transactions page requires authentication"""
    response = client.get('/all-transactions/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_edit_expense_requires_login(client):
    """Test that edit expense requires authentication"""
    response = client.get('/edit_expense/1/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_edit_income_requires_login(client):
    """Test that edit income requires authentication"""
    response = client.get('/edit_income/1/1', follow_redirects=False)
    assert response.status_code in [302, 401]


def test_logout_redirects(client):
    """Test that logout redirects"""
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302


def test_static_css_accessible(client):
    """Test that static CSS is accessible"""
    response = client.get('/static/css/style.css')
    assert response.status_code == 200


def test_static_js_accessible(client):
    """Test that static JS is accessible"""
    response = client.get('/static/js/script.js')
    assert response.status_code == 200


def test_invalid_route_returns_404(client):
    """Test that invalid routes return 404"""
    response = client.get('/this-route-does-not-exist-123')
    assert response.status_code == 404


def test_login_accepts_post_requests(client):
    """Test that login accepts POST requests"""
    response = client.post('/login', data={
        'email_or_phone': 'test@example.com',
        'password': 'TestPass123!'
    })
    # Should process the request (even if login fails)
    assert response.status_code in [200, 302]
