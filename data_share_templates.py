"""
Data Share Templates Generator
Creates templates for data sharing compliance and reporting
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def add_header_footer_ds(canvas_obj, doc, logo_path=None, classification="RESTRICTED - INTERNAL"):
    """Add unified professional header and footer for data share templates"""
    canvas_obj.saveState()
    
    # Header background - compact
    canvas_obj.setFillColor(colors.HexColor('#f8f9fa'))
    canvas_obj.rect(0, A4[1] - 75, A4[0], 75, fill=1, stroke=0)
    
    # Logo - optimized size
    if logo_path and os.path.exists(logo_path):
        try:
            canvas_obj.drawImage(
                logo_path, 
                45, 
                A4[1] - 60, 
                width=2.0*inch, 
                height=0.7*inch, 
                preserveAspectRatio=True,
                mask='auto'
            )
        except:
            pass
    
    # Title - compact
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.setFillColor(colors.HexColor('#1f77b4'))
    canvas_obj.drawCentredString(A4[0]/2, A4[1] - 35, "NDMO/NDI Data Governance Compliance")
    
    # Classification - compact
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.setFillColor(colors.HexColor('#e74c3c'))
    canvas_obj.drawRightString(A4[0] - 45, A4[1] - 30, classification)
    
    # Date - compact
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(colors.HexColor('#7f8c8d'))
    canvas_obj.drawRightString(A4[0] - 45, A4[1] - 50, f"Print: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Footer - compact
    canvas_obj.setFillColor(colors.HexColor('#f8f9fa'))
    canvas_obj.rect(0, 0, A4[0], 45, fill=1, stroke=0)
    
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.HexColor('#7f8c8d'))
    canvas_obj.drawCentredString(A4[0]/2, 28, f"Page {canvas_obj.getPageNumber()} - NDMO/NDI Compliance Tool")
    canvas_obj.drawRightString(A4[0] - 45, 28, classification)
    
    # Lines - thinner
    canvas_obj.setStrokeColor(colors.HexColor('#1f77b4'))
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(45, A4[1] - 75, A4[0] - 45, A4[1] - 75)
    canvas_obj.line(45, 45, A4[0] - 45, 45)
    
    canvas_obj.restoreState()

def create_data_share_agreement_template():
    """Create Data Share Agreement template"""
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Data_Share_Agreement_{datetime.now().strftime('%Y%m%d')}.pdf"
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
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#ecf0f1'),
        borderPadding=8
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
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
        colWidths=[7*inch],
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
    story.append(Paragraph("Data Share Agreement", title_style))
    story.append(Spacer(1, 0.12*inch))
    
    # Agreement Information
    story.append(Paragraph("Agreement Information", heading_style))
    
    # Enhanced field sizes and fonts
    field_label_style = ParagraphStyle(
        'FieldLabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=16
    )
    
    agreement_data = [
        [Paragraph('<b>Agreement ID:</b>', field_label_style), '_________________________________', Paragraph('<b>Date:</b>', field_label_style), datetime.now().strftime("%Y-%m-%d")],
        [Paragraph('<b>Data Provider:</b>', field_label_style), '_________________________________', Paragraph('<b>Data Recipient:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Purpose of Data Share:</b>', field_label_style), '_________________________________', '', ''],
        ['', '_________________________________', '', ''],
        ['', '_________________________________', '', ''],
        [Paragraph('<b>Data Classification:</b>', field_label_style), '☐ Public  ☐ Internal  ☐ Restricted  ☐ Confidential', Paragraph('<b>Data Categories:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Volume:</b>', field_label_style), '_________________________________', Paragraph('<b>Retention Period:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Format:</b>', field_label_style), '☐ CSV  ☐ JSON  ☐ XML  ☐ Other', '', '']
    ]
    
    agreement_table = Table(agreement_data, colWidths=[1.8*inch, 2.4*inch, 1.8*inch, 2.4*inch])
    agreement_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (1, 2), (1, 4)),
        ('SPAN', (2, 2), (3, 2)),
        ('SPAN', (2, 3), (3, 3)),
        ('SPAN', (2, 4), (3, 4)),
        ('SPAN', (2, 7), (3, 7)),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(agreement_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Terms and Conditions
    story.append(Paragraph("Terms and Conditions", heading_style))
    
    terms_data = [
        [Paragraph('<b>Security Requirements:</b>', field_label_style), '_________________________________'],
        ['', '_________________________________'],
        ['', '_________________________________'],
        [Paragraph('<b>Access Controls:</b>', field_label_style), '_________________________________'],
        ['', '_________________________________'],
        ['', '_________________________________'],
        [Paragraph('<b>Data Usage Restrictions:</b>', field_label_style), '_________________________________'],
        ['', '_________________________________'],
        ['', '_________________________________']
    ]
    
    terms_table = Table(terms_data, colWidths=[2.0*inch, 5.0*inch])
    terms_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 6), (0, 6), colors.HexColor('#f8f9fa')),
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
    story.append(terms_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Compliance
    story.append(Paragraph("Compliance Requirements", heading_style))
    
    compliance_data = [
        [Paragraph('<b>NDMO Compliance:</b>', field_label_style), '☐ Compliant  ☐ Non-Compliant', Paragraph('<b>NDI Compliance:</b>', field_label_style), '☐ Compliant  ☐ Non-Compliant'],
        [Paragraph('<b>Data Protection:</b>', field_label_style), '☐ Yes  ☐ No', Paragraph('<b>Privacy Impact Assessment:</b>', field_label_style), '☐ Completed  ☐ Pending'],
        [Paragraph('<b>Approval Required:</b>', field_label_style), '☐ Yes  ☐ No', Paragraph('<b>Approval Date:</b>', field_label_style), '_________________________________']
    ]
    
    compliance_table = Table(compliance_data, colWidths=[2.0*inch, 2.5*inch, 2.0*inch, 1.9*inch])
    compliance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
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
    story.append(compliance_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Signatures
    story.append(Paragraph("Signatures", heading_style))
    signature_data = [
        [Paragraph('<b>Data Provider Representative:</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Name:</b>', field_label_style), '_________________________', Paragraph('<b>Title:</b>', field_label_style), '_________________________'],
        ['', '', '', ''],
        [Paragraph('<b>Data Recipient Representative:</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Name:</b>', field_label_style), '_________________________', Paragraph('<b>Title:</b>', field_label_style), '_________________________'],
        ['', '', '', ''],
        [Paragraph('<b>Approved By (Data Governance):</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________']
    ]
    
    sig_table = Table(signature_data, colWidths=[2.0*inch, 2.2*inch, 1.5*inch, 2.3*inch])
    sig_table.setStyle(TableStyle([
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
    story.append(sig_table)
    
    # Build PDF
    logo_path = "logo@3x.png"
    
    def on_first_page(canvas, doc):
        add_header_footer_ds(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        add_header_footer_ds(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

def create_data_sharing_report_template():
    """Create Data Sharing Report template"""
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Data_Sharing_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
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
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#ecf0f1'),
        borderPadding=8
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
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
        colWidths=[7*inch],
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
    story.append(Spacer(1, 0.2*inch))
    
    # Title
    story.append(Paragraph("Data Sharing Report", title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Report Information
    story.append(Paragraph("Report Information", heading_style))
    
    # Enhanced field label style
    field_label_style = ParagraphStyle(
        'FieldLabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=16
    )
    
    report_data = [
        [Paragraph('<b>Report Period:</b>', field_label_style), 'From: ___________  To: ___________', Paragraph('<b>Report Date:</b>', field_label_style), datetime.now().strftime("%Y-%m-%d")],
        [Paragraph('<b>Entity Name:</b>', field_label_style), '_________________________________', Paragraph('<b>Department:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Prepared By:</b>', field_label_style), '_________________________________', Paragraph('<b>Review Date:</b>', field_label_style), '_________________________________']
    ]
    
    report_table = Table(report_data, colWidths=[1.8*inch, 2.4*inch, 1.8*inch, 2.4*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
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
    
    # Sharing Summary
    story.append(Paragraph("Data Sharing Summary", heading_style))
    
    summary_data = [
        [Paragraph('<b>Total Agreements:</b>', field_label_style), '___________', Paragraph('<b>Active Agreements:</b>', field_label_style), '___________'],
        [Paragraph('<b>Data Providers:</b>', field_label_style), '___________', Paragraph('<b>Data Recipients:</b>', field_label_style), '___________'],
        [Paragraph('<b>Data Volume Shared:</b>', field_label_style), '___________', Paragraph('<b>Compliance Rate:</b>', field_label_style), '___________ %']
    ]
    
    summary_table = Table(summary_data, colWidths=[2.4*inch, 2.4*inch, 2.0*inch, 1.6*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
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
    
    # Sharing Details
    story.append(Paragraph("Sharing Details", heading_style))
    
    details_headers = [Paragraph('<b>Agreement ID</b>', field_label_style), Paragraph('<b>Provider</b>', field_label_style), 
                      Paragraph('<b>Recipient</b>', field_label_style), Paragraph('<b>Status</b>', field_label_style), 
                      Paragraph('<b>Compliance</b>', field_label_style)]
    details_data = [details_headers]
    
    for i in range(6):
        details_data.append([
            '___________',
            '___________',
            '___________',
            '☐ Active ☐ Inactive',
            '☐ C ☐ NC'
        ])
    
    details_table = Table(details_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1.0*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Findings
    story.append(Paragraph("Findings and Recommendations", heading_style))
    
    findings_data = [
        [Paragraph('<b>Key Findings:</b>', field_label_style), '_________________________________'],
        ['', '_________________________________'],
        ['', '_________________________________'],
        [Paragraph('<b>Recommendations:</b>', field_label_style), '_________________________________'],
        ['', '_________________________________'],
        ['', '_________________________________']
    ]
    
    findings_table = Table(findings_data, colWidths=[2.0*inch, 5.0*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#f8f9fa')),
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
    story.append(findings_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Signatures
    story.append(Paragraph("Approval", heading_style))
    signature_data = [
        [Paragraph('<b>Prepared By:</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Reviewed By:</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Approved By:</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________']
    ]
    
    sig_table = Table(signature_data, colWidths=[1.6*inch, 2.1*inch, 1.6*inch, 2.1*inch])
    sig_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(sig_table)
    
    # Build PDF
    logo_path = "logo@3x.png"
    
    def on_first_page(canvas, doc):
        add_header_footer_ds(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        add_header_footer_ds(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

