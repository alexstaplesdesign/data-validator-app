import csv
from pathlib import Path
from typing import Iterable

from validator.models import CustomerRecord, ValidationError


REQUIRED_COLUMNS = ("customer_id", "full_name", "email", "signup_date")


def read_customers_csv(path: Path) -> list[CustomerRecord]:
    """Read and parse a CSV file into CustomerRecord objects."""
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            return []

        header = [h.strip() for h in reader.fieldnames]
        missing = [c for c in REQUIRED_COLUMNS if c not in header]
        if missing:
            raise ValueError(f"Missing required column(s) in {path.name}: {', '.join(missing)}")

        rows: list[CustomerRecord] = []
        for row in reader:
            rows.append(CustomerRecord(
                customer_id=(row.get("customer_id") or "").strip(),
                full_name=(row.get("full_name") or "").strip(),
                email=(row.get("email") or "").strip(),
                signup_date=(row.get("signup_date") or "").strip(),
            ))
        return rows


def write_errors_csv(path: Path, errors: Iterable[ValidationError]) -> None:
    """Write validation errors to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["row_number", "field", "message"])
        for e in errors:
            writer.writerow([e.row_number, e.field, e.message])