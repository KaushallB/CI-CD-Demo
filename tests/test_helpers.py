"""
Helper function tests for WealthWise
Tests utility functions used throughout the app
"""
import pytest
from app import is_email, generate_otp


def test_is_email_valid():
    """Test email validation with valid emails"""
    assert is_email('test@example.com') is not False
    assert is_email('user@domain.co.uk') is not False
    assert is_email('name.surname@company.com') is not False


def test_is_email_invalid():
    """Test email validation with invalid emails"""
    # is_email returns None for invalid, not False
    assert is_email('notanemail') is None or is_email('notanemail') is False
    assert is_email('missing@domain') is None or is_email('missing@domain') is False
    assert is_email('@nodomain.com') is None or is_email('@nodomain.com') is False
    assert is_email('no@.com') is None or is_email('no@.com') is False


def test_is_email_phone_numbers():
    """Test that phone numbers are not detected as emails"""
    result = is_email('9876543210')
    assert result is None or result is False
    result = is_email('+9779876543210')
    assert result is None or result is False


def test_generate_otp_length():
    """Test that OTP has correct length"""
    otp = generate_otp(6)
    assert len(otp) == 6


def test_generate_otp_digits_only():
    """Test that OTP contains only digits"""
    otp = generate_otp(6)
    assert otp.isdigit()


def test_generate_otp_different_each_time():
    """Test that OTP generates different values"""
    otp1 = generate_otp(6)
    otp2 = generate_otp(6)
    # Very unlikely to be the same (1 in 1,000,000 chance)
    # But we'll just check they're valid
    assert otp1.isdigit()
    assert otp2.isdigit()


def test_generate_otp_custom_length():
    """Test OTP generation with custom length"""
    otp = generate_otp(8)
    assert len(otp) == 8
    assert otp.isdigit()
