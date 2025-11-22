"""
Use Case Brief Template Generator
Creates a simple Use Case Brief template for NDMO/NDI compliance
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def create_use_case_brief_template():
    """Create Use Case Brief template"""
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Use_Case_Brief_{datetime.now().strftime('%Y%m%d')}.pdf"
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
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=25,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=24
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=18,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#ecf0f1'),
        borderPadding=10
    )
    
    field_label_style = ParagraphStyle(
        'FieldLabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=16
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        leading=16,
        wordWrap='CJK'
    )
    
    # Classification banner
    classification = "RESTRICTED - INTERNAL"
    classification_style = ParagraphStyle(
        'ClassificationStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.white,
        alignment=TA_CENTER,
        leading=16
    )
    classification_table = Table(
        [[Paragraph(f"<b>CLASSIFICATION: {classification}</b>", classification_style)]],
        colWidths=[7.1*inch],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ])
    )
    story.append(classification_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Title
    story.append(Paragraph("Use Case Brief", title_style))
    story.append(Spacer(1, 0.12*inch))
    
    # Document Information
    story.append(Paragraph("Document Information", heading_style))
    
    doc_data = [
        [Paragraph('<b>Use Case ID:</b>', field_label_style), Paragraph('_________________________________', normal_style), 
         Paragraph('<b>Date:</b>', field_label_style), Paragraph(datetime.now().strftime("%Y-%m-%d"), normal_style)],
        [Paragraph('<b>Use Case Name:</b>', field_label_style), Paragraph('_________________________________', normal_style), 
         Paragraph('<b>Version:</b>', field_label_style), Paragraph('___________', normal_style)],
        [Paragraph('<b>Department:</b>', field_label_style), Paragraph('_________________________________', normal_style), 
         Paragraph('<b>Status:</b>', field_label_style), Paragraph('☐ Draft ☐ Review ☐ Approved', normal_style)]
    ]
    
    doc_table = Table(doc_data, colWidths=[1.9*inch, 2.3*inch, 1.9*inch, 2.3*inch])
    doc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
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
    story.append(doc_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Use Case Overview
    story.append(Paragraph("Use Case Overview", heading_style))
    
    overview_data = [
        [Paragraph('<b>Description:</b>', field_label_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('<b>Business Objective:</b>', field_label_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('<b>Stakeholders:</b>', field_label_style), Paragraph('_________________________________', normal_style)]
    ]
    
    overview_table = Table(overview_data, colWidths=[2.2*inch, 4.9*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (1, 0), (1, 2)),
        ('SPAN', (1, 3), (1, 4)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Product Image Section
    story.append(Paragraph("Product Image", heading_style))
    story.append(Paragraph("(Image placeholder - Upload product image in fillable form)", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Technical Details
    story.append(Paragraph("Technical Details", heading_style))
    
    tech_data = [
        [Paragraph('<b>Data Sources:</b>', field_label_style), Paragraph('_________________________________', normal_style)],
        [Paragraph('<b>Data Types:</b>', field_label_style), Paragraph('_________________________________', normal_style)],
        [Paragraph('<b>Data Volume:</b>', field_label_style), Paragraph('_________________________________', normal_style)],
        [Paragraph('<b>Processing Requirements:</b>', field_label_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style)]
    ]
    
    tech_table = Table(tech_data, colWidths=[2.2*inch, 4.9*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (1, 3), (1, 4)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Compliance & Security
    story.append(Paragraph("Compliance & Security", heading_style))
    
    compliance_data = [
        [Paragraph('<b>NDMO Compliance:</b>', field_label_style), Paragraph('☐ Compliant ☐ Non-Compliant', normal_style)],
        [Paragraph('<b>NDI Compliance:</b>', field_label_style), Paragraph('☐ Compliant ☐ Non-Compliant', normal_style)],
        [Paragraph('<b>Data Classification:</b>', field_label_style), Paragraph('☐ Public ☐ Internal ☐ Restricted ☐ Confidential', normal_style)],
        [Paragraph('<b>Security Requirements:</b>', field_label_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style)]
    ]
    
    compliance_table = Table(compliance_data, colWidths=[2.2*inch, 4.9*inch])
    compliance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (1, 3), (1, 4)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(compliance_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Signatures
    story.append(Paragraph("Approval", heading_style))
    signature_data = [
        [Paragraph('<b>Prepared By:</b>', field_label_style), Paragraph('_________________________', normal_style), 
         Paragraph('<b>Date:</b>', field_label_style), Paragraph('_________________________', normal_style)],
        [Paragraph('<b>Reviewed By:</b>', field_label_style), Paragraph('_________________________', normal_style), 
         Paragraph('<b>Date:</b>', field_label_style), Paragraph('_________________________', normal_style)],
        [Paragraph('<b>Approved By:</b>', field_label_style), Paragraph('_________________________', normal_style), 
         Paragraph('<b>Date:</b>', field_label_style), Paragraph('_________________________', normal_style)]
    ]
    
    sig_table = Table(signature_data, colWidths=[1.6*inch, 2.1*inch, 1.6*inch, 2.1*inch])
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
    
    # Build PDF
    logo_path = "logo@3x.png"
    
    def on_first_page(canvas, doc):
        from unified_templates import add_unified_header_footer
        add_unified_header_footer(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        from unified_templates import add_unified_header_footer
        add_unified_header_footer(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

