"""
Enhanced Professional Templates
Improved field sizes, fonts, and layout for all templates
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

def add_enhanced_header_footer(canvas_obj, doc, logo_path=None, classification="RESTRICTED - INTERNAL"):
    """Add enhanced professional header and footer"""
    canvas_obj.saveState()
    
    # Header background
    canvas_obj.setFillColor(colors.HexColor('#f8f9fa'))
    canvas_obj.rect(0, A4[1] - 85, A4[0], 85, fill=1, stroke=0)
    
    # Logo - better positioned
    if logo_path and os.path.exists(logo_path):
        try:
            canvas_obj.drawImage(
                logo_path, 
                50, 
                A4[1] - 70, 
                width=2.2*inch, 
                height=0.8*inch, 
                preserveAspectRatio=True,
                mask='auto'
            )
        except:
            pass
    
    # Title - centered, larger
    canvas_obj.setFont("Helvetica-Bold", 13)
    canvas_obj.setFillColor(colors.HexColor('#1f77b4'))
    canvas_obj.drawCentredString(A4[0]/2, A4[1] - 40, "NDMO/NDI Data Governance Compliance")
    
    # Classification - top right
    canvas_obj.setFont("Helvetica-Bold", 11)
    canvas_obj.setFillColor(colors.HexColor('#e74c3c'))
    canvas_obj.drawRightString(A4[0] - 50, A4[1] - 35, classification)
    
    # Date - below classification
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(colors.HexColor('#7f8c8d'))
    canvas_obj.drawRightString(A4[0] - 50, A4[1] - 55, f"Print Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Footer background
    canvas_obj.setFillColor(colors.HexColor('#f8f9fa'))
    canvas_obj.rect(0, 0, A4[0], 55, fill=1, stroke=0)
    
    # Footer content
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(colors.HexColor('#7f8c8d'))
    canvas_obj.drawCentredString(A4[0]/2, 35, f"Page {canvas_obj.getPageNumber()} - NDMO/NDI Compliance Tool")
    canvas_obj.drawRightString(A4[0] - 50, 35, classification)
    
    # Line separators
    canvas_obj.setStrokeColor(colors.HexColor('#1f77b4'))
    canvas_obj.setLineWidth(2.5)
    canvas_obj.line(50, A4[1] - 85, A4[0] - 50, A4[1] - 85)
    canvas_obj.line(50, 55, A4[0] - 50, 55)
    
    canvas_obj.restoreState()

def create_enhanced_evidence_template(control_id, control_name, spec_id, spec_text, description, priority, domain, evidence_requirements=None):
    """Create enhanced evidence template with better field sizes and fonts"""
    
    os.makedirs("templates", exist_ok=True)
    
    filename = f"templates/Evidence_{spec_id.replace('.', '_')}.pdf"
    doc = SimpleDocTemplate(
        filename, 
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=90,
        bottomMargin=65
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Enhanced styles with better sizing
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
    
    subheading_style = ParagraphStyle(
        'SubheadingStyle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
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
    
    field_label_style = ParagraphStyle(
        'FieldLabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=16
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
    story.append(Paragraph("Evidence Collection Form", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Control Information Section - Enhanced with better spacing
    story.append(Paragraph("Control Information", heading_style))
    
    control_data = [
        [Paragraph('<b>Control ID:</b>', field_label_style), Paragraph(control_id, normal_style)],
        [Paragraph('<b>Control Name:</b>', field_label_style), Paragraph(control_name, normal_style)],
        [Paragraph('<b>Domain:</b>', field_label_style), Paragraph(domain, normal_style)],
        [Paragraph('<b>Specification ID:</b>', field_label_style), Paragraph(spec_id, normal_style)],
        [Paragraph('<b>Priority:</b>', field_label_style), Paragraph(f'<b>{priority}</b>', normal_style)],
        [Paragraph('<b>Document Date:</b>', field_label_style), Paragraph(datetime.now().strftime("%Y-%m-%d"), normal_style)]
    ]
    
    control_table = Table(control_data, colWidths=[2.3*inch, 4.8*inch])
    control_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(control_table)
    story.append(Spacer(1, 0.35*inch))
    
    # Specification Details - Enhanced
    story.append(Paragraph("Specification Details", heading_style))
    
    story.append(Paragraph("<b>Specification Text:</b>", subheading_style))
    if spec_text:
        spec_paragraphs = spec_text.split('. ')
        for para in spec_paragraphs[:6]:
            if para.strip():
                story.append(Paragraph(para.strip() + ('.' if not para.endswith('.') else ''), normal_style))
    else:
        story.append(Paragraph("N/A", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Description:</b>", subheading_style))
    if description:
        desc_paragraphs = description.split('. ')
        for para in desc_paragraphs[:4]:
            if para.strip():
                story.append(Paragraph(para.strip() + ('.' if not para.endswith('.') else ''), normal_style))
    else:
        story.append(Paragraph("N/A", normal_style))
    
    story.append(Spacer(1, 0.35*inch))
    
    # Evidence Requirements Section
    if evidence_requirements:
        story.append(Paragraph("Evidence Requirements", heading_style))
        
        req_data = [[Paragraph('<b>Requirement</b>', field_label_style), Paragraph('<b>Description</b>', field_label_style), 
                    Paragraph('<b>Format</b>', field_label_style), Paragraph('<b>Required</b>', field_label_style)]]
        for req in evidence_requirements[:6]:
            req_data.append([
                Paragraph(req.get('type', 'Document'), normal_style),
                Paragraph(req.get('description', '')[:90] + '...' if len(req.get('description', '')) > 90 else req.get('description', ''), normal_style),
                Paragraph(req.get('format', 'PDF'), normal_style),
                Paragraph('Yes' if req.get('required', True) else 'No', normal_style)
            ])
        
        req_table = Table(req_data, colWidths=[1.6*inch, 3.2*inch, 1.1*inch, 1.2*inch])
        req_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(req_table)
        story.append(Spacer(1, 0.35*inch))
    
    # Evidence Collection Section - Enhanced with better field sizes
    story.append(Paragraph("Evidence Collection", heading_style))
    
    evidence_fields = [
        [Paragraph('<b>Evidence Type:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>Evidence Category:</b>', field_label_style), '☐ Policy  ☐ Procedure  ☐ Configuration  ☐ Report'],
        [Paragraph('<b>Evidence Description:</b>', field_label_style), '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
        [Paragraph('<b>File Name:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>File Size:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>File Location/Path:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>File Format:</b>', field_label_style), '☐ PDF  ☐ DOCX  ☐ XLSX  ☐ Other'],
        [Paragraph('<b>Upload Date:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>Version:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Uploaded By:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>Department:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Reviewed By:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>Review Date:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Approved By:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>Approval Date:</b>', field_label_style), '_________________________________']
    ]
    
    evidence_table = Table(evidence_fields, colWidths=[1.9*inch, 2.3*inch, 1.9*inch, 2.3*inch])
    evidence_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (1, 1), (3, 3)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(evidence_table)
    story.append(Spacer(1, 0.35*inch))
    
    # Acceptance Criteria Section - Enhanced
    if evidence_requirements:
        story.append(Paragraph("Acceptance Criteria", heading_style))
        for req in evidence_requirements[:4]:
            if req.get('acceptance_criteria'):
                story.append(Paragraph(f"<b>{req.get('type', 'Document')}:</b>", subheading_style))
                criteria_text = req.get('acceptance_criteria', '')
                if len(criteria_text) > 250:
                    sentences = criteria_text.split('. ')
                    for sent in sentences[:5]:
                        if sent.strip():
                            story.append(Paragraph(sent.strip() + ('.' if not sent.endswith('.') else ''), normal_style))
                else:
                    story.append(Paragraph(criteria_text, normal_style))
                story.append(Spacer(1, 0.2*inch))
    
    # Compliance Status Section - Enhanced
    story.append(Paragraph("Compliance Status", heading_style))
    
    status_data = [
        [Paragraph('<b>Compliance Status:</b>', field_label_style), '☐ Compliant  ☐ Partially Compliant  ☐ Non-Compliant  ☐ Not Applicable'],
        [Paragraph('<b>Compliance Score (%):</b>', field_label_style), '___________ %', 
         Paragraph('<b>Maturity Level:</b>', field_label_style), '☐ Level 0  ☐ Level 1  ☐ Level 2  ☐ Level 3  ☐ Level 4  ☐ Level 5'],
        [Paragraph('<b>Implementation Date:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>Review Date:</b>', field_label_style), '_________________________________'],
        [Paragraph('<b>Next Review Date:</b>', field_label_style), '_________________________________', 
         Paragraph('<b>Last Audit Date:</b>', field_label_style), '_________________________________']
    ]
    
    status_table = Table(status_data, colWidths=[2.1*inch, 2.6*inch, 1.6*inch, 2.1*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(status_table)
    story.append(Spacer(1, 0.35*inch))
    
    # Notes Section - Enhanced with more space
    story.append(Paragraph("Notes and Comments", heading_style))
    
    notes_data = [
        [Paragraph('<b>Notes:</b>', field_label_style), ''],
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
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8f9fa')),
        ('SPAN', (1, 0), (1, 7)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(notes_table)
    story.append(Spacer(1, 0.35*inch))
    
    # Signatures Section - Enhanced
    story.append(Paragraph("Signatures and Approvals", heading_style))
    
    signature_data = [
        [Paragraph('<b>Prepared By:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Name:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Title:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Signature:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Email:</b>', field_label_style), '_________________________'],
        ['', '', '', ''],
        [Paragraph('<b>Reviewed By:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Name:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Title:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Signature:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Email:</b>', field_label_style), '_________________________'],
        ['', '', '', ''],
        [Paragraph('<b>Approved By:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Date:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Name:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Title:</b>', field_label_style), '_________________________'],
        [Paragraph('<b>Signature:</b>', field_label_style), '_________________________', 
         Paragraph('<b>Email:</b>', field_label_style), '_________________________']
    ]
    
    sig_table = Table(signature_data, colWidths=[1.6*inch, 2.1*inch, 1.6*inch, 2.1*inch])
    sig_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(sig_table)
    
    # Build PDF with enhanced header/footer
    logo_path = "logo@3x.png"
    
    def on_first_page(canvas, doc):
        add_enhanced_header_footer(canvas, doc, logo_path, classification)
    
    def on_later_pages(canvas, doc):
        add_enhanced_header_footer(canvas, doc, logo_path, classification)
    
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename


