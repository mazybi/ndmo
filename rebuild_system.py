"""
Rebuild the entire NDMO system from SANS Excel file
Extract all data: Controls, Specifications, Evidence, Calculations, Templates
"""
import pandas as pd
import json
import os
from datetime import datetime

def rebuild_system_from_sans(excel_path):
    """Rebuild complete system from SANS Excel"""
    
    print("=" * 80)
    print("REBUILDING NDMO SYSTEM FROM SANS EXCEL")
    print("=" * 80)
    
    # 1. Read NDMO Specs Overview (Specifications)
    print("\n1️⃣ Reading NDMO Specifications...")
    df_specs = pd.read_excel(excel_path, sheet_name="NDMO Specs. Overview", header=0)
    df_specs = df_specs.iloc[3:].copy()  # Skip header rows
    df_specs = df_specs[df_specs['ID'].notna()]
    df_specs = df_specs[df_specs['ID'] != 'ID']
    
    print(f"   ✓ Found {len(df_specs)} specifications")
    
    # 2. Read Master sheet (Controls, Evidence, Acceptance Criteria)
    print("\n2️⃣ Reading Master Sheet (Controls & Evidence)...")
    df_master = pd.read_excel(excel_path, sheet_name="Master", header=3)
    df_master = df_master[df_master['Domain Name'].notna()]
    
    print(f"   ✓ Found {len(df_master)} master records")
    
    # 3. Read Priority Items
    print("\n3️⃣ Reading Priority Items...")
    df_priority = pd.read_excel(excel_path, sheet_name="Priority Items", header=3)
    df_priority = df_priority[df_priority['Domain Name'].notna()]
    
    print(f"   ✓ Found {len(df_priority)} priority items")
    
    # 4. Read Maturity Questions
    print("\n4️⃣ Reading Maturity Questions...")
    df_maturity = pd.read_excel(excel_path, sheet_name="Maturity Questions Overview", header=3)
    
    print(f"   ✓ Found maturity questions data")
    
    # 5. Read Calculation sheet
    print("\n5️⃣ Reading Calculation Sheet...")
    df_calc = pd.read_excel(excel_path, sheet_name="Calculation", header=2)
    
    print(f"   ✓ Found calculation data")
    
    # 6. Read Hiden- Spec (Compliance status)
    print("\n6️⃣ Reading Compliance Status...")
    df_compliance = pd.read_excel(excel_path, sheet_name="Hiden- Spec", header=0)
    
    print(f"   ✓ Found {len(df_compliance)} compliance records")
    
    # Process Specifications
    print("\n📋 Processing Specifications...")
    specifications = []
    current_domain = None
    
    for idx, row in df_specs.iterrows():
        spec_id = str(row['ID']).strip()
        if not spec_id or spec_id == 'nan' or spec_id.lower() == 'id':
            continue
        
        # Get domain (carry forward if empty)
        domain = str(row['Domain']) if pd.notna(row['Domain']) else current_domain
        if domain and domain != 'nan':
            current_domain = domain.strip()
        else:
            domain = current_domain
        
        spec_text = str(row['Specification']) if pd.notna(row['Specification']) else ''
        description = str(row['Description']) if pd.notna(row['Description']) else ''
        priority = str(row['Priority']) if pd.notna(row['Priority']) else 'P1'
        compliance_level = str(row['Compliance Level']) if pd.notna(row['Compliance Level']) else ''
        
        # Extract control ID
        if '.' in spec_id:
            parts = spec_id.split('.')
            control_id = f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else parts[0]
        else:
            control_id = spec_id
        
        # Get compliance status from Hiden- Spec
        compliance_status = 'Unknown'
        if 'Spec iD' in df_compliance.columns:
            compliance_row = df_compliance[df_compliance['Spec iD'] == spec_id]
            if not compliance_row.empty:
                compliance_status = str(compliance_row.iloc[0]['Compliance']) if pd.notna(compliance_row.iloc[0]['Compliance']) else 'Unknown'
        
        spec = {
            'spec_id': spec_id,
            'control_id': control_id,
            'domain': domain,
            'specification_text': spec_text,
            'description': description,
            'priority': priority,
            'compliance_level': compliance_level,
            'compliance_status': compliance_status
        }
        specifications.append(spec)
    
    print(f"   ✓ Processed {len(specifications)} specifications")
    
    # Process Controls
    print("\n📋 Processing Controls...")
    controls_dict = {}
    
    for spec in specifications:
        control_id = spec['control_id']
        if control_id not in controls_dict:
            controls_dict[control_id] = {
                'control_id': control_id,
                'domain': spec['domain'],
                'specifications': []
            }
        controls_dict[control_id]['specifications'].append(spec)
    
    controls = []
    for control_id, control_data in sorted(controls_dict.items()):
        # Get control name from first specification
        control_name = f"Control {control_id}"
        if control_data['specifications']:
            first_spec = control_data['specifications'][0]
            spec_text = first_spec.get('specification_text', '')
            if spec_text:
                # Extract meaningful name
                words = spec_text.split()[:6]
                control_name = ' '.join(words)
        
        # Calculate control statistics
        specs = control_data['specifications']
        p1_count = len([s for s in specs if s['priority'] == 'P1'])
        p2_count = len([s for s in specs if s['priority'] == 'P2'])
        p3_count = len([s for s in specs if s['priority'] == 'P3'])
        
        control = {
            'id': control_id,
            'title': control_name,
            'domain': control_data['domain'],
            'category': control_data['domain'],
            'description': f"Control {control_id} in {control_data['domain']} domain",
            'phase': 'Unknown',
            'priority': 'High' if p1_count > 0 else 'Medium',
            'specifications': specs,
            'specifications_count': len(specs),
            'priority_distribution': {
                'P1': p1_count,
                'P2': p2_count,
                'P3': p3_count
            }
        }
        controls.append(control)
    
    print(f"   ✓ Processed {len(controls)} controls")
    
    # Process Evidence from Master sheet
    print("\n📋 Processing Evidence...")
    evidence_dict = {}
    
    for idx, row in df_master.iterrows():
        ndmo_spec = str(row.get('NDMO Specifications', '')).strip() if pd.notna(row.get('NDMO Specifications')) else ''
        evidence = str(row.get('Evidence', '')).strip() if pd.notna(row.get('Evidence')) else ''
        evidence_doc_name = str(row.get('Evidence Document Name', '')).strip() if pd.notna(row.get('Evidence Document Name')) else ''
        acceptance_criteria = str(row.get('Acceptance Criteria', '')).strip() if pd.notna(row.get('Acceptance Criteria')) else ''
        priority = str(row.get('Priority', '')).strip() if pd.notna(row.get('Priority')) else ''
        maturity_level = str(row.get('Maturity Level', '')).strip() if pd.notna(row.get('Maturity Level')) else ''
        level_no = str(row.get('Level No.', '')).strip() if pd.notna(row.get('Level No.')) else ''
        
        if not ndmo_spec or ndmo_spec == 'nan':
            continue
        
        # Match with specification
        spec_id = None
        if '.' in ndmo_spec:
            parts = ndmo_spec.split('.')
            if len(parts) >= 3:
                spec_id = f"{parts[0]}.{parts[1]}.{parts[2]}"
        
        # If not found, try text matching
        if not spec_id:
            for spec in specifications:
                if spec['specification_text'].startswith(ndmo_spec[:40]) or ndmo_spec[:40] in spec['specification_text']:
                    spec_id = spec['spec_id']
                    break
        
        if spec_id:
            if spec_id not in evidence_dict:
                evidence_dict[spec_id] = []
            
            if evidence and evidence != 'nan':
                evidence_dict[spec_id].append({
                    'type': 'Document',
                    'description': evidence,
                    'document_name': evidence_doc_name,
                    'acceptance_criteria': acceptance_criteria,
                    'format': 'PDF/DOCX',
                    'required': True,
                    'priority': priority,
                    'maturity_level': maturity_level,
                    'level_no': level_no
                })
    
    print(f"   ✓ Processed {sum(len(v) for v in evidence_dict.values())} evidence items")
    
    # Process Calculations
    print("\n📋 Processing Calculations...")
    calculations = {}
    
    if 'NDI ID' in df_calc.columns:
        for idx, row in df_calc.iterrows():
            ndi_id = str(row.get('NDI ID', '')).strip() if pd.notna(row.get('NDI ID')) else ''
            if ndi_id and ndi_id != 'nan':
                calc_data = {}
                for col in df_calc.columns:
                    if col not in ['NDI ID', 'Unnamed: 0']:
                        val = row.get(col)
                        if pd.notna(val):
                            calc_data[str(col)] = val
                calculations[ndi_id] = calc_data
    
    print(f"   ✓ Processed {len(calculations)} calculation records")
    
    # Process Maturity Questions
    print("\n📋 Processing Maturity Questions...")
    maturity_questions = []
    
    if 'Domain' in df_maturity.columns or 'Unnamed: 1' in df_maturity.columns:
        domain_col = 'Domain' if 'Domain' in df_maturity.columns else 'Unnamed: 1'
        for idx, row in df_maturity.iterrows():
            domain = str(row.get(domain_col, '')).strip() if pd.notna(row.get(domain_col)) else ''
            if domain and domain != 'nan' and domain.lower() != 'domain':
                question_data = {
                    'domain': domain,
                    'levels': {}
                }
                for level in ['Level 0', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']:
                    if level in df_maturity.columns:
                        val = row.get(level)
                        if pd.notna(val):
                            question_data['levels'][level] = str(val)
                if question_data['levels']:
                    maturity_questions.append(question_data)
    
    print(f"   ✓ Processed {len(maturity_questions)} maturity questions")
    
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
        'domains': sorted(list(set([s['domain'] for s in specifications if s['domain']]))),
        'total_calculations': len(calculations),
        'total_maturity_questions': len(maturity_questions)
    }
    
    # Create complete output
    output = {
        'import_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'source_file': excel_path,
        'controls': controls,
        'specifications': specifications,
        'evidence': evidence_dict,
        'calculations': calculations,
        'maturity_questions': maturity_questions,
        'statistics': stats
    }
    
    # Save to JSON
    os.makedirs("imported_data", exist_ok=True)
    output_file = f"imported_data/complete_sans_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("✅ SYSTEM REBUILD COMPLETE")
    print("=" * 80)
    print(f"📊 Final Statistics:")
    print(f"   - Controls: {stats['total_controls']}")
    print(f"   - Specifications: {stats['total_specifications']}")
    print(f"   - Evidence Items: {stats['total_evidence_items']}")
    print(f"   - P1: {stats['specifications_by_priority']['P1']}, P2: {stats['specifications_by_priority']['P2']}, P3: {stats['specifications_by_priority']['P3']}")
    print(f"   - Domains: {len(stats['domains'])}")
    print(f"   - Calculations: {stats['total_calculations']}")
    print(f"   - Maturity Questions: {stats['total_maturity_questions']}")
    print(f"\n📁 Complete system saved to: {output_file}")
    
    return output

if __name__ == "__main__":
    excel_file = "SANS - NDI  NDMO Assessment Tool_(Data Management).xlsx"
    result = rebuild_system_from_sans(excel_file)
    if result:
        print("\n✅ System ready to use!")


