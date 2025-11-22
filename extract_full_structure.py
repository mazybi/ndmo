"""
Extract the complete structure: 77 controls and 191 specifications
"""
import pdfplumber
import re
import json

def extract_complete_structure(pdf_path):
    """Extract all 77 controls and 191 specifications"""
    
    domains_info = []
    all_controls = []
    all_specifications = []
    
    current_domain = None
    current_control = None
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line_clean = line.strip()
                
                # Detect domain header (9.1, 9.2, etc.)
                domain_match = re.search(r'^9\.(\d+)\.\s+(.+?)\s+Domain', line_clean, re.IGNORECASE)
                if domain_match:
                    domain_num = int(domain_match.group(1))
                    domain_name = domain_match.group(2).strip()
                    
                    # Get domain code (first letters)
                    domain_code = ''.join([word[0].upper() for word in domain_name.split() if word])
                    # Common domain codes from PDF
                    domain_codes_map = {
                        1: 'DG',  # Data Governance
                        2: 'DC',  # Data Catalog
                        3: 'DQ',  # Data Quality
                        4: 'DO',  # Data Operations
                        5: 'DM',  # Document Management
                        6: 'DA',  # Data Architecture
                        7: 'DS',  # Data Sharing
                        8: 'RM',  # Reference and Master
                        9: 'BI',  # Business Intelligence
                        10: 'DV', # Data Value
                        11: 'OD', # Open Data
                        12: 'FO', # Freedom of Information
                        13: 'CL', # Classification
                        14: 'PD', # Personal Data Protection
                        15: 'SP'  # Security and Protection
                    }
                    
                    current_domain = {
                        'number': domain_num,
                        'name': domain_name,
                        'code': domain_codes_map.get(domain_num, domain_code),
                        'page': page_num
                    }
                    domains_info.append(current_domain)
                    continue
                
                # Detect control (format: DG.1 Control Name or just Control Name)
                # Controls are usually numbered like: 1. Control Name or DG.1 Control Name
                control_match = re.search(r'^([A-Z]{2})\.(\d+)\s+(.+?)(?:\s+P[123])?$', line_clean)
                if control_match:
                    domain_code = control_match.group(1)
                    control_num = int(control_match.group(2))
                    control_name = control_match.group(3).strip()
                    
                    control_id = f"{domain_code}.{control_num}"
                    current_control = {
                        'control_id': control_id,
                        'control_name': control_name,
                        'domain': current_domain['name'] if current_domain else 'Unknown',
                        'domain_code': domain_code,
                        'domain_number': current_domain['number'] if current_domain else 0,
                        'page': page_num,
                        'specifications': []
                    }
                    all_controls.append(current_control)
                    continue
                
                # Detect specification (format: DG.1.1 Specification text P1)
                spec_match = re.search(r'^([A-Z]{2})\.(\d+)\.(\d+)\s+(.+?)(?:\s+(P[123]))?\s*$', line_clean)
                if spec_match:
                    domain_code = spec_match.group(1)
                    control_num = int(spec_match.group(2))
                    spec_num = int(spec_match.group(3))
                    spec_text = spec_match.group(4).strip()
                    priority = spec_match.group(5) if len(spec_match.groups()) >= 5 else None
                    
                    # Check if priority is on next line
                    if not priority and i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line in ['P1', 'P2', 'P3']:
                            priority = next_line
                    
                    spec_id = f"{domain_code}.{control_num}.{spec_num}"
                    control_id = f"{domain_code}.{control_num}"
                    
                    specification = {
                        'spec_id': spec_id,
                        'control_id': control_id,
                        'specification_text': spec_text,
                        'priority': priority or 'Unknown',
                        'domain': current_domain['name'] if current_domain else 'Unknown',
                        'domain_code': domain_code,
                        'page': page_num
                    }
                    
                    all_specifications.append(specification)
                    
                    # Add to current control if it matches
                    if current_control and current_control['control_id'] == control_id:
                        current_control['specifications'].append(specification)
                    else:
                        # Find or create control
                        matching_control = next((c for c in all_controls if c['control_id'] == control_id), None)
                        if matching_control:
                            matching_control['specifications'].append(specification)
    
    return {
        'domains': domains_info,
        'controls': all_controls,
        'specifications': all_specifications
    }

if __name__ == "__main__":
    pdf_path = "PoliciesEn001 (1).pdf"
    print("Extracting complete structure from PDF...\n")
    
    structure = extract_complete_structure(pdf_path)
    
    print(f"Domains found: {len(structure['domains'])}")
    print(f"Controls found: {len(structure['controls'])}")
    print(f"Specifications found: {len(structure['specifications'])}\n")
    
    # Count by priority
    p1_specs = [s for s in structure['specifications'] if s.get('priority') == 'P1']
    p2_specs = [s for s in structure['specifications'] if s.get('priority') == 'P2']
    p3_specs = [s for s in structure['specifications'] if s.get('priority') == 'P3']
    
    print(f"P1 Specifications: {len(p1_specs)}")
    print(f"P2 Specifications: {len(p2_specs)}")
    print(f"P3 Specifications: {len(p3_specs)}\n")
    
    # Show sample
    print("Sample Controls (first 5):")
    for i, ctrl in enumerate(structure['controls'][:5], 1):
        print(f"{i}. {ctrl['control_id']}: {ctrl['control_name']}")
        print(f"   Domain: {ctrl['domain']}")
        print(f"   Specifications: {len(ctrl['specifications'])}")
        if ctrl['specifications']:
            print(f"   Priorities: {', '.join(set(s.get('priority', 'Unknown') for s in ctrl['specifications']))}")
        print()
    
    # Save to JSON
    with open('complete_structure.json', 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    
    print(f"\nComplete structure saved to complete_structure.json")
    print(f"\nExpected: 77 controls, 191 specifications")
    print(f"Found: {len(structure['controls'])} controls, {len(structure['specifications'])} specifications")


