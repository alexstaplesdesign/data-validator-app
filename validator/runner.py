import json
import logging
from pathlib import Path

from validator.config import AppConfig
from validator.csv_io import read_customers_csv, write_errors_csv
from validator.exit_codes import EXIT_OK, EXIT_INVALID_ARGS, EXIT_VALIDATION_ERRORS
from validator.validation import validate_file
from validator.models import FileValidationResult


log = logging.getLogger(__name__)


def run_validation(cfg: AppConfig, files: list[Path]) -> int:
    """Run validation on all files and generate reports."""
    summary = {
        "files": 0,
        "total_rows": 0,
        "invalid_rows": 0,
        "validation_errors": 0,
        "per_file": []
    }

    any_errors = False
    results: list[FileValidationResult] = []

    for file_path in files:
        if not file_path.is_file():
            continue

        summary["files"] += 1
        log.info("Validating %s", file_path.name)

        try:
            records = read_customers_csv(file_path)
        except ValueError as e:
            # Treat bad header/format as invalid args/config for this run
            log.error("File format error: %s", e)
            return EXIT_INVALID_ARGS

        errors, counts = validate_file(records)

        out_errors = cfg.reports_dir / f"{file_path.name}.errors.csv"
        write_errors_csv(out_errors, errors)

        # Create validation result
        result = FileValidationResult(
            filename=file_path.name,
            errors=errors,
            counts=counts,
            errors_report_path=str(out_errors.as_posix())
        )
        results.append(result)

        # Update summary
        summary["total_rows"] += counts.total_rows
        summary["invalid_rows"] += counts.invalid_row_count
        summary["validation_errors"] += counts.validation_error_count

        summary["per_file"].append({
            "file": file_path.name,
            "total_rows": counts.total_rows,
            "invalid_rows": counts.invalid_row_count,
            "validation_errors": counts.validation_error_count,
            "errors_report": str(out_errors.as_posix()),
        })

        if counts.validation_error_count > 0:
            any_errors = True
            log.warning("%s: invalid_rows=%d validation_errors=%d",
                        file_path.name, counts.invalid_row_count, counts.validation_error_count)

    # Write run summary
    run_summary_path = cfg.reports_dir / "run_summary.json"
    with run_summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    log.info("Run summary written to %s", run_summary_path)

    if cfg.fail_on_error and any_errors:
        return EXIT_VALIDATION_ERRORS
    return EXIT_OK


def run_validation_for_web(files: list[Path], reports_dir: Path) -> list[FileValidationResult]:
    """Run validation for web interface and return results without exit codes."""
    results: list[FileValidationResult] = []
    
    for file_path in files:
        if not file_path.is_file():
            continue

        try:
            records = read_customers_csv(file_path)
            errors, counts = validate_file(records)

            out_errors = reports_dir / f"{file_path.name}.errors.csv"
            write_errors_csv(out_errors, errors)

            result = FileValidationResult(
                filename=file_path.name,
                errors=errors,
                counts=counts,
                errors_report_path=str(out_errors.as_posix())
            )
            results.append(result)

        except ValueError as e:
            # For web interface, we'll handle errors differently
            log.error("File format error in %s: %s", file_path.name, e)
            continue

    return results