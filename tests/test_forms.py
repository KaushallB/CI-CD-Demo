"""
Form validation tests for WealthWise
Tests all form validators and custom validation logic
"""
import pytest
from forms import RegistrationForm, LoginForm, name_val, number_val, pw_val
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField


class DummyForm(FlaskForm):
    """Dummy form for testing validators"""
    test_field = StringField()


def test_name_validation_valid(app):
    """Test that valid names pass validation"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "John Doe"
        
        try:
            name_val(form, form.test_field)
        except ValidationError:
            pytest.fail("Valid name should not raise ValidationError")


def test_name_validation_invalid_numbers(app):
    """Test that names with numbers fail validation"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "John123"
        
        with pytest.raises(ValidationError, match="letters and spaces"):
            name_val(form, form.test_field)


def test_name_validation_invalid_special_chars(app):
    """Test that names with special characters fail validation"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "John@Doe"
        
        with pytest.raises(ValidationError, match="letters and spaces"):
            name_val(form, form.test_field)


def test_phone_validation_valid(app):
    """Test that valid phone numbers pass validation"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "9876543210"
        
        try:
            number_val(form, form.test_field)
            assert len(form.test_field.data) == 10
        except ValidationError:
            pytest.fail("Valid phone number should not raise ValidationError")


def test_phone_validation_with_country_code(app):
    """Test that phone numbers with +977 are handled correctly"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "+9779876543210"
        
        try:
            number_val(form, form.test_field)
            # Should strip country code and keep 10 digits
            assert len(form.test_field.data) == 10
        except ValidationError:
            pytest.fail("Phone number with country code should be valid")


def test_phone_validation_invalid_length(app):
    """Test that phone numbers with wrong length fail"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "98765"
        
        with pytest.raises(ValidationError, match="10 digits"):
            number_val(form, form.test_field)


def test_password_validation_valid(app):
    """Test that strong passwords pass validation"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "SecurePass123!"
        
        try:
            pw_val(form, form.test_field)
        except ValidationError:
            pytest.fail("Valid password should not raise ValidationError")


def test_password_validation_no_uppercase(app):
    """Test that passwords without uppercase fail"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "weakpass123!"
        
        with pytest.raises(ValidationError, match="uppercase"):
            pw_val(form, form.test_field)


def test_password_validation_no_number(app):
    """Test that passwords without numbers fail"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "WeakPassword!"
        
        with pytest.raises(ValidationError, match="numbers"):
            pw_val(form, form.test_field)


def test_password_validation_no_special_char(app):
    """Test that passwords without special characters fail"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "WeakPass123"
        
        with pytest.raises(ValidationError, match="special characters"):
            pw_val(form, form.test_field)


def test_password_validation_too_short(app):
    """Test that short passwords fail"""
    with app.app_context():
        form = DummyForm()
        form.test_field.data = "Weak1!"
        
        with pytest.raises(ValidationError, match="8 characters"):
            pw_val(form, form.test_field)


def test_registration_form_valid(app, test_user_data):
    """Test that valid registration data passes form validation"""
    with app.app_context():
        form = RegistrationForm(data=test_user_data)
        assert form.validate()


def test_registration_form_password_mismatch(app, test_user_data):
    """Test that mismatched passwords fail validation"""
    with app.app_context():
        data = test_user_data.copy()
        data['confirm_pw'] = 'DifferentPass123!'
        form = RegistrationForm(data=data)
        assert not form.validate()


def test_login_form_valid(app):
    """Test that valid login data passes validation"""
    with app.app_context():
        data = {
            'email_or_phone': 'test@example.com',
            'password': 'TestPass123!'
        }
        form = LoginForm(data=data)
        assert form.validate()
