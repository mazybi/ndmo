"""
Fillable Data Share Forms Handler
Handles form data storage and PDF generation for Data Share forms
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

FORMS_DIR = "filled_forms"
PDF_FORMS_DIR = "filled_forms_pdf"

def save_data_share_form(form_type, form_data):
    """Save filled data share form data to JSON file"""
    os.makedirs(FORMS_DIR, exist_ok=True)
    
    filename = f"{FORMS_DIR}/{form_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    form_record = {
        "form_type": form_type,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": form_data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(form_record, f, indent=2, ensure_ascii=False)
    
    return filename

def load_data_share_form(form_type):
    """Load saved data share form data"""
    if not os.path.exists(FORMS_DIR):
        return None
    
    files = [f for f in os.listdir(FORMS_DIR) if f.startswith(f"{form_type}_") and f.endswith('.json')]
    if not files:
        return None
    
    latest_file = sorted(files)[-1]
    with open(f"{FORMS_DIR}/{latest_file}", 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_pdf_from_data_share_form(form_type, form_data):
    """Generate PDF from filled data share form data with unified design"""
    os.makedirs(PDF_FORMS_DIR, exist_ok=True)
    
    filename = f"{PDF_FORMS_DIR}/{form_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
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
    if form_type == "data_share_agreement":
        title = "Data Share Agreement"
    else:
        title = "Data Sharing Report"
    
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Form data
    story.append(Paragraph("Form Information", heading_style))
    
    form_info = []
    for key, value in form_data.items():
        if value:
            label = key.replace('_', ' ').title()
            form_info.append([Paragraph(f'<b>{label}:</b>', field_label_style), Paragraph(str(value), normal_style)])
    
    if form_info:
        info_table = Table(form_info, colWidths=[2.0*inch, 5.1*inch])
        info_table.setStyle(TableStyle([
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
        story.append(info_table)
    
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

