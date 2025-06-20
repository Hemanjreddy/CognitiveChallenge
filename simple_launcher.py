#!/usr/bin/env python3
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
