"""
Find all controls with P1, P2, P3 priorities
"""
import pdfplumber
import re
import json

def find_controls(pdf_path):
    """Find all controls in PDF"""
    controls = []
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
                
                # Detect domain headers (9.1, 9.2, etc.)
                domain_match = re.search(r'^9\.(\d+)\.\s+(.+?)\s+Domain', line_clean, re.IGNORECASE)
                if domain_match:
                    current_domain = {
                        'number': domain_match.group(1),
                        'name': domain_match.group(2),
                        'page': page_num
                    }
                    continue
                
                # Look for control patterns - try different formats
                # Pattern 1: Control ID like "DG-001" or similar
                control_id_match = re.search(r'([A-Z]{2,3}-\d{3,4})', line_clean)
                
                # Pattern 2: Look for P1, P2, P3
                priority_match = re.search(r'\b(P[123])\b', line_clean, re.IGNORECASE)
                
                # Pattern 3: Look for "Control" keyword with numbers
                control_num_match = re.search(r'Control\s+(\d+)', line_clean, re.IGNORECASE)
                
                if control_id_match or priority_match or control_num_match:
                    control_info = {
                        'page': page_num,
                        'line': i + 1,
                        'text': line_clean,
                        'domain': current_domain['name'] if current_domain else 'Unknown'
                    }
                    
                    if control_id_match:
                        control_info['control_id'] = control_id_match.group(1)
                    if priority_match:
                        control_info['priority'] = priority_match.group(1).upper()
                    if control_num_match:
                        control_info['control_number'] = control_num_match.group(1)
                    
                    controls.append(control_info)
    
    return controls

if __name__ == "__main__":
    pdf_path = "PoliciesEn001 (1).pdf"
    print("Searching for controls in PDF...\n")
    
    controls = find_controls(pdf_path)
    
    print(f"Found {len(controls)} potential controls\n")
    
    # Group by priority
    p1_controls = [c for c in controls if c.get('priority') == 'P1']
    p2_controls = [c for c in controls if c.get('priority') == 'P2']
    p3_controls = [c for c in controls if c.get('priority') == 'P3']
    
    print(f"P1 Controls: {len(p1_controls)}")
    print(f"P2 Controls: {len(p2_controls)}")
    print(f"P3 Controls: {len(p3_controls)}")
    print(f"Without Priority: {len(controls) - len(p1_controls) - len(p2_controls) - len(p3_controls)}\n")
    
    print("\nSample controls (first 30):")
    for i, ctrl in enumerate(controls[:30], 1):
        print(f"{i}. Page {ctrl['page']}, Line {ctrl['line']}: {ctrl['text'][:80]}")
        if 'priority' in ctrl:
            print(f"   Priority: {ctrl['priority']}")
        if 'control_id' in ctrl:
            print(f"   Control ID: {ctrl['control_id']}")
        print()
    
    # Save to JSON
    with open('found_controls.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(controls),
            'p1_count': len(p1_controls),
            'p2_count': len(p2_controls),
            'p3_count': len(p3_controls),
            'controls': controls
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nFull results saved to found_controls.json")


