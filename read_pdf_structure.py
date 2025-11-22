"""
Better PDF reading to understand structure
"""
import pdfplumber
import json

def read_pdf_structure(pdf_path):
    """Read PDF and show structure"""
    all_text = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}\n")
        
        # Read first 20 pages to understand structure
        for page_num in range(min(20, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                print(f"\n{'='*80}")
                print(f"PAGE {page_num + 1}")
                print(f"{'='*80}")
                # Show first 30 lines of each page
                for i, line in enumerate(lines[:30], 1):
                    if line.strip():
                        print(f"{i:3}: {line}")
                all_text.append({
                    'page': page_num + 1,
                    'text': text
                })
    
    return all_text

if __name__ == "__main__":
    pdf_path = "PoliciesEn001 (1).pdf"
    read_pdf_structure(pdf_path)


