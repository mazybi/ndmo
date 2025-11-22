"""
Generate NDMO Evidence Templates and Forms
Creates standardized templates for evidence collection
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

def create_evidence_template(control_id, control_name, spec_id, spec_text, priority, template_type="Evidence Collection"):
    """Create a fillable evidence template for a specification"""
    
    # Create directory if it doesn't exist
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Evidence_{spec_id.replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("NDMO/NDI Evidence Collection Form", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Control Information
    story.append(Paragraph("Control Information", heading_style))
    
    control_data = [
        ['Control ID:', control_id],
        ['Control Name:', control_name],
        ['Specification ID:', spec_id],
        ['Priority:', priority],
        ['Date:', datetime.now().strftime("%Y-%m-%d")]
    ]
    
    control_table = Table(control_data, colWidths=[2*inch, 5*inch])
    control_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(control_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Specification Details
    story.append(Paragraph("Specification Details", heading_style))
    story.append(Paragraph(f"<b>Specification:</b> {spec_text}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Evidence Collection Section
    story.append(Paragraph("Evidence Collection", heading_style))
    
    evidence_fields = [
        ['Evidence Type:', '_________________________________'],
        ['Evidence Description:', ''],
        ['', ''],
        ['File Name:', '_________________________________'],
        ['File Location/Path:', '_________________________________'],
        ['Upload Date:', '_________________________________'],
        ['Uploaded By:', '_________________________________'],
        ['Approved By:', '_________________________________'],
        ['Approval Date:', '_________________________________']
    ]
    
    evidence_table = Table(evidence_fields, colWidths=[2*inch, 5*inch])
    evidence_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (1, 2), (1, 2), 'TOP')
    ]))
    story.append(evidence_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Compliance Status
    story.append(Paragraph("Compliance Status", heading_style))
    
    status_data = [
        ['Compliance Status:', '☐ Compliant  ☐ Partially Compliant  ☐ Non-Compliant'],
        ['Compliance Score (%):', '_________________________________'],
        ['Implementation Date:', '_________________________________'],
        ['Review Date:', '_________________________________'],
        ['Next Review Date:', '_________________________________']
    ]
    
    status_table = Table(status_data, colWidths=[2*inch, 5*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(status_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Notes Section
    story.append(Paragraph("Notes and Comments", heading_style))
    notes_data = [
        ['Notes:', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', '']
    ]
    
    notes_table = Table(notes_data, colWidths=[7*inch])
    notes_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(notes_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Signatures
    story.append(Paragraph("Signatures", heading_style))
    signature_data = [
        ['Prepared By:', '_________________________', 'Date:', '_________________________'],
        ['Reviewed By:', '_________________________', 'Date:', '_________________________'],
        ['Approved By:', '_________________________', 'Date:', '_________________________']
    ]
    
    sig_table = Table(signature_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    sig_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(sig_table)
    
    # Build PDF
    doc.build(story)
    return filename

def create_compliance_report_template(domain_name, control_id, control_name):
    """Create a compliance report template for a control"""
    
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Compliance_Report_{control_id.replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("NDMO/NDI Compliance Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report Information
    story.append(Paragraph("Report Information", heading_style))
    
    report_data = [
        ['Domain:', domain_name],
        ['Control ID:', control_id],
        ['Control Name:', control_name],
        ['Report Period:', 'From: ___________  To: ___________'],
        ['Report Date:', datetime.now().strftime("%Y-%m-%d")],
        ['Entity Name:', '_________________________________'],
        ['Prepared By:', '_________________________________']
    ]
    
    report_table = Table(report_data, colWidths=[2*inch, 5*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(report_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Compliance Summary
    story.append(Paragraph("Compliance Summary", heading_style))
    
    summary_data = [
        ['Overall Compliance Status:', '☐ Compliant  ☐ Partially Compliant  ☐ Non-Compliant'],
        ['Overall Compliance Score:', '___________ %'],
        ['Total Specifications:', '___________'],
        ['Compliant Specifications:', '___________'],
        ['Partially Compliant:', '___________'],
        ['Non-Compliant:', '___________']
    ]
    
    summary_table = Table(summary_data, colWidths=[2.5*inch, 4.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Specifications Details
    story.append(Paragraph("Specifications Compliance Details", heading_style))
    story.append(Paragraph("(List all specifications for this control)", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    spec_headers = ['Spec ID', 'Priority', 'Status', 'Score %', 'Evidence']
    spec_data = [
        spec_headers,
        ['________', 'P1/P2/P3', '☐ C ☐ PC ☐ NC', '____', '☐ Yes ☐ No'],
        ['________', 'P1/P2/P3', '☐ C ☐ PC ☐ NC', '____', '☐ Yes ☐ No'],
        ['________', 'P1/P2/P3', '☐ C ☐ PC ☐ NC', '____', '☐ Yes ☐ No'],
        ['________', 'P1/P2/P3', '☐ C ☐ PC ☐ NC', '____', '☐ Yes ☐ No'],
        ['________', 'P1/P2/P3', '☐ C ☐ PC ☐ NC', '____', '☐ Yes ☐ No']
    ]
    
    spec_table = Table(spec_data, colWidths=[1.2*inch, 1*inch, 1.5*inch, 1*inch, 1.3*inch])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(spec_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Findings and Recommendations
    story.append(Paragraph("Findings and Recommendations", heading_style))
    
    findings_data = [
        ['Key Findings:', ''],
        ['', ''],
        ['', ''],
        ['Recommendations:', ''],
        ['', ''],
        ['', ''],
        ['Action Items:', ''],
        ['', ''],
        ['', '']
    ]
    
    findings_table = Table(findings_data, colWidths=[2*inch, 5*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#ecf0f1')),
        ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#ecf0f1')),
        ('BACKGROUND', (0, 6), (0, 6), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
        ('FONTNAME', (0, 6), (0, 6), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(findings_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Signatures
    story.append(Paragraph("Approval", heading_style))
    signature_data = [
        ['Prepared By:', '_________________________', 'Date:', '_________________________'],
        ['Reviewed By:', '_________________________', 'Date:', '_________________________'],
        ['Approved By:', '_________________________', 'Date:', '_________________________']
    ]
    
    sig_table = Table(signature_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    sig_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(sig_table)
    
    doc.build(story)
    return filename

def create_audit_checklist_template(control_id, control_name):
    """Create an audit checklist template"""
    
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Audit_Checklist_{control_id.replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("NDMO/NDI Audit Checklist", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Control Information
    story.append(Paragraph("Control Information", heading_style))
    
    control_data = [
        ['Control ID:', control_id],
        ['Control Name:', control_name],
        ['Audit Date:', '_________________________________'],
        ['Auditor Name:', '_________________________________'],
        ['Entity Name:', '_________________________________']
    ]
    
    control_table = Table(control_data, colWidths=[2*inch, 5*inch])
    control_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(control_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Checklist Items
    story.append(Paragraph("Audit Checklist", heading_style))
    
    checklist_headers = ['#', 'Check Item', 'Yes', 'No', 'N/A', 'Notes']
    checklist_data = [
        checklist_headers,
        ['1', 'Policy documented and approved', '☐', '☐', '☐', ''],
        ['2', 'Procedures implemented', '☐', '☐', '☐', ''],
        ['3', 'Roles and responsibilities defined', '☐', '☐', '☐', ''],
        ['4', 'Training conducted', '☐', '☐', '☐', ''],
        ['5', 'Evidence available', '☐', '☐', '☐', ''],
        ['6', 'Monitoring in place', '☐', '☐', '☐', ''],
        ['7', 'Compliance verified', '☐', '☐', '☐', ''],
        ['8', 'Documentation complete', '☐', '☐', '☐', ''],
        ['9', 'Review conducted', '☐', '☐', '☐', ''],
        ['10', 'Improvements identified', '☐', '☐', '☐', '']
    ]
    
    checklist_table = Table(checklist_data, colWidths=[0.5*inch, 3*inch, 0.6*inch, 0.6*inch, 0.6*inch, 1.7*inch])
    checklist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(checklist_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Audit Findings
    story.append(Paragraph("Audit Findings", heading_style))
    
    findings_data = [
        ['Findings:', ''],
        ['', ''],
        ['', ''],
        ['Recommendations:', ''],
        ['', ''],
        ['', '']
    ]
    
    findings_table = Table(findings_data, colWidths=[2*inch, 5*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#ecf0f1')),
        ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(findings_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Signatures
    story.append(Paragraph("Signatures", heading_style))
    signature_data = [
        ['Auditor:', '_________________________', 'Date:', '_________________________'],
        ['Reviewed By:', '_________________________', 'Date:', '_________________________'],
        ['Approved By:', '_________________________', 'Date:', '_________________________']
    ]
    
    sig_table = Table(signature_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    sig_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(sig_table)
    
    doc.build(story)
    return filename

def generate_all_templates():
    """Generate templates for all controls"""
    try:
        from ndmo_controls_structure import get_all_controls_with_specs
        
        all_controls = get_all_controls_with_specs()
        generated_files = []
        
        for control in all_controls[:5]:  # Generate for first 5 controls as example
            # Generate compliance report
            report_file = create_compliance_report_template(
                control['domain'],
                control['control_id'],
                control['control_name']
            )
            generated_files.append(report_file)
            
            # Generate audit checklist
            checklist_file = create_audit_checklist_template(
                control['control_id'],
                control['control_name']
            )
            generated_files.append(checklist_file)
            
            # Generate evidence templates for each specification
            for spec in control['specifications'][:2]:  # First 2 specs as example
                evidence_file = create_evidence_template(
                    control['control_id'],
                    control['control_name'],
                    spec['spec_id'],
                    spec.get('specification_text', spec.get('text', '')),
                    spec['priority']
                )
                generated_files.append(evidence_file)
        
        return generated_files
    except Exception as e:
        print(f"Error generating templates: {e}")
        return []

if __name__ == "__main__":
    print("Generating NDMO templates...")
    files = generate_all_templates()
    print(f"\nGenerated {len(files)} template files in 'templates' directory")


