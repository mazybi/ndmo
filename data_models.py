"""
Data Models for NDMO/NDI Compliance System
Interface between app.py and sans_data_loader.py
"""
from sans_data_loader import (
    load_sans_system,
    get_all_specifications as get_sans_specs,
    get_evidence_by_spec,
    get_statistics as get_sans_stats
)

# Load SANS system data
SANS_DATA = load_sans_system() or {}

# Domain definitions
DOMAINS = [
    {"id": 1, "code": "DG", "name": "Data Governance", "controls_count": 8, "specs_count": 28},
    {"id": 2, "code": "DM", "name": "Data Management", "controls_count": 10, "specs_count": 35},
    {"id": 3, "code": "DS", "name": "Data Security", "controls_count": 12, "specs_count": 42},
    {"id": 4, "code": "DP", "name": "Data Privacy", "controls_count": 9, "specs_count": 32},
    {"id": 5, "code": "DQ", "name": "Data Quality", "controls_count": 7, "specs_count": 25},
    {"id": 6, "code": "DA", "name": "Data Architecture", "controls_count": 8, "specs_count": 29},
]

def get_all_controls():
    """Get all controls from SANS system"""
    if SANS_DATA and SANS_DATA.get('controls'):
        return SANS_DATA['controls']
    return []

def get_control_by_id(control_id):
    """Get a specific control by ID"""
    controls = get_all_controls()
    for control in controls:
        if control.get('id') == control_id or control.get('control_id') == control_id:
            return control
    return None

def get_all_specifications():
    """Get all specifications"""
    return get_sans_specs()

def get_specification_by_id(spec_id):
    """Get a specific specification by ID"""
    specs = get_all_specifications()
    for spec in specs:
        if spec.get('spec_id') == spec_id or spec.get('id') == spec_id:
            return spec
    return None

def get_specifications_by_priority(priority=None):
    """Get specifications filtered by priority"""
    specs = get_all_specifications()
    if priority:
        return [s for s in specs if s.get('priority') == priority]
    return specs

def get_phases():
    """Get compliance phases"""
    return [
        {
            "id": 1,
            "name": "Planning",
            "description": "Initial planning and assessment phase",
            "controls_count": 0
        },
        {
            "id": 2,
            "name": "Implementation",
            "description": "Implementation of controls and processes",
            "controls_count": 0
        },
        {
            "id": 3,
            "name": "Monitoring",
            "description": "Ongoing monitoring and review",
            "controls_count": 0
        },
        {
            "id": 4,
            "name": "Improvement",
            "description": "Continuous improvement phase",
            "controls_count": 0
        }
    ]

def get_documents_by_control(control_id):
    """Get documents required for a control"""
    control = get_control_by_id(control_id)
    if not control:
        return []
    
    # Get evidence for all specifications in this control
    specs = get_all_specifications()
    control_specs = [s for s in specs if s.get('control_id') == control_id]
    
    documents = []
    for spec in control_specs:
        evidence_list = get_evidence_by_spec(spec.get('spec_id', ''))
        for ev in evidence_list:
            doc = {
                "id": ev.get('id', ''),
                "name": ev.get('name', ev.get('type', 'Document')),
                "type": ev.get('type', 'Document'),
                "description": ev.get('description', ''),
                "required": ev.get('required', True)
            }
            if doc not in documents:
                documents.append(doc)
    
    return documents

def get_evidence_requirements(control_id, spec_id=None):
    """Get evidence requirements for a control or specification"""
    if spec_id:
        return get_evidence_by_spec(spec_id)
    
    # Get evidence for all specifications in the control
    control = get_control_by_id(control_id)
    if not control:
        return []
    
    specs = get_all_specifications()
    control_specs = [s for s in specs if s.get('control_id') == control_id]
    
    all_evidence = []
    for spec in control_specs:
        evidence_list = get_evidence_by_spec(spec.get('spec_id', ''))
        all_evidence.extend(evidence_list)
    
    return all_evidence

def calculate_compliance_score(compliance_data, controls=None):
    """Calculate overall compliance score"""
    if not compliance_data:
        return 0.0
    
    if controls is None:
        controls = get_all_controls()
    
    if not controls:
        return 0.0
    
    total_score = 0
    total_weight = 0
    
    for control in controls:
        control_id = control.get('id') or control.get('control_id')
        if control_id in compliance_data:
            control_data = compliance_data[control_id]
            score = control_data.get('score', 0)
            weight = control.get('weight', 1)
            total_score += score * weight
            total_weight += weight
    
    if total_weight == 0:
        return 0.0
    
    return round(total_score / total_weight, 2)

def get_statistics():
    """Get system statistics"""
    stats = get_sans_stats()
    if stats:
        return stats
    
    # Fallback statistics
    controls = get_all_controls()
    specs = get_all_specifications()
    
    return {
        "total_controls": len(controls),
        "total_specifications": len(specs),
        "total_evidence_items": 0,
        "domains_count": len(DOMAINS)
    }

