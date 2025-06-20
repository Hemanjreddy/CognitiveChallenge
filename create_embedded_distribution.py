#!/usr/bin/env python3
"""
Create embedded Python distribution for Mercedes-Benz MF4 Signal Peak Detector
This creates a truly self-contained executable that doesn't require Python installation
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

def create_embedded_python_app():
    """Create application with embedded Python"""
    
    print("Creating self-contained application with embedded Python...")
    
    # Create distribution directory
    dist_dir = Path("Mercedes_Benz_MF4_Detector_SelfContained")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy application files
    app_files = ["app.py", "utils/", ".streamlit/"]
    for file_path in app_files:
        src = Path(file_path)
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dist_dir / src.name)
            else:
                shutil.copy2(src, dist_dir / src.name)
    
    # Create requirements file with exact versions
    requirements_content = """streamlit==1.45.1
pandas==2.3.0
numpy==2.3.0
plotly==6.1.2
scipy==1.15.3
asammdf==8.5.0
openpyxl==3.1.5
altair==5.5.0
lxml==5.4.0
lz4==4.4.4
numexpr==2.11.0
"""
    
    with open(dist_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)
    
    # Create advanced launcher with embedded Python check
    launcher_content = """@echo off
title Mercedes-Benz MF4 Signal Peak Detector
cd /d "%~dp0"

echo ====================================================
echo Mercedes-Benz MF4 Signal Peak Detector
echo Professional Vehicle Measurement Analysis
echo ====================================================
echo.

set PYTHON_DIR=%~dp0python
set PYTHON_EXE=%PYTHON_DIR%\\python.exe
set SCRIPTS_DIR=%PYTHON_DIR%\\Scripts

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
"""
    
    with open(dist_dir / "Mercedes_Benz_MF4_Detector.bat", "w") as f:
        f.write(launcher_content)
    
    return dist_dir

def create_installation_guide():
    """Create detailed installation guide"""
    
    guide_content = """# Mercedes-Benz MF4 Signal Peak Detector - Installation Guide

## Quick Start (Recommended)

### For Windows Users:
1. Extract all files to a folder (e.g., C:\\Mercedes_MF4_Detector)
2. Double-click `Mercedes_Benz_MF4_Detector.bat`
3. Wait for the application to start (30-60 seconds)
4. Browser will open automatically to http://localhost:8501

## System Requirements

### Minimum Requirements:
- Windows 10/11 (64-bit)
- 4GB RAM
- 2GB free disk space
- Internet connection (for initial setup)

### Recommended:
- 8GB RAM (for large MF4 files)
- SSD storage
- Modern web browser (Chrome, Firefox, Edge)

## Installation Options

### Option A: Automatic Setup (Easiest)
The provided batch file will automatically:
1. Detect if Python is installed
2. Install required packages
3. Start the application
4. Open your browser

### Option B: Manual Python Installation
If you don't have Python:
1. Download Python 3.8+ from https://python.org/downloads/
2. During installation, CHECK "Add Python to PATH"
3. Run Mercedes_Benz_MF4_Detector.bat

### Option C: Portable Python (Advanced)
For completely self-contained deployment:
1. Download Python embeddable package
2. Extract to 'python' subfolder
3. Install pip manually
4. Run the application

## Troubleshooting

### "Python not found" Error
**Solution**: Install Python from python.org and ensure "Add Python to PATH" is checked

### "pip not recognized" Error
**Solution**: Reinstall Python with pip included, or use: python -m pip instead of pip

### "Failed to install packages" Error
**Causes**:
- No internet connection
- Corporate firewall blocking PyPI
- Insufficient permissions

**Solutions**:
- Check internet connection
- Run as administrator
- Configure proxy settings if needed
- Contact IT for corporate environments

### Port 8501 Already in Use
**Solution**: Close other Streamlit applications or change port in the batch file

### Browser Doesn't Open
**Solution**: Manually navigate to http://localhost:8501

### Application Runs Slowly
**Causes**:
- Large MF4 files
- Insufficient RAM
- Many signals selected

**Solutions**:
- Process smaller file sections
- Close other applications
- Select fewer signals initially

## Features Overview

### File Processing
- Supports standard MF4 format files
- Handles multi-group measurements
- Processes files up to several GB
- Real-time progress feedback

### Peak Detection
- Configurable height thresholds
- Distance and prominence filtering
- Width calculation
- Batch processing capabilities

### Anomaly Detection
- Statistical outlier detection
- Z-score analysis
- Interquartile range method
- Temporal pattern analysis
- Isolation forest algorithm

### Visualization
- Interactive Plotly charts
- Multi-signal display
- Zoom and pan capabilities
- Color-coded peak markers

### Export Options
- CSV format with metadata
- JSON structured data
- Excel multi-sheet format
- Comprehensive statistics

## Performance Tips

### For Large Files:
- Select specific signals instead of all
- Adjust peak detection parameters
- Process in smaller time windows
- Close unnecessary applications

### For Better Results:
- Use appropriate height thresholds
- Configure distance parameters based on signal characteristics
- Enable relevant anomaly detection methods
- Adjust sensitivity thresholds

## Security and Privacy

### Data Handling:
- All processing is local (no cloud upload)
- Temporary files are cleaned automatically
- No data is stored permanently
- Session-based processing only

### Network Usage:
- Only for downloading packages (first run)
- No data transmission to external servers
- Local web interface only

## Support

### Self-Help:
1. Check console output for error messages
2. Verify MF4 file format compatibility
3. Ensure sufficient system resources
4. Review this installation guide

### Enterprise Support:
- Contact your system administrator
- Provide error messages and system specifications
- Include sample MF4 file for testing (if possible)

---

Mercedes-Benz MF4 Signal Peak Detector v1.0
Professional Vehicle Measurement Analysis Tool
"""
    
    with open("Installation_Guide.md", "w") as f:
        f.write(guide_content)
    
    print("Installation guide created: Installation_Guide.md")

def create_simple_exe_alternative():
    """Create a simple Python script that can be converted to EXE"""
    
    simple_app_content = """#!/usr/bin/env python3
'''
Simple launcher for Mercedes-Benz MF4 Signal Peak Detector
This version is designed to be converted to EXE with auto-py-to-exe
'''

import subprocess
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

def install_requirements():
    '''Install required packages'''
    requirements = [
        'streamlit==1.45.1',
        'pandas==2.3.0', 
        'numpy==2.3.0',
        'plotly==6.1.2',
        'scipy==1.15.3',
        'asammdf==8.5.0',
        'openpyxl==3.1.5'
    ]
    
    print("Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--quiet'])
        except subprocess.CalledProcessError:
            print(f"Warning: Could not install {package}")

def open_browser():
    '''Open browser after delay'''
    time.sleep(5)
    webbrowser.open('http://localhost:8501')

def main():
    print("=" * 60)
    print("Mercedes-Benz MF4 Signal Peak Detector")
    print("Professional Vehicle Measurement Analysis")
    print("=" * 60)
    
    # Install requirements
    install_requirements()
    
    # Start browser thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Get app directory
    if getattr(sys, 'frozen', False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent
    
    app_file = app_dir / 'app.py'
    
    if not app_file.exists():
        print(f"Error: app.py not found in {app_dir}")
        input("Press Enter to exit...")
        return
    
    print("Starting application server...")
    print("Browser will open automatically at http://localhost:8501")
    print("To stop: Close this window")
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', str(app_file),
            '--server.port', '8501',
            '--browser.gatherUsageStats', 'false',
            '--server.headless', 'true'
        ])
    except KeyboardInterrupt:
        print("Application stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
"""
    
    with open("simple_launcher.py", "w") as f:
        f.write(simple_app_content)
    
    print("Simple launcher created: simple_launcher.py")

def main():
    """Create comprehensive distribution packages"""
    
    print("=== Creating Self-Contained Mercedes-Benz MF4 Detector ===\n")
    
    # Create self-contained app
    dist_dir = create_embedded_python_app()
    
    # Create installation guide  
    create_installation_guide()
    
    # Create simple EXE alternative
    create_simple_exe_alternative()
    
    # Create updated ZIP package
    zip_name = "Mercedes_Benz_MF4_Detector_Complete.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(dist_dir.parent)
                zipf.write(file_path, arcname)
        
        # Add documentation
        zipf.write("Installation_Guide.md")
        zipf.write("simple_launcher.py")
    
    print(f"\n=== Distribution Complete ===")
    print(f"Created files:")
    print(f"1. {dist_dir}/ - Self-contained application")
    print(f"2. {zip_name} - Complete distribution package")
    print(f"3. Installation_Guide.md - Detailed setup instructions")
    print(f"4. simple_launcher.py - EXE-compatible launcher")
    
    print(f"\n=== Usage Instructions ===")
    print(f"For end users:")
    print(f"1. Extract {zip_name}")
    print(f"2. Run Mercedes_Benz_MF4_Detector.bat")
    print(f"3. Application opens in web browser")
    
    print(f"\nFor EXE creation:")
    print(f"1. Install auto-py-to-exe: pip install auto-py-to-exe")
    print(f"2. Run: auto-py-to-exe simple_launcher.py")
    print(f"3. Configure as one-file executable")
    
    return True

if __name__ == "__main__":
    main()