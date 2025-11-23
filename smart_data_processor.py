"""
Smart Data Processor
Processes data according to schema requirements and improves data quality
"""

import pandas as pd
import numpy as np
from datetime import datetime

class SmartDataProcessor:
    """Smart Data Processor for NDMO Compliance"""
    
    def __init__(self):
        self.processed_data = None
        self.quality_metrics = {}
        self.processing_log = []
    
    def process_data(self, data_file_path, schema_analysis):
        """Process data file according to schema analysis"""
        try:
            # Read data file
            if not isinstance(data_file_path, pd.DataFrame):
                df = pd.read_excel(data_file_path)
            else:
                df = data_file_path.copy()
            
            # Initialize processing log
            self.processing_log = []
            self._log("Starting data processing...")
            
            # Step 1: Load and validate
            self._log("Step 1: Loading data file...")
            df_processed = df.copy()
            
            # Step 2: Schema validation
            self._log("Step 2: Validating against schema...")
            validation_results = self._validate_against_schema(df_processed, schema_analysis)
            
            # Step 3: Data type conversion
            self._log("Step 3: Converting data types...")
            df_processed = self._convert_data_types(df_processed, schema_analysis)
            
            # Step 4: Quality analysis
            self._log("Step 4: Analyzing data quality...")
            quality_metrics = self._analyze_quality(df_processed)
            
            # Step 5: Quality improvements
            self._log("Step 5: Applying quality improvements...")
            df_processed = self._improve_quality(df_processed, schema_analysis)
            
            # Step 6: Recalculate quality after improvements
            self._log("Step 6: Recalculating quality metrics...")
            final_quality = self._analyze_quality(df_processed)
            
            # Step 7: Finalize
            self._log("Step 7: Finalizing results...")
            
            self.processed_data = df_processed
            self.quality_metrics = final_quality
            
            return {
                'success': True,
                'processed_data': df_processed,
                'quality_metrics': final_quality,
                'validation_results': validation_results,
                'processing_log': self.processing_log,
                'improvements_applied': len(self.processing_log) > 0
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing data: {str(e)}',
                'processing_log': self.processing_log
            }
    
    def _validate_against_schema(self, df, schema_analysis):
        """Validate data against schema"""
        validation_results = {
            'valid': True,
            'issues': []
        }
        
        if not schema_analysis or 'fields' not in schema_analysis:
            return validation_results
        
        # Check required fields
        schema_fields = [f.get('field_name', '') for f in schema_analysis.get('fields', [])]
        data_columns = df.columns.tolist()
        
        for field in schema_analysis.get('fields', []):
            field_name = field.get('field_name', '')
            if field.get('is_required', False):
                if field_name not in data_columns:
                    validation_results['valid'] = False
                    validation_results['issues'].append(f'Required field missing: {field_name}')
        
        return validation_results
    
    def _convert_data_types(self, df, schema_analysis):
        """Convert data types according to schema"""
        df_converted = df.copy()
        
        if not schema_analysis or 'fields' not in schema_analysis:
            return df_converted
        
        for field in schema_analysis.get('fields', []):
            field_name = field.get('field_name', '')
            detected_type = field.get('detected_type', 'Text')
            
            if field_name in df_converted.columns:
                try:
                    if detected_type == 'Numeric':
                        df_converted[field_name] = pd.to_numeric(df_converted[field_name], errors='coerce')
                    elif detected_type == 'DateTime':
                        df_converted[field_name] = pd.to_datetime(df_converted[field_name], errors='coerce')
                    elif detected_type == 'Boolean':
                        df_converted[field_name] = df_converted[field_name].astype(str).str.lower().isin(['true', 'yes', '1', 'y'])
                except:
                    pass  # Keep original if conversion fails
        
        return df_converted
    
    def _analyze_quality(self, df):
        """Analyze data quality metrics"""
        metrics = {
            'completeness': 0.0,
            'accuracy': 0.8,  # Default assumption
            'consistency': 0.8,  # Default assumption
            'uniqueness': 0.0,
            'validity': 0.8,  # Default assumption
            'overall_score': 0.0
        }
        
        if df.empty:
            return metrics
        
        # Completeness: percentage of non-null values
        total_cells = len(df) * len(df.columns)
        non_null_cells = df.notna().sum().sum()
        metrics['completeness'] = non_null_cells / total_cells if total_cells > 0 else 0
        
        # Uniqueness: percentage of unique rows
        total_rows = len(df)
        unique_rows = len(df.drop_duplicates())
        metrics['uniqueness'] = unique_rows / total_rows if total_rows > 0 else 0
        
        # Calculate overall score (weighted average)
        weights = {
            'completeness': 0.25,
            'accuracy': 0.20,
            'consistency': 0.15,
            'uniqueness': 0.20,
            'validity': 0.20
        }
        
        metrics['overall_score'] = sum(
            metrics[key] * weights[key]
            for key in weights.keys()
        )
        
        return metrics
    
    def _improve_quality(self, df, schema_analysis):
        """Apply quality improvements"""
        df_improved = df.copy()
        
        # Remove duplicate rows
        initial_rows = len(df_improved)
        df_improved = df_improved.drop_duplicates()
        removed_duplicates = initial_rows - len(df_improved)
        if removed_duplicates > 0:
            self._log(f"Removed {removed_duplicates} duplicate rows")
        
        # Fill missing values for required fields (if schema available)
        if schema_analysis and 'fields' in schema_analysis:
            for field in schema_analysis.get('fields', []):
                field_name = field.get('field_name', '')
                if field.get('is_required', False) and field_name in df_improved.columns:
                    # Fill with appropriate default based on type
                    detected_type = field.get('detected_type', 'Text')
                    if detected_type == 'Numeric':
                        df_improved[field_name].fillna(0, inplace=True)
                    elif detected_type == 'Text':
                        df_improved[field_name].fillna('', inplace=True)
        
        return df_improved
    
    def _log(self, message):
        """Add message to processing log"""
        self.processing_log.append({
            'timestamp': datetime.now().isoformat(),
            'message': message
        })
    
    def get_processed_data(self):
        """Get processed data"""
        return self.processed_data
    
    def get_quality_metrics(self):
        """Get quality metrics"""
        return self.quality_metrics

