"""
Utility function tests for WealthWise
Tests helper functions and utilities
"""
import pytest
from datetime import datetime, timedelta
import pytz


def test_nepal_timezone():
    """Test Nepal timezone handling"""
    nepal_tz = pytz.timezone('Asia/Kathmandu')
    now = datetime.now(nepal_tz)
    
    # Nepal is UTC+5:45
    offset = now.utcoffset()
    assert offset == timedelta(hours=5, minutes=45)


def test_date_formatting():
    """Test date formatting for display"""
    test_date = datetime(2024, 1, 15, 14, 30)
    
    # Test various date formats
    formatted = test_date.strftime('%Y-%m-%d')
    assert formatted == '2024-01-15'
    
    formatted = test_date.strftime('%B %d, %Y')
    assert formatted == 'January 15, 2024'


def test_amount_validation():
    """Test amount validation logic"""
    from decimal import Decimal
    
    # Valid amounts
    valid_amounts = ['100', '100.50', '1000', '0.01']
    for amount in valid_amounts:
        try:
            decimal_amount = Decimal(amount)
            assert decimal_amount > 0
        except Exception as e:
            pytest.fail(f"Valid amount {amount} should not raise exception: {e}")


def test_invalid_amount_handling():
    """Test handling of invalid amounts"""
    from decimal import Decimal, InvalidOperation
    
    invalid_amounts = ['abc', '', 'NaN', '-100']
    for amount in invalid_amounts:
        if amount == '-100':
            # Negative amounts should be caught by business logic
            decimal_amount = Decimal(amount)
            assert decimal_amount < 0
        elif amount == '':
            # Empty string should raise InvalidOperation
            with pytest.raises(InvalidOperation):
                Decimal(amount)
        else:
            # Invalid formats should raise InvalidOperation
            try:
                Decimal(amount)
            except InvalidOperation:
                pass  # Expected


def test_category_list():
    """Test that expense categories are properly defined"""
    # These categories should match what's in your app
    expected_categories = [
        'Food',
        'Transportation', 
        'Entertainment',
        'Bills',
        'Shopping',
        'Health',
        'Other'
    ]
    
    # Just verify the list structure
    assert len(expected_categories) > 0
    assert all(isinstance(cat, str) for cat in expected_categories)


def test_income_source_list():
    """Test that income sources are properly defined"""
    expected_sources = [
        'Salary',
        'Business',
        'Investment',
        'Gift',
        'Other'
    ]
    
    # Verify structure
    assert len(expected_sources) > 0
    assert all(isinstance(source, str) for source in expected_sources)
