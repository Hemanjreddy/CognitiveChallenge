@echo off
title Mercedes-Benz MF4 Signal Peak Detector
cd /d "%~dp0"

echo.
echo =====================================================
echo    Mercedes-Benz MF4 Signal Peak Detector
echo    Professional Vehicle Measurement Analysis
echo =====================================================
echo.

REM Create log file for debugging
set LOG_FILE=%~dp0setup.log
echo Installation started at %date% %time% > "%LOG_FILE%"

echo Checking system requirements...

REM Check if we're on 64-bit Windows
if not exist "%ProgramFiles(x86)%" (
    echo ERROR: This application requires 64-bit Windows
    echo Current system appears to be 32-bit
    echo.
    echo Please use a 64-bit Windows system
    pause
    exit /b 1
)

REM Try multiple Python detection methods
set PYTHON_FOUND=0
set PYTHON_EXE=

REM Method 1: Check PATH
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=python
    set PYTHON_FOUND=1
    echo Found Python in PATH
    goto :install_packages
)

REM Method 2: Check common installation paths
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
    "%ProgramFiles%\Python*\python.exe"
    "%ProgramFiles(x86)%\Python*\python.exe"
    "%USERPROFILE%\AppData\Local\Programs\Python\Python*\python.exe"
) do (
    if exist "%%P" (
        set PYTHON_EXE=%%P
        set PYTHON_FOUND=1
        echo Found Python at %%P
        goto :install_packages
    )
)

REM Method 3: Try py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=py
    set PYTHON_FOUND=1
    echo Found Python via py launcher
    goto :install_packages
)

REM No Python found
echo.
echo =====================================================
echo ERROR: Python not found on this system
echo =====================================================
echo.
echo This application requires Python 3.8 or later.
echo.
echo SOLUTION:
echo 1. Download Python from: https://python.org/downloads/
echo 2. During installation, CHECK "Add Python to PATH"
echo 3. Restart this application after installation
echo.
echo For enterprise users: Contact IT support
echo.
echo Details logged to: %LOG_FILE%
echo Python not found >> "%LOG_FILE%"
pause
exit /b 1

:install_packages
echo.
echo Installing required packages (this may take 2-3 minutes)...
echo Please wait - downloading Mercedes-Benz MF4 analysis tools...
echo.

REM Upgrade pip first
echo Updating package installer... >> "%LOG_FILE%"
"%PYTHON_EXE%" -m pip install --upgrade pip --quiet --disable-pip-version-check 2>> "%LOG_FILE%"

REM Install packages with better error handling
echo Installing Streamlit framework... >> "%LOG_FILE%"
"%PYTHON_EXE%" -m pip install streamlit --quiet --disable-pip-version-check 2>> "%LOG_FILE%"
if %errorlevel% neq 0 goto :install_error

echo Installing data analysis libraries... >> "%LOG_FILE%"
"%PYTHON_EXE%" -m pip install pandas numpy --quiet --disable-pip-version-check 2>> "%LOG_FILE%"
if %errorlevel% neq 0 goto :install_error

echo Installing visualization tools... >> "%LOG_FILE%"
"%PYTHON_EXE%" -m pip install plotly --quiet --disable-pip-version-check 2>> "%LOG_FILE%"
if %errorlevel% neq 0 goto :install_error

echo Installing signal processing... >> "%LOG_FILE%"
"%PYTHON_EXE%" -m pip install scipy --quiet --disable-pip-version-check 2>> "%LOG_FILE%"
if %errorlevel% neq 0 goto :install_error

echo Installing MF4 file processor... >> "%LOG_FILE%"
"%PYTHON_EXE%" -m pip install asammdf --quiet --disable-pip-version-check 2>> "%LOG_FILE%"
if %errorlevel% neq 0 goto :install_error

echo Installing Excel export... >> "%LOG_FILE%"
"%PYTHON_EXE%" -m pip install openpyxl --quiet --disable-pip-version-check 2>> "%LOG_FILE%"
if %errorlevel% neq 0 goto :install_error

echo Setup completed successfully >> "%LOG_FILE%"

goto :start_application

:install_error
echo.
echo =====================================================
echo ERROR: Failed to install required packages
echo =====================================================
echo.
echo POSSIBLE CAUSES:
echo - No internet connection
echo - Corporate firewall blocking downloads
echo - Insufficient disk space
echo - Python installation corrupted
echo.
echo SOLUTIONS:
echo - Check internet connection
echo - Run as Administrator
echo - Contact IT for corporate networks
echo - Reinstall Python from python.org
echo.
echo Details logged to: %LOG_FILE%
echo Package installation failed >> "%LOG_FILE%"
pause
exit /b 1

:start_application
echo.
echo =====================================================
echo Starting Mercedes-Benz MF4 Signal Peak Detector...
echo =====================================================
echo.
echo Opening web browser...
echo Application URL: http://localhost:8501
echo.
echo READY TO USE:
echo - Upload your MF4 files using the sidebar
echo - Configure peak detection parameters
echo - Enable anomaly detection for advanced analysis
echo - Export results to Excel or CSV
echo.
echo To stop: Close this window or press Ctrl+C
echo =====================================================

REM Start browser after delay
start "" "http://localhost:8501"

REM Start the application
"%PYTHON_EXE%" -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false --server.headless true 2>> "%LOG_FILE%"

if %errorlevel% neq 0 (
    echo.
    echo Application stopped with error
    echo Check %LOG_FILE% for details
    pause
)
