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
                'total_columns': len(df.columns),
                'columns': list(df.columns),
                'fields': [],
                'has_primary_key': False,
                'has_foreign_keys': False,
                'has_audit_trail': False,
                'data_types': {},
                'constraints': [],
                'issues': [],
                'recommendations': [],
                'ndmo_compliance': {}
            }
            
            # Analyze each column/field
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
            
            # Analyze each column for NDMO compliance
            analysis['column_analysis'] = self._analyze_columns(df)
            
            # Calculate NDMO compliance per column
            analysis['ndmo_compliance'] = self._calculate_ndmo_compliance_per_column(analysis)
            
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
        # Try to get field name from common column names
        field_name = None
        for col_name in ['Field Name', 'Column Name', 'Field', 'Column', 'Name']:
            if col_name in columns:
                field_name = str(row.get(col_name, ''))
                break
        
        if not field_name:
            # Use first column or index
            field_name = str(row.get(columns[0], f'Field_{row.name}'))
        
        field_info = {
            'field_name': field_name,
            'detected_type': 'Text',
            'is_primary_key': False,
            'is_foreign_key': False,
            'is_audit_field': False,
            'is_required': False,
            'constraints': [],
            'business_rules': [],
            'ndmo_standards': [],
            'compliance_score': 0.0
        }
        
        # Detect field name
        field_name_lower = field_name.lower()
        
        # Check for primary key
        pk_keywords = ['id', 'key', 'pk', 'primary', '_id', 'identifier']
        if any(keyword in field_name_lower for keyword in pk_keywords):
            field_info['is_primary_key'] = True
            field_info['ndmo_standards'].append('DG001')  # Unique Identifiers
        
        # Check for foreign keys
        fk_keywords = ['foreign', 'fk', 'reference', 'ref', '_ref', '_fk']
        if any(keyword in field_name_lower for keyword in fk_keywords):
            field_info['is_foreign_key'] = True
            field_info['ndmo_standards'].append('BR002')  # Data Relationships
        
        # Check for audit trail fields
        audit_keywords = ['created', 'updated', 'modified', 'deleted', 'timestamp', 'date', 'user', 'audit', 'by', 'at', 'on']
        if any(keyword in field_name_lower for keyword in audit_keywords):
            field_info['is_audit_field'] = True
            field_info['ndmo_standards'].append('DS004')  # Audit Trail
        
        # Detect data type from field name or row data
        detected_type = self._detect_data_type_from_name(field_name_lower)
        
        # Try to get type from columns
        for type_col_name in ['Type', 'Data Type', 'DataType', 'Field Type']:
            if type_col_name in columns:
                type_value = str(row.get(type_col_name, '')).lower()
                if type_value:
                    detected_type = self._detect_data_type(type_value)
                    break
        
        field_info['detected_type'] = detected_type
        
        # Add data quality standards based on type
        if detected_type == 'Email':
            field_info['ndmo_standards'].append('DQ005')  # Data Validity
        elif detected_type == 'Phone':
            field_info['ndmo_standards'].append('DQ005')  # Data Validity
        elif detected_type == 'DateTime':
            field_info['ndmo_standards'].append('DQ006')  # Data Timeliness
        
        # Check if required
        for req_col_name in ['Required', 'Mandatory', 'Nullable']:
            if req_col_name in columns:
                req_value = str(row.get(req_col_name, '')).lower()
                if req_value in ['yes', 'true', '1', 'y', 'required', 'mandatory']:
                    field_info['is_required'] = True
                    field_info['ndmo_standards'].append('DQ001')  # Data Completeness
                elif req_value in ['no', 'false', '0', 'n', 'optional', 'nullable']:
                    field_info['is_required'] = False
                break
        
        # Calculate compliance score for this field
        field_info['compliance_score'] = self._calculate_field_compliance_score(field_info)
        
        return field_info
    
    def _detect_data_type_from_name(self, field_name):
        """Detect data type from field name"""
        field_name = field_name.lower()
        
        if any(t in field_name for t in ['email', 'mail', 'e-mail']):
            return 'Email'
        elif any(t in field_name for t in ['phone', 'mobile', 'tel', 'telephone']):
            return 'Phone'
        elif any(t in field_name for t in ['date', 'time', 'datetime', 'timestamp', 'created', 'updated', 'modified']):
            return 'DateTime'
        elif any(t in field_name for t in ['id', 'number', 'num', 'count', 'quantity', 'amount', 'price', 'cost']):
            return 'Numeric'
        elif any(t in field_name for t in ['flag', 'is_', 'has_', 'active', 'enabled', 'status']):
            return 'Boolean'
        else:
            return 'Text'
    
    def _calculate_field_compliance_score(self, field_info):
        """Calculate NDMO compliance score for a field"""
        score = 0.0
        max_score = 0.0
        
        # Primary key check (DG001)
        max_score += 0.15
        if field_info.get('is_primary_key'):
            score += 0.15
        
        # Required field check (DQ001)
        max_score += 0.15
        if field_info.get('is_required'):
            score += 0.15
        
        # Audit trail check (DS004)
        max_score += 0.10
        if field_info.get('is_audit_field'):
            score += 0.10
        
        # Data type detection (DQ005)
        max_score += 0.10
        if field_info.get('detected_type') != 'Unknown':
            score += 0.10
        
        return score / max_score if max_score > 0 else 0.0
    
    def _analyze_columns(self, df):
        """Analyze all columns in the dataframe"""
        column_analysis = []
        
        # Get all columns from the dataframe
        all_columns = list(df.columns)
        
        for col in all_columns:
            try:
                col_info = {
                    'column_name': str(col),
                    'data_type': str(df[col].dtype),
                    'non_null_count': int(df[col].notna().sum()),
                    'null_count': int(df[col].isna().sum()),
                    'unique_count': int(df[col].nunique()),
                    'total_count': len(df),
                    'completeness': (df[col].notna().sum() / len(df)) * 100 if len(df) > 0 else 0,
                    'uniqueness': (df[col].nunique() / len(df)) * 100 if len(df) > 0 else 0
                }
                
                # Detect type from column name
                col_info['detected_type'] = self._detect_data_type_from_name(str(col).lower())
                
                # Check for primary key
                col_info['is_primary_key'] = any(kw in str(col).lower() for kw in ['id', 'key', 'pk', 'primary', '_id'])
                
                # Check for audit fields
                col_info['is_audit_field'] = any(kw in str(col).lower() for kw in ['created', 'updated', 'modified', 'deleted', 'timestamp', 'date', 'user', 'audit', 'created_by', 'updated_by'])
                
                # NDMO standards applicable
                col_info['ndmo_standards'] = []
                if col_info['is_primary_key']:
                    col_info['ndmo_standards'].append('DG001')
                if col_info['is_audit_field']:
                    col_info['ndmo_standards'].append('DS004')
                if col_info['completeness'] < 100:
                    col_info['ndmo_standards'].append('DQ001')
                if col_info['uniqueness'] < 100 and not col_info['is_primary_key']:
                    col_info['ndmo_standards'].append('DQ004')
                
                column_analysis.append(col_info)
            except Exception as e:
                # Skip columns that cause errors
                continue
        
        return column_analysis
    
    def _calculate_ndmo_compliance_per_column(self, analysis):
        """Calculate NDMO compliance for each column"""
        compliance = {}
        
        for col_info in analysis.get('column_analysis', []):
            col_name = col_info['column_name']
            score = 0.0
            max_score = 0.0
            
            # DG001: Unique Identifiers
            if col_info.get('is_primary_key'):
                max_score += 0.15
                score += 0.15
            
            # DQ001: Data Completeness
            max_score += 0.15
            completeness = col_info.get('completeness', 0)
            score += 0.15 * (completeness / 100)
            
            # DQ004: Data Uniqueness
            max_score += 0.10
            uniqueness = col_info.get('uniqueness', 0)
            score += 0.10 * (uniqueness / 100)
            
            # DS004: Audit Trail
            if col_info.get('is_audit_field'):
                max_score += 0.10
                score += 0.10
            
            # DQ005: Data Validity (type detection)
            max_score += 0.10
            if col_info.get('detected_type') != 'Text':
                score += 0.10
            
            compliance[col_name] = {
                'score': score / max_score if max_score > 0 else 0.0,
                'standards': col_info.get('ndmo_standards', []),
                'completeness': completeness,
                'uniqueness': uniqueness,
                'data_type': col_info.get('detected_type', 'Unknown')
            }
        
        return compliance
    
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

