#!/usr/bin/env python3
"""
Create distribution packages for Mercedes-Benz MF4 Signal Peak Detector
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path

def create_portable_app():
    """Create a portable Python application package"""
    
    print("Creating portable application package...")
    
    # Create distribution directory
    dist_dir = Path("Mercedes_Benz_MF4_Detector_Portable")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy application files
    files_to_copy = [
        "app.py",
        "utils/",
        ".streamlit/",
        "requirements_build.txt",
        "README_EXECUTABLE.txt"
    ]
    
    for file_path in files_to_copy:
        src = Path(file_path)
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dist_dir / src.name)
            else:
                shutil.copy2(src, dist_dir / src.name)
    
    # Create launcher script
    launcher_script = f'''@echo off
title Mercedes-Benz MF4 Signal Peak Detector
echo ====================================================
echo Mercedes-Benz MF4 Signal Peak Detector
echo Professional Vehicle Measurement Analysis
echo ====================================================
echo.
echo Installing required packages...
pip install -r requirements_build.txt

echo.
echo Starting application...
echo This may take 30-60 seconds on first launch...
echo.
echo The application will open in your web browser at:
echo http://localhost:8501
echo.
echo To stop the application, close this window or press Ctrl+C
echo ====================================================

streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

pause
'''
    
    with open(dist_dir / "start_detector.bat", "w") as f:
        f.write(launcher_script)
    
    # Create Linux/Mac launcher
    linux_launcher = f'''#!/bin/bash
echo "===================================================="
echo "Mercedes-Benz MF4 Signal Peak Detector"
echo "Professional Vehicle Measurement Analysis"
echo "===================================================="
echo ""
echo "Installing required packages..."
pip3 install -r requirements_build.txt

echo ""
echo "Starting application..."
echo "This may take 30-60 seconds on first launch..."
echo ""
echo "The application will open in your web browser at:"
echo "http://localhost:8501"
echo ""
echo "To stop the application, press Ctrl+C"
echo "===================================================="

streamlit run app.py --server.port 8501 --browser.gatherUsageStats false
'''
    
    with open(dist_dir / "start_detector.sh", "w") as f:
        f.write(linux_launcher)
    
    # Make shell script executable
    os.chmod(dist_dir / "start_detector.sh", 0o755)
    
    print(f"Portable application created in: {dist_dir}")
    return dist_dir

def create_zip_package(dist_dir):
    """Create ZIP package of the portable application"""
    
    zip_name = "Mercedes_Benz_MF4_Detector_Portable.zip"
    
    print(f"Creating ZIP package: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(dist_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"ZIP package created: {zip_name}")
    return zip_name

def create_installer_script():
    """Create a simple installer script"""
    
    installer_content = '''@echo off
title Mercedes-Benz MF4 Detector Installer
echo ====================================================
echo Mercedes-Benz MF4 Signal Peak Detector - Installer
echo ====================================================
echo.

set INSTALL_DIR=%USERPROFILE%\\Mercedes_Benz_MF4_Detector

echo Installing to: %INSTALL_DIR%
echo.

if exist "%INSTALL_DIR%" (
    echo Removing existing installation...
    rmdir /s /q "%INSTALL_DIR%"
)

echo Creating installation directory...
mkdir "%INSTALL_DIR%"

echo Copying application files...
xcopy /s /e /y Mercedes_Benz_MF4_Detector_Portable\\* "%INSTALL_DIR%\\"

echo Creating desktop shortcut...
set SHORTCUT_PATH=%USERPROFILE%\\Desktop\\Mercedes-Benz MF4 Detector.lnk
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\start_detector.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Mercedes-Benz MF4 Signal Peak Detector'; $Shortcut.Save()"

echo.
echo ====================================================
echo Installation complete!
echo.
echo Application installed to: %INSTALL_DIR%
echo Desktop shortcut created: Mercedes-Benz MF4 Detector
echo.
echo To start the application:
echo 1. Double-click the desktop shortcut, or
echo 2. Run: %INSTALL_DIR%\\start_detector.bat
echo ====================================================

pause
'''
    
    with open("install_detector.bat", "w") as f:
        f.write(installer_content)
    
    print("Installer script created: install_detector.bat")

def create_user_guide():
    """Create comprehensive user guide"""
    
    guide_content = '''# Mercedes-Benz MF4 Signal Peak Detector - User Guide

## System Requirements
- Windows 10/11, macOS 10.14+, or Linux
- Python 3.8 or later
- 4GB RAM (8GB recommended for large files)
- 2GB free disk space
- Web browser (Chrome, Firefox, Safari, Edge)

## Installation Options

### Option 1: Portable Application (Recommended)
1. Extract Mercedes_Benz_MF4_Detector_Portable.zip
2. Run start_detector.bat (Windows) or start_detector.sh (Linux/Mac)
3. Wait for browser to open automatically

### Option 2: Manual Installation
1. Install Python 3.8+ from python.org
2. Extract application files
3. Run: pip install -r requirements_build.txt
4. Run: streamlit run app.py

### Option 3: Standalone Executable (if available)
1. Run Mercedes_Benz_MF4_Peak_Detector.exe
2. Wait for browser to open at http://localhost:8501

## Using the Application

### 1. Upload MF4 File
- Click "Browse files" in the sidebar
- Select your .mf4 or .dat file
- Wait for processing to complete

### 2. Configure Peak Detection
- Adjust Height Threshold (signal noise sensitivity)
- Set Minimum Distance between peaks
- Configure Prominence requirements
- Set Peak Width Range

### 3. Enable Anomaly Detection
- Check "Enable Anomaly Detection"
- Select detection methods:
  * Statistical: Robust outlier detection
  * Z-Score: Standard deviation based
  * IQR: Interquartile range method
  * Temporal: Time pattern analysis
  * Isolation Forest: Advanced feature analysis
- Adjust thresholds for sensitivity

### 4. Analyze Results
- View interactive signal plots
- Examine detected peaks (red diamonds)
- Review anomalous peaks (orange triangles)
- Check statistics and summaries

### 5. Export Data
- Export to CSV for spreadsheet analysis
- Export to JSON for programmatic use
- Download detailed peak information

## Troubleshooting

### Application Won't Start
- Ensure Python is installed and accessible
- Check that port 8501 is not in use
- Try running as administrator (Windows)
- Verify all dependencies are installed

### File Processing Errors
- Ensure MF4 file is not corrupted
- Check file permissions
- For large files, allow extra processing time
- Verify sufficient disk space

### Browser Issues
- Clear browser cache
- Try different browser
- Disable ad blockers
- Check firewall settings for localhost

### Performance Issues
- Close other applications
- Increase available RAM
- Process smaller file sections
- Reduce number of selected signals

## Features Overview

### Peak Detection Algorithms
- Scipy-based signal processing
- Configurable height, distance, prominence
- Width calculation and filtering
- Progress tracking for batch processing

### Anomaly Detection Methods
- **Statistical**: Modified Z-score using median absolute deviation
- **Z-Score**: Classic mean/standard deviation approach
- **IQR**: Quartile-based outlier identification
- **Temporal**: Pattern analysis in peak timing
- **Isolation Forest**: Multi-dimensional feature analysis

### Visualization
- Interactive Plotly charts
- Multi-signal subplot display
- Zoom, pan, and hover capabilities
- Color-coded peak and anomaly markers

### Export Capabilities
- CSV format with metadata headers
- JSON format with structured data
- Excel format with multiple sheets
- Comprehensive statistics inclusion

## Support and Maintenance

### Regular Maintenance
- Update Python and dependencies monthly
- Clear temporary files periodically
- Backup important analysis results
- Monitor disk space usage

### Getting Help
- Check console output for error messages
- Verify file formats are supported
- Ensure system requirements are met
- Contact system administrator for enterprise support

## Technical Specifications

### Supported File Formats
- MF4 (Measurement File Format version 4)
- DAT files compatible with ASAMDF
- Multi-group measurement files
- Files with complex channel hierarchies

### Processing Capabilities
- Handles files up to several GB
- Processes thousands of signals
- Real-time progress feedback
- Memory-efficient data handling

### Security Features
- Local processing only (no cloud upload)
- Temporary file cleanup
- Session-based data handling
- No persistent data storage

---

Version: 1.0
Built for Mercedes-Benz automotive engineers and data analysts
Compatible with industry-standard MF4 measurement files
'''
    
    with open("User_Guide.md", "w") as f:
        f.write(guide_content)
    
    print("User guide created: User_Guide.md")

def main():
    """Main distribution creation process"""
    
    print("=== Mercedes-Benz MF4 Signal Peak Detector - Distribution Creator ===\n")
    
    try:
        # Create portable application
        dist_dir = create_portable_app()
        
        # Create ZIP package
        zip_file = create_zip_package(dist_dir)
        
        # Create installer script
        create_installer_script()
        
        # Create user guide
        create_user_guide()
        
        print(f"\n=== Distribution Creation Complete ===")
        print(f"Created files:")
        print(f"1. {dist_dir}/ - Portable application folder")
        print(f"2. {zip_file} - ZIP package for distribution")
        print(f"3. install_detector.bat - Windows installer script")
        print(f"4. User_Guide.md - Comprehensive user guide")
        
        print(f"\n=== Distribution Instructions ===")
        print(f"To distribute the application:")
        print(f"1. Share {zip_file} with users")
        print(f"2. Users extract and run start_detector.bat (Windows) or start_detector.sh (Linux/Mac)")
        print(f"3. Application opens in web browser automatically")
        
        return True
        
    except Exception as e:
        print(f"Error creating distribution: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)