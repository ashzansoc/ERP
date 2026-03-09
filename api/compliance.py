import frappe
from frappe import _
from datetime import datetime, timedelta
import json


@frappe.whitelist()
def get_compliance_health_score(company=None):
    """
    Calculate and return the Compliance Health Score dashboard data.
    Score is calculated based on multiple compliance factors.
    """
    if not company:
        company = frappe.defaults.get_user_default("Company")
    
    score_data = {
        'overall_score': 0,
        'score_breakdown': {},
        'alerts': [],
        'metrics': {}
    }
    
    # 1. IEC Validation Score (20 points)
    iec_score = calculate_iec_score(company)
    score_data['score_breakdown']['iec_validation'] = iec_score
    
    # 2. GST Refund Compliance Score (15 points)
    gst_score = calculate_gst_refund_score(company)
    score_data['score_breakdown']['gst_refund'] = gst_score
    
    # 3. LUT/Bond Validity Score (15 points)
    lut_score = calculate_lut_bond_score(company)
    score_data['score_breakdown']['lut_bond'] = lut_score
    
    # 4. Export Incentive Scheme Score (15 points)
    incentive_score = calculate_incentive_scheme_score(company)
    score_data['score_breakdown']['export_incentives'] = incentive_score
    
    # 5. Duty Drawback Score (15 points)
    drawback_score = calculate_duty_drawback_score(company)
    score_data['score_breakdown']['duty_drawback'] = drawback_score
    
    # 6. DGFT Scheme Compliance Score (20 points)
    dgft_score = calculate_dgft_scheme_score(company)
    score_data['score_breakdown']['dgft_schemes'] = dgft_score
    
    # Calculate overall score
    score_data['overall_score'] = sum(score_data['score_breakdown'].values())
    
    # Get alerts
    score_data['alerts'] = get_compliance_alerts(company)
    
    # Get metrics
    score_data['metrics'] = get_compliance_metrics(company)
    
    return score_data


def calculate_iec_score(company):
    """Calculate IEC validation score (max 20 points)"""
    score = 0
    
    # Check if IEC exists
    iec_list = frappe.get_all('IEC Registration', 
                              filters={'company': company, 'status': 'Active'},
                              fields=['name', 'valid_till'])
    
    if not iec_list:
        return 0  # No IEC = 0 points
    
    score += 10  # IEC exists
    
    # Check validity
    for iec in iec_list:
        if iec.valid_till:
            days_to_expiry = (iec.valid_till - datetime.now().date()).days
            if days_to_expiry > 180:
                score += 10  # Valid for more than 6 months
            elif days_to_expiry > 90:
                score += 7  # Valid for 3-6 months
            elif days_to_expiry > 30:
                score += 5  # Valid for 1-3 months
            elif days_to_expiry > 0:
                score += 2  # Valid but expiring soon
        else:
            score += 10  # No expiry date (permanent)
    
    return min(score, 20)


def calculate_gst_refund_score(company):
    """Calculate GST refund compliance score (max 15 points)"""
    score = 0
    
    # Get refund statistics
    total_refunds = frappe.db.count('GST Export Refund', {'company': company})
    
    if total_refunds == 0:
        return 15  # No refunds = no issues
    
    # Check processing efficiency
    approved = frappe.db.count('GST Export Refund', 
                               {'company': company, 'status': 'Refund Processed'})
    pending = frappe.db.count('GST Export Refund', 
                              {'company': company, 'status': ['in', ['Submitted', 'Under Review']]})
    rejected = frappe.db.count('GST Export Refund', 
                               {'company': company, 'status': 'Rejected'})
    
    # Calculate approval rate
    if total_refunds > 0:
        approval_rate = (approved / total_refunds) * 100
        if approval_rate >= 90:
            score += 10
        elif approval_rate >= 75:
            score += 7
        elif approval_rate >= 60:
            score += 5
        else:
            score += 2
    
    # Check pending ratio
    if total_refunds > 0:
        pending_ratio = (pending / total_refunds) * 100
        if pending_ratio < 10:
            score += 5
        elif pending_ratio < 25:
            score += 3
        elif pending_ratio < 50:
            score += 1
    
    return min(score, 15)


def calculate_lut_bond_score(company):
    """Calculate LUT/Bond validity score (max 15 points)"""
    score = 0
    
    # Get active LUT/Bonds
    active_luts = frappe.get_all('LUT Bond Tracking',
                                 filters={'company': company, 'status': 'Active'},
                                 fields=['name', 'valid_till', 'financial_year'])
    
    if not active_luts:
        return 0  # No active LUT/Bond
    
    score += 5  # Has active LUT/Bond
    
    # Check validity
    for lut in active_luts:
        if lut.valid_till:
            days_to_expiry = (lut.valid_till - datetime.now().date()).days
            if days_to_expiry > 90:
                score += 10
            elif days_to_expiry > 30:
                score += 7
            elif days_to_expiry > 0:
                score += 3
    
    return min(score, 15)


def calculate_incentive_scheme_score(company):
    """Calculate export incentive scheme score (max 15 points)"""
    score = 0
    
    # Get scheme statistics
    total_schemes = frappe.db.count('Export Incentive Scheme', {'company': company})
    
    if total_schemes == 0:
        return 15  # No schemes = no issues
    
    # Check scrip utilization
    approved = frappe.db.count('Export Incentive Scheme',
                               {'company': company, 'status': ['in', ['Scrip Issued', 'Scrip Utilized']]})
    pending = frappe.db.count('Export Incentive Scheme',
                              {'company': company, 'status': ['in', ['Submitted', 'Under Review']]})
    
    if total_schemes > 0:
        approval_rate = (approved / total_schemes) * 100
        if approval_rate >= 80:
            score += 10
        elif approval_rate >= 60:
            score += 7
        elif approval_rate >= 40:
            score += 4
        else:
            score += 2
    
    # Check pending ratio
    if total_schemes > 0:
        pending_ratio = (pending / total_schemes) * 100
        if pending_ratio < 20:
            score += 5
        elif pending_ratio < 40:
            score += 3
        else:
            score += 1
    
    return min(score, 15)


def calculate_duty_drawback_score(company):
    """Calculate duty drawback score (max 15 points)"""
    score = 0
    
    # Get drawback statistics
    total_claims = frappe.db.count('Duty Drawback Claim', {'company': company})
    
    if total_claims == 0:
        return 15  # No claims = no issues
    
    # Check approval rate
    approved = frappe.db.count('Duty Drawback Claim',
                               {'company': company, 'status': 'Payment Processed'})
    rejected = frappe.db.count('Duty Drawback Claim',
                               {'company': company, 'status': 'Rejected'})
    
    if total_claims > 0:
        approval_rate = (approved / total_claims) * 100
        if approval_rate >= 85:
            score += 10
        elif approval_rate >= 70:
            score += 7
        elif approval_rate >= 50:
            score += 4
        else:
            score += 2
    
    # Check rejection rate
    if total_claims > 0:
        rejection_rate = (rejected / total_claims) * 100
        if rejection_rate < 10:
            score += 5
        elif rejection_rate < 20:
            score += 3
        elif rejection_rate < 30:
            score += 1
    
    return min(score, 15)


def calculate_dgft_scheme_score(company):
    """Calculate DGFT scheme compliance score (max 20 points)"""
    score = 0
    
    # Get active schemes
    active_schemes = frappe.get_all('DGFT Scheme Tracking',
                                    filters={'company': company, 
                                            'status': ['not in', ['Cancelled', 'Expired']]},
                                    fields=['name', 'export_obligation_percentage', 
                                           'valid_till', 'compliance_status'])
    
    if not active_schemes:
        return 20  # No schemes = no compliance issues
    
    # Check export obligation fulfillment
    total_obligation_percentage = 0
    compliant_count = 0
    
    for scheme in active_schemes:
        if scheme.export_obligation_percentage:
            total_obligation_percentage += scheme.export_obligation_percentage
        
        if scheme.compliance_status == 'Compliant':
            compliant_count += 1
    
    if len(active_schemes) > 0:
        avg_obligation = total_obligation_percentage / len(active_schemes)
        if avg_obligation >= 90:
            score += 10
        elif avg_obligation >= 75:
            score += 7
        elif avg_obligation >= 50:
            score += 4
        else:
            score += 2
        
        # Compliance ratio
        compliance_ratio = (compliant_count / len(active_schemes)) * 100
        if compliance_ratio >= 90:
            score += 10
        elif compliance_ratio >= 75:
            score += 7
        elif compliance_ratio >= 50:
            score += 4
        else:
            score += 2
    
    return min(score, 20)


def get_compliance_alerts(company):
    """Get compliance alerts and warnings"""
    alerts = []
    
    # IEC Expiry Alerts
    iec_expiring = frappe.get_all('IEC Registration',
                                  filters={
                                      'company': company,
                                      'status': 'Active',
                                      'valid_till': ['<=', (datetime.now().date() + timedelta(days=90))]
                                  },
                                  fields=['name', 'iec_number', 'valid_till'])
    
    for iec in iec_expiring:
        days_left = (iec.valid_till - datetime.now().date()).days
        alerts.append({
            'type': 'warning' if days_left > 30 else 'critical',
            'category': 'IEC Validation',
            'message': f'IEC {iec.iec_number} expiring in {days_left} days',
            'action': 'Renew IEC Registration',
            'reference': iec.name
        })
    
    # LUT/Bond Expiry Alerts
    lut_expiring = frappe.get_all('LUT Bond Tracking',
                                  filters={
                                      'company': company,
                                      'status': 'Active',
                                      'valid_till': ['<=', (datetime.now().date() + timedelta(days=60))]
                                  },
                                  fields=['name', 'lut_bond_number', 'valid_till'])
    
    for lut in lut_expiring:
        days_left = (lut.valid_till - datetime.now().date()).days
        alerts.append({
            'type': 'warning' if days_left > 30 else 'critical',
            'category': 'LUT/Bond',
            'message': f'LUT/Bond {lut.lut_bond_number} expiring in {days_left} days',
            'action': 'Renew LUT/Bond',
            'reference': lut.name
        })
    
    # DGFT Export Obligation Alerts
    dgft_pending = frappe.get_all('DGFT Scheme Tracking',
                                  filters={
                                      'company': company,
                                      'status': 'Export Obligation Pending',
                                      'export_obligation_deadline': ['<=', (datetime.now().date() + timedelta(days=90))]
                                  },
                                  fields=['name', 'authorization_number', 'export_obligation_deadline',
                                         'export_obligation_percentage'])
    
    for dgft in dgft_pending:
        days_left = (dgft.export_obligation_deadline - datetime.now().date()).days
        alerts.append({
            'type': 'warning' if days_left > 30 else 'critical',
            'category': 'DGFT Scheme',
            'message': f'Export obligation {dgft.export_obligation_percentage}% fulfilled for {dgft.authorization_number}, deadline in {days_left} days',
            'action': 'Fulfill Export Obligation',
            'reference': dgft.name
        })
    
    # Pending GST Refunds
    pending_refunds = frappe.db.count('GST Export Refund',
                                     {'company': company, 
                                      'status': ['in', ['Submitted', 'Under Review']]})
    
    if pending_refunds > 5:
        alerts.append({
            'type': 'info',
            'category': 'GST Refund',
            'message': f'{pending_refunds} GST refund applications pending',
            'action': 'Follow up with GST Department',
            'reference': None
        })
    
    return alerts


def get_compliance_metrics(company):
    """Get compliance metrics for dashboard"""
    metrics = {}
    
    # IEC Metrics
    metrics['iec'] = {
        'total': frappe.db.count('IEC Registration', {'company': company}),
        'active': frappe.db.count('IEC Registration', {'company': company, 'status': 'Active'}),
        'expiring_soon': frappe.db.count('IEC Registration', {
            'company': company,
            'status': 'Active',
            'valid_till': ['<=', (datetime.now().date() + timedelta(days=90))]
        })
    }
    
    # GST Refund Metrics
    metrics['gst_refund'] = {
        'total': frappe.db.count('GST Export Refund', {'company': company}),
        'processed': frappe.db.count('GST Export Refund', {'company': company, 'status': 'Refund Processed'}),
        'pending': frappe.db.count('GST Export Refund', {'company': company, 'status': ['in', ['Submitted', 'Under Review']]}),
        'total_claimed': frappe.db.sql("""
            SELECT COALESCE(SUM(total_refund_claimed), 0) 
            FROM `tabGST Export Refund` 
            WHERE company = %s
        """, company)[0][0] or 0,
        'total_sanctioned': frappe.db.sql("""
            SELECT COALESCE(SUM(refund_sanctioned), 0) 
            FROM `tabGST Export Refund` 
            WHERE company = %s AND status = 'Refund Processed'
        """, company)[0][0] or 0
    }
    
    # LUT/Bond Metrics
    metrics['lut_bond'] = {
        'total': frappe.db.count('LUT Bond Tracking', {'company': company}),
        'active': frappe.db.count('LUT Bond Tracking', {'company': company, 'status': 'Active'}),
        'expiring_soon': frappe.db.count('LUT Bond Tracking', {
            'company': company,
            'status': 'Active',
            'valid_till': ['<=', (datetime.now().date() + timedelta(days=60))]
        })
    }
    
    # Export Incentive Metrics
    metrics['export_incentives'] = {
        'total': frappe.db.count('Export Incentive Scheme', {'company': company}),
        'scrip_issued': frappe.db.count('Export Incentive Scheme', {'company': company, 'status': 'Scrip Issued'}),
        'total_incentive': frappe.db.sql("""
            SELECT COALESCE(SUM(incentive_amount), 0) 
            FROM `tabExport Incentive Scheme` 
            WHERE company = %s
        """, company)[0][0] or 0,
        'total_approved': frappe.db.sql("""
            SELECT COALESCE(SUM(approved_amount), 0) 
            FROM `tabExport Incentive Scheme` 
            WHERE company = %s AND status IN ('Approved', 'Scrip Issued', 'Scrip Utilized')
        """, company)[0][0] or 0
    }
    
    # Duty Drawback Metrics
    metrics['duty_drawback'] = {
        'total': frappe.db.count('Duty Drawback Claim', {'company': company}),
        'processed': frappe.db.count('Duty Drawback Claim', {'company': company, 'status': 'Payment Processed'}),
        'total_claimed': frappe.db.sql("""
            SELECT COALESCE(SUM(claimed_amount), 0) 
            FROM `tabDuty Drawback Claim` 
            WHERE company = %s
        """, company)[0][0] or 0,
        'total_sanctioned': frappe.db.sql("""
            SELECT COALESCE(SUM(sanctioned_amount), 0) 
            FROM `tabDuty Drawback Claim` 
            WHERE company = %s AND status = 'Payment Processed'
        """, company)[0][0] or 0
    }
    
    # DGFT Scheme Metrics
    metrics['dgft_schemes'] = {
        'total': frappe.db.count('DGFT Scheme Tracking', {'company': company}),
        'active': frappe.db.count('DGFT Scheme Tracking', {
            'company': company,
            'status': ['not in', ['Cancelled', 'Expired']]
        }),
        'obligation_pending': frappe.db.count('DGFT Scheme Tracking', {
            'company': company,
            'status': 'Export Obligation Pending'
        }),
        'total_import_value': frappe.db.sql("""
            SELECT COALESCE(SUM(import_value_allowed), 0) 
            FROM `tabDGFT Scheme Tracking` 
            WHERE company = %s
        """, company)[0][0] or 0,
        'total_duty_saved': frappe.db.sql("""
            SELECT COALESCE(SUM(duty_saved), 0) 
            FROM `tabDGFT Scheme Tracking` 
            WHERE company = %s
        """, company)[0][0] or 0
    }
    
    return metrics


@frappe.whitelist()
def get_compliance_trend(company=None, period='monthly'):
    """Get compliance trend data for charts"""
    if not company:
        company = frappe.defaults.get_user_default("Company")
    
    # Implementation for trend analysis
    # This would return time-series data for compliance scores
    pass


@frappe.whitelist()
def export_compliance_report(company=None, format='pdf'):
    """Export compliance report in PDF/Excel format"""
    if not company:
        company = frappe.defaults.get_user_default("Company")
    
    # Implementation for report export
    pass
