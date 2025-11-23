"""
Smart Schema Analyzer
Analyzes Excel schema files and detects data types, constraints, and NDMO compliance
"""

import pandas as pd
import os
from datetime import datetime

class SmartSchemaAnalyzer:
    """Smart Schema Analyzer for NDMO Compliance"""
    
    def __init__(self):
        self.schema_data = None
        self.analysis_results = {}
    
    def analyze_schema(self, schema_file_path):
        """Analyze schema file and return comprehensive analysis"""
        try:
            # Read schema file
            if not os.path.exists(schema_file_path):
                return {'error': f'Schema file not found: {schema_file_path}'}
            
            # Try to read as Excel
            try:
                df = pd.read_excel(schema_file_path)
            except:
                return {'error': 'Failed to read schema file. Please ensure it is a valid Excel file.'}
            
            # Analyze schema structure
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'file_name': os.path.basename(schema_file_path),
                'total_fields': len(df),
                'fields': [],
                'has_primary_key': False,
                'has_foreign_keys': False,
                'has_audit_trail': False,
                'data_types': {},
                'constraints': [],
                'issues': [],
                'recommendations': []
            }
            
            # Analyze each field
            for idx, row in df.iterrows():
                field_info = self._analyze_field(row, df.columns)
                analysis['fields'].append(field_info)
                
                # Check for primary key
                if field_info.get('is_primary_key', False):
                    analysis['has_primary_key'] = True
                
                # Check for foreign keys
                if field_info.get('is_foreign_key', False):
                    analysis['has_foreign_keys'] = True
                
                # Check for audit trail fields
                if field_info.get('is_audit_field', False):
                    analysis['has_audit_trail'] = True
                
                # Track data types
                data_type = field_info.get('detected_type', 'Unknown')
                analysis['data_types'][data_type] = analysis['data_types'].get(data_type, 0) + 1
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_recommendations(analysis)
            
            # Identify issues
            analysis['issues'] = self._identify_issues(analysis)
            
            self.schema_data = df
            self.analysis_results = analysis
            
            return analysis
            
        except Exception as e:
            return {'error': f'Error analyzing schema: {str(e)}'}
    
    def _analyze_field(self, row, columns):
        """Analyze individual field"""
        field_info = {
            'field_name': str(row.get('Field Name', row.get('Column Name', f'Field_{row.name}'))),
            'detected_type': 'Text',
            'is_primary_key': False,
            'is_foreign_key': False,
            'is_audit_field': False,
            'is_required': False,
            'constraints': [],
            'business_rules': []
        }
        
        # Detect field name
        field_name = field_info['field_name'].lower()
        
        # Check for primary key
        if any(keyword in field_name for keyword in ['id', 'key', 'pk', 'primary']):
            field_info['is_primary_key'] = True
        
        # Check for foreign keys
        if any(keyword in field_name for keyword in ['foreign', 'fk', 'reference', 'ref']):
            field_info['is_foreign_key'] = True
        
        # Check for audit trail fields
        audit_keywords = ['created', 'updated', 'modified', 'deleted', 'timestamp', 'date', 'user', 'audit']
        if any(keyword in field_name for keyword in audit_keywords):
            field_info['is_audit_field'] = True
        
        # Detect data type from field name or row data
        if 'type' in [col.lower() for col in columns]:
            type_col = next((col for col in columns if col.lower() == 'type'), None)
            if type_col:
                detected_type = self._detect_data_type(str(row.get(type_col, '')).lower())
                field_info['detected_type'] = detected_type
        
        # Check if required
        if 'required' in [col.lower() for col in columns]:
            required_col = next((col for col in columns if col.lower() == 'required'), None)
            if required_col:
                field_info['is_required'] = str(row.get(required_col, '')).lower() in ['yes', 'true', '1', 'y']
        
        return field_info
    
    def _detect_data_type(self, type_str):
        """Detect data type from string"""
        type_str = type_str.lower()
        
        if any(t in type_str for t in ['int', 'integer', 'number', 'numeric']):
            return 'Numeric'
        elif any(t in type_str for t in ['date', 'time', 'datetime', 'timestamp']):
            return 'DateTime'
        elif any(t in type_str for t in ['email', 'mail']):
            return 'Email'
        elif any(t in type_str for t in ['phone', 'mobile', 'tel']):
            return 'Phone'
        elif any(t in type_str for t in ['bool', 'boolean', 'yes/no']):
            return 'Boolean'
        else:
            return 'Text'
    
    def _generate_recommendations(self, analysis):
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if not analysis['has_primary_key']:
            recommendations.append({
                'type': 'Critical',
                'message': 'Add primary key field to ensure data uniqueness (DG001)',
                'standard': 'DG001'
            })
        
        if not analysis['has_audit_trail']:
            recommendations.append({
                'type': 'Critical',
                'message': 'Add audit trail fields (created_date, updated_date, created_by) (DS004)',
                'standard': 'DS004'
            })
        
        if analysis['has_foreign_keys']:
            recommendations.append({
                'type': 'Info',
                'message': 'Foreign key relationships detected. Ensure referential integrity is maintained.',
                'standard': 'BR002'
            })
        
        return recommendations
    
    def _identify_issues(self, analysis):
        """Identify schema issues"""
        issues = []
        
        if not analysis['has_primary_key']:
            issues.append({
                'severity': 'High',
                'issue': 'Missing Primary Key',
                'impact': 'Cannot ensure data uniqueness',
                'standard': 'DG001'
            })
        
        if not analysis['has_audit_trail']:
            issues.append({
                'severity': 'High',
                'issue': 'Missing Audit Trail',
                'impact': 'Cannot track data changes',
                'standard': 'DS004'
            })
        
        return issues
    
    def get_analysis_results(self):
        """Get stored analysis results"""
        return self.analysis_results

