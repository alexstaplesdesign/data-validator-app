import pytest
import json
from pathlib import Path

from validator.cli import main


def test_cli_help():
    """Test CLI help output."""
    exit_code = main(["--help"])
    assert exit_code == 0


def test_cli_missing_required_args():
    """Test CLI with missing required arguments."""
    exit_code = main([])
    assert exit_code == 2  # EXIT_INVALID_ARGS


def test_cli_invalid_input_directory():
    """Test CLI with non-existent input directory."""
    exit_code = main([
        "--input", "/nonexistent/path",
        "--reports", "/tmp/reports"
    ])
    assert exit_code == 2  # EXIT_INVALID_ARGS


def test_cli_successful_validation(tmp_path):
    """Test successful CLI validation run."""
    # Setup directories
    input_dir = tmp_path / "input"
    reports_dir = tmp_path / "reports"
    input_dir.mkdir()
    
    # Create valid test CSV
    csv_content = """customer_id,full_name,email,signup_date
1,Jane Doe,jane@example.com,2025-12-01
2,John Smith,john@example.com,2025-12-02"""
    
    (input_dir / "customers.csv").write_text(csv_content, encoding="utf-8")
    
    # Run CLI
    exit_code = main([
        "--input", str(input_dir),
        "--reports", str(reports_dir),
        "--pattern", "*.csv",
        "--failOnError", "false"
    ])
    
    assert exit_code == 0
    
    # Check outputs
    assert (reports_dir / "customers.csv.errors.csv").exists()
    assert (reports_dir / "run_summary.json").exists()
    
    # Check summary content
    summary = json.loads((reports_dir / "run_summary.json").read_text(encoding="utf-8"))
    assert summary["files"] == 1
    assert summary["total_rows"] == 2
    assert summary["validation_errors"] == 0


def test_cli_validation_with_errors(tmp_path):
    """Test CLI validation with validation errors."""
    # Setup directories
    input_dir = tmp_path / "input"
    reports_dir = tmp_path / "reports"
    input_dir.mkdir()
    
    # Create CSV with errors
    csv_content = """customer_id,full_name,email,signup_date
0,J,bad-email,invalid-date
2,John Smith,john@example.com,2025-12-02"""
    
    (input_dir / "customers.csv").write_text(csv_content, encoding="utf-8")
    
    # Run CLI with failOnError=false
    exit_code = main([
        "--input", str(input_dir),
        "--reports", str(reports_dir),
        "--pattern", "*.csv",
        "--failOnError", "false"
    ])
    
    assert exit_code == 0  # Should succeed even with validation errors
    
    # Run CLI with failOnError=true
    exit_code = main([
        "--input", str(input_dir),
        "--reports", str(reports_dir),
        "--pattern", "*.csv",
        "--failOnError", "true"
    ])
    
    assert exit_code == 4  # EXIT_VALIDATION_ERRORS


def test_cli_invalid_file_format(tmp_path):
    """Test CLI with invalid file format."""
    # Setup directories
    input_dir = tmp_path / "input"
    reports_dir = tmp_path / "reports"
    input_dir.mkdir()
    
    # Create CSV missing required columns
    csv_content = """customer_id,full_name
1,Jane Doe"""
    
    (input_dir / "bad.csv").write_text(csv_content, encoding="utf-8")
    
    # Run CLI
    exit_code = main([
        "--input", str(input_dir),
        "--reports", str(reports_dir),
        "--pattern", "*.csv"
    ])
    
    assert exit_code == 2  # EXIT_INVALID_ARGS


def test_cli_custom_log_level(tmp_path):
    """Test CLI with custom log level."""
    input_dir = tmp_path / "input"
    reports_dir = tmp_path / "reports"
    input_dir.mkdir()
    
    # Create valid test CSV
    csv_content = """customer_id,full_name,email,signup_date
1,Jane Doe,jane@example.com,2025-12-01"""
    
    (input_dir / "test.csv").write_text(csv_content, encoding="utf-8")
    
    # Run with DEBUG log level
    exit_code = main([
        "--input", str(input_dir),
        "--reports", str(reports_dir),
        "--logLevel", "DEBUG"
    ])
    
    assert exit_code == 0