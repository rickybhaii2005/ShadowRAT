@echo off
echo Generating configuration for RemoteBatControl...

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

:: Run the configuration generator script
python generate_config.py

pause