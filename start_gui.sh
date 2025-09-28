#!/bin/bash
# Password Generator Launcher for Unix/Linux/macOS
# This script activates the virtual environment and launches the password generator

echo "Starting Password Generator..."
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python -m venv venv"
    echo "Then: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and run launcher  
source venv/bin/activate
python launcher.py "$@"