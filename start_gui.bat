@echo off
REM Password Generator Launcher for Windows
REM This script activates the virtual environment and launches the password generator

echo Starting Password Generator...
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment and run launcher
call venv\Scripts\activate.bat
echo Setting up Tcl/Tk environment...
python launcher.py %*

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit...
    pause >nul
)