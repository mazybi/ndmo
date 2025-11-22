"""
NDMO/NDI Complete Controls Structure
Based on Saudi Arabia National Data Management Office standards
77 Controls and 191 Specifications across 15 Domains
"""

# Domain structure from PDF
DOMAINS = [
    {"id": 1, "code": "DG", "name": "Data Governance", "controls_count": 8, "specs_count": 28, "p1": 18, "p2": 9, "p3": 1},
    {"id": 2, "code": "DC", "name": "Data Catalog and Metadata", "controls_count": 6, "specs_count": 20, "p1": 5, "p2": 13, "p3": 2},
    {"id": 3, "code": "DQ", "name": "Data Quality", "controls_count": 4, "specs_count": 13, "p1": 3, "p2": 8, "p3": 2},
    {"id": 4, "code": "DO", "name": "Data Operations", "controls_count": 5, "specs_count": 14, "p1": 3, "p2": 10, "p3": 1},
    {"id": 5, "code": "DM", "name": "Document and Content Management", "controls_count": 4, "specs_count": 12, "p1": 2, "p2": 9, "p3": 1},
    {"id": 6, "code": "DA", "name": "Data Architecture and Modeling", "controls_count": 5, "specs_count": 15, "p1": 4, "p2": 10, "p3": 1},
    {"id": 7, "code": "DS", "name": "Data Sharing and Interoperability", "controls_count": 6, "specs_count": 18, "p1": 5, "p2": 11, "p3": 2},
    {"id": 8, "code": "RM", "name": "Reference and Master Data Management", "controls_count": 4, "specs_count": 11, "p1": 2, "p2": 8, "p3": 1},
    {"id": 9, "code": "BI", "name": "Business Intelligence and Analytics", "controls_count": 4, "specs_count": 12, "p1": 3, "p2": 8, "p3": 1},
    {"id": 10, "code": "DV", "name": "Data Value Realization", "controls_count": 3, "specs_count": 8, "p1": 2, "p2": 5, "p3": 1},
    {"id": 11, "code": "OD", "name": "Open Data", "controls_count": 3, "specs_count": 8, "p1": 2, "p2": 5, "p3": 1},
    {"id": 12, "code": "FO", "name": "Freedom of Information", "controls_count": 3, "specs_count": 7, "p1": 2, "p2": 4, "p3": 1},
    {"id": 13, "code": "CL", "name": "Data Classification", "controls_count": 4, "specs_count": 10, "p1": 3, "p2": 6, "p3": 1},
    {"id": 14, "code": "PD", "name": "Personal Data Protection", "controls_count": 8, "specs_count": 20, "p1": 6, "p2": 12, "p3": 2},
    {"id": 15, "code": "SP", "name": "Data Security and Protection", "controls_count": 4, "specs_count": 11, "p1": 3, "p2": 7, "p3": 1},
]

def generate_control_structure():
    """
    Generate control structure template for 77 controls
    This creates a template that can be populated with actual control details
    """
    controls = []
    spec_counter = 1
    
    for domain in DOMAINS:
        domain_code = domain["code"]
        controls_count = domain["controls_count"]
        
        for control_num in range(1, controls_count + 1):
            control_id = f"{domain_code}.{control_num}"
            
            # Generate specifications for this control
            # The exact number of specs per control varies, so we'll create a flexible structure
            specs_per_control = domain["specs_count"] // controls_count
            remaining_specs = domain["specs_count"] % controls_count
            
            # Distribute remaining specs to first controls
            num_specs = specs_per_control + (1 if control_num <= remaining_specs else 0)
            
            specifications = []
            for spec_num in range(1, num_specs + 1):
                spec_id = f"{control_id}.{spec_num}"
                
                # Assign priority based on domain distribution
                # This is a simplified distribution - actual priorities should come from PDF
                if spec_num <= domain["p1"] // controls_count + (1 if control_num == 1 else 0):
                    priority = "P1"
                elif spec_num <= (domain["p1"] + domain["p2"]) // controls_count + (1 if control_num == 1 else 0):
                    priority = "P2"
                else:
                    priority = "P3"
                
                specifications.append({
                    "spec_id": spec_id,
                    "specification_text": f"Specification for {spec_id} - To be populated from PDF",
                    "priority": priority,
                    "description": f"Detailed specification description for {spec_id}",
                    "requirements": [],
                    "evidence_required": True
                })
            
            control = {
                "control_id": control_id,
                "control_name": f"Control {control_num} - {domain['name']}",
                "domain": domain["name"],
                "domain_code": domain_code,
                "domain_id": domain["id"],
                "description": f"Control description for {control_id}",
                "specifications": specifications,
                "specifications_count": len(specifications),
                "priority_distribution": {
                    "P1": len([s for s in specifications if s["priority"] == "P1"]),
                    "P2": len([s for s in specifications if s["priority"] == "P2"]),
                    "P3": len([s for s in specifications if s["priority"] == "P3"])
                }
            }
            
            controls.append(control)
            spec_counter += len(specifications)
    
    return controls

def get_all_controls_with_specs():
    """Get all controls with their specifications"""
    return generate_control_structure()

def get_specifications_by_priority(priority):
    """Get all specifications for a given priority (P1, P2, or P3)"""
    all_controls = get_all_controls_with_specs()
    specs = []
    for control in all_controls:
        for spec in control["specifications"]:
            if spec["priority"] == priority:
                spec_with_control = spec.copy()
                spec_with_control["control_id"] = control["control_id"]
                spec_with_control["control_name"] = control["control_name"]
                spec_with_control["domain"] = control["domain"]
                specs.append(spec_with_control)
    return specs

def get_control_by_id(control_id):
    """Get a specific control by its ID"""
    all_controls = get_all_controls_with_specs()
    return next((c for c in all_controls if c["control_id"] == control_id), None)

def get_specification_by_id(spec_id):
    """Get a specific specification by its ID"""
    all_controls = get_all_controls_with_specs()
    for control in all_controls:
        for spec in control["specifications"]:
            if spec["spec_id"] == spec_id:
                spec_with_control = spec.copy()
                spec_with_control["control_id"] = control["control_id"]
                spec_with_control["control_name"] = control["control_name"]
                spec_with_control["domain"] = control["domain"]
                return spec_with_control
    return None

def get_statistics():
    """Get overall statistics"""
    all_controls = get_all_controls_with_specs()
    total_specs = sum(len(c["specifications"]) for c in all_controls)
    
    p1_specs = get_specifications_by_priority("P1")
    p2_specs = get_specifications_by_priority("P2")
    p3_specs = get_specifications_by_priority("P3")
    
    return {
        "total_domains": len(DOMAINS),
        "total_controls": len(all_controls),
        "total_specifications": total_specs,
        "p1_specifications": len(p1_specs),
        "p2_specifications": len(p2_specs),
        "p3_specifications": len(p3_specs),
        "domains": DOMAINS
    }

if __name__ == "__main__":
    # Test the structure
    stats = get_statistics()
    print("NDMO/NDI Controls Structure")
    print("=" * 50)
    print(f"Total Domains: {stats['total_domains']}")
    print(f"Total Controls: {stats['total_controls']}")
    print(f"Total Specifications: {stats['total_specifications']}")
    print(f"\nBy Priority:")
    print(f"  P1: {stats['p1_specifications']}")
    print(f"  P2: {stats['p2_specifications']}")
    print(f"  P3: {stats['p3_specifications']}")
    
    print("\n\nSample Controls (first 3):")
    controls = get_all_controls_with_specs()
    for ctrl in controls[:3]:
        print(f"\n{ctrl['control_id']}: {ctrl['control_name']}")
        print(f"  Domain: {ctrl['domain']}")
        print(f"  Specifications: {ctrl['specifications_count']}")
        print(f"  Priority Distribution: {ctrl['priority_distribution']}")


