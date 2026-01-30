from datetime import date

from validator.models import CustomerRecord, ValidationError, ValidationCounts


def validate_customer(record: CustomerRecord, row_number: int) -> list[ValidationError]:
    """Validate a single customer record and return any errors found."""
    errors: list[ValidationError] = []

    # customer_id: required, integer, > 0
    if not record.customer_id:
        errors.append(ValidationError(row_number, "customer_id", "Required"))
    else:
        try:
            cid = int(record.customer_id)
            if cid <= 0:
                errors.append(ValidationError(row_number, "customer_id", "Must be > 0"))
        except ValueError:
            errors.append(ValidationError(row_number, "customer_id", "Must be an integer"))

    # full_name: required, length 2..80
    if not record.full_name:
        errors.append(ValidationError(row_number, "full_name", "Required"))
    else:
        if len(record.full_name) < 2 or len(record.full_name) > 80:
            errors.append(ValidationError(row_number, "full_name", "Length must be 2..80"))

    # email: required, simple format check
    if not record.email:
        errors.append(ValidationError(row_number, "email", "Required"))
    else:
        if "@" not in record.email or record.email.endswith("@"):
            errors.append(ValidationError(row_number, "email", "Invalid format"))

    # signup_date: required, YYYY-MM-DD format, not in future
    if not record.signup_date:
        errors.append(ValidationError(row_number, "signup_date", "Required"))
    else:
        try:
            yyyy, mm, dd = record.signup_date.split("-")
            d = date(int(yyyy), int(mm), int(dd))
            if d > date.today():
                errors.append(ValidationError(row_number, "signup_date", "Must not be in the future"))
        except Exception:
            errors.append(ValidationError(row_number, "signup_date", "Must be YYYY-MM-DD"))

    return errors


def validate_file(records: list[CustomerRecord]) -> tuple[list[ValidationError], ValidationCounts]:
    """Validate all records in a file and return errors and statistics."""
    all_errors: list[ValidationError] = []
    invalid_rows = 0

    # Row number 1 corresponds to first data row (header excluded)
    for idx, rec in enumerate(records, start=1):
        errs = validate_customer(rec, idx)
        if errs:
            invalid_rows += 1
            all_errors.extend(errs)

    counts = ValidationCounts(
        total_rows=len(records),
        invalid_row_count=invalid_rows,
        validation_error_count=len(all_errors),
    )
    return all_errors, counts