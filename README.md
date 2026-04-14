# CSV Data Validator

Python tool for validating CSV files, with both a CLI and a web dashboard.

## Stack

Python 3.10+ · FastAPI · Tailwind CSS · Alpine.js · Pytest · GitHub Actions

## Quick start

```bash
git clone https://github.com/alexstaplesdesign/data-validator-app.git
cd data-validator-app
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` for the web dashboard, or use the CLI directly.

## What it validates

- Customer ID (must be a positive integer)
- Full name (2–80 characters)
- Email (basic format check)
- Signup date (ISO format)

## Tests

```bash
pytest
```

22 tests covering validation rules, edge cases, and API endpoints.
