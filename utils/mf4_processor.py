import numpy as np
import pandas as pd
from asammdf import MDF
import streamlit as st
from typing import Dict, Any, Optional
import tempfile
import os

class MF4Processor:
    """Handles MF4 file processing using ASAMDF library"""
    
    def __init__(self):
        self.mdf = None
        
    def process_file(self, uploaded_file) -> Optional[Dict[str, Any]]:
        """
        Process an uploaded MF4 file and extract signal data
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary containing processed signal data or None if error
        """
        try:
            # Create temporary file for ASAMDF processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mf4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            
            try:
                # Load MF4 file with ASAMDF
                self.mdf = MDF(tmp_file_path)
                
                # Extract basic file information
                file_info = self._extract_file_info()
                
                # Extract signal data
                signals_data = self._extract_signals()
                
                # Create time axis
                time_axis = self._create_time_axis()
                
                # Combine all data
                processed_data = {
                    'file_info': file_info,
                    'signals': signals_data,
                    'time': time_axis,
                    'duration': file_info.get('duration', 0),
                    'sample_rate': file_info.get('sample_rate', 1)
                }
                
                return processed_data
                
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            st.error(f"Error processing MF4 file: {str(e)}")
            return None
    
    def _extract_file_info(self) -> Dict[str, Any]:
        """Extract basic information from MF4 file"""
        try:
            info = {
                'version': getattr(self.mdf.header, 'version', 'Unknown'),
                'author': getattr(self.mdf.header, 'author', 'Unknown'),
                'subject': getattr(self.mdf.header, 'subject', 'Unknown'),
                'comment': getattr(self.mdf.header, 'comment', ''),
                'start_time': getattr(self.mdf.header, 'start_time', None),
            }
            
            # Calculate duration and sample rate
            if len(self.mdf.groups) > 0:
                # Get time information from first group
                first_group = self.mdf.groups[0]
                if hasattr(first_group, 'channel_group') and first_group.channel_group:
                    # Try to get sample rate
                    if hasattr(first_group.channel_group, 'acq_source'):
                        info['sample_rate'] = getattr(first_group.channel_group.acq_source, 'sample_rate', 1.0)
                    else:
                        info['sample_rate'] = 1.0
                else:
                    info['sample_rate'] = 1.0
                
                # Calculate duration from actual data
                try:
                    # Get a sample channel to determine duration
                    channels = list(self.mdf.channels_db.keys())
                    if channels:
                        sample_signal = self.mdf.get(channels[0])
                        if hasattr(sample_signal, 'timestamps') and len(sample_signal.timestamps) > 0:
                            info['duration'] = float(sample_signal.timestamps[-1] - sample_signal.timestamps[0])
                        else:
                            info['duration'] = 0.0
                    else:
                        info['duration'] = 0.0
                except:
                    info['duration'] = 0.0
            else:
                info['sample_rate'] = 1.0
                info['duration'] = 0.0
            
            return info
            
        except Exception as e:
            st.warning(f"Could not extract complete file info: {str(e)}")
            return {
                'version': 'Unknown',
                'author': 'Unknown',
                'subject': 'Unknown',
                'comment': '',
                'start_time': None,
                'duration': 0.0,
                'sample_rate': 1.0
            }
    
    def _extract_signals(self) -> Dict[str, np.ndarray]:
        """Extract all signal data from MF4 file"""
        signals = {}
        
        try:
            # Get all available channels
            channel_names = list(self.mdf.channels_db.keys())
            
            # Progress bar for signal extraction
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, channel_name in enumerate(channel_names):
                try:
                    status_text.text(f'Extracting signal: {channel_name}')
                    
                    # Get signal data
                    signal = self.mdf.get(channel_name)
                    
                    if signal is not None and hasattr(signal, 'samples'):
                        # Convert to numpy array and handle different data types
                        signal_data = np.array(signal.samples, dtype=np.float64)
                        
                        # Skip if signal is empty or invalid
                        if len(signal_data) == 0:
                            continue
                            
                        # Handle NaN values
                        if np.isnan(signal_data).all():
                            continue
                            
                        # Replace NaN values with interpolation or zero
                        if np.isnan(signal_data).any():
                            # Simple linear interpolation for NaN values
                            mask = ~np.isnan(signal_data)
                            if mask.sum() > 1:  # At least 2 valid points for interpolation
                                indices = np.arange(len(signal_data))
                                signal_data = np.interp(indices, indices[mask], signal_data[mask])
                            else:
                                signal_data = np.nan_to_num(signal_data)
                        
                        signals[channel_name] = signal_data
                        
                except Exception as e:
                    st.warning(f"Could not extract signal '{channel_name}': {str(e)}")
                    continue
                
                # Update progress
                progress_bar.progress((i + 1) / len(channel_names))
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            if not signals:
                raise ValueError("No valid signals found in MF4 file")
                
            return signals
            
        except Exception as e:
            st.error(f"Error extracting signals: {str(e)}")
            return {}
    
    def _create_time_axis(self) -> np.ndarray:
        """Create time axis for signals"""
        try:
            # Try to get time information from a signal
            channel_names = list(self.mdf.channels_db.keys())
            
            if not channel_names:
                return np.array([])
            
            # Get first available signal to determine time axis
            first_signal = self.mdf.get(channel_names[0])
            
            if first_signal is not None and hasattr(first_signal, 'timestamps'):
                # Use actual timestamps if available
                timestamps = np.array(first_signal.timestamps, dtype=np.float64)
                # Convert to relative time (start from 0)
                if len(timestamps) > 0:
                    timestamps = timestamps - timestamps[0]
                return timestamps
            else:
                # Create synthetic time axis
                if first_signal is not None and hasattr(first_signal, 'samples'):
                    sample_count = len(first_signal.samples)
                    # Use extracted sample rate
                    file_info = getattr(self, '_cached_file_info', {'sample_rate': 1.0})
                    sample_rate = file_info.get('sample_rate', 1.0)
                    
                    return np.linspace(0, sample_count / sample_rate, sample_count)
                else:
                    return np.array([])
                    
        except Exception as e:
            st.warning(f"Could not create time axis: {str(e)}")
            return np.array([])
    
    def get_signal_info(self, signal_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific signal"""
        try:
            if self.mdf is None:
                return {}
                
            signal = self.mdf.get(signal_name)
            if signal is None:
                return {}
                
            info = {
                'name': signal_name,
                'unit': getattr(signal, 'unit', ''),
                'comment': getattr(signal, 'comment', ''),
                'samples_count': len(signal.samples) if hasattr(signal, 'samples') else 0,
                'min_value': float(np.min(signal.samples)) if hasattr(signal, 'samples') and len(signal.samples) > 0 else 0,
                'max_value': float(np.max(signal.samples)) if hasattr(signal, 'samples') and len(signal.samples) > 0 else 0,
                'mean_value': float(np.mean(signal.samples)) if hasattr(signal, 'samples') and len(signal.samples) > 0 else 0,
            }
            
            return info
            
        except Exception as e:
            st.warning(f"Could not get signal info for '{signal_name}': {str(e)}")
            return {}
    
    def cleanup(self):
        """Clean up resources"""
        if self.mdf is not None:
            try:
                self.mdf.close()
            except:
                pass
            self.mdf = None
