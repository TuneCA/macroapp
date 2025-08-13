@echo off
title Ragnarok X Auto Fishing Bot - Installation
echo.
echo ==========================================
echo   Ragnarok X Auto Fishing Bot Setup
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Installing required packages...
echo.

REM Install packages from requirements.txt
if exist "requirements.txt" (
    echo Installing packages from requirements.txt...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) else (
    echo requirements.txt not found, installing packages individually...
    python -m pip install --upgrade pip
    python -m pip install pyautogui opencv-python numpy pillow pynput psutil configparser
)

if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Installation Complete!
echo ==========================================
echo.
echo The Ragnarok X Auto Fishing Bot is now ready to use.
echo.
echo To start the bot:
echo 1. Double-click "start_bot.bat" or
echo 2. Run "python launcher.py" from this directory
echo.
echo First-time setup:
echo 1. Run the system check from the launcher
echo 2. Use coordinate detector to set up positions
echo 3. Configure your settings
echo 4. Start with short test sessions
echo.
echo For help and documentation, see README.md
echo.
pause
