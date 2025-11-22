"""
NDI Controls Loader
Loads and manages NDI controls from SANS Excel file
"""
import pandas as pd
import json
import os
from datetime import datetime

def load_ndi_controls_from_sans(excel_path):
    """Load NDI controls from SANS Excel file"""
    
    try:
        # Read Master sheet for NDI Q# and NDI ID
        df_master = pd.read_excel(excel_path, sheet_name="Master", header=3)
        df_master = df_master[df_master['Domain Name'].notna()]
        
        # Read Priority Items for NDI information
        df_priority = pd.read_excel(excel_path, sheet_name="Priority Items", header=3)
        df_priority = df_priority[df_priority['Domain Name'].notna()]
        
        ndi_controls = []
        
        for idx, row in df_master.iterrows():
            ndi_q = str(row.get('NDI Q#', '')).strip() if pd.notna(row.get('NDI Q#')) else ''
            ndi_id = str(row.get('NDI ID', '')).strip() if pd.notna(row.get('NDI ID')) else ''
            domain = str(row.get('Domain Name', '')).strip() if pd.notna(row.get('Domain Name')) else ''
            maturity_level = str(row.get('Maturity Level', '')).strip() if pd.notna(row.get('Maturity Level')) else ''
            level_no = str(row.get('Level No.', '')).strip() if pd.notna(row.get('Level No.')) else ''
            evidence = str(row.get('Evidence', '')).strip() if pd.notna(row.get('Evidence')) else ''
            acceptance_criteria = str(row.get('Acceptance Criteria', '')).strip() if pd.notna(row.get('Acceptance Criteria')) else ''
            priority = str(row.get('Priority', '')).strip() if pd.notna(row.get('Priority')) else ''
            ndmo_specs = str(row.get('NDMO Specifications', '')).strip() if pd.notna(row.get('NDMO Specifications')) else ''
            
            if ndi_id and ndi_id != 'nan':
                ndi_control = {
                    'ndi_id': ndi_id,
                    'ndi_q': ndi_q,
                    'domain': domain,
                    'maturity_level': maturity_level,
                    'level_no': level_no,
                    'evidence': evidence,
                    'acceptance_criteria': acceptance_criteria,
                    'priority': priority,
                    'ndmo_specifications': ndmo_specs,
                    'meets_ndmo': str(row.get('Meets NDMO criteria?', '')).strip() if pd.notna(row.get('Meets NDMO criteria?')) else '',
                    'meets_ndi': str(row.get('Meets NDI Criteria?', '')).strip() if pd.notna(row.get('Meets NDI Criteria?')) else '',
                    'compliance_flag': str(row.get('Compliance Validation Flag', '')).strip() if pd.notna(row.get('Compliance Validation Flag')) else '',
                    'comments': str(row.get('Comments', '')).strip() if pd.notna(row.get('Comments')) else '',
                    'evidence_doc_name': str(row.get('Evidence Document Name', '')).strip() if pd.notna(row.get('Evidence Document Name')) else '',
                    'stakeholders': str(row.get('Current Stakeholders', '')).strip() if pd.notna(row.get('Current Stakeholders')) else ''
                }
                ndi_controls.append(ndi_control)
        
        # Save to JSON
        os.makedirs("imported_data", exist_ok=True)
        output_file = f"imported_data/ndi_controls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output = {
            'import_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source_file': excel_path,
            'ndi_controls': ndi_controls,
            'total_controls': len(ndi_controls)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        return output
        
    except Exception as e:
        print(f"Error loading NDI controls: {e}")
        return None

def get_ndi_controls():
    """Get all NDI controls from saved file"""
    try:
        import glob
        ndi_files = glob.glob("imported_data/ndi_controls_*.json")
        if ndi_files:
            latest_file = sorted(ndi_files)[-1]
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return None


