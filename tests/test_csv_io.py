import pytest
from pathlib import Path
import tempfile

from validator.csv_io import read_customers_csv, write_errors_csv
from validator.models import ValidationError


def test_read_customers_csv_valid_file(tmp_path):
    """Test reading a valid CSV file."""
    csv_content = """customer_id,full_name,email,signup_date
1,Jane Doe,jane@example.com,2025-12-01
2,John Smith,john@example.com,2025-12-02"""
    
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    records = read_customers_csv(csv_file)
    
    assert len(records) == 2
    assert records[0].customer_id == "1"
    assert records[0].full_name == "Jane Doe"
    assert records[0].email == "jane@example.com"
    assert records[0].signup_date == "2025-12-01"


def test_read_customers_csv_missing_columns(tmp_path):
    """Test reading CSV file with missing required columns."""
    csv_content = """customer_id,full_name
1,Jane Doe
2,John Smith"""
    
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    with pytest.raises(ValueError, match="Missing required column"):
        read_customers_csv(csv_file)


def test_read_customers_csv_empty_file(tmp_path):
    """Test reading empty CSV file."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")
    
    records = read_customers_csv(csv_file)
    assert len(records) == 0


def test_read_customers_csv_whitespace_handling(tmp_path):
    """Test CSV reading handles whitespace correctly."""
    csv_content = """customer_id,full_name,email,signup_date
  1  , Jane Doe , jane@example.com , 2025-12-01 """
    
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    records = read_customers_csv(csv_file)
    
    assert len(records) == 1
    assert records[0].customer_id == "1"
    assert records[0].full_name == "Jane Doe"
    assert records[0].email == "jane@example.com"
    assert records[0].signup_date == "2025-12-01"


def test_write_errors_csv(tmp_path):
    """Test writing validation errors to CSV file."""
    errors = [
        ValidationError(1, "customer_id", "Required"),
        ValidationError(2, "email", "Invalid format"),
        ValidationError(2, "signup_date", "Must be YYYY-MM-DD"),
    ]
    
    output_file = tmp_path / "reports" / "errors.csv"
    write_errors_csv(output_file, errors)
    
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    lines = content.strip().split('\n')
    
    assert len(lines) == 4  # Header + 3 error rows
    assert "row_number,field,message" in lines[0]
    assert "1,customer_id,Required" in lines[1]
    assert "2,email,Invalid format" in lines[2]
    assert "2,signup_date,Must be YYYY-MM-DD" in lines[3]


def test_write_errors_csv_empty(tmp_path):
    """Test writing empty errors list."""
    errors = []
    output_file = tmp_path / "empty_errors.csv"
    write_errors_csv(output_file, errors)
    
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    lines = content.strip().split('\n')
    
    assert len(lines) == 1  # Only header
    assert "row_number,field,message" in lines[0]