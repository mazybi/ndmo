"""
Explore Excel file structure and extract all data
"""
import pandas as pd
import json
from datetime import datetime

def explore_excel_file(excel_path):
    """Explore Excel file structure completely"""
    
    print("=" * 80)
    print(f"Exploring Excel File: {excel_path}")
    print("=" * 80)
    
    try:
        excel_file = pd.ExcelFile(excel_path)
        sheet_names = excel_file.sheet_names
        
        print(f"\n📊 Total Sheets: {len(sheet_names)}")
        print(f"Sheets: {', '.join(sheet_names)}")
        print("\n" + "=" * 80)
        
        all_data = {}
        statistics = {
            'total_sheets': len(sheet_names),
            'total_controls': 0,
            'total_specifications': 0,
            'total_evidence': 0,
            'sheets_info': []
        }
        
        for sheet_name in sheet_names:
            print(f"\n📄 Sheet: {sheet_name}")
            print("-" * 80)
            
            try:
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                
                print(f"  Rows: {len(df)}")
                print(f"  Columns: {len(df.columns)}")
                print(f"  Column Names:")
                for i, col in enumerate(df.columns, 1):
                    print(f"    {i}. {col}")
                
                # Show first few rows
                print(f"\n  First 3 rows (sample):")
                print(df.head(3).to_string())
                
                # Analyze data
                sheet_info = {
                    'name': sheet_name,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': df.columns.tolist(),
                    'sample_data': df.head(5).to_dict('records')
                }
                
                # Try to identify what this sheet contains
                sheet_lower = sheet_name.lower()
                col_names_lower = [str(col).lower() for col in df.columns]
                
                # Check for controls
                if any(keyword in sheet_lower or any(keyword in col for col in col_names_lower) 
                       for keyword in ['control', 'كنترول', 'control id', 'control_id']):
                    controls_count = len(df)
                    statistics['total_controls'] += controls_count
                    sheet_info['type'] = 'Controls'
                    sheet_info['count'] = controls_count
                    print(f"\n  ✓ Identified as: Controls Sheet ({controls_count} controls)")
                
                # Check for specifications
                elif any(keyword in sheet_lower or any(keyword in col for col in col_names_lower) 
                        for keyword in ['spec', 'مواصفة', 'specification', 'spec id', 'spec_id']):
                    specs_count = len(df)
                    statistics['total_specifications'] += specs_count
                    sheet_info['type'] = 'Specifications'
                    sheet_info['count'] = specs_count
                    print(f"\n  ✓ Identified as: Specifications Sheet ({specs_count} specifications)")
                
                # Check for evidence
                elif any(keyword in sheet_lower or any(keyword in col for col in col_names_lower) 
                        for keyword in ['evidence', 'أدلة', 'proof', 'document', 'doc']):
                    evidence_count = len(df)
                    statistics['total_evidence'] += evidence_count
                    sheet_info['type'] = 'Evidence'
                    sheet_info['count'] = evidence_count
                    print(f"\n  ✓ Identified as: Evidence Sheet ({evidence_count} evidence items)")
                
                else:
                    sheet_info['type'] = 'Unknown'
                    print(f"\n  ? Type: Unknown (needs manual review)")
                
                all_data[sheet_name] = {
                    'dataframe': df,
                    'info': sheet_info
                }
                
                statistics['sheets_info'].append(sheet_info)
                
            except Exception as e:
                print(f"  ❌ Error reading sheet: {str(e)}")
                all_data[sheet_name] = {'error': str(e)}
        
        print("\n" + "=" * 80)
        print("📈 SUMMARY STATISTICS")
        print("=" * 80)
        print(f"Total Sheets: {statistics['total_sheets']}")
        print(f"Total Controls: {statistics['total_controls']}")
        print(f"Total Specifications: {statistics['total_specifications']}")
        print(f"Total Evidence Items: {statistics['total_evidence']}")
        
        # Save exploration results
        output = {
            'file_path': excel_path,
            'exploration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'statistics': statistics,
            'sheets_data': {}
        }
        
        # Save sheet data (without full dataframes to keep JSON small)
        for sheet_name, sheet_data in all_data.items():
            if 'dataframe' in sheet_data:
                df = sheet_data['dataframe']
                output['sheets_data'][sheet_name] = {
                    'info': sheet_data['info'],
                    'sample_rows': df.head(10).to_dict('records'),
                    'all_columns': df.columns.tolist()
                }
            else:
                output['sheets_data'][sheet_name] = sheet_data
        
        # Save to JSON
        import os
        os.makedirs("exploration_results", exist_ok=True)
        output_file = f"exploration_results/exploration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✅ Exploration results saved to: {output_file}")
        
        return all_data, statistics
        
    except Exception as e:
        print(f"❌ Error exploring Excel file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    excel_file = "SANS - NDI  NDMO Assessment Tool_(Data Management).xlsx"
    explore_excel_file(excel_file)


