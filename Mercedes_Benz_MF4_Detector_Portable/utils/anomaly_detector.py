import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Any, Tuple
import streamlit as st

class AnomalyDetector:
    """Detects anomalies in peak detection results using statistical methods"""
    
    def __init__(self):
        self.anomaly_methods = {
            'statistical': self._detect_statistical_anomalies,
            'isolation_forest': self._detect_isolation_forest_anomalies,
            'zscore': self._detect_zscore_anomalies,
            'iqr': self._detect_iqr_anomalies,
            'temporal': self._detect_temporal_anomalies
        }
    
    def detect_peak_anomalies(self, detected_peaks: Dict[str, Dict[str, np.ndarray]], 
                            data: Dict[str, Any], selected_signals: List[str],
                            anomaly_config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Detect anomalies in peak detection results
        
        Args:
            detected_peaks: Peak detection results
            data: Original signal data
            selected_signals: List of analyzed signals
            anomaly_config: Configuration for anomaly detection
            
        Returns:
            Dictionary with anomaly detection results for each signal
        """
        anomaly_results = {}
        
        for signal_name in selected_signals:
            peaks_info = detected_peaks[signal_name]
            signal_data = data['signals'][signal_name]
            time_data = data['time']
            
            if len(peaks_info['indices']) == 0:
                anomaly_results[signal_name] = {
                    'anomalies': [],
                    'anomaly_indices': np.array([]),
                    'anomaly_scores': np.array([]),
                    'anomaly_types': [],
                    'statistics': {}
                }
                continue
            
            # Detect anomalies using selected methods
            signal_anomalies = self._analyze_signal_anomalies(
                peaks_info, signal_data, time_data, anomaly_config
            )
            
            anomaly_results[signal_name] = signal_anomalies
        
        return anomaly_results
    
    def _analyze_signal_anomalies(self, peaks_info: Dict[str, np.ndarray], 
                                signal_data: np.ndarray, time_data: np.ndarray,
                                config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze anomalies for a single signal"""
        
        all_anomalies = []
        all_anomaly_indices = []
        all_anomaly_scores = []
        all_anomaly_types = []
        
        # Apply selected anomaly detection methods
        for method_name in config.get('methods', ['statistical', 'zscore']):
            if method_name in self.anomaly_methods:
                try:
                    method_results = self.anomaly_methods[method_name](
                        peaks_info, signal_data, time_data, config
                    )
                    
                    if method_results['anomalies']:
                        all_anomalies.extend(method_results['anomalies'])
                        all_anomaly_indices.extend(method_results['indices'])
                        all_anomaly_scores.extend(method_results['scores'])
                        all_anomaly_types.extend([method_name] * len(method_results['anomalies']))
                
                except Exception as e:
                    st.warning(f"Anomaly detection method '{method_name}' failed: {str(e)}")
        
        # Remove duplicates and sort by anomaly score
        unique_anomalies = self._remove_duplicate_anomalies(
            all_anomalies, all_anomaly_indices, all_anomaly_scores, all_anomaly_types
        )
        
        # Calculate statistics
        statistics = self._calculate_anomaly_statistics(peaks_info, unique_anomalies)
        
        return {
            'anomalies': unique_anomalies['anomalies'],
            'anomaly_indices': np.array(unique_anomalies['indices']),
            'anomaly_scores': np.array(unique_anomalies['scores']),
            'anomaly_types': unique_anomalies['types'],
            'statistics': statistics
        }
    
    def _detect_statistical_anomalies(self, peaks_info: Dict[str, np.ndarray], 
                                    signal_data: np.ndarray, time_data: np.ndarray,
                                    config: Dict[str, Any]) -> Dict[str, Any]:
        """Detect anomalies using statistical methods (modified z-score)"""
        
        anomalies = []
        indices = []
        scores = []
        
        if len(peaks_info['heights']) == 0:
            return {'anomalies': [], 'indices': [], 'scores': []}
        
        # Modified Z-score for peak heights
        heights = peaks_info['heights']
        median_height = np.median(heights)
        mad_height = np.median(np.abs(heights - median_height))
        
        if mad_height > 0:
            modified_z_scores = 0.6745 * (heights - median_height) / mad_height
            threshold = config.get('statistical_threshold', 3.5)
            
            anomalous_mask = np.abs(modified_z_scores) > threshold
            
            for i, is_anomaly in enumerate(anomalous_mask):
                if is_anomaly:
                    peak_idx = peaks_info['indices'][i]
                    anomalies.append({
                        'peak_index': int(peak_idx),
                        'time': float(time_data[peak_idx]) if peak_idx < len(time_data) else 0,
                        'height': float(heights[i]),
                        'anomaly_type': 'statistical_height',
                        'description': f"Peak height {heights[i]:.3f} is statistically anomalous"
                    })
                    indices.append(peak_idx)
                    scores.append(float(np.abs(modified_z_scores[i])))
        
        return {'anomalies': anomalies, 'indices': indices, 'scores': scores}
    
    def _detect_zscore_anomalies(self, peaks_info: Dict[str, np.ndarray], 
                               signal_data: np.ndarray, time_data: np.ndarray,
                               config: Dict[str, Any]) -> Dict[str, Any]:
        """Detect anomalies using standard Z-score method"""
        
        anomalies = []
        indices = []
        scores = []
        
        if len(peaks_info['heights']) == 0:
            return {'anomalies': [], 'indices': [], 'scores': []}
        
        # Z-score for peak heights
        heights = peaks_info['heights']
        z_scores = np.abs(stats.zscore(heights))
        threshold = config.get('zscore_threshold', 2.5)
        
        anomalous_mask = z_scores > threshold
        
        for i, is_anomaly in enumerate(anomalous_mask):
            if is_anomaly:
                peak_idx = peaks_info['indices'][i]
                anomalies.append({
                    'peak_index': int(peak_idx),
                    'time': float(time_data[peak_idx]) if peak_idx < len(time_data) else 0,
                    'height': float(heights[i]),
                    'anomaly_type': 'zscore_height',
                    'description': f"Peak height {heights[i]:.3f} has Z-score {z_scores[i]:.2f}"
                })
                indices.append(peak_idx)
                scores.append(float(z_scores[i]))
        
        return {'anomalies': anomalies, 'indices': indices, 'scores': scores}
    
    def _detect_iqr_anomalies(self, peaks_info: Dict[str, np.ndarray], 
                            signal_data: np.ndarray, time_data: np.ndarray,
                            config: Dict[str, Any]) -> Dict[str, Any]:
        """Detect anomalies using Interquartile Range (IQR) method"""
        
        anomalies = []
        indices = []
        scores = []
        
        if len(peaks_info['heights']) == 0:
            return {'anomalies': [], 'indices': [], 'scores': []}
        
        # IQR for peak heights
        heights = peaks_info['heights']
        Q1 = np.percentile(heights, 25)
        Q3 = np.percentile(heights, 75)
        IQR = Q3 - Q1
        
        if IQR > 0:
            multiplier = config.get('iqr_multiplier', 1.5)
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            
            anomalous_mask = (heights < lower_bound) | (heights > upper_bound)
            
            for i, is_anomaly in enumerate(anomalous_mask):
                if is_anomaly:
                    peak_idx = peaks_info['indices'][i]
                    score = max(abs(heights[i] - lower_bound), abs(heights[i] - upper_bound)) / IQR
                    
                    anomalies.append({
                        'peak_index': int(peak_idx),
                        'time': float(time_data[peak_idx]) if peak_idx < len(time_data) else 0,
                        'height': float(heights[i]),
                        'anomaly_type': 'iqr_height',
                        'description': f"Peak height {heights[i]:.3f} outside IQR bounds [{lower_bound:.3f}, {upper_bound:.3f}]"
                    })
                    indices.append(peak_idx)
                    scores.append(float(score))
        
        return {'anomalies': anomalies, 'indices': indices, 'scores': scores}
    
    def _detect_temporal_anomalies(self, peaks_info: Dict[str, np.ndarray], 
                                 signal_data: np.ndarray, time_data: np.ndarray,
                                 config: Dict[str, Any]) -> Dict[str, Any]:
        """Detect temporal anomalies in peak occurrence patterns"""
        
        anomalies = []
        indices = []
        scores = []
        
        if len(peaks_info['indices']) < 3:
            return {'anomalies': [], 'indices': [], 'scores': []}
        
        # Calculate time intervals between peaks
        peak_times = time_data[peaks_info['indices']]
        intervals = np.diff(peak_times)
        
        if len(intervals) < 2:
            return {'anomalies': [], 'indices': [], 'scores': []}
        
        # Detect anomalous intervals
        median_interval = np.median(intervals)
        mad_interval = np.median(np.abs(intervals - median_interval))
        
        if mad_interval > 0:
            threshold = config.get('temporal_threshold', 3.0)
            
            for i, interval in enumerate(intervals):
                z_score = abs(interval - median_interval) / mad_interval
                
                if z_score > threshold:
                    peak_idx = peaks_info['indices'][i + 1]
                    anomalies.append({
                        'peak_index': int(peak_idx),
                        'time': float(peak_times[i + 1]),
                        'height': float(peaks_info['heights'][i + 1]),
                        'anomaly_type': 'temporal_interval',
                        'description': f"Unusual time interval {interval:.3f}s between peaks"
                    })
                    indices.append(peak_idx)
                    scores.append(float(z_score))
        
        return {'anomalies': anomalies, 'indices': indices, 'scores': scores}
    
    def _detect_isolation_forest_anomalies(self, peaks_info: Dict[str, np.ndarray], 
                                         signal_data: np.ndarray, time_data: np.ndarray,
                                         config: Dict[str, Any]) -> Dict[str, Any]:
        """Detect anomalies using Isolation Forest (simplified implementation)"""
        
        anomalies = []
        indices = []
        scores = []
        
        if len(peaks_info['heights']) < 10:  # Need minimum samples
            return {'anomalies': [], 'indices': [], 'scores': []}
        
        try:
            # Create feature matrix
            features = []
            for i in range(len(peaks_info['indices'])):
                feature_vector = [
                    peaks_info['heights'][i],
                    peaks_info['widths'][i] if i < len(peaks_info['widths']) and not np.isnan(peaks_info['widths'][i]) else 0,
                    peaks_info['prominences'][i] if i < len(peaks_info['prominences']) and not np.isnan(peaks_info['prominences'][i]) else 0
                ]
                features.append(feature_vector)
            
            features = np.array(features)
            
            # Simple outlier detection based on feature distances
            mean_features = np.mean(features, axis=0)
            std_features = np.std(features, axis=0)
            
            # Normalize features
            normalized_features = (features - mean_features) / (std_features + 1e-8)
            
            # Calculate distances from mean
            distances = np.linalg.norm(normalized_features, axis=1)
            threshold = np.percentile(distances, config.get('isolation_percentile', 95))
            
            anomalous_mask = distances > threshold
            
            for i, is_anomaly in enumerate(anomalous_mask):
                if is_anomaly:
                    peak_idx = peaks_info['indices'][i]
                    anomalies.append({
                        'peak_index': int(peak_idx),
                        'time': float(time_data[peak_idx]) if peak_idx < len(time_data) else 0,
                        'height': float(peaks_info['heights'][i]),
                        'anomaly_type': 'isolation_forest',
                        'description': f"Peak with unusual feature combination"
                    })
                    indices.append(peak_idx)
                    scores.append(float(distances[i]))
        
        except Exception as e:
            st.warning(f"Isolation forest anomaly detection failed: {str(e)}")
        
        return {'anomalies': anomalies, 'indices': indices, 'scores': scores}
    
    def _remove_duplicate_anomalies(self, anomalies: List[Dict], indices: List[int], 
                                  scores: List[float], types: List[str]) -> Dict[str, Any]:
        """Remove duplicate anomalies and keep the highest scoring ones"""
        
        if not anomalies:
            return {'anomalies': [], 'indices': [], 'scores': [], 'types': []}
        
        # Group by peak index
        grouped = {}
        for i, anomaly in enumerate(anomalies):
            peak_idx = anomaly['peak_index']
            if peak_idx not in grouped:
                grouped[peak_idx] = []
            grouped[peak_idx].append({
                'anomaly': anomaly,
                'index': indices[i],
                'score': scores[i],
                'type': types[i]
            })
        
        # Keep highest scoring anomaly for each peak
        unique_anomalies = []
        unique_indices = []
        unique_scores = []
        unique_types = []
        
        for peak_idx, group in grouped.items():
            best = max(group, key=lambda x: x['score'])
            unique_anomalies.append(best['anomaly'])
            unique_indices.append(best['index'])
            unique_scores.append(best['score'])
            unique_types.append(best['type'])
        
        # Sort by score (highest first)
        sorted_indices = np.argsort(unique_scores)[::-1]
        
        return {
            'anomalies': [unique_anomalies[i] for i in sorted_indices],
            'indices': [unique_indices[i] for i in sorted_indices],
            'scores': [unique_scores[i] for i in sorted_indices],
            'types': [unique_types[i] for i in sorted_indices]
        }
    
    def _calculate_anomaly_statistics(self, peaks_info: Dict[str, np.ndarray], 
                                    unique_anomalies: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate statistics about detected anomalies"""
        
        total_peaks = len(peaks_info['indices'])
        total_anomalies = len(unique_anomalies['anomalies'])
        anomaly_rate = total_anomalies / total_peaks if total_peaks > 0 else 0
        
        # Count anomalies by type
        type_counts = {}
        for anomaly_type in unique_anomalies['types']:
            type_counts[anomaly_type] = type_counts.get(anomaly_type, 0) + 1
        
        return {
            'total_peaks': total_peaks,
            'total_anomalies': total_anomalies,
            'anomaly_rate': anomaly_rate,
            'anomaly_types_count': type_counts,
            'mean_anomaly_score': float(np.mean(unique_anomalies['scores'])) if unique_anomalies['scores'] else 0,
            'max_anomaly_score': float(np.max(unique_anomalies['scores'])) if unique_anomalies['scores'] else 0
        }