@echo off
echo Starting RemoteBatControl...

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

:: Check if requirements are installed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

:: Run the application
echo Running RemoteBatControl...
cd RemoteBatControl
python main.py

:: Deactivate virtual environment on exit
call venv\Scripts\deactivate.bat