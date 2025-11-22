"""
Test script for NDMO Compliance Dashboard
Tests all major components
"""
import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    try:
        import streamlit
        import pandas
        import plotly
        from reportlab.lib.pagesizes import A4
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_data_models():
    """Test data models"""
    print("\nTesting data models...")
    try:
        from data_models import (
            get_all_controls,
            get_phases,
            get_documents_by_control,
            get_evidence_requirements,
            calculate_compliance_score
        )
        
        controls = get_all_controls()
        phases = get_phases()
        
        assert len(controls) > 0, "No controls found"
        assert len(phases) == 4, "Should have 4 phases"
        
        print(f"✓ Controls loaded: {len(controls)}")
        print(f"✓ Phases loaded: {len(phases)}")
        
        # Test compliance score calculation
        test_data = {controls[0]['id']: {'score': 100, 'status': 'Compliant'}}
        score = calculate_compliance_score(test_data, controls)
        assert score >= 0 and score <= 100, "Score should be between 0 and 100"
        print(f"✓ Compliance score calculation works: {score:.1f}%")
        
        return True
    except Exception as e:
        print(f"✗ Data models error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates_generator():
    """Test templates generator"""
    print("\nTesting templates generator...")
    try:
        from templates_generator import (
            create_evidence_template,
            create_compliance_report_template,
            create_audit_checklist_template
        )
        
        # Test evidence template
        test_file = create_evidence_template(
            "DG-001",
            "Test Control",
            "DG.1.1",
            "Test specification",
            "P1"
        )
        assert os.path.exists(test_file), f"Template file not created: {test_file}"
        print(f"✓ Evidence template created: {test_file}")
        
        # Test compliance report
        report_file = create_compliance_report_template(
            "Data Governance",
            "DG-001",
            "Test Control"
        )
        assert os.path.exists(report_file), f"Report file not created: {report_file}"
        print(f"✓ Compliance report created: {report_file}")
        
        # Test audit checklist
        checklist_file = create_audit_checklist_template(
            "DG-001",
            "Test Control"
        )
        assert os.path.exists(checklist_file), f"Checklist file not created: {checklist_file}"
        print(f"✓ Audit checklist created: {checklist_file}")
        
        return True
    except Exception as e:
        print(f"✗ Templates generator error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ndmo_structure():
    """Test NDMO controls structure"""
    print("\nTesting NDMO controls structure...")
    try:
        from ndmo_controls_structure import (
            get_all_controls_with_specs,
            get_specifications_by_priority,
            get_statistics,
            DOMAINS
        )
        
        assert len(DOMAINS) == 15, "Should have 15 domains"
        print(f"✓ Domains loaded: {len(DOMAINS)}")
        
        stats = get_statistics()
        assert stats['total_domains'] == 15, "Should have 15 domains"
        print(f"✓ Statistics: {stats['total_controls']} controls, {stats['total_specifications']} specifications")
        
        p1_specs = get_specifications_by_priority("P1")
        p2_specs = get_specifications_by_priority("P2")
        p3_specs = get_specifications_by_priority("P3")
        
        print(f"✓ P1 specs: {len(p1_specs)}, P2 specs: {len(p2_specs)}, P3 specs: {len(p3_specs)}")
        
        return True
    except Exception as e:
        print(f"✗ NDMO structure error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test file structure"""
    print("\nTesting file structure...")
    required_files = [
        'app.py',
        'data_models.py',
        'templates_generator.py',
        'ndmo_controls_structure.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✓ All required files present")
        return True

def test_templates_directory():
    """Test templates directory"""
    print("\nTesting templates directory...")
    if os.path.exists('templates'):
        files = [f for f in os.listdir('templates') if f.endswith('.pdf')]
        print(f"✓ Templates directory exists with {len(files)} PDF files")
        return True
    else:
        print("⚠ Templates directory doesn't exist (will be created on first use)")
        return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("NDMO Compliance Dashboard - Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("File Structure", test_file_structure()))
    results.append(("Data Models", test_data_models()))
    results.append(("Templates Generator", test_templates_generator()))
    results.append(("NDMO Structure", test_ndmo_structure()))
    results.append(("Templates Directory", test_templates_directory()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The application is ready to use.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())


