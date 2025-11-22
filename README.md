# NDMO/NDI Data Governance Compliance Dashboard

A comprehensive data governance compliance measurement tool for Saudi Arabia's National Data Management Office (NDMO) and National Data Index (NDI) standards.

## Features

- **Dashboard Overview**: Real-time compliance metrics, status distribution, and category-wise compliance rates
- **Controls & Specifications**: Complete list of all data governance controls with detailed specifications and requirements
- **Compliance Phases**: Four-phase compliance journey (Assessment & Planning, Policy Development, Implementation, Monitoring & Reporting)
- **Documents & Evidence**: Track required documents and upload evidence for each control
- **Compliance Measurement**: Measure and track compliance scores for each control with detailed notes

## Controls Included

The tool includes 17 comprehensive data governance controls organized into the following categories:

1. **Data Governance Framework** (2 controls)
   - DG-001: Data Governance Framework Establishment
   - DG-002: Data Governance Policy

2. **Data Classification** (2 controls)
   - DC-001: Data Classification Framework
   - DC-002: Data Inventory and Catalog

3. **Data Quality** (2 controls)
   - DQ-001: Data Quality Standards
   - DQ-002: Data Quality Monitoring

4. **Data Privacy & Security** (3 controls)
   - DP-001: Data Privacy Policy
   - DP-002: Data Access Controls
   - DP-003: Data Encryption

5. **Data Retention & Disposal** (2 controls)
   - DR-001: Data Retention Policy
   - DR-002: Secure Data Disposal

6. **Data Lineage & Metadata** (2 controls)
   - DL-001: Data Lineage Documentation
   - DL-002: Metadata Management

7. **Compliance & Reporting** (2 controls)
   - CR-001: Compliance Monitoring
   - CR-002: Compliance Reporting

8. **Data Sharing & Integration** (2 controls)
   - DS-001: Data Sharing Agreements
   - DS-002: Data Integration Standards

## Installation

1. Install Python 3.8 or higher

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Navigation

- **Dashboard Overview**: View overall compliance metrics and visualizations
- **Controls & Specifications**: Browse all controls with detailed specifications
- **Specifications by Priority**: View all 191 specifications filtered by P1/P2/P3
- **Templates & Forms**: Download standardized NDMO templates for evidence collection and reporting
- **Compliance Phases**: Review the four-phase compliance journey
- **Documents & Evidence**: Manage required documents and upload evidence
- **Compliance Measurement**: Measure and track compliance for each control

## Features

### Controls & Specifications
- All controls are in English
- Detailed specifications for each control
- Requirements list for each control
- Filter by category or search controls

### Evidence Management
- Upload evidence files (PDF, DOC, DOCX, XLSX, XLS, TXT)
- Track evidence upload dates
- View evidence requirements for each control

### Compliance Measurement
- Set compliance status (Not Started, In Progress, Compliant, Non-Compliant)
- Assign compliance scores (0-100%)
- Add notes and comments
- Export compliance data to JSON

### Templates & Forms
- **Evidence Collection Templates**: Standardized forms for documenting evidence for each specification
- **Compliance Report Templates**: Templates for creating comprehensive compliance reports
- **Audit Checklist Templates**: Checklists for conducting compliance audits
- Download templates as PDF
- Upload completed templates as evidence
- All templates follow NDMO/NDI standards

### Dashboard
- Overall compliance score
- Status distribution charts
- Category-wise compliance rates
- Recent activity tracking

## Data Persistence

The application uses Streamlit's session state to store compliance data during the session. For production use, consider integrating with a database or file storage system.

## Compliance Phases

1. **Assessment & Planning** (2-4 weeks)
2. **Policy & Framework Development** (4-6 weeks)
3. **Implementation** (8-12 weeks)
4. **Monitoring & Reporting** (Ongoing)

## Templates & Forms

The tool includes standardized templates for:
- **Evidence Collection**: Document evidence for each specification with required fields and signatures
- **Compliance Reports**: Create comprehensive compliance reports with findings and recommendations
- **Audit Checklists**: Conduct structured compliance audits with checklists

All templates are:
- Based on NDMO/NDI standards
- Available in PDF format
- Fillable and printable
- Include signature fields for approval workflow

See `TEMPLATES_README.md` for detailed information about templates.

## Based on NDMO/NDI Standards

This tool is designed based on Saudi Arabia's National Data Management Office (NDMO) and National Data Index (NDI) requirements for data governance compliance.

The tool supports:
- **77 Controls** across 15 domains
- **191 Specifications** with P1, P2, P3 priorities
- Standardized evidence collection
- Compliance reporting and auditing

## License

This tool is provided for data governance compliance purposes.

