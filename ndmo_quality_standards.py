"""
NDMO Data Quality Standards Manager
Manages NDMO quality standards and compliance assessment
"""

class NDMOQualityStandards:
    """NDMO Data Quality Standards Manager"""
    
    def __init__(self):
        self.standards = {
            'Data Governance (DG)': {
                'DG001': {
                    'name': 'Unique Identifiers',
                    'description': 'All entities must have unique identifiers',
                    'weight': 0.15,
                    'critical': True,
                    'category': 'Data Governance'
                },
                'DG002': {
                    'name': 'Data Lineage',
                    'description': 'Data lineage must be documented',
                    'weight': 0.10,
                    'critical': False,
                    'category': 'Data Governance'
                },
                'DG003': {
                    'name': 'Data Ownership',
                    'description': 'Data ownership must be clearly defined',
                    'weight': 0.10,
                    'critical': False,
                    'category': 'Data Governance'
                }
            },
            'Data Quality (DQ)': {
                'DQ001': {
                    'name': 'Data Completeness',
                    'description': 'Data must be complete (no missing required fields)',
                    'weight': 0.15,
                    'critical': True,
                    'category': 'Data Quality'
                },
                'DQ002': {
                    'name': 'Data Accuracy',
                    'description': 'Data must be accurate and valid',
                    'weight': 0.12,
                    'critical': True,
                    'category': 'Data Quality'
                },
                'DQ003': {
                    'name': 'Data Consistency',
                    'description': 'Data must be consistent across records',
                    'weight': 0.10,
                    'critical': False,
                    'category': 'Data Quality'
                },
                'DQ004': {
                    'name': 'Data Uniqueness',
                    'description': 'No duplicate records allowed',
                    'weight': 0.10,
                    'critical': True,
                    'category': 'Data Quality'
                },
                'DQ005': {
                    'name': 'Data Validity',
                    'description': 'Data must conform to defined formats and ranges',
                    'weight': 0.08,
                    'critical': False,
                    'category': 'Data Quality'
                },
                'DQ006': {
                    'name': 'Data Timeliness',
                    'description': 'Data must be up-to-date and timely',
                    'weight': 0.05,
                    'critical': False,
                    'category': 'Data Quality'
                }
            },
            'Data Security (DS)': {
                'DS001': {
                    'name': 'Data Encryption',
                    'description': 'Sensitive data must be encrypted',
                    'weight': 0.10,
                    'critical': True,
                    'category': 'Data Security'
                },
                'DS002': {
                    'name': 'Access Control',
                    'description': 'Access controls must be implemented',
                    'weight': 0.08,
                    'critical': True,
                    'category': 'Data Security'
                },
                'DS003': {
                    'name': 'Data Masking',
                    'description': 'PII data must be masked when appropriate',
                    'weight': 0.05,
                    'critical': False,
                    'category': 'Data Security'
                },
                'DS004': {
                    'name': 'Audit Trail',
                    'description': 'All data changes must be logged',
                    'weight': 0.07,
                    'critical': True,
                    'category': 'Data Security'
                }
            },
            'Data Architecture (DA)': {
                'DA001': {
                    'name': 'Data Modeling',
                    'description': 'Data models must follow NDMO standards',
                    'weight': 0.08,
                    'critical': False,
                    'category': 'Data Architecture'
                },
                'DA002': {
                    'name': 'Data Integration',
                    'description': 'Data integration must be standardized',
                    'weight': 0.07,
                    'critical': False,
                    'category': 'Data Architecture'
                },
                'DA003': {
                    'name': 'Data Storage',
                    'description': 'Data storage must meet NDMO requirements',
                    'weight': 0.05,
                    'critical': False,
                    'category': 'Data Architecture'
                }
            },
            'Business Rules (BR)': {
                'BR001': {
                    'name': 'Business Rule Validation',
                    'description': 'Business rules must be enforced',
                    'weight': 0.10,
                    'critical': False,
                    'category': 'Business Rules'
                },
                'BR002': {
                    'name': 'Data Relationships',
                    'description': 'Data relationships must be maintained',
                    'weight': 0.08,
                    'critical': False,
                    'category': 'Business Rules'
                },
                'BR003': {
                    'name': 'Calculated Fields',
                    'description': 'Calculated fields must be validated',
                    'weight': 0.05,
                    'critical': False,
                    'category': 'Business Rules'
                }
            }
        }
    
    def get_all_standards(self):
        """Get all NDMO quality standards"""
        return self.standards
    
    def get_standards_by_category(self, category):
        """Get standards by category"""
        return self.standards.get(category, {})
    
    def calculate_compliance_score(self, schema_analysis, data_quality_metrics):
        """Calculate overall NDMO compliance score"""
        total_score = 0
        total_weight = 0
        category_scores = {}
        standard_scores = {}
        
        for category, standards in self.standards.items():
            category_score = 0
            category_weight = 0
            
            for std_id, std_info in standards.items():
                weight = std_info['weight']
                total_weight += weight
                category_weight += weight
                
                # Calculate score for this standard based on schema and data quality
                score = self._calculate_standard_score(std_id, std_info, schema_analysis, data_quality_metrics)
                standard_scores[std_id] = {
                    'score': score,
                    'weight': weight,
                    'critical': std_info['critical'],
                    'name': std_info['name']
                }
                
                total_score += score * weight
                category_score += score * weight
            
            if category_weight > 0:
                category_scores[category] = category_score / category_weight
            else:
                category_scores[category] = 0
        
        overall_score = total_score / total_weight if total_weight > 0 else 0
        
        return {
            'overall_score': overall_score,
            'category_scores': category_scores,
            'standard_scores': standard_scores,
            'status': self._determine_status(overall_score, standard_scores)
        }
    
    def _calculate_standard_score(self, std_id, std_info, schema_analysis, data_quality_metrics):
        """Calculate score for a specific standard"""
        # Simplified scoring - in real implementation, this would be more sophisticated
        score = 0.5  # Default score
        
        # Check schema analysis results
        if schema_analysis:
            if 'has_primary_key' in schema_analysis and std_id == 'DG001':
                score = 1.0 if schema_analysis['has_primary_key'] else 0.3
            
            if 'has_audit_trail' in schema_analysis and std_id == 'DS004':
                score = 1.0 if schema_analysis['has_audit_trail'] else 0.2
        
        # Check data quality metrics
        if data_quality_metrics:
            if std_id == 'DQ001':  # Completeness
                score = data_quality_metrics.get('completeness', 0.5)
            elif std_id == 'DQ002':  # Accuracy
                score = data_quality_metrics.get('accuracy', 0.5)
            elif std_id == 'DQ003':  # Consistency
                score = data_quality_metrics.get('consistency', 0.5)
            elif std_id == 'DQ004':  # Uniqueness
                score = data_quality_metrics.get('uniqueness', 0.5)
            elif std_id == 'DQ005':  # Validity
                score = data_quality_metrics.get('validity', 0.5)
        
        return min(max(score, 0), 1)  # Ensure score is between 0 and 1
    
    def _determine_status(self, overall_score, standard_scores):
        """Determine overall compliance status"""
        # Check critical standards
        critical_failed = any(
            std['score'] < 0.7 and std['critical']
            for std in standard_scores.values()
        )
        
        if critical_failed:
            return 'Non-Compliant'
        elif overall_score >= 0.9:
            return 'Compliant'
        elif overall_score >= 0.7:
            return 'Partially Compliant'
        else:
            return 'Non-Compliant'
    
    def get_recommendations(self, compliance_results):
        """Get recommendations based on compliance results"""
        recommendations = []
        standard_scores = compliance_results.get('standard_scores', {})
        
        for std_id, std_info in standard_scores.items():
            if std_info['score'] < 0.7:
                std_details = self._get_standard_details(std_id)
                if std_details:
                    recommendations.append({
                        'standard_id': std_id,
                        'standard_name': std_details['name'],
                        'current_score': std_info['score'],
                        'recommendation': f"Improve {std_details['name']}: {std_details['description']}",
                        'priority': 'High' if std_info['critical'] else 'Medium'
                    })
        
        return recommendations
    
    def _get_standard_details(self, std_id):
        """Get standard details by ID"""
        for category, standards in self.standards.items():
            if std_id in standards:
                return standards[std_id]
        return None

