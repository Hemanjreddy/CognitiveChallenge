#!/usr/bin/env python3
"""
Build script to create standalone executable for Mercedes-Benz MF4 Signal Peak Detector
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_spec_file():
    """Create PyInstaller spec file for the application"""
    
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('utils', 'utils'),
        ('.streamlit', '.streamlit'),
    ],
    hiddenimports=[
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'scipy',
        'asammdf',
        'openpyxl',
        'altair',
        'click',
        'tornado',
        'pyarrow',
        'plotly.graph_objects',
        'plotly.subplots',
        'scipy.signal',
        'scipy.stats',
        'streamlit.web.cli',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Mercedes_Benz_MF4_Peak_Detector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='mercedes_icon.ico'
)
'''
    
    with open('mercedes_detector.spec', 'w') as f:
        f.write(spec_content.strip())
    
    print("Created PyInstaller spec file: mercedes_detector.spec")

def create_launcher_script():
    """Create a launcher script that starts Streamlit server"""
    
    launcher_content = '''
import streamlit.web.cli as stcli
import sys
import os
from pathlib import Path

def main():
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = Path(sys.executable).parent
    else:
        # Running as script
        app_dir = Path(__file__).parent
    
    # Set the working directory
    os.chdir(app_dir)
    
    # Add the app directory to Python path
    sys.path.insert(0, str(app_dir))
    
    # Launch Streamlit with the app
    sys.argv = [
        "streamlit",
        "run",
        str(app_dir / "app.py"),
        "--server.port=8501",
        "--server.address=127.0.0.1",
        "--browser.serverAddress=127.0.0.1",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ]
    
    print("Starting Mercedes-Benz MF4 Signal Peak Detector...")
    print("Open your browser and go to: http://localhost:8501")
    
    stcli.main()

if __name__ == "__main__":
    main()
'''
    
    with open('launcher.py', 'w') as f:
        f.write(launcher_content.strip())
    
    print("Created launcher script: launcher.py")

def create_requirements_file():
    """Create requirements file for building"""
    
    requirements = '''
streamlit>=1.45.1
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.0.0
scipy>=1.10.0
asammdf>=8.0.0
openpyxl>=3.0.0
pyinstaller>=5.0.0
altair>=5.0.0
'''
    
    with open('requirements_build.txt', 'w') as f:
        f.write(requirements.strip())
    
    print("Created requirements file: requirements_build.txt")

def create_build_batch():
    """Create batch file for Windows build process"""
    
    batch_content = '''@echo off
echo Building Mercedes-Benz MF4 Signal Peak Detector...

echo Installing build dependencies...
pip install -r requirements_build.txt

echo Creating executable...
pyinstaller --clean mercedes_detector.spec

echo Build complete!
echo Executable location: dist/Mercedes_Benz_MF4_Peak_Detector.exe

pause
'''
    
    with open('build.bat', 'w') as f:
        f.write(batch_content)
    
    print("Created build batch file: build.bat")

def create_readme():
    """Create README for the executable"""
    
    readme_content = '''# Mercedes-Benz MF4 Signal Peak Detector - Standalone Application

## About
This is a standalone executable version of the Mercedes-Benz MF4 Signal Peak Detector application.
It provides comprehensive analysis of vehicle measurement files (MF4 format) with advanced peak detection
and anomaly analysis capabilities.

## Features
- MF4 file processing using ASAMMDF library
- Interactive signal visualization
- Peak detection with configurable parameters
- Advanced anomaly detection with multiple methods:
  * Statistical outlier detection
  * Z-score analysis
  * Interquartile Range (IQR)
  * Temporal pattern analysis
  * Isolation Forest approach
- Export capabilities (CSV, JSON, Excel)
- Professional Mercedes-Benz themed interface

## How to Use
1. Run Mercedes_Benz_MF4_Peak_Detector.exe
2. Wait for the application to start (may take 30-60 seconds on first run)
3. Open your web browser and go to: http://localhost:8501
4. Upload your MF4 file and configure analysis parameters
5. View results and export data as needed

## System Requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space
- Web browser (Chrome, Firefox, Edge)

## Troubleshooting
- If the application doesn't start, try running as administrator
- Ensure port 8501 is not blocked by firewall
- For large MF4 files, allow extra time for processing
- Close any other applications using port 8501

## Support
This application was built for Mercedes-Benz automotive engineers and data analysts.
For technical support, please contact your system administrator.

Version: 1.0
Built with Python, Streamlit, and PyInstaller
'''
    
    with open('README_EXECUTABLE.txt', 'w') as f:
        f.write(readme_content)
    
    print("Created README file: README_EXECUTABLE.txt")

def build_executable():
    """Main build process"""
    
    print("=== Mercedes-Benz MF4 Signal Peak Detector - Executable Builder ===\n")
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Create build files
    create_spec_file()
    create_launcher_script()
    create_requirements_file()
    create_build_batch()
    create_readme()
    
    print("\n=== Build Files Created ===")
    print("1. mercedes_detector.spec - PyInstaller specification")
    print("2. launcher.py - Application launcher")
    print("3. requirements_build.txt - Build dependencies")
    print("4. build.bat - Windows build script")
    print("5. README_EXECUTABLE.txt - User instructions")
    
    print("\n=== Next Steps ===")
    print("To build the executable:")
    print("1. Run: pip install -r requirements_build.txt")
    print("2. Run: pyinstaller --clean mercedes_detector.spec")
    print("3. Find executable in: dist/Mercedes_Benz_MF4_Peak_Detector.exe")
    print("\nOr simply run: build.bat (Windows)")
    
    return True

if __name__ == "__main__":
    try:
        build_executable()
        print("\n✓ Build setup completed successfully!")
    except Exception as e:
        print(f"\n✗ Build setup failed: {str(e)}")
        sys.exit(1)