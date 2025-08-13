@echo off
title Ragnarok X Auto Fishing Bot Launcher
echo.
echo ============================================
echo    Ragnarok X Auto Fishing Bot Launcher
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from python.org
    echo.
    pause
    exit /b 1
)

REM Check if main files exist
if not exist "launcher.py" (
    echo ERROR: launcher.py not found
    echo Please make sure you're running this from the correct directory
    echo.
    pause
    exit /b 1
)

echo Starting Ragnarok X Auto Fishing Bot...
echo.
echo If this is your first time running the bot:
echo 1. Run the system check from the launcher
echo 2. Use the coordinate detector to set up positions
echo 3. Configure settings before starting
echo.

REM Launch the Python launcher
python launcher.py

REM If launcher exits, show message
echo.
echo Bot launcher has closed.
echo.
pause
