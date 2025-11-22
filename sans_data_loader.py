"""
Load SANS system data (Controls, Specifications, Evidence, Calculations, Maturity)
"""
import json
import glob
import os

def load_sans_system():
    """Load the complete SANS system data"""
    try:
        # Find most recent complete system file
        complete_files = glob.glob("imported_data/complete_sans_system_*.json")
        if complete_files:
            latest_file = sorted(complete_files)[-1]
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading SANS system: {e}")
    return None

def get_all_specifications():
    """Get all specifications from SANS system"""
    system_data = load_sans_system()
    if system_data and system_data.get('specifications'):
        return system_data['specifications']
    return []

def get_evidence_by_spec(spec_id):
    """Get evidence for a specific specification"""
    system_data = load_sans_system()
    if system_data and system_data.get('evidence'):
        return system_data['evidence'].get(spec_id, [])
    return []

def get_calculations():
    """Get calculation data"""
    system_data = load_sans_system()
    if system_data and system_data.get('calculations'):
        return system_data['calculations']
    return {}

def get_maturity_questions():
    """Get maturity questions"""
    system_data = load_sans_system()
    if system_data and system_data.get('maturity_questions'):
        return system_data['maturity_questions']
    return []

def get_statistics():
    """Get system statistics"""
    system_data = load_sans_system()
    if system_data and system_data.get('statistics'):
        return system_data['statistics']
    return {}


