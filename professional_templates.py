"""
Professional NDMO Templates Generator
Enhanced templates with logo, classification, and detailed control information
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def add_header_footer(canvas_obj, doc, logo_path=None, classification="RESTRICTED - INTERNAL"):
    """Add unified professional header and footer to each page"""
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

def create_professional_evidence_template(control_id, control_name, spec_id, spec_text, description, priority, domain, evidence_requirements=None):
    """Create professional evidence template with logo and classification"""
    
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Evidence_{spec_id.replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(
        filename, 
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=75,
        bottomMargin=50
    )
    
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Heading style
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
    
    # Subheading style
    subheading_style = ParagraphStyle(
        'SubheadingStyle',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    # Field label style for table labels
    field_label_style = ParagraphStyle(
        'FieldLabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=14
    )
    
    # Normal text style - must be defined early for use in tables
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        leading=14,
        wordWrap='CJK'
    )
    
    # Text display style for long texts
    text_display_style = ParagraphStyle(
        'TextDisplayStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        leading=16,
        wordWrap='CJK',
        spaceAfter=6
    )
    
    # Specification text style
    spec_text_style = ParagraphStyle(
        'SpecTextStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_LEFT,
        leading=16,
        wordWrap='CJK',
        spaceAfter=8,
        leftIndent=0,
        rightIndent=0
    )
    
    # Classification banner
    classification = "RESTRICTED - INTERNAL"
    # Classification style (white text)
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
    story.append(Paragraph("Evidence Collection Form", title_style))
    story.append(Spacer(1, 0.12*inch))
    
    # Control Information Section
    story.append(Paragraph("Control Information", heading_style))
    
    # Create table data with proper Paragraph objects for HTML rendering
    control_data = [
        [Paragraph('<b>Control ID:</b>', normal_style), Paragraph(control_id, normal_style)],
        [Paragraph('<b>Control Name:</b>', normal_style), Paragraph(control_name, normal_style)],
        [Paragraph('<b>Domain:</b>', normal_style), Paragraph(domain, normal_style)],
        [Paragraph('<b>Specification ID:</b>', normal_style), Paragraph(spec_id, normal_style)],
        [Paragraph('<b>Priority:</b>', normal_style), Paragraph(f'<b>{priority}</b>', normal_style)],
        [Paragraph('<b>Document Date:</b>', normal_style), Paragraph(datetime.now().strftime("%Y-%m-%d"), normal_style)]
    ]
    
    control_table = Table(control_data, colWidths=[2.2*inch, 4.8*inch])
    control_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(control_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Specification Details Section
    story.append(Paragraph("Specification Details", heading_style))
    
    # Display specification text professionally
    story.append(Paragraph("<b>Specification Text:</b>", subheading_style))
    if spec_text:
        # Split long text into paragraphs for better display
        spec_paragraphs = spec_text.split('. ')
        for para in spec_paragraphs[:5]:  # First 5 sentences
            if para.strip():
                story.append(Paragraph(para.strip() + ('.' if not para.endswith('.') else ''), spec_text_style))
    else:
        story.append(Paragraph("N/A", text_display_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Description
    story.append(Paragraph("<b>Description:</b>", subheading_style))
    if description:
        desc_paragraphs = description.split('. ')
        for para in desc_paragraphs[:3]:  # First 3 sentences
            if para.strip():
                story.append(Paragraph(para.strip() + ('.' if not para.endswith('.') else ''), text_display_style))
    else:
        story.append(Paragraph("N/A", text_display_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Evidence Requirements Section
    if evidence_requirements:
        story.append(Paragraph("Evidence Requirements", heading_style))
        
        req_data = [['<b>Requirement</b>', '<b>Description</b>', '<b>Format</b>', '<b>Required</b>']]
        for req in evidence_requirements[:5]:  # First 5 requirements
            req_data.append([
                req.get('type', 'Document'),
                req.get('description', '')[:80] + '...' if len(req.get('description', '')) > 80 else req.get('description', ''),
                req.get('format', 'PDF'),
                'Yes' if req.get('required', True) else 'No'
            ])
        
        req_table = Table(req_data, colWidths=[1.5*inch, 3*inch, 1*inch, 1.5*inch])
        req_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        story.append(req_table)
        story.append(Spacer(1, 0.2*inch))
    
    # Evidence Collection Section
    story.append(Paragraph("Evidence Collection", heading_style))
    
    # More practical evidence fields with better spacing - using Paragraph for HTML
    evidence_fields = [
        [Paragraph('<b>Evidence Type:</b>', field_label_style), '_________________________________', Paragraph('<b>Evidence Category:</b>', field_label_style), '☐ Policy  ☐ Procedure  ☐ Configuration  ☐ Report'],
        [Paragraph('<b>Evidence Description:</b>', field_label_style), '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
        [Paragraph('<b>File Name:</b>', field_label_style), '_________________________________', Paragraph('<b>File Size:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>File Location/Path:</b>', field_label_style), '_________________________________', Paragraph('<b>File Format:</b>', field_label_style), '☐ PDF  ☐ DOCX  ☐ XLSX  ☐ Other'],
        [Paragraph('<b>Upload Date:</b>', field_label_style), '_________________________________', Paragraph('<b>Version:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Uploaded By:</b>', field_label_style), '_________________________________', Paragraph('<b>Department:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Reviewed By:</b>', field_label_style), '_________________________________', Paragraph('<b>Review Date:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Approved By:</b>', field_label_style), '_________________________________', Paragraph('<b>Approval Date:</b>', field_label_style), '_________________________________']
    ]
    
    evidence_table = Table(evidence_fields, colWidths=[1.8*inch, 2.2*inch, 1.8*inch, 2.2*inch])
    evidence_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (1, 1), (3, 3))  # Span description field across 3 rows for more writing space
    ]))
    story.append(evidence_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Acceptance Criteria Section
    story.append(Paragraph("Acceptance Criteria", heading_style))
    
    if evidence_requirements:
        for req in evidence_requirements[:3]:
            if req.get('acceptance_criteria'):
                story.append(Paragraph(f"<b>{req.get('type', 'Document')}:</b>", subheading_style))
                # Split long acceptance criteria into readable paragraphs
                criteria_text = req.get('acceptance_criteria', '')
                if len(criteria_text) > 200:
                    # Split by sentences for long text
                    sentences = criteria_text.split('. ')
                    for sent in sentences[:4]:  # First 4 sentences
                        if sent.strip():
                            story.append(Paragraph(sent.strip() + ('.' if not sent.endswith('.') else ''), text_display_style))
                else:
                    story.append(Paragraph(criteria_text, text_display_style))
                story.append(Spacer(1, 0.15*inch))
    
    # Compliance Status Section
    story.append(Paragraph("Compliance Status", heading_style))
    
    status_data = [
        [Paragraph('<b>Compliance Status:</b>', field_label_style), '☐ Compliant  ☐ Partially Compliant  ☐ Non-Compliant  ☐ Not Applicable'],
        [Paragraph('<b>Compliance Score (%):</b>', field_label_style), '___________ %', Paragraph('<b>Maturity Level:</b>', field_label_style), '☐ Level 0  ☐ Level 1  ☐ Level 2  ☐ Level 3  ☐ Level 4  ☐ Level 5'],
        [Paragraph('<b>Implementation Date:</b>', field_label_style), '_________________________________', Paragraph('<b>Review Date:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Next Review Date:</b>', field_label_style), '_________________________________', Paragraph('<b>Last Audit Date:</b>', field_label_style), '_________________________________']
    ]
    
    status_table = Table(status_data, colWidths=[2.1*inch, 2.6*inch, 1.6*inch, 2.1*inch])
    status_table.setStyle(TableStyle([
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
    story.append(status_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Notes Section - More practical with more writing space
    story.append(Paragraph("Notes and Comments", heading_style))
    
    # Use a simpler approach with better text display
    notes_data = [
        ['<b>Notes:</b>', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', '']
    ]
    
    notes_table = Table(notes_data, colWidths=[1.6*inch, 5.5*inch])
    notes_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8f9fa')),
        ('SPAN', (1, 0), (1, 7)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(notes_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Signatures Section
    story.append(Paragraph("Signatures and Approvals", heading_style))
    
    # More practical signature fields with better spacing - using Paragraph
    signature_data = [
        [Paragraph('<b>Prepared By:</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Name:</b>', field_label_style), '_________________________', Paragraph('<b>Title:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Signature:</b>', field_label_style), '_________________________', Paragraph('<b>Email:</b>', field_label_style), '_________________________'],
        ['', '', '', ''],
        [Paragraph('<b>Reviewed By:</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Name:</b>', field_label_style), '_________________________', Paragraph('<b>Title:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Signature:</b>', field_label_style), '_________________________', Paragraph('<b>Email:</b>', field_label_style), '_________________________'],
        ['', '', '', ''],
        [Paragraph('<b>Approved By:</b>', field_label_style), '_________________________', Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Name:</b>', field_label_style), '_________________________', Paragraph('<b>Title:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Signature:</b>', field_label_style), '_________________________', Paragraph('<b>Email:</b>', field_label_style), '_________________________']
    ]
    
    sig_table = Table(signature_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    sig_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(sig_table)
    
    # Build PDF with header/footer
    logo_path = "logo@3x.png"
    
    def on_first_page(canvas, doc):
        add_header_footer(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        add_header_footer(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

def create_professional_compliance_report(control_id, control_name, domain, specifications, evidence_summary=None):
    """Create professional compliance report with logo and classification"""
    
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Compliance_Report_{control_id.replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=75,
        bottomMargin=50
    )
    
    story = []
    
    # Styles
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
    
    # Normal text style for tables
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
    # Classification style (white text)
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
    story.append(Paragraph("Compliance Report", title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Report Information
    story.append(Paragraph("Report Information", heading_style))
    
    # Better text display for control name and domain
    control_name_display = control_name if len(control_name) <= 50 else control_name[:47] + '...'
    domain_display = domain if len(domain) <= 40 else domain[:37] + '...'
    
    report_data = [
        [Paragraph('<b>Control ID:</b>', field_label_style), Paragraph(control_id, normal_style), Paragraph('<b>Domain:</b>', field_label_style), Paragraph(domain_display, normal_style)],
        [Paragraph('<b>Control Name:</b>', field_label_style), Paragraph(control_name_display, normal_style), Paragraph('<b>Report Period:</b>', field_label_style), 'From: ___________  To: ___________'],
        [Paragraph('<b>Report Date:</b>', field_label_style), Paragraph(datetime.now().strftime("%Y-%m-%d"), normal_style), Paragraph('<b>Entity Name:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Prepared By:</b>', field_label_style), '_________________________________', Paragraph('<b>Department:</b>', field_label_style), '_________________________________']
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
    
    # Compliance Summary
    story.append(Paragraph("Compliance Summary", heading_style))
    
    summary_data = [
        [Paragraph('<b>Overall Compliance Status:</b>', normal_style), '☐ Compliant  ☐ Partially Compliant  ☐ Non-Compliant'],
        [Paragraph('<b>Overall Compliance Score:</b>', normal_style), '___________ %', Paragraph('<b>Total Specifications:</b>', normal_style), f'{len(specifications)}'],
        [Paragraph('<b>Compliant Specifications:</b>', normal_style), '___________', Paragraph('<b>Partially Compliant:</b>', normal_style), '___________'],
        [Paragraph('<b>Non-Compliant:</b>', normal_style), '___________', Paragraph('<b>Not Applicable:</b>', normal_style), '___________']
    ]
    
    summary_table = Table(summary_data, colWidths=[2.6*inch, 2.6*inch, 1.6*inch, 1.6*inch])
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
    
    # Specifications Details
    story.append(Paragraph("Specifications Compliance Details", heading_style))
    
    spec_headers = [Paragraph('<b>Spec ID</b>', normal_style), Paragraph('<b>Priority</b>', normal_style), Paragraph('<b>Status</b>', normal_style), Paragraph('<b>Score %</b>', normal_style), Paragraph('<b>Evidence</b>', normal_style)]
    spec_data = [spec_headers]
    
    for spec in specifications[:10]:  # First 10 specs
        spec_id = spec.get('spec_id', '')
        # Truncate long spec IDs if needed
        spec_id_display = spec_id if len(spec_id) <= 12 else spec_id[:9] + '...'
        spec_data.append([
            spec_id_display,
            spec.get('priority', 'P1'),
            '☐ C ☐ PC ☐ NC ☐ NA',
            '____',
            '☐ Yes ☐ No'
        ])
    
    spec_table = Table(spec_data, colWidths=[1.3*inch, 1.1*inch, 1.9*inch, 1.1*inch, 1.1*inch])
    spec_table.setStyle(TableStyle([
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
    story.append(spec_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Findings and Recommendations - Better text display
    story.append(Paragraph("Findings and Recommendations", heading_style))
    
    findings_data = [
        [Paragraph('<b>Key Findings:</b>', normal_style), ''],
        ['', ''],
        ['', ''],
        ['', ''],
        [Paragraph('<b>Recommendations:</b>', normal_style), ''],
        ['', ''],
        ['', ''],
        ['', ''],
        [Paragraph('<b>Action Items:</b>', normal_style), ''],
        ['', ''],
        ['', ''],
        ['', '']
    ]
    
    findings_table = Table(findings_data, colWidths=[2.2*inch, 4.9*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 4), (0, 4), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 8), (0, 8), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (1, 0), (1, 3)),
        ('SPAN', (1, 4), (1, 7)),
        ('SPAN', (1, 8), (1, 11)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
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
        add_header_footer(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        add_header_footer(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

def create_professional_audit_checklist(control_id, control_name, domain, specifications):
    """Create professional audit checklist with logo and classification"""
    
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Audit_Checklist_{control_id.replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=75,
        bottomMargin=50
    )
    
    story = []
    
    # Styles
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
    
    # Normal text style for tables
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
    # Classification style (white text)
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
    
    # Normal style for tables (redefine for this function)
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        leading=14,
        wordWrap='CJK'
    )
    
    # Title
    story.append(Paragraph("Audit Checklist", title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Control Information
    story.append(Paragraph("Control Information", heading_style))
    
    control_data = [
        [Paragraph('<b>Control ID:</b>', normal_style), Paragraph(control_id, normal_style), Paragraph('<b>Domain:</b>', normal_style), Paragraph(domain, normal_style)],
        [Paragraph('<b>Control Name:</b>', normal_style), Paragraph(control_name, normal_style), Paragraph('<b>Audit Date:</b>', normal_style), '_________________________________'],
        [Paragraph('<b>Auditor Name:</b>', normal_style), '_________________________________', Paragraph('<b>Entity Name:</b>', normal_style), '_________________________________'],
        [Paragraph('<b>Audit Type:</b>', normal_style), '☐ Internal  ☐ External  ☐ Regulatory', Paragraph('<b>Audit Scope:</b>', normal_style), '☐ Full  ☐ Partial']
    ]
    
    control_table = Table(control_data, colWidths=[1.8*inch, 2.2*inch, 1.8*inch, 2.2*inch])
    control_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    story.append(control_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Audit Checklist Items
    story.append(Paragraph("Audit Checklist", heading_style))
    
    checklist_headers = [Paragraph('<b>#</b>', normal_style), Paragraph('<b>Check Item</b>', normal_style), Paragraph('<b>Yes</b>', normal_style), Paragraph('<b>No</b>', normal_style), Paragraph('<b>N/A</b>', normal_style), Paragraph('<b>Notes</b>', normal_style)]
    checklist_items = [
        'Policy documented and approved',
        'Procedures implemented',
        'Roles and responsibilities defined',
        'Training conducted',
        'Evidence available',
        'Monitoring in place',
        'Compliance verified',
        'Documentation complete',
        'Review conducted',
        'Improvements identified'
    ]
    
    checklist_data = [checklist_headers]
    for i, item in enumerate(checklist_items, 1):
        checklist_data.append([str(i), item, '☐', '☐', '☐', ''])
    
    # Add specification-specific items with better text display
    for spec in specifications[:5]:
        spec_id = spec.get('spec_id', '')
        spec_text = spec.get('specification_text', '')
        # Truncate long text professionally
        if len(spec_text) > 60:
            spec_text_display = spec_text[:57] + '...'
        else:
            spec_text_display = spec_text
        
        checklist_data.append([
            '',
            f"Spec {spec_id}: {spec_text_display}",
            '☐', '☐', '☐', ''
        ])
    
    checklist_table = Table(checklist_data, colWidths=[0.5*inch, 3*inch, 0.6*inch, 0.6*inch, 0.6*inch, 1.7*inch])
    checklist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    story.append(checklist_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Audit Findings
    story.append(Paragraph("Audit Findings", heading_style))
    
    findings_data = [
        [Paragraph('<b>Findings:</b>', normal_style), ''],
        ['', ''],
        ['', ''],
        ['', ''],
        [Paragraph('<b>Recommendations:</b>', normal_style), ''],
        ['', ''],
        ['', ''],
        ['', '']
    ]
    
    findings_table = Table(findings_data, colWidths=[2*inch, 5*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 4), (0, 4), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (1, 0), (1, 3)),   # Span findings
        ('SPAN', (1, 4), (1, 7))    # Span recommendations
    ]))
    story.append(findings_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Signatures
    story.append(Paragraph("Signatures", heading_style))
    signature_data = [
        [Paragraph('<b>Auditor:</b>', normal_style), '_________________________', Paragraph('<b>Date:</b>', normal_style), '_________________________'],
        [Paragraph('<b>Name:</b>', normal_style), '_________________________', Paragraph('<b>Title:</b>', normal_style), '_________________________'],
        ['', '', '', ''],
        [Paragraph('<b>Reviewed By:</b>', normal_style), '_________________________', Paragraph('<b>Date:</b>', normal_style), '_________________________'],
        [Paragraph('<b>Approved By:</b>', normal_style), '_________________________', Paragraph('<b>Date:</b>', normal_style), '_________________________']
    ]
    
    sig_table = Table(signature_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    sig_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
    ]))
    story.append(sig_table)
    
    # Build PDF
    logo_path = "logo@3x.png"
    
    def on_first_page(canvas, doc):
        add_header_footer(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        add_header_footer(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

