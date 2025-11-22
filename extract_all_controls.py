"""
Extract all controls with their details from PDF
"""
import pdfplumber
import re
import json

def extract_controls_detailed(pdf_path):
    """Extract all controls with full details"""
    controls = []
    current_domain = None
    current_control_id = None
    current_control_name = None
    current_priority = None
    current_specs = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line_clean = line.strip()
                
                # Detect domain (9.1, 9.2, etc.)
                domain_match = re.search(r'^9\.(\d+)\.\s+(.+?)\s+Domain', line_clean, re.IGNORECASE)
                if domain_match:
                    current_domain = {
                        'number': int(domain_match.group(1)),
                        'name': domain_match.group(2).strip(),
                        'page': page_num
                    }
                    continue
                
                # Detect control ID pattern (e.g., DG.1.1, DC.2.3, etc.)
                # Format: Two letters, dot, number, dot, number
                control_id_match = re.search(r'^([A-Z]{2})\.(\d+)\.(\d+)\s+(.+)', line_clean)
                if control_id_match:
                    domain_code = control_id_match.group(1)
                    control_num = control_id_match.group(2)
                    spec_num = control_id_match.group(3)
                    rest_text = control_id_match.group(4)
                    
                    # This might be a specification, not a control
                    # Controls usually don't have the third number
                    # Let's check if it's actually a control (format: DG.1 Control Name)
                    control_only_match = re.search(r'^([A-Z]{2})\.(\d+)\s+(.+?)(?:\s+P[123]|$)', line_clean)
                    if control_only_match and not spec_num:
                        # This is a control header
                        if current_control_id:
                            # Save previous control
                            controls.append({
                                'control_id': current_control_id,
                                'control_name': current_control_name,
                                'domain': current_domain['name'] if current_domain else 'Unknown',
                                'domain_number': current_domain['number'] if current_domain else 0,
                                'priority': current_priority,
                                'page': page_num - 1 if page_num > 1 else 1,
                                'specifications_count': len(current_specs)
                            })
                        
                        current_control_id = f"{control_only_match.group(1)}.{control_only_match.group(2)}"
                        current_control_name = control_only_match.group(3).strip()
                        current_specs = []
                        
                        # Check for priority in the same line or next lines
                        priority_in_line = re.search(r'\b(P[123])\b', line_clean)
                        if priority_in_line:
                            current_priority = priority_in_line.group(1)
                        continue
                
                # Check for priority markers (P1, P2, P3) - might be on separate line
                priority_match = re.search(r'^\s*(P[123])\s*$', line_clean)
                if priority_match and current_control_id:
                    current_priority = priority_match.group(1)
                
                # Look for specification patterns (DG.1.1, DG.1.2, etc.)
                spec_match = re.search(r'^([A-Z]{2})\.(\d+)\.(\d+)\s+(.+?)(?:\s+(P[123]))?', line_clean)
                if spec_match:
                    domain_code = spec_match.group(1)
                    control_num = spec_match.group(2)
                    spec_num = spec_match.group(3)
                    spec_text = spec_match.group(4).strip()
                    spec_priority = spec_match.group(5) if len(spec_match.groups()) > 4 else None
                    
                    spec_id = f"{domain_code}.{control_num}.{spec_num}"
                    current_specs.append({
                        'spec_id': spec_id,
                        'text': spec_text,
                        'priority': spec_priority or current_priority
                    })
    
    # Add last control
    if current_control_id:
        controls.append({
            'control_id': current_control_id,
            'control_name': current_control_name,
            'domain': current_domain['name'] if current_domain else 'Unknown',
            'domain_number': current_domain['number'] if current_domain else 0,
            'priority': current_priority,
            'page': page_num,
            'specifications_count': len(current_specs)
        })
    
    return controls

def extract_specifications_by_priority(pdf_path):
    """Extract all specifications grouped by priority"""
    all_specs = {'P1': [], 'P2': [], 'P3': []}
    current_domain = None
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line_clean = line.strip()
                
                # Detect domain
                domain_match = re.search(r'^9\.(\d+)\.\s+(.+?)\s+Domain', line_clean, re.IGNORECASE)
                if domain_match:
                    current_domain = domain_match.group(2).strip()
                    continue
                
                # Look for specification with priority (format: DG.1.1 Specification text P1)
                spec_match = re.search(r'^([A-Z]{2})\.(\d+)\.(\d+)\s+(.+?)\s+(P[123])\s*$', line_clean)
                if spec_match:
                    domain_code = spec_match.group(1)
                    control_num = spec_match.group(2)
                    spec_num = spec_match.group(3)
                    spec_text = spec_match.group(4).strip()
                    priority = spec_match.group(5)
                    
                    spec_id = f"{domain_code}.{control_num}.{spec_num}"
                    control_id = f"{domain_code}.{control_num}"
                    
                    spec_info = {
                        'spec_id': spec_id,
                        'control_id': control_id,
                        'text': spec_text,
                        'priority': priority,
                        'domain': current_domain or 'Unknown',
                        'page': page_num
                    }
                    
                    all_specs[priority].append(spec_info)
                
                # Also check for priority on previous line
                if i > 0 and line_clean in ['P1', 'P2', 'P3']:
                    # Check previous line for specification
                    prev_line = lines[i-1].strip() if i > 0 else ''
                    spec_match_prev = re.search(r'^([A-Z]{2})\.(\d+)\.(\d+)\s+(.+)', prev_line)
                    if spec_match_prev:
                        domain_code = spec_match_prev.group(1)
                        control_num = spec_match_prev.group(2)
                        spec_num = spec_match_prev.group(3)
                        spec_text = spec_match_prev.group(4).strip()
                        priority = line_clean
                        
                        spec_id = f"{domain_code}.{control_num}.{spec_num}"
                        control_id = f"{domain_code}.{control_num}"
                        
                        spec_info = {
                            'spec_id': spec_id,
                            'control_id': control_id,
                            'text': spec_text,
                            'priority': priority,
                            'domain': current_domain or 'Unknown',
                            'page': page_num
                        }
                        
                        if priority in all_specs:
                            all_specs[priority].append(spec_info)
    
    return all_specs

if __name__ == "__main__":
    pdf_path = "PoliciesEn001 (1).pdf"
    print("Extracting all controls and specifications from PDF...\n")
    
    # Extract specifications by priority
    specs_by_priority = extract_specifications_by_priority(pdf_path)
    
    p1_count = len(specs_by_priority['P1'])
    p2_count = len(specs_by_priority['P2'])
    p3_count = len(specs_by_priority['P3'])
    total_specs = p1_count + p2_count + p3_count
    
    print(f"Total Specifications Found: {total_specs}")
    print(f"  P1 Specifications: {p1_count}")
    print(f"  P2 Specifications: {p2_count}")
    print(f"  P3 Specifications: {p3_count}\n")
    
    # Get unique controls
    all_control_ids = set()
    for priority in ['P1', 'P2', 'P3']:
        for spec in specs_by_priority[priority]:
            all_control_ids.add(spec['control_id'])
    
    print(f"Unique Controls Found: {len(all_control_ids)}\n")
    
    # Show sample
    print("Sample P1 Specifications (first 10):")
    for i, spec in enumerate(specs_by_priority['P1'][:10], 1):
        print(f"{i}. {spec['spec_id']}: {spec['text'][:60]}...")
    
    # Save to JSON
    output = {
        'total_specifications': total_specs,
        'p1_count': p1_count,
        'p2_count': p2_count,
        'p3_count': p3_count,
        'unique_controls': len(all_control_ids),
        'specifications': specs_by_priority
    }
    
    with open('all_controls_extracted.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nFull extraction saved to all_controls_extracted.json")
    print(f"\nNote: The PDF contains {total_specs} specifications across {len(all_control_ids)} controls")


