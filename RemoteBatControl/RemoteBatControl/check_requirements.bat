@echo off
echo Checking system requirements for RemoteBatControl...

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

:: Run the requirements checker script
python check_requirements.py

pause