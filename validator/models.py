from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CustomerRecord:
    """Represents a customer record from CSV data."""
    customer_id: str
    full_name: str
    email: str
    signup_date: str


@dataclass(frozen=True)
class ValidationError:
    """Represents a validation error for a specific field and row."""
    row_number: int
    field: str
    message: str


@dataclass(frozen=True)
class ValidationCounts:
    """Statistics about validation results."""
    total_rows: int
    invalid_row_count: int
    validation_error_count: int


@dataclass(frozen=True)
class FileValidationResult:
    """Complete validation result for a single file."""
    filename: str
    errors: list[ValidationError]
    counts: ValidationCounts
    errors_report_path: Optional[str] = None