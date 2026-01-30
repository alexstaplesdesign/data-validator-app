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
echo Starting web server...
echo.
echo Opening http://localhost:8000 in your browser...
echo Press Ctrl+C to stop the server
echo.
python -m validator.web
pause