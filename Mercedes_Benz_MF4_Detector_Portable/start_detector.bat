@echo off
title Mercedes-Benz MF4 Signal Peak Detector
echo ====================================================
echo Mercedes-Benz MF4 Signal Peak Detector
echo Professional Vehicle Measurement Analysis
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    echo.
    echo Please reinstall Python with pip included
    echo.
    pause
    exit /b 1
)

echo Installing required packages...
python -m pip install -r requirements_build.txt --quiet --disable-pip-version-check

if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    echo.
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo Starting application...
echo This may take 30-60 seconds on first launch...
echo.
echo The application will open in your web browser at:
echo http://localhost:8501
echo.
echo To stop the application, close this window or press Ctrl+C
echo ====================================================

python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

pause
