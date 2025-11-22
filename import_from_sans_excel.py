"""
Import data from SANS NDI NDMO Assessment Tool Excel file
"""
import pandas as pd
import json
import os
from datetime import datetime

def import_from_sans_excel(excel_path):
    """Import controls, specifications, and evidence from SANS Excel file"""
    
    print("=" * 80)
    print("Importing from SANS NDI NDMO Assessment Tool")
    print("=" * 80)
    
    try:
        # Read NDMO Specs Overview sheet
        print("\n📋 Reading NDMO Specs. Overview...")
        df_specs = pd.read_excel(excel_path, sheet_name="NDMO Specs. Overview", header=None)
        
        # Header is in row 0, data starts from row 3
        # Columns: 0=Domain, 1=ID, 2=Specification, 3=Description, 4=Priority, 5=Compliance Level
        df_specs.columns = ['Domain', 'ID', 'Specification', 'Description', 'Priority', 'Compliance Level', 'Extra']
        
        # Remove header rows and empty rows
        df_specs = df_specs.iloc[3:].copy()  # Start from row 3 (0-indexed)
        df_specs = df_specs[df_specs['ID'].notna()]  # Remove rows without ID
        df_specs = df_specs[df_specs['ID'] != 'ID']  # Remove header row if repeated
        
        print(f"Found {len(df_specs)} specifications")
        
        # Read Master sheet for evidence
        print("\n📋 Reading Master sheet for evidence...")
        df_master = pd.read_excel(excel_path, sheet_name="Master", header=None)
        
        # Header is in row 3, data starts from row 4
        # Columns: 0=Domain Name, 1=Domain ID, 5=Evidence, 6=Acceptance Criteria, 7=Priority, 8=NDMO Specifications, 14=Evidence Document Name
        df_master.columns = [f'Col_{i}' for i in range(len(df_master.columns))]
        df_master = df_master.iloc[4:].copy()  # Start from row 4
        
        # Rename key columns based on position
        df_master.rename(columns={
            'Col_0': 'Domain Name',
            'Col_1': 'Domain ID',
            'Col_5': 'Evidence',
            'Col_6': 'Acceptance Criteria',
            'Col_7': 'Priority',
            'Col_8': 'NDMO Specifications',
            'Col_14': 'Evidence Document Name'
        }, inplace=True)
        
        df_master = df_master[df_master['Domain Name'].notna()]
        print(f"Found {len(df_master)} rows with evidence data")
        
        # Process specifications
        print("\n📋 Processing specifications...")
        specifications = []
        controls_dict = {}
        
        for idx, row in df_specs.iterrows():
            spec_id = str(row['ID']).strip()
            if not spec_id or spec_id == 'nan' or spec_id.lower() == 'id':
                continue
            
            domain = str(row['Domain']) if pd.notna(row['Domain']) else ''
            if not domain or domain == 'nan':
                # Try to get domain from previous rows
                current_idx = df_specs.index.get_loc(idx)
                if current_idx > 0:
                    for i in range(current_idx - 1, -1, -1):
                        prev_row = df_specs.iloc[i]
                        prev_domain = prev_row['Domain']
                        if pd.notna(prev_domain) and str(prev_domain).strip() and str(prev_domain) != 'nan':
                            domain = str(prev_domain)
                            break
            
            spec_text = str(row['Specification']) if pd.notna(row['Specification']) else ''
            description = str(row['Description']) if pd.notna(row['Description']) else ''
            priority = str(row['Priority']) if pd.notna(row['Priority']) else 'P1'
            compliance_level = str(row['Compliance Level']) if pd.notna(row['Compliance Level']) else ''
            
            # Extract control ID from spec ID (e.g., DG.1.1 -> DG.1)
            if '.' in spec_id:
                parts = spec_id.split('.')
                if len(parts) >= 2:
                    control_id = f"{parts[0]}.{parts[1]}"
                else:
                    control_id = parts[0]
            else:
                control_id = spec_id
            
            spec = {
                'spec_id': spec_id,
                'control_id': control_id,
                'domain': domain.strip(),
                'specification_text': spec_text.strip(),
                'description': description.strip(),
                'priority': priority.strip(),
                'compliance_level': compliance_level.strip()
            }
            specifications.append(spec)
            
            # Group by control
            if control_id not in controls_dict:
                controls_dict[control_id] = {
                    'control_id': control_id,
                    'domain': domain.strip(),
                    'specifications': []
                }
            controls_dict[control_id]['specifications'].append(spec)
        
        # Process evidence from Master sheet
        print("\n📋 Processing evidence...")
        evidence_dict = {}
        
        for idx, row in df_master.iterrows():
            ndmo_spec = str(row.get('NDMO Specifications', '')).strip() if pd.notna(row.get('NDMO Specifications')) else ''
            evidence = str(row.get('Evidence', '')).strip() if pd.notna(row.get('Evidence')) else ''
            evidence_doc_name = str(row.get('Evidence Document Name', '')).strip() if pd.notna(row.get('Evidence Document Name')) else ''
            acceptance_criteria = str(row.get('Acceptance Criteria', '')).strip() if pd.notna(row.get('Acceptance Criteria')) else ''
            priority = str(row.get('Priority', '')).strip() if pd.notna(row.get('Priority')) else ''
            
            if not ndmo_spec or ndmo_spec == 'nan':
                continue
            
            # Try to match with specification by ID
            spec_id = None
            if '.' in ndmo_spec:
                # Extract spec ID (e.g., "DG.1.1" from "DG.1.1 specification text")
                parts = ndmo_spec.split('.')
                if len(parts) >= 3:
                    spec_id = f"{parts[0]}.{parts[1]}.{parts[2]}"
                elif len(parts) >= 2:
                    spec_id = f"{parts[0]}.{parts[1]}"
            
            # If not found by ID, try to match by text
            if not spec_id:
                for spec in specifications:
                    if spec['specification_text'].startswith(ndmo_spec[:30]) or ndmo_spec[:30] in spec['specification_text']:
                        spec_id = spec['spec_id']
                        break
            
            if spec_id:
                if spec_id not in evidence_dict:
                    evidence_dict[spec_id] = []
                
                if evidence and evidence != 'nan':
                    evidence_dict[spec_id].append({
                        'type': 'Document',
                        'description': evidence,
                        'document_name': evidence_doc_name if evidence_doc_name != 'nan' else '',
                        'acceptance_criteria': acceptance_criteria if acceptance_criteria != 'nan' else '',
                        'format': 'PDF/DOCX',
                        'required': True,
                        'priority': priority if priority else 'P1'
                    })
        
        # Create controls list
        print("\n📋 Creating controls structure...")
        controls = []
        for control_id, control_data in sorted(controls_dict.items()):
            # Get control name from first specification
            control_name = "Control " + control_id
            if control_data['specifications']:
                first_spec = control_data['specifications'][0]
                # Try to extract control name from specification text
                spec_text = first_spec.get('specification_text', '')
                if spec_text:
                    # Get first part of specification as control name
                    words = spec_text.split()[:5]
                    control_name = ' '.join(words)
            
            control = {
                'id': control_id,
                'title': control_name,
                'domain': control_data['domain'],
                'category': control_data['domain'],
                'description': f"Control {control_id} in {control_data['domain']} domain",
                'phase': 'Unknown',
                'priority': 'Medium',
                'specifications': control_data['specifications'],
                'specifications_count': len(control_data['specifications'])
            }
            controls.append(control)
        
        # Statistics
        stats = {
            'total_controls': len(controls),
            'total_specifications': len(specifications),
            'total_evidence_items': sum(len(v) for v in evidence_dict.values()),
            'specifications_by_priority': {
                'P1': len([s for s in specifications if s['priority'] == 'P1']),
                'P2': len([s for s in specifications if s['priority'] == 'P2']),
                'P3': len([s for s in specifications if s['priority'] == 'P3'])
            },
            'domains': sorted(list(set([s['domain'] for s in specifications if s['domain']])))
        }
        
        # Create output
        output = {
            'import_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source_file': excel_path,
            'controls': controls,
            'specifications': specifications,
            'evidence': evidence_dict,
            'statistics': stats
        }
        
        # Save to JSON
        os.makedirs("imported_data", exist_ok=True)
        output_file = f"imported_data/sans_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 80)
        print("✅ IMPORT COMPLETE")
        print("=" * 80)
        print(f"📊 Statistics:")
        print(f"   - Controls: {stats['total_controls']}")
        print(f"   - Specifications: {stats['total_specifications']}")
        print(f"   - Evidence Items: {stats['total_evidence_items']}")
        print(f"   - P1 Specifications: {stats['specifications_by_priority']['P1']}")
        print(f"   - P2 Specifications: {stats['specifications_by_priority']['P2']}")
        print(f"   - P3 Specifications: {stats['specifications_by_priority']['P3']}")
        print(f"   - Domains: {len(stats['domains'])}")
        print(f"     {', '.join(stats['domains'])}")
        print(f"\n📁 Data saved to: {output_file}")
        
        return output
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    excel_file = "SANS - NDI  NDMO Assessment Tool_(Data Management).xlsx"
    result = import_from_sans_excel(excel_file)
    if result:
        print("\n✅ Ready to use in the application!")
