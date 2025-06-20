# Mercedes-Benz MF4 Signal Peak Detector - Installation Guide

## Quick Start (Recommended)

### For Windows Users:
1. Extract all files to a folder (e.g., C:\Mercedes_MF4_Detector)
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
