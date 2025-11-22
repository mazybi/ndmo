"""
Rebuild the entire system from SANS Excel file
Analyze all sheets and rebuild data structure
"""
import pandas as pd
import json
import os
from datetime import datetime

def analyze_all_sheets(excel_path):
    """Analyze all sheets in the Excel file"""
    
    print("=" * 80)
    print("COMPLETE ANALYSIS OF SANS EXCEL FILE")
    print("=" * 80)
    
    excel_file = pd.ExcelFile(excel_path)
    sheet_names = excel_file.sheet_names
    
    print(f"\n📊 Total Sheets: {len(sheet_names)}")
    print(f"Sheets: {', '.join(sheet_names)}\n")
    
    all_sheets_data = {}
    
    for sheet_name in sheet_names:
        print(f"\n{'='*80}")
        print(f"📄 Analyzing Sheet: {sheet_name}")
        print(f"{'='*80}")
        
        try:
            # Try reading with different header positions
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
            
            print(f"  Total Rows: {len(df)}")
            print(f"  Total Columns: {len(df.columns)}")
            
            # Find header row
            header_row = None
            for i in range(min(5, len(df))):
                row_values = df.iloc[i].values
                non_null_count = sum(1 for v in row_values if pd.notna(v) and str(v).strip())
                if non_null_count > len(df.columns) * 0.5:  # More than 50% filled
                    header_row = i
                    break
            
            if header_row is not None:
                print(f"  Header Row: {header_row}")
                # Read with proper header
                df_with_header = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row)
                print(f"  Columns: {', '.join([str(c) for c in df_with_header.columns[:10]])}")
                if len(df_with_header.columns) > 10:
                    print(f"  ... and {len(df_with_header.columns) - 10} more columns")
                
                # Show sample data
                print(f"\n  Sample Data (first 3 rows):")
                print(df_with_header.head(3).to_string(max_cols=5))
                
                all_sheets_data[sheet_name] = {
                    'header_row': header_row,
                    'columns': df_with_header.columns.tolist(),
                    'row_count': len(df_with_header),
                    'sample_data': df_with_header.head(5).to_dict('records')
                }
            else:
                print(f"  No clear header found, showing raw data:")
                print(df.head(3).to_string(max_cols=5))
                all_sheets_data[sheet_name] = {
                    'header_row': None,
                    'columns': [f'Col_{i}' for i in range(len(df.columns))],
                    'row_count': len(df),
                    'sample_data': df.head(5).to_dict('records')
                }
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            all_sheets_data[sheet_name] = {'error': str(e)}
    
    return all_sheets_data

if __name__ == "__main__":
    excel_file = "SANS - NDI  NDMO Assessment Tool_(Data Management).xlsx"
    result = analyze_all_sheets(excel_file)
    
    # Save analysis
    os.makedirs("analysis", exist_ok=True)
    with open("analysis/sheets_analysis.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n✅ Analysis saved to: analysis/sheets_analysis.json")


