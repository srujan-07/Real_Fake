@echo off
REM Sic Mundus Vision - Quick Start Script for Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     SIC MUNDUS VISION - TIMELINE ARTIFACT ANALYSIS         ║
echo ║     Quick Start Setup for Windows                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python is not installed or not in PATH
    echo [!] Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

echo [+] Python detected

REM Install dependencies
echo.
echo [*] Installing dependencies from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo [!] Failed to install dependencies
    pause
    exit /b 1
)

echo [+] Dependencies installed successfully

REM Verify dataset
if not exist "artifacts\real\real_00.jpg" (
    echo.
    echo [*] Generating dataset...
    python generate_dataset.py
) else (
    echo [+] Dataset already exists
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     SETUP COMPLETE!                                       ║
echo ║                                                          ║
echo ║  To start the challenge server, run:                    ║
echo ║  python app.py                                          ║
echo ║                                                          ║
echo ║  Then open your browser to:                             ║
echo ║  http://127.0.0.1:5000                                  ║
echo ║                                                          ║
echo ║  To run the automated solver:                           ║
echo ║  python solver.py                                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pause
