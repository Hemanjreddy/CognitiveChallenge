import pandas as pd
import numpy as np
import json
import io
from typing import Dict, List, Any

class DataExporter:
    """Handles exporting peak detection results to various formats"""
    
    def __init__(self):
        pass
    
    def export_to_csv(self, detected_peaks: Dict[str, Dict[str, np.ndarray]], 
                     data: Dict[str, Any], selected_signals: List[str]) -> str:
        """
        Export peak detection results to CSV format
        
        Args:
            detected_peaks: Peak detection results
            data: Original signal data
            selected_signals: List of analyzed signals
            
        Returns:
            CSV data as string
        """
        try:
            export_rows = []
            
            for signal_name in selected_signals:
                peaks_info = detected_peaks[signal_name]
                
                if len(peaks_info['indices']) == 0:
                    # Add a row indicating no peaks found
                    export_rows.append({
                        'Signal_Name': signal_name,
                        'Peak_Index': None,
                        'Time_s': None,
                        'Height': None,
                        'Width': None,
                        'Prominence': None,
                        'Note': 'No peaks detected'
                    })
                else:
                    # Add rows for each detected peak
                    for i in range(len(peaks_info['indices'])):
                        row = {
                            'Signal_Name': signal_name,
                            'Peak_Index': int(peaks_info['indices'][i]),
                            'Time_s': float(peaks_info['times'][i]) if len(peaks_info['times']) > i else None,
                            'Height': float(peaks_info['heights'][i]) if len(peaks_info['heights']) > i else None,
                            'Width': float(peaks_info['widths'][i]) if len(peaks_info['widths']) > i and not np.isnan(peaks_info['widths'][i]) else None,
                            'Prominence': float(peaks_info['prominences'][i]) if len(peaks_info['prominences']) > i and not np.isnan(peaks_info['prominences'][i]) else None,
                            'Note': 'Peak detected'
                        }
                        export_rows.append(row)
            
            # Create DataFrame and convert to CSV
            df = pd.DataFrame(export_rows)
            
            # Add metadata header
            metadata_rows = [
                f"# MF4 Peak Detection Results",
                f"# Export Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"# Total Signals Analyzed: {len(selected_signals)}",
                f"# Total Peaks Detected: {sum(len(peaks['indices']) for peaks in detected_peaks.values())}",
                f"# Signal Duration: {data.get('duration', 0):.3f} seconds",
                f"# Sample Rate: {data.get('sample_rate', 1):.1f} Hz",
                ""
            ]
            
            # Convert DataFrame to CSV
            csv_buffer = io.StringIO()
            
            # Write metadata
            for line in metadata_rows:
                csv_buffer.write(line + '\n')
            
            # Write data
            df.to_csv(csv_buffer, index=False)
            
            return csv_buffer.getvalue()
            
        except Exception as e:
            return f"Error generating CSV: {str(e)}"
    
    def export_to_json(self, detected_peaks: Dict[str, Dict[str, np.ndarray]], 
                      data: Dict[str, Any], selected_signals: List[str]) -> str:
        """
        Export peak detection results to JSON format
        
        Args:
            detected_peaks: Peak detection results
            data: Original signal data
            selected_signals: List of analyzed signals
            
        Returns:
            JSON data as string
        """
        try:
            # Prepare export data structure
            export_data = {
                'metadata': {
                    'export_date': pd.Timestamp.now().isoformat(),
                    'total_signals_analyzed': len(selected_signals),
                    'total_peaks_detected': sum(len(peaks['indices']) for peaks in detected_peaks.values()),
                    'signal_duration_seconds': float(data.get('duration', 0)),
                    'sample_rate_hz': float(data.get('sample_rate', 1)),
                    'file_info': data.get('file_info', {})
                },
                'signals': {}
            }
            
            # Process each signal
            for signal_name in selected_signals:
                peaks_info = detected_peaks[signal_name]
                
                # Convert numpy arrays to lists for JSON serialization
                signal_data = {
                    'signal_name': signal_name,
                    'peaks_count': int(len(peaks_info['indices'])),
                    'peaks': []
                }
                
                if len(peaks_info['indices']) > 0:
                    for i in range(len(peaks_info['indices'])):
                        peak = {
                            'index': int(peaks_info['indices'][i]),
                            'time_seconds': float(peaks_info['times'][i]) if len(peaks_info['times']) > i else None,
                            'height': float(peaks_info['heights'][i]) if len(peaks_info['heights']) > i else None,
                            'width': float(peaks_info['widths'][i]) if len(peaks_info['widths']) > i and not np.isnan(peaks_info['widths'][i]) else None,
                            'prominence': float(peaks_info['prominences'][i]) if len(peaks_info['prominences']) > i and not np.isnan(peaks_info['prominences'][i]) else None
                        }
                        signal_data['peaks'].append(peak)
                
                # Add signal statistics
                signal_data['statistics'] = self._calculate_signal_statistics(peaks_info)
                
                export_data['signals'][signal_name] = signal_data
            
            # Convert to JSON string with proper formatting
            return json.dumps(export_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({'error': f'Error generating JSON: {str(e)}'}, indent=2)
    
    def export_to_excel(self, detected_peaks: Dict[str, Dict[str, np.ndarray]], 
                       data: Dict[str, Any], selected_signals: List[str]) -> bytes:
        """
        Export peak detection results to Excel format
        
        Args:
            detected_peaks: Peak detection results
            data: Original signal data
            selected_signals: List of analyzed signals
            
        Returns:
            Excel file as bytes
        """
        try:
            # Create Excel writer object
            excel_buffer = io.BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # Create summary sheet
                summary_data = []
                for signal_name in selected_signals:
                    peaks_info = detected_peaks[signal_name]
                    stats = self._calculate_signal_statistics(peaks_info)
                    
                    summary_data.append({
                        'Signal Name': signal_name,
                        'Peaks Count': stats['count'],
                        'Mean Height': stats['mean_height'],
                        'Mean Width': stats['mean_width'],
                        'Mean Prominence': stats['mean_prominence'],
                        'Peak Rate (peaks/s)': stats['peak_rate']
                    })
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Create detailed sheets for each signal
                for signal_name in selected_signals:
                    peaks_info = detected_peaks[signal_name]
                    
                    if len(peaks_info['indices']) > 0:
                        detail_data = []
                        for i in range(len(peaks_info['indices'])):
                            detail_data.append({
                                'Peak Index': int(peaks_info['indices'][i]),
                                'Time (s)': float(peaks_info['times'][i]) if len(peaks_info['times']) > i else None,
                                'Height': float(peaks_info['heights'][i]) if len(peaks_info['heights']) > i else None,
                                'Width': float(peaks_info['widths'][i]) if len(peaks_info['widths']) > i and not np.isnan(peaks_info['widths'][i]) else None,
                                'Prominence': float(peaks_info['prominences'][i]) if len(peaks_info['prominences']) > i and not np.isnan(peaks_info['prominences'][i]) else None
                            })
                        
                        detail_df = pd.DataFrame(detail_data)
                        # Truncate sheet name if too long
                        sheet_name = signal_name[:31] if len(signal_name) > 31 else signal_name
                        detail_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            excel_buffer.seek(0)
            return excel_buffer.getvalue()
            
        except Exception as e:
            # Return empty bytes if error
            return b''
    
    def _calculate_signal_statistics(self, peaks_info: Dict[str, np.ndarray]) -> Dict[str, float]:
        """
        Calculate statistics for a signal's peaks
        
        Args:
            peaks_info: Peak information for a single signal
            
        Returns:
            Dictionary with calculated statistics
        """
        try:
            if len(peaks_info['indices']) == 0:
                return {
                    'count': 0,
                    'mean_height': 0.0,
                    'mean_width': 0.0,
                    'mean_prominence': 0.0,
                    'peak_rate': 0.0
                }
            
            stats = {
                'count': len(peaks_info['indices'])
            }
            
            # Height statistics
            if len(peaks_info['heights']) > 0:
                stats['mean_height'] = float(np.mean(peaks_info['heights']))
            else:
                stats['mean_height'] = 0.0
            
            # Width statistics
            if len(peaks_info['widths']) > 0:
                valid_widths = peaks_info['widths'][~np.isnan(peaks_info['widths'])]
                if len(valid_widths) > 0:
                    stats['mean_width'] = float(np.mean(valid_widths))
                else:
                    stats['mean_width'] = 0.0
            else:
                stats['mean_width'] = 0.0
            
            # Prominence statistics
            if len(peaks_info['prominences']) > 0:
                valid_prominences = peaks_info['prominences'][~np.isnan(peaks_info['prominences'])]
                if len(valid_prominences) > 0:
                    stats['mean_prominence'] = float(np.mean(valid_prominences))
                else:
                    stats['mean_prominence'] = 0.0
            else:
                stats['mean_prominence'] = 0.0
            
            # Peak rate
            if len(peaks_info['times']) > 0:
                time_span = np.max(peaks_info['times']) - np.min(peaks_info['times'])
                if time_span > 0:
                    stats['peak_rate'] = len(peaks_info['indices']) / time_span
                else:
                    stats['peak_rate'] = 0.0
            else:
                stats['peak_rate'] = 0.0
            
            return stats
            
        except Exception:
            return {
                'count': 0,
                'mean_height': 0.0,
                'mean_width': 0.0,
                'mean_prominence': 0.0,
                'peak_rate': 0.0
            }
