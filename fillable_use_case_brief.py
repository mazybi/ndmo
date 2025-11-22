"""
Fillable Use Case Brief Handler
Handles form data storage and PDF generation for Use Case Brief with product image support
"""
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

FORMS_DIR = "filled_forms"
PDF_FORMS_DIR = "filled_forms_pdf"

def save_use_case_brief_form(form_data, image_path=None):
    """Save filled use case brief form data to JSON file"""
    os.makedirs(FORMS_DIR, exist_ok=True)
    
    filename = f"{FORMS_DIR}/use_case_brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    form_record = {
        "form_type": "use_case_brief",
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": form_data,
        "image_path": image_path
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(form_record, f, indent=2, ensure_ascii=False)
    
    return filename

def load_use_case_brief_form():
    """Load saved use case brief form data"""
    if not os.path.exists(FORMS_DIR):
        return None
    
    files = [f for f in os.listdir(FORMS_DIR) if f.startswith("use_case_brief_") and f.endswith('.json')]
    if not files:
        return None
    
    latest_file = sorted(files)[-1]
    with open(f"{FORMS_DIR}/{latest_file}", 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_pdf_from_use_case_brief(form_data, image_path=None):
    """Generate PDF from filled use case brief form data with unified design and product image"""
    os.makedirs(PDF_FORMS_DIR, exist_ok=True)
    
    filename = f"{PDF_FORMS_DIR}/use_case_brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
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
    story.append(Paragraph("Use Case Brief", title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Document Information
    story.append(Paragraph("Document Information", heading_style))
    
    doc_info = []
    doc_info.append([Paragraph('<b>Use Case ID:</b>', field_label_style), Paragraph(str(form_data.get('use_case_id', '')), normal_style)])
    doc_info.append([Paragraph('<b>Use Case Name:</b>', field_label_style), Paragraph(str(form_data.get('use_case_name', '')), normal_style)])
    doc_info.append([Paragraph('<b>Date:</b>', field_label_style), Paragraph(str(form_data.get('date', '')), normal_style)])
    doc_info.append([Paragraph('<b>Version:</b>', field_label_style), Paragraph(str(form_data.get('version', '')), normal_style)])
    doc_info.append([Paragraph('<b>Department:</b>', field_label_style), Paragraph(str(form_data.get('department', '')), normal_style)])
    doc_info.append([Paragraph('<b>Status:</b>', field_label_style), Paragraph(str(form_data.get('status', '')), normal_style)])
    
    if doc_info:
        info_table = Table(doc_info, colWidths=[2.5*inch, 4.6*inch])
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
    
    # Use Case Overview
    story.append(Paragraph("Use Case Overview", heading_style))
    
    overview_info = []
    overview_info.append([Paragraph('<b>Description:</b>', field_label_style), Paragraph(str(form_data.get('description', '')), normal_style)])
    overview_info.append([Paragraph('<b>Business Objective:</b>', field_label_style), Paragraph(str(form_data.get('business_objective', '')), normal_style)])
    overview_info.append([Paragraph('<b>Stakeholders:</b>', field_label_style), Paragraph(str(form_data.get('stakeholders', '')), normal_style)])
    
    if overview_info:
        overview_table = Table(overview_info, colWidths=[2.5*inch, 4.6*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(overview_table)
    
    story.append(Spacer(1, 0.2*inch))
    
    # Product Image Section
    story.append(Paragraph("Product Image", heading_style))
    
    if image_path and os.path.exists(image_path):
        try:
            # Add product image
            img = Image(image_path, width=4*inch, height=3*inch)
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(f"<i>Product Image: {os.path.basename(image_path)}</i>", normal_style))
        except Exception as e:
            story.append(Paragraph(f"<i>Error loading image: {str(e)}</i>", normal_style))
    else:
        story.append(Paragraph("<i>No product image provided</i>", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Capabilities & Features
    story.append(Paragraph("Capabilities & Features", heading_style))
    capabilities = form_data.get('capabilities', '')
    if capabilities:
        story.append(Paragraph(capabilities, normal_style))
        story.append(Spacer(1, 0.15*inch))
    
    # Links & Resources
    story.append(Paragraph("Links & Resources", heading_style))
    links_info = []
    if form_data.get('documentation_link'):
        links_info.append([Paragraph('<b>Documentation:</b>', field_label_style), Paragraph(str(form_data.get('documentation_link', '')), normal_style)])
    if form_data.get('demo_link'):
        links_info.append([Paragraph('<b>Demo:</b>', field_label_style), Paragraph(str(form_data.get('demo_link', '')), normal_style)])
    if form_data.get('repository_link'):
        links_info.append([Paragraph('<b>Repository:</b>', field_label_style), Paragraph(str(form_data.get('repository_link', '')), normal_style)])
    if form_data.get('additional_links'):
        links_info.append([Paragraph('<b>Additional Links:</b>', field_label_style), Paragraph(str(form_data.get('additional_links', '')), normal_style)])
    
    if links_info:
        links_table = Table(links_info, colWidths=[2.5*inch, 4.6*inch])
        links_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(links_table)
        story.append(Spacer(1, 0.2*inch))
    
    # Technical Details
    story.append(Paragraph("Technical Details", heading_style))
    
    tech_info = []
    tech_info.append([Paragraph('<b>Data Sources:</b>', field_label_style), Paragraph(str(form_data.get('data_sources', '')), normal_style)])
    tech_info.append([Paragraph('<b>Data Types:</b>', field_label_style), Paragraph(str(form_data.get('data_types', '')), normal_style)])
    tech_info.append([Paragraph('<b>Data Volume:</b>', field_label_style), Paragraph(str(form_data.get('data_volume', '')), normal_style)])
    tech_info.append([Paragraph('<b>Processing Requirements:</b>', field_label_style), Paragraph(str(form_data.get('processing_requirements', '')), normal_style)])
    
    if tech_info:
        tech_table = Table(tech_info, colWidths=[2.5*inch, 4.6*inch])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(tech_table)
    
    story.append(Spacer(1, 0.2*inch))
    
    # Compliance & Security
    story.append(Paragraph("Compliance & Security", heading_style))
    
    compliance_info = []
    compliance_info.append([Paragraph('<b>NDMO Compliance:</b>', field_label_style), Paragraph(str(form_data.get('ndmo_compliance', '')), normal_style)])
    compliance_info.append([Paragraph('<b>NDI Compliance:</b>', field_label_style), Paragraph(str(form_data.get('ndi_compliance', '')), normal_style)])
    compliance_info.append([Paragraph('<b>Data Classification:</b>', field_label_style), Paragraph(str(form_data.get('data_classification', '')), normal_style)])
    compliance_info.append([Paragraph('<b>Security Requirements:</b>', field_label_style), Paragraph(str(form_data.get('security_requirements', '')), normal_style)])
    
    if compliance_info:
        compliance_table = Table(compliance_info, colWidths=[2.5*inch, 4.6*inch])
        compliance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(compliance_table)
    
    story.append(Spacer(1, 0.2*inch))
    
    # Signatures
    story.append(Paragraph("Approval", heading_style))
    signature_info = []
    signature_info.append([Paragraph('<b>Prepared By:</b>', field_label_style), Paragraph(str(form_data.get('prepared_by', '')), normal_style), 
                          Paragraph('<b>Date:</b>', field_label_style), Paragraph(str(form_data.get('prepared_date', '')), normal_style)])
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

