@echo off
title Mercedes-Benz MF4 Signal Peak Detector
cd /d "%~dp0"

echo ====================================================
echo Mercedes-Benz MF4 Signal Peak Detector
echo Professional Vehicle Measurement Analysis
echo ====================================================
echo.

set PYTHON_DIR=%~dp0python
set PYTHON_EXE=%PYTHON_DIR%\python.exe
set SCRIPTS_DIR=%PYTHON_DIR%\Scripts

REM Check for embedded Python first
if exist "%PYTHON_EXE%" (
    echo Using embedded Python...
    set PATH=%PYTHON_DIR%;%SCRIPTS_DIR%;%PATH%
    goto :install_packages
)

REM Check for system Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using system Python...
    set PYTHON_EXE=python
    goto :install_packages
)

REM No Python found
echo ERROR: Python not found
echo.
echo This application requires Python 3.8 or later.
echo.
echo Option 1: Install Python from https://python.org/downloads/
echo           Make sure to check "Add Python to PATH"
echo.
echo Option 2: Download the self-contained version with embedded Python
echo.
pause
exit /b 1

:install_packages
echo Installing/updating required packages...
"%PYTHON_EXE%" -m pip install --upgrade pip --quiet --disable-pip-version-check
"%PYTHON_EXE%" -m pip install -r requirements.txt --quiet --disable-pip-version-check

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install packages
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo Starting Mercedes-Benz MF4 Signal Peak Detector...
echo.
echo The application will open in your web browser
echo URL: http://localhost:8501
echo.
echo To stop: Close this window or press Ctrl+C
echo ====================================================

start "" "http://localhost:8501"
"%PYTHON_EXE%" -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false --server.headless true

pause
