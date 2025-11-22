"""
Unified Professional Templates
All templates with consistent design, logo, and optimized layout
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

def add_unified_header_footer(canvas_obj, doc, logo_path=None, classification="RESTRICTED - INTERNAL"):
    """Unified header and footer for all templates"""
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

def get_unified_styles():
    """Get unified styles for all templates"""
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'UnifiedTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=15,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=20
    )
    
    heading_style = ParagraphStyle(
        'UnifiedHeading',
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
        'UnifiedFieldLabel',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=14
    )
    
    normal_style = ParagraphStyle(
        'UnifiedNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        leading=14,
        wordWrap='CJK'
    )
    
    return {
        'title': title_style,
        'heading': heading_style,
        'field_label': field_label_style,
        'normal': normal_style
    }

def create_unified_table(data, col_widths, header_rows=0):
    """Create unified table with consistent styling"""
    table = Table(data, colWidths=col_widths)
    
    table_style = [
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]
    
    if header_rows > 0:
        table_style.extend([
            ('BACKGROUND', (0, 0), (-1, header_rows-1), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, header_rows-1), colors.white),
            ('FONTNAME', (0, 0), (-1, header_rows-1), 'Helvetica-Bold'),
        ])
    
    # Add background for label columns
    for row_idx in range(header_rows, len(data)):
        table_style.append(('BACKGROUND', (0, row_idx), (0, row_idx), colors.HexColor('#f8f9fa')))
    
    table.setStyle(TableStyle(table_style))
    return table

def update_fillable_forms_with_logo():
    """Update fillable_forms.py to use unified design with logo"""
    # This will be done by modifying fillable_forms.py directly
    pass


