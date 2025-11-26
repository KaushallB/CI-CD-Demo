"""
Pytest configuration and fixtures for WealthWise tests
"""
import pytest
import os
from app import app as flask_app
from psycopg2 import connect
from psycopg2.extras import DictCursor


@pytest.fixture
def app():
    """Create and configure a test Flask application instance"""
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
        'SECRET_KEY': 'test-secret-key',
        'MAIL_SUPPRESS_SEND': True,  # Don't send real emails in tests
    })
    
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a CLI test runner"""
    return app.test_cli_runner()


@pytest.fixture
def db_connection():
    """Create a database connection for testing"""
    db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:root@localhost/wealthwisenew')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    conn = connect(db_url)
    yield conn
    conn.close()


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        'full_name': 'Test User',
        'email': 'test@example.com',
        'phone_num': '9876543210',
        'address': 'Test Address, Kathmandu',
        'password': 'TestPass123!',
        'confirm_pw': 'TestPass123!'
    }


@pytest.fixture
def test_expense_data():
    """Sample expense data for testing"""
    return {
        'date': '2024-01-15',
        'category': 'Food',
        'amount': '500',
        'description': 'Lunch at restaurant'
    }


@pytest.fixture
def test_income_data():
    """Sample income data for testing"""
    return {
        'date': '2024-01-01',
        'source': 'Salary',
        'amount': '50000',
        'description': 'Monthly salary'
    }
