# Mercedes-Benz MF4 Signal Peak Detector - User Guide

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
