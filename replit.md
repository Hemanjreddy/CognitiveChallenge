# MF4 Signal Peak Detector

## Overview

This is a Streamlit-based web application designed for Mercedes-Benz automotive engineers and data analysts to process and analyze vehicle measurement files (MF4 format). The application provides automated peak detection capabilities with advanced anomaly detection for signal analysis, allowing users to upload MF4 files, visualize signal data, and export comprehensive analysis results.

The application is built using Python with Streamlit as the web framework, leveraging scientific computing libraries for signal processing and peak detection algorithms.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with interactive widgets
- **Visualization**: Plotly for interactive charts and signal plotting
- **Layout**: Wide layout with sidebar configuration panel
- **State Management**: Streamlit session state for maintaining data across interactions

### Backend Architecture
- **Core Processing**: Modular utility classes for specialized functionality
- **File Processing**: ASAMDF library for MF4 file parsing and data extraction
- **Signal Analysis**: SciPy-based peak detection algorithms
- **Data Export**: Multiple format support (CSV, Excel) for analysis results

### Application Structure
```
app.py                    # Main Streamlit application
utils/
├── mf4_processor.py     # MF4 file processing and data extraction
├── peak_detector.py     # Signal peak detection algorithms
└── data_exporter.py     # Result export functionality
```

## Key Components

### 1. MF4 File Processor (`MF4Processor`)
- **Purpose**: Parse and extract signal data from MF4 measurement files
- **Technology**: ASAMDF library for automotive data format handling
- **Features**: 
  - Temporary file handling for secure processing
  - Signal metadata extraction
  - Time axis generation
  - Error handling for corrupted files

### 2. Peak Detection Engine (`PeakDetector`)
- **Purpose**: Identify peaks in signal data using configurable parameters
- **Technology**: SciPy signal processing algorithms
- **Features**:
  - Customizable height, distance, and prominence thresholds
  - Width calculation for detected peaks
  - Progress tracking for batch processing
  - Per-signal error handling

### 3. Data Export System (`DataExporter`)
- **Purpose**: Export analysis results in various formats
- **Supported Formats**: CSV, Excel (planned)
- **Features**:
  - Structured peak information export
  - Signal metadata inclusion
  - Configurable output formatting

### 4. Main Application (`app.py`)
- **Purpose**: User interface and workflow orchestration
- **Features**:
  - File upload interface
  - Parameter configuration sidebar
  - Interactive signal visualization
  - Real-time analysis feedback

## Data Flow

1. **File Upload**: User uploads MF4 file through Streamlit interface
2. **File Processing**: MF4Processor extracts signals and metadata using ASAMDF
3. **Signal Selection**: User selects specific signals for analysis
4. **Parameter Configuration**: User sets peak detection parameters (height, distance, prominence)
5. **Peak Detection**: PeakDetector analyzes selected signals using SciPy algorithms
6. **Visualization**: Results displayed using Plotly interactive charts
7. **Export**: Analysis results exported to CSV/Excel format

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **asamdf**: MF4 file format processing
- **scipy**: Scientific computing and signal processing
- **plotly**: Interactive data visualization
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **openpyxl**: Excel file generation

### Development Environment
- **Python**: 3.11+ runtime
- **uv**: Fast Python package installer
- **Nix**: Package management and environment isolation

## Deployment Strategy

### Platform
- **Target**: Replit Autoscale deployment
- **Runtime**: Python 3.11 with Nix package management
- **Port**: 5000 (configured for Streamlit server)

### Configuration
- **Entry Point**: `streamlit run app.py --server.port 5000`
- **Dependencies**: Automatically installed via uv package manager
- **Environment**: Headless server configuration for production deployment

### Scaling Considerations
- Stateless application design for horizontal scaling
- Session state management for user data persistence
- Temporary file cleanup for memory management

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### June 20, 2025 - Standalone Distribution Complete
- Created comprehensive portable application packages
- Built self-contained Windows launcher with Python detection
- Generated complete installation guide and troubleshooting documentation
- Provided multiple distribution formats (ZIP, portable, EXE-ready)
- Added professional branding and user-friendly error handling

### Distribution Packages Created:
- `Mercedes_Benz_MF4_Detector_Portable.zip` - Portable version requiring Python
- `Mercedes_Benz_MF4_Detector_Complete.zip` - Self-contained with advanced launcher
- `simple_launcher.py` - EXE-conversion ready script
- `Installation_Guide.md` - Comprehensive setup instructions
- `EXE_Creation_Instructions.md` - Professional executable creation guide

## Changelog

- June 17, 2025: Initial setup with MF4 processing and peak detection
- June 20, 2025: Completed standalone distribution with multiple deployment options