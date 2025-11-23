"""
Professional Data Quality Technical Report Generator
Creates comprehensive NDMO compliance reports with unified design
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import json

def create_data_quality_report(analysis_results, schema_file_name, logo_path="logo@3x.png"):
    """Create professional data quality technical report"""
    
    os.makedirs("reports", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/Data_Quality_Report_{timestamp}.pdf"
    
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
    
    # Unified styles
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
    
    field_label_style = ParagraphStyle(
        'FieldLabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=14
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
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=9,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Courier',
        leading=12,
        leftIndent=20,
        rightIndent=20,
        backColor=colors.HexColor('#f8f9fa'),
        borderPadding=10
    )
    
    # Header functions
    def on_first_page(canvas_obj, doc):
        from unified_templates import add_unified_header_footer
        add_unified_header_footer(canvas_obj, doc, logo_path, "RESTRICTED - INTERNAL")
    
    def on_later_pages(canvas_obj, doc):
        from unified_templates import add_unified_header_footer
        add_unified_header_footer(canvas_obj, doc, logo_path, "RESTRICTED - INTERNAL")
    
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
    story.append(Paragraph("Data Quality Technical Report", title_style))
    story.append(Paragraph("NDMO Compliance Analysis & Recommendations", ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        spaceAfter=20
    )))
    story.append(Spacer(1, 0.15*inch))
    
    # Report Information
    story.append(Paragraph("Report Information", heading_style))
    
    report_info_data = [
        [Paragraph('<b>Report Date:</b>', field_label_style), Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), normal_style), Paragraph('<b>Schema File:</b>', field_label_style), Paragraph(schema_file_name, normal_style)],
        [Paragraph('<b>Total Columns Analyzed:</b>', field_label_style), Paragraph(str(analysis_results.get('total_columns', 0)), normal_style), Paragraph('<b>Total Fields:</b>', field_label_style), Paragraph(str(analysis_results.get('total_fields', 0)), normal_style)],
        [Paragraph('<b>Primary Key:</b>', field_label_style), Paragraph("✅ Yes" if analysis_results.get('has_primary_key') else "❌ No", normal_style), Paragraph('<b>Audit Trail:</b>', field_label_style), Paragraph("✅ Yes" if analysis_results.get('has_audit_trail') else "❌ No", normal_style)]
    ]
    
    report_info_table = Table(report_info_data, colWidths=[1.9*inch, 2.3*inch, 1.9*inch, 2.3*inch])
    report_info_table.setStyle(TableStyle([
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
    story.append(report_info_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    
    total_cols = len(analysis_results.get('column_analysis', []))
    compliant_cols = sum(1 for col in analysis_results.get('ndmo_compliance', {}).values() if col.get('score', 0) >= 0.7)
    compliance_percentage = (compliant_cols / total_cols * 100) if total_cols > 0 else 0
    
    summary_text = f"""
    This technical report provides a comprehensive analysis of the data schema file "{schema_file_name}" 
    according to NDMO (National Data Management Office) quality standards. The analysis examined {total_cols} columns 
    and identified {compliant_cols} columns ({compliance_percentage:.1f}%) that meet NDMO compliance requirements.
    
    Key findings include:
    • Primary Key Status: {'Present' if analysis_results.get('has_primary_key') else 'Missing - Critical Issue'}
    • Audit Trail Status: {'Present' if analysis_results.get('has_audit_trail') else 'Missing - Critical Issue'}
    • Data Quality Issues: {len(analysis_results.get('issues', []))} issues identified
    • Recommendations: {len(analysis_results.get('recommendations', []))} recommendations provided
    """
    
    story.append(Paragraph(summary_text.strip(), normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Column Analysis Details
    story.append(Paragraph("Detailed Column Analysis", heading_style))
    
    column_analysis = analysis_results.get('column_analysis', [])
    ndmo_compliance = analysis_results.get('ndmo_compliance', {})
    
    if column_analysis:
        # Create table for column details
        col_details_data = [[
            Paragraph('<b>Column Name</b>', field_label_style),
            Paragraph('<b>Data Type</b>', field_label_style),
            Paragraph('<b>Completeness</b>', field_label_style),
            Paragraph('<b>Uniqueness</b>', field_label_style),
            Paragraph('<b>NDMO Score</b>', field_label_style),
            Paragraph('<b>Standards</b>', field_label_style)
        ]]
        
        for col_info in column_analysis[:50]:  # Limit to first 50 columns
            col_name = col_info['column_name']
            compliance_info = ndmo_compliance.get(col_name, {})
            
            col_details_data.append([
                Paragraph(str(col_name)[:30], normal_style),
                Paragraph(str(col_info.get('detected_type', 'Unknown')), normal_style),
                Paragraph(f"{col_info.get('completeness', 0):.1f}%", normal_style),
                Paragraph(f"{col_info.get('uniqueness', 0):.1f}%", normal_style),
                Paragraph(f"{compliance_info.get('score', 0)*100:.1f}%", normal_style),
                Paragraph(', '.join(compliance_info.get('standards', [])) or 'N/A', normal_style)
            ])
        
        if len(column_analysis) > 50:
            col_details_data.append([
                Paragraph(f"... and {len(column_analysis) - 50} more columns", normal_style),
                '', '', '', '', ''
            ])
        
        col_details_table = Table(col_details_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1.5*inch])
        col_details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(col_details_table)
        story.append(Spacer(1, 0.2*inch))
    
    # NDMO Standards Compliance
    story.append(Paragraph("NDMO Standards Compliance Assessment", heading_style))
    
    # Group standards by category
    standards_by_category = {
        'Data Governance (DG)': [],
        'Data Quality (DQ)': [],
        'Data Security (DS)': [],
        'Data Architecture (DA)': [],
        'Business Rules (BR)': []
    }
    
    for col_info in column_analysis:
        col_name = col_info['column_name']
        compliance_info = ndmo_compliance.get(col_name, {})
        standards = compliance_info.get('standards', [])
        
        for std in standards:
            if std.startswith('DG'):
                standards_by_category['Data Governance (DG)'].append(std)
            elif std.startswith('DQ'):
                standards_by_category['Data Quality (DQ)'].append(std)
            elif std.startswith('DS'):
                standards_by_category['Data Security (DS)'].append(std)
            elif std.startswith('DA'):
                standards_by_category['Data Architecture (DA)'].append(std)
            elif std.startswith('BR'):
                standards_by_category['Business Rules (BR)'].append(std)
    
    for category, stds in standards_by_category.items():
        if stds:
            unique_stds = sorted(set(stds))
            story.append(Paragraph(f"<b>{category}</b>", ParagraphStyle(
                'CategoryStyle',
                parent=styles['Heading3'],
                fontSize=11,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=5,
                spaceBefore=10
            )))
            story.append(Paragraph(f"Applicable Standards: {', '.join(unique_stds)}", normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Issues and Recommendations
    if analysis_results.get('issues'):
        story.append(Paragraph("Identified Issues", heading_style))
        for idx, issue in enumerate(analysis_results['issues'], 1):
            issue_text = f"<b>{idx}. {issue.get('issue', 'Unknown Issue')}</b><br/>"
            issue_text += f"Severity: {issue.get('severity', 'Unknown')}<br/>"
            issue_text += f"Impact: {issue.get('impact', 'N/A')}<br/>"
            issue_text += f"NDMO Standard: {issue.get('standard', 'N/A')}"
            story.append(Paragraph(issue_text, normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    if analysis_results.get('recommendations'):
        story.append(Paragraph("Recommendations", heading_style))
        for idx, rec in enumerate(analysis_results['recommendations'], 1):
            rec_text = f"<b>{idx}. {rec.get('type', 'Recommendation')}:</b> {rec.get('message', 'N/A')}<br/>"
            rec_text += f"NDMO Standard: {rec.get('standard', 'N/A')}"
            story.append(Paragraph(rec_text, normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.2*inch))
    
    # SQL Script Generation
    story.append(Paragraph("Schema Enhancement Script", heading_style))
    story.append(Paragraph("The following SQL script can be used to enhance the schema according to NDMO standards:", normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    sql_script = generate_sql_script(analysis_results)
    story.append(Preformatted(sql_script, code_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Python Script for Data Quality Monitoring
    story.append(Paragraph("Data Quality Monitoring Script", heading_style))
    story.append(Paragraph("Python script for continuous data quality monitoring:", normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    python_script = generate_python_monitoring_script(analysis_results)
    story.append(Preformatted(python_script, code_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Implementation Guide
    story.append(Paragraph("Implementation Guide", heading_style))
    
    implementation_text = """
    <b>Step 1: Schema Enhancement</b><br/>
    Execute the provided SQL script to add missing primary keys, audit trail fields, and constraints to your database schema.
    
    <b>Step 2: Data Quality Monitoring</b><br/>
    Deploy the Python monitoring script to continuously track data quality metrics and NDMO compliance.
    
    <b>Step 3: Regular Audits</b><br/>
    Schedule regular data quality audits using this tool to ensure ongoing compliance with NDMO standards.
    
    <b>Step 4: Documentation</b><br/>
    Maintain documentation of all schema changes and data quality improvements for audit purposes.
    """
    
    story.append(Paragraph(implementation_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

def generate_sql_script(analysis_results):
    """Generate SQL script for schema enhancement"""
    script = "-- NDMO Compliance Schema Enhancement Script\n"
    script += f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    script += "-- This script enhances the schema according to NDMO standards\n\n"
    
    script += "-- Step 1: Add Primary Key if missing\n"
    if not analysis_results.get('has_primary_key'):
        script += "-- TODO: Add primary key column\n"
        script += "-- ALTER TABLE your_table ADD COLUMN id SERIAL PRIMARY KEY;\n\n"
    
    script += "-- Step 2: Add Audit Trail Fields (DS004)\n"
    if not analysis_results.get('has_audit_trail'):
        script += "-- ALTER TABLE your_table ADD COLUMN created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;\n"
        script += "-- ALTER TABLE your_table ADD COLUMN updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;\n"
        script += "-- ALTER TABLE your_table ADD COLUMN created_by VARCHAR(100);\n"
        script += "-- ALTER TABLE your_table ADD COLUMN updated_by VARCHAR(100);\n\n"
    
    script += "-- Step 3: Add Constraints for Data Quality\n"
    column_analysis = analysis_results.get('column_analysis', [])
    for col_info in column_analysis[:20]:  # Limit to first 20
        col_name = col_info['column_name']
        if col_info.get('is_required', False) and col_info.get('completeness', 100) < 100:
            script += f"-- ALTER TABLE your_table ALTER COLUMN {col_name} SET NOT NULL;\n"
    
    script += "\n-- Step 4: Add Indexes for Performance\n"
    for col_info in column_analysis[:10]:
        col_name = col_info['column_name']
        if col_info.get('is_primary_key'):
            script += f"-- CREATE INDEX idx_{col_name} ON your_table({col_name});\n"
    
    return script

def generate_python_monitoring_script(analysis_results):
    """Generate Python script for data quality monitoring"""
    script = """# NDMO Data Quality Monitoring Script
# Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
# This script monitors data quality according to NDMO standards

import pandas as pd
from datetime import datetime

def monitor_data_quality(df, schema_analysis):
    \"\"\"Monitor data quality metrics\"\"\"
    results = {
        'timestamp': datetime.now().isoformat(),
        'total_rows': len(df),
        'quality_metrics': {}
    }
    
    # Check completeness (DQ001)
    for col in df.columns:
        completeness = (df[col].notna().sum() / len(df)) * 100
        results['quality_metrics'][col] = {
            'completeness': completeness,
            'null_count': df[col].isna().sum(),
            'unique_count': df[col].nunique()
        }
    
    # Check for primary key (DG001)
    has_pk = any('id' in str(col).lower() for col in df.columns)
    results['has_primary_key'] = has_pk
    
    # Check for audit trail (DS004)
    has_audit = any(kw in str(col).lower() for col in df.columns 
                    for kw in ['created', 'updated', 'timestamp'])
    results['has_audit_trail'] = has_audit
    
    return results

# Usage example:
# df = pd.read_excel('your_data.xlsx')
# schema_analysis = {...}  # Load from analysis results
# quality_report = monitor_data_quality(df, schema_analysis)
# print(quality_report)
"""
    return script

def create_schema_assessment_report(analysis_results, schema_file_name, logo_path="logo@3x.png"):
    """Create professional schema assessment report with NDMO compliance"""
    
    os.makedirs("reports", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/Schema_Assessment_Report_{timestamp}.pdf"
    
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
    
    # Unified styles
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
    
    field_label_style = ParagraphStyle(
        'FieldLabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        leading=14
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
    
    # Header functions
    def on_first_page(canvas_obj, doc):
        from unified_templates import add_unified_header_footer
        add_unified_header_footer(canvas_obj, doc, logo_path, "RESTRICTED - INTERNAL")
    
    def on_later_pages(canvas_obj, doc):
        from unified_templates import add_unified_header_footer
        add_unified_header_footer(canvas_obj, doc, logo_path, "RESTRICTED - INTERNAL")
    
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
    story.append(Paragraph("Schema Assessment Report", title_style))
    story.append(Paragraph("NDMO Compliance Assessment & Recommendations", ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        spaceAfter=20
    )))
    story.append(Spacer(1, 0.15*inch))
    
    # Assessment Summary
    story.append(Paragraph("Assessment Summary", heading_style))
    
    total_cols = len(analysis_results.get('column_analysis', []))
    compliant_cols = sum(1 for col in analysis_results.get('ndmo_compliance', {}).values() if col.get('score', 0) >= 0.7)
    compliance_percentage = (compliant_cols / total_cols * 100) if total_cols > 0 else 0
    
    summary_data = [
        [Paragraph('<b>Schema File:</b>', field_label_style), Paragraph(schema_file_name, normal_style), Paragraph('<b>Assessment Date:</b>', field_label_style), Paragraph(datetime.now().strftime("%Y-%m-%d"), normal_style)],
        [Paragraph('<b>Total Columns:</b>', field_label_style), Paragraph(str(total_cols), normal_style), Paragraph('<b>Compliant Columns:</b>', field_label_style), Paragraph(f"{compliant_cols} ({compliance_percentage:.1f}%)", normal_style)],
        [Paragraph('<b>Primary Key:</b>', field_label_style), Paragraph("✅ Present" if analysis_results.get('has_primary_key') else "❌ Missing", normal_style), Paragraph('<b>Audit Trail:</b>', field_label_style), Paragraph("✅ Present" if analysis_results.get('has_audit_trail') else "❌ Missing", normal_style)],
        [Paragraph('<b>Issues Found:</b>', field_label_style), Paragraph(str(len(analysis_results.get('issues', []))), normal_style), Paragraph('<b>Recommendations:</b>', field_label_style), Paragraph(str(len(analysis_results.get('recommendations', []))), normal_style)]
    ]
    
    summary_table = Table(summary_data, colWidths=[1.9*inch, 2.3*inch, 1.9*inch, 2.3*inch])
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
    
    # Compliance Score
    story.append(Paragraph("Overall Compliance Score", heading_style))
    
    overall_score = (compliance_percentage / 100) if total_cols > 0 else 0
    score_color = colors.HexColor('#28a745') if overall_score >= 0.7 else colors.HexColor('#ffc107') if overall_score >= 0.5 else colors.HexColor('#dc3545')
    
    score_text = f"<b>Overall NDMO Compliance: {overall_score*100:.1f}%</b>"
    score_para = Paragraph(score_text, ParagraphStyle(
        'ScoreStyle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=score_color,
        alignment=TA_CENTER,
        spaceAfter=10
    ))
    story.append(score_para)
    story.append(Spacer(1, 0.2*inch))
    
    # Column Assessment Details
    story.append(Paragraph("Column-by-Column Assessment", heading_style))
    
    column_analysis = analysis_results.get('column_analysis', [])
    ndmo_compliance = analysis_results.get('ndmo_compliance', {})
    
    if column_analysis:
        # Create detailed assessment table
        assessment_data = [[
            Paragraph('<b>Column</b>', field_label_style),
            Paragraph('<b>Type</b>', field_label_style),
            Paragraph('<b>Completeness</b>', field_label_style),
            Paragraph('<b>Uniqueness</b>', field_label_style),
            Paragraph('<b>NDMO Score</b>', field_label_style),
            Paragraph('<b>Status</b>', field_label_style)
        ]]
        
        for col_info in column_analysis:
            col_name = col_info['column_name']
            compliance_info = ndmo_compliance.get(col_name, {})
            score = compliance_info.get('score', 0)
            
            status = "✅ Compliant" if score >= 0.7 else "⚠️ Partial" if score >= 0.5 else "❌ Non-Compliant"
            status_color = colors.HexColor('#28a745') if score >= 0.7 else colors.HexColor('#ffc107') if score >= 0.5 else colors.HexColor('#dc3545')
            
            assessment_data.append([
                Paragraph(str(col_name)[:25], normal_style),
                Paragraph(str(col_info.get('detected_type', 'Unknown')), normal_style),
                Paragraph(f"{col_info.get('completeness', 0):.1f}%", normal_style),
                Paragraph(f"{col_info.get('uniqueness', 0):.1f}%", normal_style),
                Paragraph(f"{score*100:.1f}%", normal_style),
                Paragraph(status, ParagraphStyle('StatusStyle', parent=normal_style, textColor=status_color))
            ])
        
        assessment_table = Table(assessment_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1.5*inch])
        assessment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        story.append(assessment_table)
        story.append(Spacer(1, 0.2*inch))
    
    # Issues and Recommendations
    if analysis_results.get('issues'):
        story.append(Paragraph("Critical Issues", heading_style))
        for idx, issue in enumerate(analysis_results['issues'], 1):
            issue_text = f"<b>{idx}. {issue.get('issue', 'Unknown Issue')}</b><br/>"
            issue_text += f"Severity: {issue.get('severity', 'Unknown')} | "
            issue_text += f"Impact: {issue.get('impact', 'N/A')} | "
            issue_text += f"Standard: {issue.get('standard', 'N/A')}"
            story.append(Paragraph(issue_text, normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    if analysis_results.get('recommendations'):
        story.append(Paragraph("Recommendations", heading_style))
        for idx, rec in enumerate(analysis_results['recommendations'], 1):
            rec_text = f"<b>{idx}. {rec.get('type', 'Recommendation')}:</b> {rec.get('message', 'N/A')}<br/>"
            rec_text += f"NDMO Standard: {rec.get('standard', 'N/A')}"
            story.append(Paragraph(rec_text, normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    return filename

