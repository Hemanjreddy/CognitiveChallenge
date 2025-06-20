import numpy as np
import pandas as pd
from scipy.signal import find_peaks, peak_widths, peak_prominences
from typing import Dict, List, Any, Tuple
import streamlit as st

class PeakDetector:
    """Handles peak detection in signal data using scipy algorithms"""
    
    def __init__(self):
        pass
    
    def detect_peaks(self, data: Dict[str, Any], selected_signals: List[str], 
                    peak_params: Dict[str, Any]) -> Dict[str, Dict[str, np.ndarray]]:
        """
        Detect peaks in selected signals
        
        Args:
            data: Processed signal data dictionary
            selected_signals: List of signal names to analyze
            peak_params: Peak detection parameters
            
        Returns:
            Dictionary with peak detection results for each signal
        """
        results = {}
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, signal_name in enumerate(selected_signals):
            try:
                status_text.text(f'Detecting peaks in: {signal_name}')
                
                signal_data = data['signals'][signal_name]
                time_data = data['time']
                
                # Detect peaks for this signal
                peak_info = self._detect_signal_peaks(signal_data, time_data, peak_params)
                results[signal_name] = peak_info
                
            except Exception as e:
                st.warning(f"Peak detection failed for signal '{signal_name}': {str(e)}")
                # Return empty results for failed signal
                results[signal_name] = {
                    'indices': np.array([]),
                    'heights': np.array([]),
                    'widths': np.array([]),
                    'prominences': np.array([]),
                    'times': np.array([])
                }
            
            # Update progress
            progress_bar.progress((i + 1) / len(selected_signals))
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return results
    
    def _detect_signal_peaks(self, signal_data: np.ndarray, time_data: np.ndarray, 
                           peak_params: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """
        Detect peaks in a single signal
        
        Args:
            signal_data: Signal values
            time_data: Time values
            peak_params: Peak detection parameters
            
        Returns:
            Dictionary with peak information
        """
        try:
            # Validate input data
            if len(signal_data) == 0 or len(time_data) == 0:
                raise ValueError("Empty signal or time data")
            
            if len(signal_data) != len(time_data):
                # Truncate to shorter length
                min_len = min(len(signal_data), len(time_data))
                signal_data = signal_data[:min_len]
                time_data = time_data[:min_len]
            
            # Remove NaN values
            valid_mask = ~(np.isnan(signal_data) | np.isnan(time_data))
            if not valid_mask.any():
                raise ValueError("All data points are NaN")
            
            signal_clean = signal_data[valid_mask]
            time_clean = time_data[valid_mask]
            
            # Calculate adaptive height threshold
            signal_std = np.std(signal_clean)
            signal_mean = np.mean(signal_clean)
            height_threshold = signal_mean + peak_params['height_threshold'] * signal_std
            
            # Prepare peak detection parameters
            scipy_params = {
                'height': height_threshold,
                'distance': peak_params['distance'],
                'prominence': peak_params['prominence'] * signal_std,
                'width': peak_params['width']
            }
            
            # Find peaks
            peak_indices, peak_properties = find_peaks(signal_clean, **scipy_params)
            
            if len(peak_indices) == 0:
                # No peaks found
                return {
                    'indices': np.array([]),
                    'heights': np.array([]),
                    'widths': np.array([]),
                    'prominences': np.array([]),
                    'times': np.array([])
                }
            
            # Extract peak properties
            peak_heights = signal_clean[peak_indices]
            
            # Calculate peak widths
            try:
                widths, width_heights, left_ips, right_ips = peak_widths(
                    signal_clean, peak_indices, rel_height=0.5
                )
            except Exception:
                # Fallback if width calculation fails
                widths = np.full(len(peak_indices), np.nan)
            
            # Calculate peak prominences
            try:
                prominences, left_bases, right_bases = peak_prominences(
                    signal_clean, peak_indices
                )
            except Exception:
                # Fallback if prominence calculation fails
                prominences = np.full(len(peak_indices), np.nan)
            
            # Get corresponding times
            peak_times = time_clean[peak_indices]
            
            # Map indices back to original signal indices
            valid_indices = np.where(valid_mask)[0]
            original_indices = valid_indices[peak_indices]
            
            return {
                'indices': original_indices,
                'heights': peak_heights,
                'widths': widths,
                'prominences': prominences,
                'times': peak_times
            }
            
        except Exception as e:
            st.warning(f"Peak detection algorithm failed: {str(e)}")
            return {
                'indices': np.array([]),
                'heights': np.array([]),
                'widths': np.array([]),
                'prominences': np.array([]),
                'times': np.array([])
            }
    
    def filter_peaks_by_criteria(self, peaks_data: Dict[str, np.ndarray], 
                               criteria: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """
        Filter detected peaks based on additional criteria
        
        Args:
            peaks_data: Peak detection results
            criteria: Additional filtering criteria
            
        Returns:
            Filtered peak data
        """
        try:
            if len(peaks_data['indices']) == 0:
                return peaks_data
            
            # Initialize mask (all peaks pass initially)
            mask = np.ones(len(peaks_data['indices']), dtype=bool)
            
            # Apply height filter if specified
            if 'min_height' in criteria and len(peaks_data['heights']) > 0:
                mask &= peaks_data['heights'] >= criteria['min_height']
            
            if 'max_height' in criteria and len(peaks_data['heights']) > 0:
                mask &= peaks_data['heights'] <= criteria['max_height']
            
            # Apply width filter if specified
            if 'min_width' in criteria and len(peaks_data['widths']) > 0:
                mask &= peaks_data['widths'] >= criteria['min_width']
            
            if 'max_width' in criteria and len(peaks_data['widths']) > 0:
                mask &= peaks_data['widths'] <= criteria['max_width']
            
            # Apply prominence filter if specified
            if 'min_prominence' in criteria and len(peaks_data['prominences']) > 0:
                mask &= peaks_data['prominences'] >= criteria['min_prominence']
            
            # Apply time range filter if specified
            if 'time_range' in criteria and len(peaks_data['times']) > 0:
                time_min, time_max = criteria['time_range']
                mask &= (peaks_data['times'] >= time_min) & (peaks_data['times'] <= time_max)
            
            # Apply the mask to all arrays
            filtered_data = {}
            for key, values in peaks_data.items():
                if len(values) > 0:
                    filtered_data[key] = values[mask]
                else:
                    filtered_data[key] = values
            
            return filtered_data
            
        except Exception as e:
            st.warning(f"Peak filtering failed: {str(e)}")
            return peaks_data
    
    def calculate_peak_statistics(self, peaks_data: Dict[str, np.ndarray]) -> Dict[str, float]:
        """
        Calculate statistical information about detected peaks
        
        Args:
            peaks_data: Peak detection results
            
        Returns:
            Dictionary with peak statistics
        """
        try:
            stats = {}
            
            if len(peaks_data['indices']) == 0:
                return {
                    'count': 0,
                    'mean_height': 0.0,
                    'std_height': 0.0,
                    'mean_width': 0.0,
                    'std_width': 0.0,
                    'mean_prominence': 0.0,
                    'std_prominence': 0.0,
                    'peak_rate': 0.0
                }
            
            stats['count'] = len(peaks_data['indices'])
            
            # Height statistics
            if len(peaks_data['heights']) > 0:
                stats['mean_height'] = float(np.mean(peaks_data['heights']))
                stats['std_height'] = float(np.std(peaks_data['heights']))
                stats['min_height'] = float(np.min(peaks_data['heights']))
                stats['max_height'] = float(np.max(peaks_data['heights']))
            else:
                stats.update({'mean_height': 0.0, 'std_height': 0.0, 'min_height': 0.0, 'max_height': 0.0})
            
            # Width statistics
            if len(peaks_data['widths']) > 0 and not np.isnan(peaks_data['widths']).all():
                valid_widths = peaks_data['widths'][~np.isnan(peaks_data['widths'])]
                if len(valid_widths) > 0:
                    stats['mean_width'] = float(np.mean(valid_widths))
                    stats['std_width'] = float(np.std(valid_widths))
                    stats['min_width'] = float(np.min(valid_widths))
                    stats['max_width'] = float(np.max(valid_widths))
                else:
                    stats.update({'mean_width': 0.0, 'std_width': 0.0, 'min_width': 0.0, 'max_width': 0.0})
            else:
                stats.update({'mean_width': 0.0, 'std_width': 0.0, 'min_width': 0.0, 'max_width': 0.0})
            
            # Prominence statistics
            if len(peaks_data['prominences']) > 0 and not np.isnan(peaks_data['prominences']).all():
                valid_prominences = peaks_data['prominences'][~np.isnan(peaks_data['prominences'])]
                if len(valid_prominences) > 0:
                    stats['mean_prominence'] = float(np.mean(valid_prominences))
                    stats['std_prominence'] = float(np.std(valid_prominences))
                    stats['min_prominence'] = float(np.min(valid_prominences))
                    stats['max_prominence'] = float(np.max(valid_prominences))
                else:
                    stats.update({'mean_prominence': 0.0, 'std_prominence': 0.0, 'min_prominence': 0.0, 'max_prominence': 0.0})
            else:
                stats.update({'mean_prominence': 0.0, 'std_prominence': 0.0, 'min_prominence': 0.0, 'max_prominence': 0.0})
            
            # Peak rate (peaks per unit time)
            if len(peaks_data['times']) > 0:
                time_span = np.max(peaks_data['times']) - np.min(peaks_data['times'])
                if time_span > 0:
                    stats['peak_rate'] = len(peaks_data['indices']) / time_span
                else:
                    stats['peak_rate'] = 0.0
            else:
                stats['peak_rate'] = 0.0
            
            return stats
            
        except Exception as e:
            st.warning(f"Peak statistics calculation failed: {str(e)}")
            return {'count': 0, 'mean_height': 0.0, 'std_height': 0.0, 'mean_width': 0.0, 
                   'std_width': 0.0, 'mean_prominence': 0.0, 'std_prominence': 0.0, 'peak_rate': 0.0}
