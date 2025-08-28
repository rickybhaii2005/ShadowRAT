@echo off
title RemoteBatControl - Installer Creator
echo ================================================================
echo           REMOTEBATCONTROL INSTALLER CREATOR
echo ================================================================
echo.
echo This script will create an installer for the RemoteBatControl application.
echo The installer will package all necessary files into a single executable.
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in the PATH.
    echo Please install Python 3.7 or later and try again.
    echo.
    pause
    exit /b 1
)

echo Options:
echo 1. Create installer with console window (recommended for first run)
echo 2. Create installer without console window
echo 3. Create installer with custom icon
echo 4. Exit
echo.

:menu
set /p choice=Enter your choice (1-4): 

if "%choice%"=="1" goto console
if "%choice%"=="2" goto no_console
if "%choice%"=="3" goto custom_icon
if "%choice%"=="4" goto end

echo Invalid choice. Please try again.
goto menu

:console
echo.
echo Creating installer with console window...
echo.
python create_installer.py --console
goto success

:no_console
echo.
echo Creating installer without console window...
echo.
python create_installer.py
goto success

:custom_icon
echo.
echo Enter the path to the icon file (.ico):
set /p icon_path=Icon path: 

if not exist "%icon_path%" (
    echo ERROR: Icon file not found.
    goto menu
)

echo.
echo Creating installer with custom icon...
echo.
python create_installer.py --icon "%icon_path%"
goto success

:success
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create installer.
    echo.
    pause
    exit /b 1
)

echo.
echo Installer created successfully!
echo You can find the installer in the current directory.
echo.
echo Run the installer to install RemoteBatControl on your system.
echo.
pause
goto end

:end
exit /b 0