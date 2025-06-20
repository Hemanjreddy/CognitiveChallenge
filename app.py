import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import traceback
from utils.mf4_processor import MF4Processor
from utils.peak_detector import PeakDetector
from utils.data_exporter import DataExporter
from utils.anomaly_detector import AnomalyDetector

# Page configuration
st.set_page_config(
    page_title="MF4 Signal Peak Detector",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'detected_peaks' not in st.session_state:
    st.session_state.detected_peaks = None
if 'selected_signals' not in st.session_state:
    st.session_state.selected_signals = []
if 'anomaly_results' not in st.session_state:
    st.session_state.anomaly_results = None

def main():
    st.title("🚗 Vehicle MF4 Signal Peak Detector")
    st.markdown("Upload and analyze vehicle measurement files (MF4) with automated peak detection")
    
    # Sidebar for parameters and controls
    with st.sidebar:
        st.header("📋 Configuration")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload MF4 File",
            type=['mf4', 'dat'],
            help="Select a valid MF4 measurement file"
        )
        
        # Peak detection parameters
        st.subheader("🔍 Peak Detection Settings")
        
        height_threshold = st.slider(
            "Height Threshold",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="Minimum peak height relative to signal standard deviation"
        )
        
        distance = st.slider(
            "Minimum Distance",
            min_value=1,
            max_value=1000,
            value=100,
            help="Minimum distance between peaks (samples)"
        )
        
        prominence = st.slider(
            "Prominence",
            min_value=0.1,
            max_value=5.0,
            value=0.5,
            step=0.1,
            help="Required prominence of peaks"
        )
        
        width_range = st.slider(
            "Peak Width Range",
            min_value=1,
            max_value=100,
            value=(5, 50),
            help="Minimum and maximum peak width (samples)"
        )
        
        # Anomaly Detection Settings
        st.subheader("🚨 Anomaly Detection")
        
        enable_anomaly_detection = st.checkbox(
            "Enable Anomaly Detection",
            value=True,
            help="Detect unusual peaks in the signal data"
        )
        
        if enable_anomaly_detection:
            anomaly_methods = st.multiselect(
                "Detection Methods",
                options=['statistical', 'zscore', 'iqr', 'temporal', 'isolation_forest'],
                default=['statistical', 'zscore'],
                help="Select anomaly detection methods to apply"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                zscore_threshold = st.slider(
                    "Z-Score Threshold",
                    min_value=1.5,
                    max_value=4.0,
                    value=2.5,
                    step=0.1,
                    help="Threshold for Z-score anomaly detection"
                )
            
            with col2:
                statistical_threshold = st.slider(
                    "Statistical Threshold",
                    min_value=2.0,
                    max_value=5.0,
                    value=3.5,
                    step=0.1,
                    help="Threshold for modified Z-score detection"
                )
    
    # Main content area
    if uploaded_file is not None:
        try:
            # Process MF4 file
            with st.spinner("Processing MF4 file..."):
                processor = MF4Processor()
                st.session_state.processed_data = processor.process_file(uploaded_file)
            
            if st.session_state.processed_data is not None:
                data = st.session_state.processed_data
                
                # Display file information
                st.success(f"✅ Successfully loaded MF4 file with {len(data['signals'])} signals")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Signals", len(data['signals']))
                with col2:
                    st.metric("Duration (s)", f"{data['duration']:.2f}")
                with col3:
                    st.metric("Sample Rate (Hz)", f"{data['sample_rate']:.1f}")
                
                # Signal selection
                st.subheader("📈 Signal Selection")
                
                signal_names = list(data['signals'].keys())
                selected_signals = st.multiselect(
                    "Select signals to analyze:",
                    options=signal_names,
                    default=signal_names[:3] if len(signal_names) >= 3 else signal_names,
                    help="Choose which signals to visualize and analyze"
                )
                
                st.session_state.selected_signals = selected_signals
                
                if selected_signals:
                    # Peak detection
                    peak_detector = PeakDetector()
                    
                    peak_params = {
                        'height_threshold': height_threshold,
                        'distance': distance,
                        'prominence': prominence,
                        'width': width_range
                    }
                    
                    with st.spinner("Detecting peaks..."):
                        st.session_state.detected_peaks = peak_detector.detect_peaks(
                            data, selected_signals, peak_params
                        )
                    
                    # Anomaly detection
                    if enable_anomaly_detection and anomaly_methods:
                        with st.spinner("Detecting anomalies..."):
                            anomaly_detector = AnomalyDetector()
                            
                            anomaly_config = {
                                'methods': anomaly_methods,
                                'zscore_threshold': zscore_threshold,
                                'statistical_threshold': statistical_threshold,
                                'iqr_multiplier': 1.5,
                                'temporal_threshold': 3.0,
                                'isolation_percentile': 95
                            }
                            
                            st.session_state.anomaly_results = anomaly_detector.detect_peak_anomalies(
                                st.session_state.detected_peaks, data, selected_signals, anomaly_config
                            )
                    else:
                        st.session_state.anomaly_results = None
                    
                    # Display results
                    display_results(data, st.session_state.detected_peaks, selected_signals, 
                                  st.session_state.anomaly_results)
                    
                else:
                    st.warning("Please select at least one signal to analyze.")
                    
        except Exception as e:
            st.error(f"❌ Error processing MF4 file: {str(e)}")
            with st.expander("Error Details"):
                st.code(traceback.format_exc())
    
    else:
        # Landing page
        st.info("👆 Please upload an MF4 file to begin analysis")
        
        # Instructions
        with st.expander("📖 How to use this application"):
            st.markdown("""
            1. **Upload File**: Select your MF4 measurement file using the file uploader
            2. **Configure Parameters**: Adjust peak detection settings in the sidebar
            3. **Select Signals**: Choose which signals you want to analyze
            4. **View Results**: Explore interactive charts and detected peaks
            5. **Export Data**: Download results in CSV or JSON format
            
            **Supported File Types**: .mf4, .dat
            """)
        
        # Sample parameters explanation
        with st.expander("🔧 Peak Detection Parameters"):
            st.markdown("""
            - **Height Threshold**: Minimum peak height relative to signal noise level
            - **Minimum Distance**: Minimum separation between detected peaks
            - **Prominence**: How much a peak stands out from surrounding baseline
            - **Peak Width Range**: Expected width range of valid peaks
            """)

def display_results(data, detected_peaks, selected_signals, anomaly_results=None):
    """Display analysis results with interactive charts and anomaly detection"""
    
    st.subheader("📊 Signal Analysis Results")
    
    # Summary statistics with anomaly information
    total_peaks = sum(len(peaks['indices']) for peaks in detected_peaks.values())
    total_anomalies = 0
    if anomaly_results:
        total_anomalies = sum(len(anomalies['anomalies']) for anomalies in anomaly_results.values())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Peaks Detected", total_peaks)
    with col2:
        st.metric("Anomalous Peaks", total_anomalies)
    with col3:
        anomaly_rate = (total_anomalies / total_peaks * 100) if total_peaks > 0 else 0
        st.metric("Anomaly Rate", f"{anomaly_rate:.1f}%")
    
    # Create interactive plots
    fig = make_subplots(
        rows=len(selected_signals),
        cols=1,
        subplot_titles=selected_signals,
        shared_xaxes=True,
        vertical_spacing=0.05
    )
    
    time_axis = data['time']
    
    for i, signal_name in enumerate(selected_signals, 1):
        signal_data = data['signals'][signal_name]
        peaks_info = detected_peaks[signal_name]
        
        # Plot signal
        fig.add_trace(
            go.Scatter(
                x=time_axis,
                y=signal_data,
                mode='lines',
                name=f'{signal_name}',
                line=dict(width=1),
                showlegend=i==1
            ),
            row=i, col=1
        )
        
        # Plot detected peaks
        if len(peaks_info['indices']) > 0:
            peak_times = time_axis[peaks_info['indices']]
            peak_values = signal_data[peaks_info['indices']]
            
            fig.add_trace(
                go.Scatter(
                    x=peak_times,
                    y=peak_values,
                    mode='markers',
                    name=f'{signal_name} Peaks',
                    marker=dict(
                        color='red',
                        size=8,
                        symbol='diamond'
                    ),
                    showlegend=i==1
                ),
                row=i, col=1
            )
            
            # Plot anomalous peaks if available
            if anomaly_results and signal_name in anomaly_results:
                anomaly_info = anomaly_results[signal_name]
                if len(anomaly_info['anomaly_indices']) > 0:
                    anomaly_peak_times = time_axis[anomaly_info['anomaly_indices']]
                    anomaly_peak_values = signal_data[anomaly_info['anomaly_indices']]
                    
                    fig.add_trace(
                        go.Scatter(
                            x=anomaly_peak_times,
                            y=anomaly_peak_values,
                            mode='markers',
                            name=f'{signal_name} Anomalies',
                            marker=dict(
                                color='orange',
                                size=12,
                                symbol='triangle-up',
                                line=dict(width=2, color='black')
                            ),
                            showlegend=i==1
                        ),
                        row=i, col=1
                    )
    
    fig.update_layout(
        height=300 * len(selected_signals),
        title="Signal Analysis with Detected Peaks",
        xaxis_title="Time (s)" if len(selected_signals) == 1 else None
    )
    
    if len(selected_signals) > 1:
        fig.update_xaxes(title_text="Time (s)", row=len(selected_signals), col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Peak statistics table with anomaly information
    st.subheader("📋 Peak Detection Summary")
    
    summary_data = []
    for signal_name in selected_signals:
        peaks_info = detected_peaks[signal_name]
        anomaly_count = 0
        if anomaly_results and signal_name in anomaly_results:
            anomaly_count = len(anomaly_results[signal_name]['anomalies'])
            
        summary_data.append({
            'Signal': signal_name,
            'Peaks Count': len(peaks_info['indices']),
            'Anomalous Peaks': anomaly_count,
            'Avg Height': f"{np.mean(peaks_info['heights']):.3f}" if len(peaks_info['heights']) > 0 else "N/A",
            'Max Height': f"{np.max(peaks_info['heights']):.3f}" if len(peaks_info['heights']) > 0 else "N/A",
            'Avg Width': f"{np.mean(peaks_info['widths']):.1f}" if len(peaks_info['widths']) > 0 else "N/A"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)
    
    # Export section
    st.subheader("💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as CSV", type="primary"):
            exporter = DataExporter()
            csv_data = exporter.export_to_csv(detected_peaks, data, selected_signals)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="peak_detection_results.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Export as JSON"):
            exporter = DataExporter()
            json_data = exporter.export_to_json(detected_peaks, data, selected_signals)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="peak_detection_results.json",
                mime="application/json"
            )
    
    # Anomaly Analysis Section
    if anomaly_results:
        st.subheader("🚨 Anomaly Analysis Results")
        
        # Anomaly overview
        total_signals_with_anomalies = sum(1 for anomalies in anomaly_results.values() if len(anomalies['anomalies']) > 0)
        st.info(f"Found anomalies in {total_signals_with_anomalies} out of {len(selected_signals)} signals")
        
        # Detailed anomaly information per signal
        for signal_name in selected_signals:
            if signal_name in anomaly_results:
                anomaly_info = anomaly_results[signal_name]
                if len(anomaly_info['anomalies']) > 0:
                    with st.expander(f"🔍 Anomalies in {signal_name} ({len(anomaly_info['anomalies'])} found)"):
                        
                        # Anomaly statistics
                        stats = anomaly_info['statistics']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Anomaly Rate", f"{stats['anomaly_rate']*100:.1f}%")
                        with col2:
                            st.metric("Mean Score", f"{stats['mean_anomaly_score']:.2f}")
                        with col3:
                            st.metric("Max Score", f"{stats['max_anomaly_score']:.2f}")
                        
                        # Anomaly details table
                        anomaly_data = []
                        for anomaly in anomaly_info['anomalies']:
                            anomaly_data.append({
                                'Time (s)': f"{anomaly['time']:.3f}",
                                'Height': f"{anomaly['height']:.3f}",
                                'Type': anomaly['anomaly_type'],
                                'Description': anomaly['description']
                            })
                        
                        anomaly_df = pd.DataFrame(anomaly_data)
                        st.dataframe(anomaly_df, use_container_width=True)
    
    # Detailed peak information
    with st.expander("🔍 Detailed Peak Information"):
        for signal_name in selected_signals:
            peaks_info = detected_peaks[signal_name]
            if len(peaks_info['indices']) > 0:
                st.write(f"**{signal_name}**")
                
                peak_details = pd.DataFrame({
                    'Peak Index': peaks_info['indices'],
                    'Time (s)': data['time'][peaks_info['indices']],
                    'Height': peaks_info['heights'],
                    'Width': peaks_info['widths'],
                    'Prominence': peaks_info['prominences']
                })
                
                st.dataframe(peak_details, use_container_width=True)
            else:
                st.write(f"**{signal_name}**: No peaks detected")

if __name__ == "__main__":
    main()
