"""
Script to extract controls from PDF file
"""
import pdfplumber
import re
import json

def extract_controls_from_pdf(pdf_path):
    """Extract controls from PDF file"""
    controls = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                # Look for control patterns (e.g., P1, P2, P3 or control IDs)
                # Adjust pattern based on actual PDF structure
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    # Try to identify control patterns
                    # This is a template - adjust based on actual PDF format
                    if re.search(r'P[123]|Control|DG-|DC-|DQ-|DP-|DR-|DL-|CR-|DS-', line, re.IGNORECASE):
                        controls.append({
                            'page': page_num,
                            'line': i + 1,
                            'text': line.strip()
                        })
    
    return controls

if __name__ == "__main__":
    pdf_path = "PoliciesEn001 (1).pdf"
    print(f"Extracting controls from {pdf_path}...")
    
    controls = extract_controls_from_pdf(pdf_path)
    
    print(f"\nFound {len(controls)} potential control references")
    print("\nFirst 20 entries:")
    for ctrl in controls[:20]:
        print(f"Page {ctrl['page']}, Line {ctrl['line']}: {ctrl['text']}")
    
    # Save to JSON for review
    with open('extracted_controls.json', 'w', encoding='utf-8') as f:
        json.dump(controls, f, indent=2, ensure_ascii=False)
    
    print(f"\nFull extraction saved to extracted_controls.json")


