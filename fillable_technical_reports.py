"""
Fillable Technical Reports Handler
Handles form data storage and PDF generation for Technical Reports (Gap Analysis & Risk Assessment)
"""
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

FORMS_DIR = "filled_forms"
PDF_FORMS_DIR = "filled_forms_pdf"

def save_technical_report_form(report_type, form_data):
    """Save filled technical report form data to JSON file"""
    os.makedirs(FORMS_DIR, exist_ok=True)
    
    filename = f"{FORMS_DIR}/{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    form_record = {
        "report_type": report_type,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": form_data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(form_record, f, indent=2, ensure_ascii=False)
    
    return filename

def load_technical_report_form(report_type):
    """Load saved technical report form data"""
    if not os.path.exists(FORMS_DIR):
        return None
    
    files = [f for f in os.listdir(FORMS_DIR) if f.startswith(f"{report_type}_") and f.endswith('.json')]
    if not files:
        return None
    
    latest_file = sorted(files)[-1]
    with open(f"{FORMS_DIR}/{latest_file}", 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_pdf_from_technical_report(report_type, form_data):
    """Generate PDF from filled technical report form data with unified design"""
    os.makedirs(PDF_FORMS_DIR, exist_ok=True)
    
    filename = f"{PDF_FORMS_DIR}/{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
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
        leading=14,
        wordWrap='CJK'
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
    if report_type == "gap_analysis":
        title = "Gap Analysis Report"
    else:
        title = "Risk Assessment Report"
    
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Report Information
    story.append(Paragraph("Report Information", heading_style))
    
    if report_type == "gap_analysis":
        report_info = []
        report_info.append([Paragraph('<b>Report Date:</b>', field_label_style), Paragraph(str(form_data.get('report_date', '')), normal_style)])
        report_info.append([Paragraph('<b>Entity Name:</b>', field_label_style), Paragraph(str(form_data.get('entity_name', '')), normal_style)])
        report_info.append([Paragraph('<b>Assessment Period From:</b>', field_label_style), Paragraph(str(form_data.get('period_from', '')), normal_style)])
        report_info.append([Paragraph('<b>Assessment Period To:</b>', field_label_style), Paragraph(str(form_data.get('period_to', '')), normal_style)])
        report_info.append([Paragraph('<b>Department:</b>', field_label_style), Paragraph(str(form_data.get('department', '')), normal_style)])
        report_info.append([Paragraph('<b>Prepared By:</b>', field_label_style), Paragraph(str(form_data.get('prepared_by', '')), normal_style)])
        report_info.append([Paragraph('<b>Review Date:</b>', field_label_style), Paragraph(str(form_data.get('review_date', '')), normal_style)])
    else:
        report_info = []
        report_info.append([Paragraph('<b>Report Date:</b>', field_label_style), Paragraph(str(form_data.get('report_date', '')), normal_style)])
        report_info.append([Paragraph('<b>Entity Name:</b>', field_label_style), Paragraph(str(form_data.get('entity_name', '')), normal_style)])
        report_info.append([Paragraph('<b>Assessment Date:</b>', field_label_style), Paragraph(str(form_data.get('assessment_date', '')), normal_style)])
        report_info.append([Paragraph('<b>Department:</b>', field_label_style), Paragraph(str(form_data.get('department', '')), normal_style)])
        report_info.append([Paragraph('<b>Assessed By:</b>', field_label_style), Paragraph(str(form_data.get('assessed_by', '')), normal_style)])
        report_info.append([Paragraph('<b>Review Date:</b>', field_label_style), Paragraph(str(form_data.get('review_date', '')), normal_style)])
    
    if report_info:
        info_table = Table(report_info, colWidths=[2.5*inch, 4.6*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(info_table)
    
    story.append(Spacer(1, 0.2*inch))
    
    # Summary Section
    if report_type == "gap_analysis":
        story.append(Paragraph("Gap Summary", heading_style))
        summary_info = []
        summary_info.append([Paragraph('<b>Total Controls Assessed:</b>', field_label_style), Paragraph(str(form_data.get('total_controls', '')), normal_style)])
        summary_info.append([Paragraph('<b>Compliant Controls:</b>', field_label_style), Paragraph(str(form_data.get('compliant_controls', '')), normal_style)])
        summary_info.append([Paragraph('<b>Partially Compliant:</b>', field_label_style), Paragraph(str(form_data.get('partially_compliant', '')), normal_style)])
        summary_info.append([Paragraph('<b>Non-Compliant:</b>', field_label_style), Paragraph(str(form_data.get('non_compliant', '')), normal_style)])
        summary_info.append([Paragraph('<b>Gap Percentage:</b>', field_label_style), Paragraph(str(form_data.get('gap_percentage', '')) + '%', normal_style)])
        summary_info.append([Paragraph('<b>Priority Gaps (P1):</b>', field_label_style), Paragraph(str(form_data.get('priority_gaps', '')), normal_style)])
    else:
        story.append(Paragraph("Risk Summary", heading_style))
        summary_info = []
        summary_info.append([Paragraph('<b>Total Risks Identified:</b>', field_label_style), Paragraph(str(form_data.get('total_risks', '')), normal_style)])
        summary_info.append([Paragraph('<b>High Risk:</b>', field_label_style), Paragraph(str(form_data.get('high_risk', '')), normal_style)])
        summary_info.append([Paragraph('<b>Medium Risk:</b>', field_label_style), Paragraph(str(form_data.get('medium_risk', '')), normal_style)])
        summary_info.append([Paragraph('<b>Low Risk:</b>', field_label_style), Paragraph(str(form_data.get('low_risk', '')), normal_style)])
        summary_info.append([Paragraph('<b>Risk Score (Average):</b>', field_label_style), Paragraph(str(form_data.get('risk_score', '')), normal_style)])
        summary_info.append([Paragraph('<b>Mitigation Status:</b>', field_label_style), Paragraph(str(form_data.get('mitigation_status', '')), normal_style)])
    
    if summary_info:
        summary_table = Table(summary_info, colWidths=[2.5*inch, 4.6*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
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
    
    # Details Section
    if report_type == "gap_analysis":
        story.append(Paragraph("Gap Details", heading_style))
        details_text = form_data.get('gap_details', '')
    else:
        story.append(Paragraph("Risk Details", heading_style))
        details_text = form_data.get('risk_details', '')
    
    if details_text:
        story.append(Paragraph(details_text, normal_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Action Plan Section
    if report_type == "gap_analysis":
        story.append(Paragraph("Remediation Plan", heading_style))
        action_plan = form_data.get('remediation_plan', '')
    else:
        story.append(Paragraph("Mitigation Plan", heading_style))
        action_plan = form_data.get('mitigation_plan', '')
    
    if action_plan:
        story.append(Paragraph(action_plan, normal_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Signatures
    story.append(Paragraph("Approval", heading_style))
    signature_info = []
    if report_type == "gap_analysis":
        signature_info.append([Paragraph('<b>Prepared By:</b>', field_label_style), Paragraph(str(form_data.get('prepared_by_signature', '')), normal_style), 
                              Paragraph('<b>Date:</b>', field_label_style), Paragraph(str(form_data.get('prepared_date', '')), normal_style)])
    else:
        signature_info.append([Paragraph('<b>Assessed By:</b>', field_label_style), Paragraph(str(form_data.get('assessed_by_signature', '')), normal_style), 
                              Paragraph('<b>Date:</b>', field_label_style), Paragraph(str(form_data.get('assessed_date', '')), normal_style)])
    
    signature_info.append([Paragraph('<b>Reviewed By:</b>', field_label_style), Paragraph(str(form_data.get('reviewed_by', '')), normal_style), 
                          Paragraph('<b>Date:</b>', field_label_style), Paragraph(str(form_data.get('reviewed_date', '')), normal_style)])
    signature_info.append([Paragraph('<b>Approved By:</b>', field_label_style), Paragraph(str(form_data.get('approved_by', '')), normal_style), 
                          Paragraph('<b>Date:</b>', field_label_style), Paragraph(str(form_data.get('approved_date', '')), normal_style)])
    
    if signature_info:
        sig_table = Table(signature_info, colWidths=[1.6*inch, 2.1*inch, 1.6*inch, 2.1*inch])
        sig_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10)
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

