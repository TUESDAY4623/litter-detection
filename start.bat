@echo off
echo ==========================================
echo       Litter Project Starter
echo ==========================================

if not exist venv (
    echo [ERROR] Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo [INFO] Activating environment...
call venv\Scripts\activate.bat

echo [INFO] Starting Application...
python main.py --mode full

pause
