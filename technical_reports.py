"""
Technical Reports Generator
Creates technical reports for NDMO/NDI compliance
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def add_tech_header_footer(canvas_obj, doc, logo_path=None, classification="RESTRICTED - INTERNAL"):
    """Add unified professional header and footer for technical reports"""
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

def create_gap_analysis_report():
    """Create Gap Analysis Report template"""
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Gap_Analysis_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
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
    story.append(Paragraph("Gap Analysis Report", title_style))
    story.append(Spacer(1, 0.12*inch))
    
    # Report Information
    story.append(Paragraph("Report Information", heading_style))
    
    report_data = [
        [Paragraph('<b>Report Date:</b>', field_label_style), Paragraph(datetime.now().strftime("%Y-%m-%d"), normal_style), 
         Paragraph('<b>Entity Name:</b>', field_label_style), Paragraph('_________________________________', normal_style)],
        [Paragraph('<b>Assessment Period:</b>', field_label_style), Paragraph('From: ___________  To: ___________', normal_style), 
         Paragraph('<b>Department:</b>', field_label_style), Paragraph('_________________________________', normal_style)],
        [Paragraph('<b>Prepared By:</b>', field_label_style), Paragraph('_________________________________', normal_style), 
         Paragraph('<b>Review Date:</b>', field_label_style), Paragraph('_________________________________', normal_style)]
    ]
    
    report_table = Table(report_data, colWidths=[1.9*inch, 2.3*inch, 1.9*inch, 2.3*inch])
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
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(report_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Gap Summary
    story.append(Paragraph("Gap Summary", heading_style))
    
    summary_data = [
        [Paragraph('<b>Total Controls Assessed:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Compliant Controls:</b>', field_label_style), Paragraph('___________', normal_style)],
        [Paragraph('<b>Partially Compliant:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Non-Compliant:</b>', field_label_style), Paragraph('___________', normal_style)],
        [Paragraph('<b>Gap Percentage:</b>', field_label_style), Paragraph('___________ %', normal_style), 
         Paragraph('<b>Priority Gaps (P1):</b>', field_label_style), Paragraph('___________', normal_style)]
    ]
    
    summary_table = Table(summary_data, colWidths=[2.6*inch, 2.6*inch, 2.1*inch, 1.1*inch])
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
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Gap Details
    story.append(Paragraph("Gap Details", heading_style))
    
    gap_headers = [Paragraph('<b>Control ID</b>', field_label_style), Paragraph('<b>Spec ID</b>', field_label_style),
                  Paragraph('<b>Gap Description</b>', field_label_style), Paragraph('<b>Priority</b>', field_label_style),
                  Paragraph('<b>Impact</b>', field_label_style), Paragraph('<b>Status</b>', field_label_style)]
    gap_data = [gap_headers]
    
    for i in range(8):
        gap_data.append([
            Paragraph('___________', normal_style),
            Paragraph('___________', normal_style),
            Paragraph('___________', normal_style),
            Paragraph('☐ P1 ☐ P2 ☐ P3', normal_style),
            Paragraph('☐ High ☐ Medium ☐ Low', normal_style),
            Paragraph('☐ Open ☐ In Progress ☐ Closed', normal_style)
        ])
    
    gap_table = Table(gap_data, colWidths=[1.2*inch, 1.2*inch, 2.2*inch, 1.1*inch, 1.1*inch, 1.1*inch])
    gap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(gap_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Remediation Plan
    story.append(Paragraph("Remediation Plan", heading_style))
    
    remediation_data = [
        [Paragraph('<b>Gap ID:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Target Date:</b>', field_label_style), Paragraph('___________', normal_style)],
        [Paragraph('<b>Remediation Action:</b>', field_label_style), Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('<b>Responsible Party:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Status:</b>', field_label_style), Paragraph('☐ Not Started ☐ In Progress ☐ Completed', normal_style)],
        [Paragraph('<b>Resources Required:</b>', field_label_style), Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style)]
    ]
    
    remediation_table = Table(remediation_data, colWidths=[2.2*inch, 2.3*inch, 1.6*inch, 2.3*inch])
    remediation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (1, 1), (3, 3)),
        ('SPAN', (1, 5), (3, 6)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(remediation_table)
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
        add_tech_header_footer(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        add_tech_header_footer(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

def create_risk_assessment_report():
    """Create Risk Assessment Report template"""
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Risk_Assessment_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
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
    story.append(Spacer(1, 0.25*inch))
    
    # Title
    story.append(Paragraph("Risk Assessment Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report Information
    story.append(Paragraph("Report Information", heading_style))
    
    report_data = [
        [Paragraph('<b>Report Date:</b>', field_label_style), Paragraph(datetime.now().strftime("%Y-%m-%d"), normal_style), 
         Paragraph('<b>Entity Name:</b>', field_label_style), Paragraph('_________________________________', normal_style)],
        [Paragraph('<b>Assessment Date:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Department:</b>', field_label_style), Paragraph('_________________________________', normal_style)],
        [Paragraph('<b>Assessed By:</b>', field_label_style), Paragraph('_________________________________', normal_style), 
         Paragraph('<b>Review Date:</b>', field_label_style), Paragraph('___________', normal_style)]
    ]
    
    report_table = Table(report_data, colWidths=[1.9*inch, 2.3*inch, 1.9*inch, 2.3*inch])
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
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(report_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Risk Summary
    story.append(Paragraph("Risk Summary", heading_style))
    
    summary_data = [
        [Paragraph('<b>Total Risks Identified:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>High Risk:</b>', field_label_style), Paragraph('___________', normal_style)],
        [Paragraph('<b>Medium Risk:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Low Risk:</b>', field_label_style), Paragraph('___________', normal_style)],
        [Paragraph('<b>Risk Score (Average):</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Mitigation Status:</b>', field_label_style), Paragraph('☐ Planned ☐ In Progress ☐ Completed', normal_style)]
    ]
    
    summary_table = Table(summary_data, colWidths=[2.6*inch, 2.6*inch, 2.1*inch, 1.1*inch])
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
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Risk Details
    story.append(Paragraph("Risk Details", heading_style))
    
    risk_headers = [Paragraph('<b>Risk ID</b>', field_label_style), Paragraph('<b>Description</b>', field_label_style),
                   Paragraph('<b>Likelihood</b>', field_label_style), Paragraph('<b>Impact</b>', field_label_style),
                   Paragraph('<b>Risk Level</b>', field_label_style), Paragraph('<b>Mitigation</b>', field_label_style)]
    risk_data = [risk_headers]
    
    for i in range(8):
        risk_data.append([
            Paragraph('___________', normal_style),
            Paragraph('___________', normal_style),
            Paragraph('☐ High ☐ Medium ☐ Low', normal_style),
            Paragraph('☐ High ☐ Medium ☐ Low', normal_style),
            Paragraph('☐ High ☐ Medium ☐ Low', normal_style),
            Paragraph('☐ Yes ☐ No', normal_style)
        ])
    
    risk_table = Table(risk_data, colWidths=[1.1*inch, 2.5*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Mitigation Plan
    story.append(Paragraph("Mitigation Plan", heading_style))
    
    mitigation_data = [
        [Paragraph('<b>Risk ID:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Target Date:</b>', field_label_style), Paragraph('___________', normal_style)],
        [Paragraph('<b>Mitigation Action:</b>', field_label_style), Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style), Paragraph('', normal_style)],
        [Paragraph('<b>Responsible Party:</b>', field_label_style), Paragraph('___________', normal_style), 
         Paragraph('<b>Status:</b>', field_label_style), Paragraph('☐ Not Started ☐ In Progress ☐ Completed', normal_style)]
    ]
    
    mitigation_table = Table(mitigation_data, colWidths=[2.2*inch, 2.3*inch, 1.6*inch, 2.3*inch])
    mitigation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (1, 1), (3, 3)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(mitigation_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Signatures
    story.append(Paragraph("Approval", heading_style))
    signature_data = [
        [Paragraph('<b>Assessed By:</b>', field_label_style), Paragraph('_________________________', normal_style), 
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
        add_tech_header_footer(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        add_tech_header_footer(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

