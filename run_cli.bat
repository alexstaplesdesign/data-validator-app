@echo off
cd /d "%~dp0"
if not exist .venv (
    echo Creating virtual environment...
    py -m venv .venv
)
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo Installing/updating dependencies...
pip install fastapi uvicorn[standard] python-multipart jinja2 aiofiles
echo.
echo Data Validator CLI Tool
echo Usage: python -m validator.cli [options] [file_or_directory]
echo.
echo Examples:
echo   python -m validator.cli data/sample_valid.csv
echo   python -m validator.cli data/
echo   python -m validator.cli --help
echo.
cmd /k