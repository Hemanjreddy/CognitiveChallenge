#!/usr/bin/env python3
"""
Standalone launcher for Mercedes-Benz MF4 Signal Peak Detector
This script launches the Streamlit application as a standalone executable
"""

import streamlit.web.cli as stcli
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

def open_browser():
    """Open browser after a delay to allow server to start"""
    time.sleep(3)
    webbrowser.open('http://localhost:8501')

def main():
    """Main entry point for standalone application"""
    # Print startup message
    print("=" * 60)
    print("Mercedes-Benz MF4 Signal Peak Detector")
    print("Professional Vehicle Measurement Analysis")
    print("=" * 60)
    print("")
    print("Starting application server...")
    print("This may take 30-60 seconds on first launch...")
    print("")
    
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = Path(sys.executable).parent
        print(f"Running from: {app_dir}")
    else:
        # Running as script
        app_dir = Path(__file__).parent
        print(f"Running from: {app_dir}")
    
    # Set the working directory
    os.chdir(app_dir)
    
    # Add the app directory to Python path
    sys.path.insert(0, str(app_dir))
    
    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Configure Streamlit arguments
    sys.argv = [
        "streamlit",
        "run",
        str(app_dir / "app.py"),
        "--server.port=8501",
        "--server.address=127.0.0.1",
        "--browser.serverAddress=127.0.0.1",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--server.enableXsrfProtection=false"
    ]
    
    print("Server starting...")
    print("Application will open in your default browser")
    print("URL: http://localhost:8501")
    print("")
    print("To stop the application, close this window or press Ctrl+C")
    print("=" * 60)
    
    try:
        # Launch Streamlit
        stcli.main()
    except KeyboardInterrupt:
        print("\nShutting down Mercedes-Benz MF4 Peak Detector...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting application: {e}")
        print("Please check that no other application is using port 8501")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()