@echo off
cd /d "C:\Users\ajsta\OneDrive\Desktop\data-validator-app"
call .venv\Scripts\activate.bat
echo 🚀 Starting Data Validator Web Server...
echo 📊 Open http://localhost:8000 in your browser
python -m validator.web