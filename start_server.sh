#!/bin/bash
# Linux/macOS startup script

cd "$(dirname "$0")"
source .venv/bin/activate
echo "🚀 Starting Data Validator Web Server..."
echo "📊 Open http://localhost:8000 in your browser"
python -m validator.web