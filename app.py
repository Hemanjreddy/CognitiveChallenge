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
                    
                    # Display results
                    display_results(data, st.session_state.detected_peaks, selected_signals)
                    
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

def display_results(data, detected_peaks, selected_signals):
    """Display analysis results with interactive charts"""
    
    st.subheader("📊 Signal Analysis Results")
    
    # Summary statistics
    total_peaks = sum(len(peaks['indices']) for peaks in detected_peaks.values())
    st.metric("Total Peaks Detected", total_peaks)
    
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
    
    fig.update_layout(
        height=300 * len(selected_signals),
        title="Signal Analysis with Detected Peaks",
        xaxis_title="Time (s)" if len(selected_signals) == 1 else None
    )
    
    if len(selected_signals) > 1:
        fig.update_xaxes(title_text="Time (s)", row=len(selected_signals), col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Peak statistics table
    st.subheader("📋 Peak Detection Summary")
    
    summary_data = []
    for signal_name in selected_signals:
        peaks_info = detected_peaks[signal_name]
        summary_data.append({
            'Signal': signal_name,
            'Peaks Count': len(peaks_info['indices']),
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
