"""
Fillable Forms Handler for NDMO Templates
Handles form data storage and PDF generation from filled forms
"""
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

def save_form_data(form_type, control_id, spec_id, form_data):
    """Save filled form data to JSON file"""
    os.makedirs("filled_forms", exist_ok=True)
    
    filename = f"filled_forms/{form_type}_{control_id}_{spec_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    form_record = {
        "form_type": form_type,
        "control_id": control_id,
        "spec_id": spec_id,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": form_data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(form_record, f, indent=2, ensure_ascii=False)
    
    return filename

def load_form_data(form_type, control_id, spec_id):
    """Load saved form data"""
    if not os.path.exists("filled_forms"):
        return None
    
    # Find most recent form for this control/spec
    files = [f for f in os.listdir("filled_forms") if f.startswith(f"{form_type}_{control_id}_{spec_id}")]
    if not files:
        return None
    
    latest_file = sorted(files)[-1]
    with open(f"filled_forms/{latest_file}", 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_pdf_from_form(form_type, form_data, control_id, control_name, spec_id=None, spec_text=None):
    """Generate PDF from filled form data with unified design and logo"""
    os.makedirs("filled_forms_pdf", exist_ok=True)
    
    if spec_id:
        filename = f"filled_forms_pdf/{form_type}_{control_id}_{spec_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    else:
        filename = f"filled_forms_pdf/{form_type}_{control_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    doc = SimpleDocTemplate(
        filename, 
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=75,
        bottomMargin=50
    )
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=15,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#ecf0f1'),
        borderPadding=8
    )
    
    field_label_style = ParagraphStyle(
        'FieldLabel',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=14
    )
    
    normal_style = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        leading=14
    )
    
    # Classification banner
    classification = "RESTRICTED - INTERNAL"
    classification_style = ParagraphStyle(
        'ClassificationStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.white,
        alignment=TA_CENTER,
        leading=14
    )
    classification_table = Table(
        [[Paragraph(f"<b>CLASSIFICATION: {classification}</b>", classification_style)]],
        colWidths=[7.1*inch],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ])
    )
    story.append(classification_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Title
    if form_type == "evidence":
        title = "Evidence Collection Form"
    elif form_type == "compliance_report":
        title = "Compliance Report"
    else:
        title = "Audit Checklist"
    
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Control Information
    story.append(Paragraph("Control Information", heading_style))
    
    control_info = [
        [Paragraph('<b>Control ID:</b>', field_label_style), Paragraph(form_data.get('control_id', control_id), normal_style)],
        [Paragraph('<b>Control Name:</b>', field_label_style), Paragraph(form_data.get('control_name', control_name), normal_style)],
    ]
    
    if spec_id:
        control_info.extend([
            [Paragraph('<b>Specification ID:</b>', field_label_style), Paragraph(form_data.get('spec_id', spec_id), normal_style)],
            [Paragraph('<b>Priority:</b>', field_label_style), Paragraph(form_data.get('priority', 'N/A'), normal_style)],
        ])
    
    control_info.append([Paragraph('<b>Date:</b>', field_label_style), Paragraph(form_data.get('date', datetime.now().strftime("%Y-%m-%d")), normal_style)])
    
    control_table = Table(control_info, colWidths=[2.0*inch, 5.1*inch])
    control_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(control_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Form-specific content
    if form_type == "evidence":
        # Evidence details
        story.append(Paragraph("Evidence Details", heading_style))
        evidence_data = [
            [Paragraph('<b>Evidence Type:</b>', field_label_style), Paragraph(form_data.get('evidence_type', ''), normal_style)],
            [Paragraph('<b>Evidence Description:</b>', field_label_style), Paragraph(form_data.get('evidence_description', ''), normal_style)],
            [Paragraph('<b>File Name:</b>', field_label_style), Paragraph(form_data.get('file_name', ''), normal_style)],
            [Paragraph('<b>File Location:</b>', field_label_style), Paragraph(form_data.get('file_location', ''), normal_style)],
            [Paragraph('<b>Upload Date:</b>', field_label_style), Paragraph(form_data.get('upload_date', ''), normal_style)],
            [Paragraph('<b>Uploaded By:</b>', field_label_style), Paragraph(form_data.get('uploaded_by', ''), normal_style)],
        ]
        
        evidence_table = Table(evidence_data, colWidths=[2.0*inch, 5.1*inch])
        evidence_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(evidence_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Compliance Status
        story.append(Paragraph("Compliance Status", heading_style))
        status_data = [
            [Paragraph('<b>Compliance Status:</b>', field_label_style), Paragraph(form_data.get('compliance_status', ''), normal_style)],
            [Paragraph('<b>Compliance Score:</b>', field_label_style), Paragraph(f"{form_data.get('compliance_score', 0)}%", normal_style)],
            [Paragraph('<b>Implementation Date:</b>', field_label_style), Paragraph(form_data.get('implementation_date', ''), normal_style)],
        ]
        
        status_table = Table(status_data, colWidths=[2.0*inch, 5.1*inch])
        status_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(status_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Notes
        if form_data.get('notes'):
            story.append(Paragraph("Notes", heading_style))
            story.append(Paragraph(form_data.get('notes', ''), normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    elif form_type == "compliance_report":
        # Report Information
        story.append(Paragraph("Report Information", heading_style))
        report_info = [
            [Paragraph('<b>Report Date:</b>', field_label_style), Paragraph(form_data.get('report_date', ''), normal_style)],
            [Paragraph('<b>Entity Name:</b>', field_label_style), Paragraph(form_data.get('entity_name', ''), normal_style)],
            [Paragraph('<b>Report Period:</b>', field_label_style), Paragraph(f"From: {form_data.get('report_period_from', '')} To: {form_data.get('report_period_to', '')}", normal_style)],
            [Paragraph('<b>Prepared By:</b>', field_label_style), Paragraph(form_data.get('prepared_by', ''), normal_style)],
        ]
        
        report_table = Table(report_info, colWidths=[2.0*inch, 5.1*inch])
        report_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(report_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Compliance Summary
        story.append(Paragraph("Compliance Summary", heading_style))
        summary_data = [
            [Paragraph('<b>Overall Compliance Status:</b>', field_label_style), Paragraph(form_data.get('overall_status', ''), normal_style)],
            [Paragraph('<b>Overall Compliance Score:</b>', field_label_style), Paragraph(f"{form_data.get('overall_score', 0)}%", normal_style)],
            [Paragraph('<b>Total Specifications:</b>', field_label_style), Paragraph(str(form_data.get('total_specs', '')), normal_style)],
            [Paragraph('<b>Compliant Specifications:</b>', field_label_style), Paragraph(str(form_data.get('compliant_count', '')), normal_style)],
            [Paragraph('<b>Partially Compliant:</b>', field_label_style), Paragraph(str(form_data.get('partially_compliant', '')), normal_style)],
            [Paragraph('<b>Non-Compliant:</b>', field_label_style), Paragraph(str(form_data.get('non_compliant', '')), normal_style)],
            [Paragraph('<b>Not Applicable:</b>', field_label_style), Paragraph(str(form_data.get('not_applicable', '')), normal_style)],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 4.6*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Findings
        if form_data.get('key_findings'):
            story.append(Paragraph("Key Findings", heading_style))
            story.append(Paragraph(form_data.get('key_findings', ''), normal_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        if form_data.get('recommendations'):
            story.append(Paragraph("Recommendations", heading_style))
            story.append(Paragraph(form_data.get('recommendations', ''), normal_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Action Items
        if form_data.get('action_items'):
            story.append(Paragraph("Action Items", heading_style))
            story.append(Paragraph(form_data.get('action_items', ''), normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    elif form_type == "audit_checklist":
        # Audit Information
        story.append(Paragraph("Audit Information", heading_style))
        audit_info = [
            [Paragraph('<b>Audit Date:</b>', field_label_style), Paragraph(form_data.get('audit_date', ''), normal_style)],
            [Paragraph('<b>Auditor Name:</b>', field_label_style), Paragraph(form_data.get('auditor_name', ''), normal_style)],
            [Paragraph('<b>Auditor Title:</b>', field_label_style), Paragraph(form_data.get('auditor_title', ''), normal_style)],
            [Paragraph('<b>Entity Name:</b>', field_label_style), Paragraph(form_data.get('entity_name', ''), normal_style)],
            [Paragraph('<b>Audit Type:</b>', field_label_style), Paragraph(form_data.get('audit_type', ''), normal_style)],
            [Paragraph('<b>Audit Scope:</b>', field_label_style), Paragraph(form_data.get('audit_scope', ''), normal_style)],
        ]
        
        audit_table = Table(audit_info, colWidths=[2.0*inch, 5.1*inch])
        audit_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(audit_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Checklist Results
        story.append(Paragraph("Checklist Results", heading_style))
        checklist_items = [
            "Policy documented and approved",
            "Procedures implemented",
            "Roles and responsibilities defined",
            "Training conducted",
            "Evidence available",
            "Monitoring in place",
            "Compliance verified",
            "Documentation complete",
            "Review conducted",
            "Improvements identified"
        ]
        
        checklist_data = [[Paragraph('<b>#</b>', field_label_style), Paragraph('<b>Item</b>', field_label_style), Paragraph('<b>Result</b>', field_label_style), Paragraph('<b>Notes</b>', field_label_style)]]
        for i, item in enumerate(checklist_items):
            result = form_data.get(f'checklist_{i}', 'N/A')
            notes = form_data.get(f'checklist_notes_{i}', '')
            checklist_data.append([Paragraph(str(i+1), normal_style), Paragraph(item, normal_style), Paragraph(result, normal_style), Paragraph(notes, normal_style)])
        
        checklist_table = Table(checklist_data, colWidths=[0.5*inch, 3.0*inch, 1.0*inch, 2.6*inch])
        checklist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6)
        ]))
        story.append(checklist_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Findings
        if form_data.get('findings'):
            story.append(Paragraph("Audit Findings", heading_style))
            story.append(Paragraph(form_data.get('findings', ''), normal_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        if form_data.get('recommendations'):
            story.append(Paragraph("Recommendations", heading_style))
            story.append(Paragraph(form_data.get('recommendations', ''), normal_style))
            story.append(Spacer(1, 0.2*inch))
    
    # Signatures
    story.append(Paragraph("Signatures", heading_style))
    if form_type == "audit_checklist":
        signature_data = [
            ['Auditor:', form_data.get('auditor_name', ''), 'Date:', form_data.get('audit_date', '')],
            ['Reviewed By:', form_data.get('reviewed_by', ''), 'Date:', form_data.get('reviewed_date', '')],
            ['Approved By:', form_data.get('approved_by', ''), 'Date:', form_data.get('approved_date', '')],
        ]
    elif form_type == "compliance_report":
        signature_data = [
            ['Prepared By:', form_data.get('prepared_by', ''), 'Date:', form_data.get('report_date', '')],
            ['Reviewed By:', form_data.get('reviewed_by', ''), 'Date:', form_data.get('reviewed_date', '')],
            ['Approved By:', form_data.get('approved_by', ''), 'Date:', form_data.get('approved_date', '')],
        ]
    else:
        signature_data = [
            ['Prepared By:', form_data.get('prepared_by', ''), 'Date:', form_data.get('prepared_date', '')],
            ['Reviewed By:', form_data.get('reviewed_by', ''), 'Date:', form_data.get('reviewed_date', '')],
            ['Approved By:', form_data.get('approved_by', ''), 'Date:', form_data.get('approved_date', '')],
        ]
    
    sig_table = Table(signature_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    sig_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(sig_table)
    
    # Build PDF with header/footer
    logo_path = "logo@3x.png"
    
    def on_first_page(canvas, doc):
        from unified_templates import add_unified_header_footer
        add_unified_header_footer(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        from unified_templates import add_unified_header_footer
        add_unified_header_footer(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

def get_saved_forms(control_id=None, spec_id=None):
    """Get list of saved forms"""
    if not os.path.exists("filled_forms"):
        return []
    
    files = os.listdir("filled_forms")
    forms = []
    
    for file in files:
        if file.endswith('.json'):
            try:
                with open(f"filled_forms/{file}", 'r', encoding='utf-8') as f:
                    form_data = json.load(f)
                    if control_id and form_data.get('control_id') != control_id:
                        continue
                    if spec_id and form_data.get('spec_id') != spec_id:
                        continue
                    forms.append(form_data)
            except:
                continue
    
    return sorted(forms, key=lambda x: x.get('created_date', ''), reverse=True)

