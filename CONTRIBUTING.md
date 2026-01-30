# Contributing to Data Validator App

Thank you for your interest in contributing! We welcome contributions from the community.

## 🚀 Quick Start for Contributors

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create** a virtual environment and install dependencies
4. **Create** a new branch for your feature
5. **Make** your changes and add tests
6. **Submit** a pull request

## 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/data-validator-app.git
cd data-validator-app

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest pytest-cov black isort flake8 mypy
```

## 🧪 Running Tests

```bash
# Run all tests
pytest -v

# Run tests with coverage
pytest --cov=validator --cov-report=html

# Run specific test file
pytest tests/test_validation.py -v
```

## 📝 Code Style

We use automated code formatting and linting:

```bash
# Format code
black .
isort .

# Check linting
flake8 validator tests

# Type checking
mypy validator
```

## 🐛 Bug Reports

When filing a bug report, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Sample CSV file (if applicable)

## 💡 Feature Requests

For feature requests, please:

- Check existing issues first
- Provide detailed use case
- Include examples if applicable
- Consider implementation complexity

## 📬 Pull Request Guidelines

- Keep changes focused and atomic
- Write clear commit messages
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style

## 🎯 Areas for Contribution

- 🧪 **Additional validation rules**
- 🎨 **UI/UX improvements**
- 📊 **New export formats**
- 🔧 **Performance optimizations**
- 📖 **Documentation improvements**
- 🌍 **Internationalization**

## 📞 Questions?

Feel free to open a discussion or reach out if you have questions about contributing!