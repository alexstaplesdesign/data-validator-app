import pytest
from pathlib import Path
from validator.models import CustomerRecord
from validator.validation import validate_customer, validate_file


def test_validate_customer_valid_record():
    """Test validation of a valid customer record."""
    record = CustomerRecord(
        customer_id="1",
        full_name="Jane Doe",
        email="jane@example.com",
        signup_date="2025-12-01"
    )
    errors = validate_customer(record, 1)
    assert errors == []


def test_validate_customer_missing_fields():
    """Test validation with missing required fields."""
    record = CustomerRecord(
        customer_id="",
        full_name="",
        email="",
        signup_date=""
    )
    errors = validate_customer(record, 1)
    assert len(errors) == 4  # All fields should have errors


def test_validate_customer_invalid_customer_id():
    """Test validation with invalid customer_id."""
    # Test non-integer
    record = CustomerRecord(
        customer_id="abc",
        full_name="Jane Doe",
        email="jane@example.com",
        signup_date="2025-12-01"
    )
    errors = validate_customer(record, 1)
    assert any(e.field == "customer_id" and "integer" in e.message for e in errors)
    
    # Test negative number
    record = CustomerRecord(
        customer_id="-1",
        full_name="Jane Doe",
        email="jane@example.com",
        signup_date="2025-12-01"
    )
    errors = validate_customer(record, 1)
    assert any(e.field == "customer_id" and "> 0" in e.message for e in errors)


def test_validate_customer_invalid_name_length():
    """Test validation with invalid name length."""
    # Too short
    record = CustomerRecord(
        customer_id="1",
        full_name="J",
        email="jane@example.com",
        signup_date="2025-12-01"
    )
    errors = validate_customer(record, 1)
    assert any(e.field == "full_name" and "2..80" in e.message for e in errors)
    
    # Too long
    record = CustomerRecord(
        customer_id="1",
        full_name="J" * 81,
        email="jane@example.com",
        signup_date="2025-12-01"
    )
    errors = validate_customer(record, 1)
    assert any(e.field == "full_name" and "2..80" in e.message for e in errors)


def test_validate_customer_invalid_email():
    """Test validation with invalid email format."""
    record = CustomerRecord(
        customer_id="1",
        full_name="Jane Doe",
        email="invalid-email",
        signup_date="2025-12-01"
    )
    errors = validate_customer(record, 1)
    assert any(e.field == "email" and "Invalid format" in e.message for e in errors)


def test_validate_customer_invalid_date():
    """Test validation with invalid date format."""
    record = CustomerRecord(
        customer_id="1",
        full_name="Jane Doe",
        email="jane@example.com",
        signup_date="invalid-date"
    )
    errors = validate_customer(record, 1)
    assert any(e.field == "signup_date" and "YYYY-MM-DD" in e.message for e in errors)


def test_validate_file_mixed_records():
    """Test file validation with mix of valid and invalid records."""
    records = [
        CustomerRecord("1", "Jane Doe", "jane@example.com", "2025-12-01"),  # Valid
        CustomerRecord("0", "J", "bad-email", "not-a-date"),  # Multiple errors
        CustomerRecord("3", "John Smith", "john@example.com", "2025-12-02"),  # Valid
    ]
    
    errors, counts = validate_file(records)
    
    assert counts.total_rows == 3
    assert counts.invalid_row_count == 1  # Only second record is invalid
    assert counts.validation_error_count == len(errors)
    assert len(errors) > 0  # Should have errors from second record


def test_validate_file_empty_records():
    """Test validation of empty file."""
    records = []
    errors, counts = validate_file(records)
    
    assert counts.total_rows == 0
    assert counts.invalid_row_count == 0
    assert counts.validation_error_count == 0
    assert len(errors) == 0


def test_validate_file_all_valid_records():
    """Test validation of file with all valid records."""
    records = [
        CustomerRecord("1", "Jane Doe", "jane@example.com", "2025-12-01"),
        CustomerRecord("2", "John Smith", "john@example.com", "2025-12-02"),
    ]
    
    errors, counts = validate_file(records)
    
    assert counts.total_rows == 2
    assert counts.invalid_row_count == 0
    assert counts.validation_error_count == 0
    assert len(errors) == 0