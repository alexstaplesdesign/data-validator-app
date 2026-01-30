# 🛠️ Development Setup

## Prerequisites

- Python 3.10+ (3.11+ recommended)
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd data-validator-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=validator --cov-report=html

# Run specific test file
pytest tests/test_validation.py

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 validator tests

# Type checking
mypy validator
```

### Running the Applications

#### CLI Tool
```bash
python -m validator.cli --input data --reports reports --pattern "*.csv" --failOnError true
```

#### Web Interface
```bash
python -m validator.web
# Open http://localhost:8000
```

## Project Structure

```
data-validator-app/
├── .github/workflows/      # CI/CD pipeline
├── data/                   # Sample CSV files
├── validator/              # Main application package
│   ├── __init__.py
│   ├── cli.py             # CLI interface
│   ├── web.py             # Web interface (FastAPI)
│   ├── models.py          # Data models
│   ├── validation.py      # Core validation logic
│   ├── csv_io.py          # CSV file operations
│   ├── config.py          # Configuration
│   ├── discovery.py       # File discovery
│   ├── runner.py          # Validation runner
│   └── templates/         # HTML templates
│       └── dashboard.html
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_validation.py
│   ├── test_csv_io.py
│   └── test_cli.py
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

## Architecture

### Core Components

1. **Models** (`models.py`)
   - `CustomerRecord`: Data structure for customer data
   - `ValidationError`: Represents validation failures
   - `ValidationCounts`: Statistics about validation results

2. **Validation Engine** (`validation.py`)
   - `validate_customer()`: Validates individual records
   - `validate_file()`: Validates entire files

3. **I/O Operations** (`csv_io.py`)
   - `read_customers_csv()`: Parse CSV files
   - `write_errors_csv()`: Generate error reports

4. **CLI Interface** (`cli.py`)
   - Command-line argument parsing
   - Configuration management
   - Exit code handling

5. **Web Interface** (`web.py`)
   - FastAPI application
   - File upload endpoints
   - HTML dashboard

### Validation Rules

#### Customer ID
- Required field
- Must be an integer
- Must be greater than 0

#### Full Name
- Required field
- Length must be between 2-80 characters

#### Email
- Required field
- Must contain '@' symbol
- Must not end with '@'

#### Signup Date
- Required field
- Must be in YYYY-MM-DD format
- Must not be in the future

## Adding New Validation Rules

To add new validation rules:

1. Update the validation logic in `validator/validation.py`
2. Add corresponding tests in `tests/test_validation.py`
3. Update documentation if needed

Example:
```python
def validate_customer(record: CustomerRecord, row_number: int) -> list[ValidationError]:
    errors = []
    
    # Add new validation rule
    if record.some_field and len(record.some_field) > 100:
        errors.append(ValidationError(row_number, "some_field", "Too long"))
    
    return errors
```

## Deployment

### Docker (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "-m", "validator.web"]
```

### Production Considerations

- Use a production WSGI server like Gunicorn for the web interface
- Set up proper logging configuration
- Configure file upload limits
- Add authentication if needed
- Set up monitoring and health checks