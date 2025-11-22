"""
Excel Importer for NDMO Controls and Evidence
Imports controls, specifications, and evidence requirements from Excel file
"""
import pandas as pd
import json
import os
from datetime import datetime

def import_controls_from_excel(excel_file_path, sheet_name=None):
    """
    Import controls and specifications from Excel file
    
    Expected Excel structure:
    - Sheet 1: Controls (Control ID, Control Name, Domain, Category, Description, etc.)
    - Sheet 2: Specifications (Spec ID, Control ID, Specification Text, Priority, etc.)
    - Sheet 3: Evidence Requirements (Spec ID, Evidence Type, Description, Format, Required)
    """
    
    try:
        # Read Excel file
        excel_file = pd.ExcelFile(excel_file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"Found {len(sheet_names)} sheet(s): {', '.join(sheet_names)}")
        
        controls_data = {}
        specifications_data = {}
        evidence_data = {}
        
        # Try to auto-detect sheets or use provided sheet name
        controls_sheet = None
        specs_sheet = None
        evidence_sheet = None
        
        # Auto-detect sheet names
        for sheet in sheet_names:
            sheet_lower = sheet.lower()
            if 'control' in sheet_lower or 'كنترول' in sheet_lower:
                controls_sheet = sheet
            elif 'spec' in sheet_lower or 'مواصفة' in sheet_lower or 'specification' in sheet_lower:
                specs_sheet = sheet
            elif 'evidence' in sheet_lower or 'أدلة' in sheet_lower or 'proof' in sheet_lower:
                evidence_sheet = sheet
        
        # If not auto-detected, use first sheets
        if not controls_sheet:
            controls_sheet = sheet_names[0] if len(sheet_names) > 0 else None
        if not specs_sheet:
            specs_sheet = sheet_names[1] if len(sheet_names) > 1 else sheet_names[0]
        if not evidence_sheet:
            evidence_sheet = sheet_names[2] if len(sheet_names) > 2 else None
        
        # Read Controls sheet
        if controls_sheet:
            print(f"\nReading Controls from sheet: {controls_sheet}")
            df_controls = pd.read_excel(excel_file_path, sheet_name=controls_sheet)
            print(f"Found {len(df_controls)} rows")
            print(f"Columns: {', '.join(df_controls.columns.tolist())}")
            
            # Normalize column names (handle both English and Arabic)
            column_mapping = {
                'control_id': ['Control ID', 'Control_ID', 'control_id', 'كنترول ID', 'معرف الكنترول'],
                'control_name': ['Control Name', 'Control_Name', 'control_name', 'اسم الكنترول', 'Control Title'],
                'title': ['Title', 'title', 'عنوان'],
                'domain': ['Domain', 'domain', 'المجال', 'Domain Name'],
                'category': ['Category', 'category', 'الفئة', 'Category Name'],
                'description': ['Description', 'description', 'الوصف', 'Control Description'],
                'phase': ['Phase', 'phase', 'المرحلة'],
                'priority': ['Priority', 'priority', 'الأولوية', 'Priority Level']
            }
            
            # Find actual column names
            actual_columns = {}
            for key, possible_names in column_mapping.items():
                for col in df_controls.columns:
                    if col in possible_names or col.lower() in [n.lower() for n in possible_names]:
                        actual_columns[key] = col
                        break
            
            # Process controls
            for idx, row in df_controls.iterrows():
                control_id = str(row.get(actual_columns.get('control_id', df_controls.columns[0]), '')).strip()
                if not control_id or control_id == 'nan':
                    continue
                
                control_name = str(row.get(actual_columns.get('control_name', df_controls.columns[1] if len(df_controls.columns) > 1 else ''), '')).strip()
                if not control_name or control_name == 'nan':
                    control_name = str(row.get(actual_columns.get('title', ''), '')).strip()
                
                controls_data[control_id] = {
                    'id': control_id,
                    'title': control_name,
                    'category': str(row.get(actual_columns.get('category', ''), 'Unknown')).strip(),
                    'domain': str(row.get(actual_columns.get('domain', ''), 'Unknown')).strip(),
                    'description': str(row.get(actual_columns.get('description', ''), '')).strip(),
                    'phase': str(row.get(actual_columns.get('phase', 'Unknown'))).strip(),
                    'priority': str(row.get(actual_columns.get('priority', 'Medium'))).strip(),
                    'specifications': []
                }
            
            print(f"✓ Processed {len(controls_data)} controls")
        
        # Read Specifications sheet
        if specs_sheet:
            print(f"\nReading Specifications from sheet: {specs_sheet}")
            df_specs = pd.read_excel(excel_file_path, sheet_name=specs_sheet)
            print(f"Found {len(df_specs)} rows")
            print(f"Columns: {', '.join(df_specs.columns.tolist())}")
            
            # Normalize column names for specifications
            spec_column_mapping = {
                'spec_id': ['Spec ID', 'Spec_ID', 'spec_id', 'Specification ID', 'مواصفة ID', 'معرف المواصفة'],
                'control_id': ['Control ID', 'Control_ID', 'control_id', 'كنترول ID', 'معرف الكنترول'],
                'spec_text': ['Specification', 'Specification Text', 'spec_text', 'Spec Text', 'المواصفة', 'نص المواصفة'],
                'priority': ['Priority', 'priority', 'P1/P2/P3', 'الأولوية', 'Priority Level'],
                'description': ['Description', 'description', 'الوصف']
            }
            
            spec_actual_columns = {}
            for key, possible_names in spec_column_mapping.items():
                for col in df_specs.columns:
                    if col in possible_names or col.lower() in [n.lower() for n in possible_names]:
                        spec_actual_columns[key] = col
                        break
            
            # Process specifications
            for idx, row in df_specs.iterrows():
                spec_id = str(row.get(spec_actual_columns.get('spec_id', df_specs.columns[0]), '')).strip()
                if not spec_id or spec_id == 'nan':
                    continue
                
                control_id = str(row.get(spec_actual_columns.get('control_id', ''), '')).strip()
                spec_text = str(row.get(spec_actual_columns.get('spec_text', ''), '')).strip()
                priority = str(row.get(spec_actual_columns.get('priority', 'P1'), '')).strip()
                
                if not priority or priority == 'nan':
                    priority = 'P1'
                
                specifications_data[spec_id] = {
                    'spec_id': spec_id,
                    'control_id': control_id,
                    'specification_text': spec_text,
                    'priority': priority,
                    'description': str(row.get(spec_actual_columns.get('description', ''), '')).strip()
                }
                
                # Link to control
                if control_id in controls_data:
                    controls_data[control_id]['specifications'].append(specifications_data[spec_id])
            
            print(f"✓ Processed {len(specifications_data)} specifications")
        
        # Read Evidence sheet
        if evidence_sheet:
            print(f"\nReading Evidence Requirements from sheet: {evidence_sheet}")
            df_evidence = pd.read_excel(excel_file_path, sheet_name=evidence_sheet)
            print(f"Found {len(df_evidence)} rows")
            print(f"Columns: {', '.join(df_evidence.columns.tolist())}")
            
            # Normalize column names for evidence
            evidence_column_mapping = {
                'spec_id': ['Spec ID', 'Spec_ID', 'spec_id', 'Specification ID', 'مواصفة ID'],
                'control_id': ['Control ID', 'Control_ID', 'control_id', 'كنترول ID'],
                'evidence_type': ['Evidence Type', 'Type', 'type', 'نوع الدليل'],
                'description': ['Description', 'description', 'الوصف', 'Evidence Description'],
                'format': ['Format', 'format', 'الصيغة', 'File Format'],
                'required': ['Required', 'required', 'مطلوب', 'Is Required']
            }
            
            evidence_actual_columns = {}
            for key, possible_names in evidence_column_mapping.items():
                for col in df_evidence.columns:
                    if col in possible_names or col.lower() in [n.lower() for n in possible_names]:
                        evidence_actual_columns[key] = col
                        break
            
            # Process evidence
            for idx, row in df_evidence.iterrows():
                spec_id = str(row.get(evidence_actual_columns.get('spec_id', ''), '')).strip()
                control_id = str(row.get(evidence_actual_columns.get('control_id', ''), '')).strip()
                
                if not spec_id or spec_id == 'nan':
                    continue
                
                evidence_key = control_id if control_id else spec_id
                if evidence_key not in evidence_data:
                    evidence_data[evidence_key] = []
                
                evidence_data[evidence_key].append({
                    'type': str(row.get(evidence_actual_columns.get('evidence_type', 'Document'), '')).strip(),
                    'description': str(row.get(evidence_actual_columns.get('description', ''), '')).strip(),
                    'format': str(row.get(evidence_actual_columns.get('format', 'PDF'), '')).strip(),
                    'required': str(row.get(evidence_actual_columns.get('required', 'Yes'), '')).strip().lower() in ['yes', 'true', '1', 'نعم', 'مطلوب']
                })
            
            print(f"✓ Processed evidence for {len(evidence_data)} controls/specifications")
        
        # Create output structure
        output = {
            'import_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source_file': excel_file_path,
            'controls': list(controls_data.values()),
            'specifications': list(specifications_data.values()),
            'evidence': evidence_data,
            'statistics': {
                'total_controls': len(controls_data),
                'total_specifications': len(specifications_data),
                'total_evidence_items': sum(len(v) for v in evidence_data.values())
            }
        }
        
        # Save to JSON
        os.makedirs("imported_data", exist_ok=True)
        output_file = f"imported_data/imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Import completed successfully!")
        print(f"📁 Data saved to: {output_file}")
        print(f"\nStatistics:")
        print(f"  - Controls: {output['statistics']['total_controls']}")
        print(f"  - Specifications: {output['statistics']['total_specifications']}")
        print(f"  - Evidence items: {output['statistics']['total_evidence_items']}")
        
        return output
        
    except Exception as e:
        print(f"❌ Error importing Excel file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def update_data_models_from_import(imported_data):
    """Update data_models.py with imported data"""
    if not imported_data:
        return False
    
    # This function can be used to update the data models
    # For now, we'll save the imported data separately and load it in the app
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
        if os.path.exists(excel_file):
            result = import_controls_from_excel(excel_file)
            if result:
                print("\n✅ Import successful! Data is ready to use in the application.")
        else:
            print(f"❌ File not found: {excel_file}")
    else:
        print("Usage: python excel_importer.py <excel_file_path>")
        print("\nExample: python excel_importer.py controls.xlsx")


