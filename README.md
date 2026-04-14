# CSV Data Validator

Python tool for validating CSV files against a customer record schema.
Has both a CLI for batch use and a FastAPI web dashboard for uploading
files and reviewing results in the browser.

## Stack

Python 3.10+ · FastAPI · Jinja2 · Tailwind CSS · Alpine.js · Pytest · GitHub Actions

## Quick start — web dashboard

```bash
git clone https://github.com/alexstaplesdesign/data-validator-app.git
cd data-validator-app
pip install -r requirements.txt
uvicorn validator.web:app --reload
```

Open `http://localhost:8000`. Upload one or more CSV files and get a
summary of valid/invalid rows plus a per-field error breakdown.

## Quick start — CLI

```bash
python -m validator.cli --input ./data/in --reports ./reports
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | yes | — | Directory of CSV files |
| `--reports` | yes | — | Directory for output reports |
| `--pattern` | no | `*.csv` | Glob filter |
| `--failOnError` | no | `false` | Exit non-zero if any errors found |
| `--logLevel` | no | `INFO` | DEBUG / INFO / WARNING / ERROR |

## Validation rules

Applied to each row against these fields:

| Field | Rule |
|-------|------|
| `customer_id` | Required · must be a positive integer |
| `full_name` | Required · 2–80 characters |
| `email` | Required · must contain `@` and not end with it |
| `signup_date` | Required · `YYYY-MM-DD` format · not in the future |

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Dashboard UI |
| `GET` | `/health` | Health check |
| `POST` | `/api/validate` | Upload and validate CSV files |
| `GET` | `/api/samples` | List available sample files |
| `GET` | `/api/samples/download/{filename}` | Download a sample file |
| `GET` | `/api/reports` | List generated reports |

## Project structure

```
validator/
├── cli.py          # CLI entry point (argparse)
├── web.py          # FastAPI app and routes
├── validation.py   # Validation logic
├── runner.py       # Orchestration for CLI and web
├── csv_io.py       # CSV reading/writing
├── discovery.py    # File discovery
├── models.py       # CustomerRecord, ValidationError, etc.
├── config.py       # AppConfig
├── exit_codes.py
└── templates/      # Jinja2 HTML templates

tests/
├── test_validation.py
├── test_csv_io.py
└── test_cli.py
```

## Tests

```bash
pytest
```

22 tests covering validation rules, CSV I/O, and the CLI entry point.
Sample files in `data/` cover common scenarios: clean data, mixed errors,
edge cases, large dataset, and bad headers.
