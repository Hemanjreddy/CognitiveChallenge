@echo off
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
