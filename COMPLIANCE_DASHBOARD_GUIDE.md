# Compliance & Regulatory Dashboard - Complete Guide

## Overview
The Compliance & Regulatory Dashboard provides comprehensive tracking and monitoring of all export-import compliance requirements, including IEC validation, GST refunds, LUT/Bond tracking, export incentive schemes, duty drawback, and DGFT scheme management.

---

## Features Implemented

### 1. ✅ IEC Validation Tracking
**DocType:** `IEC Registration` (Already exists)

**Features:**
- IEC number storage and validation
- Status tracking (Active/Suspended/Cancelled/Expired)
- Validity period monitoring
- Automatic expiry alerts
- Registration type (Importer/Exporter/Both)

**Access:** Search for "IEC Registration" in ERPNext

---

### 2. ✅ GST Export Refund Tracking
**DocType:** `GST Export Refund`

**Features:**
- Refund application tracking (GST-REF-####)
- Status workflow: Draft → Submitted → Under Review → Query Raised → Approved → Refund Processed
- Refund types:
  - IGST Refund
  - IGST + Cess Refund
  - Accumulated ITC Refund
- Shipping bill and invoice linking
- IGST and Cess amount calculation
- ARN number tracking
- Processing time monitoring
- Bank details and UTR tracking
- Query management
- Approval and rejection tracking

**Key Fields:**
- Shipping Bill Number & Date
- Invoice Number (linked to Sales Invoice)
- IGST Amount, Cess Amount
- Total Refund Claimed vs Sanctioned
- ARN Number
- Processing Time (Days)
- UTR Number for payment tracking

**Access:** Search for "GST Export Refund" in ERPNext

---

### 3. ✅ LUT / Bond Tracking
**DocType:** `LUT Bond Tracking`

**Features:**
- LUT (Letter of Undertaking) and Bond management
- Unique LUT/Bond number tracking
- Status: Active → Expiring Soon → Expired → Renewed → Cancelled
- Financial year tracking
- Validity period monitoring with auto-calculated days to expiry
- Bond amount and bank guarantee tracking
- Renewal tracking (link to previous and renewed LUT)
- Automatic expiry alerts
- Submission and acknowledgement tracking

**Key Fields:**
- Document Type (LUT/Bond)
- LUT/Bond Number
- Issue Date, Valid From, Valid Till
- Days to Expiry (auto-calculated)
- Bond Amount, Bank Guarantee Number
- Renewal Application Date
- Previous/Renewed LUT linking

**Access:** Search for "LUT Bond Tracking" in ERPNext

---

### 4. ✅ MEIS / RoDTEP Benefit Tracking
**DocType:** `Export Incentive Scheme`

**Features:**
- Multiple scheme types:
  - MEIS (Merchandise Exports from India Scheme)
  - RoDTEP (Remission of Duties and Taxes on Exported Products)
  - SEIS (Service Exports from India Scheme)
  - RoSCTL (Rebate of State and Central Taxes and Levies)
- Application and approval tracking
- Status workflow: Draft → Submitted → Under Review → Approved → Scrip Issued → Scrip Utilized
- Shipping bill and invoice linking
- HS Code and product description
- Incentive rate and amount calculation
- Scrip number, value, and expiry tracking
- Scrip utilization monitoring
- Processing time tracking
- Rejection reason capture

**Key Fields:**
- Scheme Type
- Application Number
- Shipping Bill Number & Date
- FOB Value
- HS Code, Product Description
- Incentive Rate (%), Eligible Value
- Incentive Amount (auto-calculated)
- Scrip Number, Value, Expiry Date
- Scrip Utilized Amount

**Access:** Search for "Export Incentive Scheme" in ERPNext

---

### 5. ✅ Duty Drawback Module
**DocType:** `Duty Drawback Claim`

**Features:**
- Drawback claim tracking (DDB-####)
- Drawback types:
  - All Industry Rate (AIR)
  - Brand Rate
  - Special Brand Rate
- Status workflow: Draft → Submitted → Under Verification → Approved → Payment Processed
- Shipping bill and invoice linking
- HS Code and product details
- Quantity-based and percentage-based calculation
- Customs verification tracking
- Bank payment details with UTR
- Processing time monitoring
- Rejection reason tracking

**Key Fields:**
- Claim Number, Claim Date
- Drawback Type
- Shipping Bill Number & Date
- HS Code, Product Description
- Quantity Exported, UOM
- Drawback Rate (per unit) or Percentage
- Calculated vs Claimed vs Sanctioned Amount
- Customs Port, Officer, Verification Date
- Payment Date, UTR Number

**Access:** Search for "Duty Drawback Claim" in ERPNext

---

### 6. ✅ DGFT Scheme Tracking
**DocType:** `DGFT Scheme Tracking`

**Features:**
- Multiple DGFT schemes:
  - Advance Authorization
  - DFIA (Duty Free Import Authorization)
  - EPCG (Export Promotion Capital Goods)
  - EOU (Export Oriented Unit)
  - SEZ (Special Economic Zone)
  - Advance Authorization for Annual Requirement
  - Duty Exemption Scheme
  - Duty Remission Scheme
- Authorization number tracking
- Status: Applied → Issued → Partially Utilized → Fully Utilized → Export Obligation Fulfilled
- Import value allowed vs utilized tracking
- Export obligation monitoring with percentage fulfillment
- Validity period tracking with expiry alerts
- Bond and bank guarantee management
- Extension and amendment tracking
- Compliance status monitoring
- Penalty tracking
- Redemption status

**Key Fields:**
- Scheme Name, Authorization Number
- Issue Date, Valid From, Valid Till
- Import Value Allowed/Utilized/Balance
- Duty Saved
- Export Obligation Value/Fulfilled/Pending
- Export Obligation Deadline
- Export Obligation Percentage (auto-calculated)
- Bond Number, Amount
- Bank Guarantee Number, Amount, Expiry
- Extension Granted Till
- Amendment Count
- Compliance Status, Penalty Amount
- Redemption Date, Status

**Access:** Search for "DGFT Scheme Tracking" in ERPNext

---

## 7. ✅ Compliance Health Score Dashboard

### Overview
The Compliance Health Score provides a comprehensive view of your organization's compliance status across all regulatory requirements.

### Score Calculation (100 Points Total)

1. **IEC Validation (20 points)**
   - IEC exists: 10 points
   - Valid for >6 months: 10 points
   - Valid for 3-6 months: 7 points
   - Valid for 1-3 months: 5 points
   - Valid for <1 month: 2 points

2. **GST Refund Compliance (15 points)**
   - Approval rate ≥90%: 10 points
   - Pending ratio <10%: 5 points

3. **LUT/Bond Validity (15 points)**
   - Has active LUT/Bond: 5 points
   - Valid for >90 days: 10 points
   - Valid for 30-90 days: 7 points
   - Valid for <30 days: 3 points

4. **Export Incentive Schemes (15 points)**
   - Approval rate ≥80%: 10 points
   - Pending ratio <20%: 5 points

5. **Duty Drawback (15 points)**
   - Approval rate ≥85%: 10 points
   - Rejection rate <10%: 5 points

6. **DGFT Scheme Compliance (20 points)**
   - Avg export obligation ≥90%: 10 points
   - Compliance ratio ≥90%: 10 points

### Score Interpretation
- **90-100**: Excellent Compliance
- **75-89**: Good Compliance
- **60-74**: Fair Compliance
- **Below 60**: Needs Improvement

### API Endpoint
```python
# Get compliance health score
frappe.call({
    method: 'api.compliance.get_compliance_health_score',
    args: {
        company: 'Your Company Name'
    },
    callback: function(r) {
        console.log(r.message);
        // Returns: overall_score, score_breakdown, alerts, metrics
    }
});
```

### Dashboard Components

#### 1. Overall Score Card
- Large score display (0-100)
- Color-coded indicator (Red/Yellow/Green)
- Score trend (up/down from last period)

#### 2. Score Breakdown
- IEC Validation: X/20
- GST Refund: X/15
- LUT/Bond: X/15
- Export Incentives: X/15
- Duty Drawback: X/15
- DGFT Schemes: X/20

#### 3. Compliance Alerts
- Critical alerts (red): <30 days to expiry
- Warning alerts (yellow): 30-90 days to expiry
- Info alerts (blue): General notifications

**Alert Types:**
- IEC expiry warnings
- LUT/Bond expiry warnings
- DGFT export obligation deadlines
- Pending GST refunds
- Pending duty drawback claims

#### 4. Compliance Metrics

**IEC Metrics:**
- Total IEC registrations
- Active IEC count
- Expiring soon count

**GST Refund Metrics:**
- Total refund applications
- Processed count
- Pending count
- Total claimed amount
- Total sanctioned amount

**LUT/Bond Metrics:**
- Total LUT/Bonds
- Active count
- Expiring soon count

**Export Incentive Metrics:**
- Total schemes
- Scrip issued count
- Total incentive amount
- Total approved amount

**Duty Drawback Metrics:**
- Total claims
- Processed count
- Total claimed amount
- Total sanctioned amount

**DGFT Scheme Metrics:**
- Total schemes
- Active schemes
- Obligation pending count
- Total import value
- Total duty saved

---

## Installation

### Prerequisites
- ERPNext system with Docker setup
- Existing export/import documentation system
- IEC Registration DocType (already created)

### Installation Steps

1. **Make installation script executable:**
```bash
chmod +x install_compliance_dashboard.sh
```

2. **Run installation:**
```bash
./install_compliance_dashboard.sh
```

3. **Verify installation:**
   - Search for "GST Export Refund" in ERPNext
   - Search for "LUT Bond Tracking" in ERPNext
   - Search for "Export Incentive Scheme" in ERPNext
   - Search for "Duty Drawback Claim" in ERPNext
   - Search for "DGFT Scheme Tracking" in ERPNext

---

## Usage Workflows

### Workflow 1: GST Export Refund Process

1. **Create GST Export Refund**
   - Go to: GST Export Refund > New
   - Enter shipping bill number and date
   - Link to Sales Invoice
   - Enter IGST and Cess amounts
   - Save as Draft

2. **Submit Application**
   - Review details
   - Change status to "Submitted"
   - Enter ARN number when received
   - Enter submission date

3. **Track Progress**
   - Update status as it progresses
   - Add query details if queries raised
   - Enter approval date when approved

4. **Record Payment**
   - Change status to "Refund Processed"
   - Enter refund sanctioned amount
   - Enter UTR number and payment date
   - System auto-calculates processing time

---

### Workflow 2: LUT/Bond Management

1. **Create LUT/Bond**
   - Go to: LUT Bond Tracking > New
   - Select document type (LUT/Bond)
   - Enter LUT/Bond number
   - Select financial year
   - Enter validity dates
   - Save

2. **Monitor Expiry**
   - System auto-calculates days to expiry
   - Automatic status change to "Expiring Soon" at 60 days
   - Receive alerts in Compliance Dashboard

3. **Renew LUT/Bond**
   - Create new LUT/Bond record
   - Link to previous LUT in "Previous LUT Number" field
   - Update old LUT status to "Renewed"
   - Link new LUT in "Renewed LUT Number" field

---

### Workflow 3: Export Incentive Scheme (MEIS/RoDTEP)

1. **Apply for Scheme**
   - Go to: Export Incentive Scheme > New
   - Select scheme type (MEIS/RoDTEP/SEIS/RoSCTL)
   - Enter shipping bill details
   - Link to Sales Invoice
   - Enter HS Code and product details
   - Enter incentive rate
   - System calculates incentive amount
   - Submit application

2. **Track Approval**
   - Update status as it progresses
   - Enter approval date when approved
   - Enter approved amount

3. **Record Scrip Details**
   - Change status to "Scrip Issued"
   - Enter scrip number, value, and expiry date
   - Track scrip utilization

---

### Workflow 4: Duty Drawback Claim

1. **File Claim**
   - Go to: Duty Drawback Claim > New
   - Select drawback type (AIR/Brand Rate/Special Brand Rate)
   - Enter shipping bill details
   - Link to Sales Invoice
   - Enter HS Code and product details
   - Enter quantity exported
   - Enter drawback rate or percentage
   - System calculates drawback amount
   - Submit claim

2. **Customs Verification**
   - Update status to "Under Verification"
   - Enter customs port and officer details
   - Enter verification date

3. **Approval & Payment**
   - Change status to "Approved"
   - Enter sanctioned amount
   - Update to "Payment Processed"
   - Enter bank details and UTR number

---

### Workflow 5: DGFT Scheme Management

1. **Apply for Authorization**
   - Go to: DGFT Scheme Tracking > New
   - Select scheme name (Advance Authorization/DFIA/EPCG/etc.)
   - Enter authorization number
   - Enter import value allowed
   - Enter export obligation value and deadline
   - Enter bond/BG details if applicable
   - Save

2. **Track Utilization**
   - Update import value utilized as imports happen
   - System auto-calculates balance
   - Update export obligation fulfilled as exports happen
   - System auto-calculates percentage

3. **Monitor Compliance**
   - Check export obligation percentage
   - Monitor deadline
   - Update compliance status
   - Record any penalties

4. **Complete Redemption**
   - When export obligation fulfilled
   - Change status to "Export Obligation Fulfilled"
   - Enter redemption date
   - Update redemption status to "Completed"

---

## Reports & Analytics

### Standard Reports

1. **GST Refund Summary**
   - Total refunds by status
   - Refund amounts by period
   - Average processing time
   - Approval vs rejection rate

2. **LUT/Bond Status Report**
   - Active LUT/Bonds
   - Expiring in next 90 days
   - Renewal history

3. **Export Incentive Analysis**
   - Scheme-wise breakdown
   - Scrip utilization rate
   - Total incentives earned

4. **Duty Drawback Analysis**
   - Drawback type distribution
   - Claim vs sanctioned amounts
   - Processing time trends

5. **DGFT Compliance Report**
   - Scheme-wise status
   - Export obligation fulfillment
   - Duty savings analysis

### Custom Reports

Create custom reports using Report Builder:
- Go to: Report Builder
- Select DocType
- Add filters and columns
- Save and share

---

## Alerts & Notifications

### Automatic Alerts

1. **IEC Expiry Alerts**
   - 90 days before expiry: Warning
   - 30 days before expiry: Critical

2. **LUT/Bond Expiry Alerts**
   - 60 days before expiry: Warning
   - 30 days before expiry: Critical

3. **DGFT Export Obligation Alerts**
   - 90 days before deadline: Warning
   - 30 days before deadline: Critical

4. **Pending Applications**
   - >5 pending GST refunds: Info alert
   - >10 pending duty drawback claims: Info alert

### Email Notifications

Configure email notifications:
- Go to: Email Alert
- Create new alert
- Select DocType and conditions
- Set recipients
- Save

---

## Best Practices

### 1. Regular Updates
- Update statuses promptly
- Record all dates accurately
- Attach supporting documents

### 2. Proactive Monitoring
- Check Compliance Dashboard weekly
- Review expiry alerts daily
- Follow up on pending applications

### 3. Documentation
- Attach all relevant documents
- Use remarks field for notes
- Maintain audit trail

### 4. Renewal Management
- Start renewal process 60 days before expiry
- Link old and new records
- Update statuses properly

### 5. Compliance Tracking
- Monitor export obligations monthly
- Track processing times
- Analyze rejection reasons

---

## Troubleshooting

### Issue: Compliance score not updating
**Solution:** Refresh the dashboard or clear cache

### Issue: Alerts not showing
**Solution:** Check date fields are filled correctly

### Issue: Auto-calculations not working
**Solution:** Ensure all required fields are filled

### Issue: Cannot link documents
**Solution:** Verify document exists and is saved

---

## API Reference

### Get Compliance Health Score
```python
GET /api/method/api.compliance.get_compliance_health_score
Parameters:
  - company: Company name (optional)

Returns:
{
  "overall_score": 85,
  "score_breakdown": {
    "iec_validation": 20,
    "gst_refund": 12,
    "lut_bond": 15,
    "export_incentives": 13,
    "duty_drawback": 10,
    "dgft_schemes": 15
  },
  "alerts": [...],
  "metrics": {...}
}
```

### Get Compliance Trend
```python
GET /api/method/api.compliance.get_compliance_trend
Parameters:
  - company: Company name (optional)
  - period: 'daily', 'weekly', 'monthly' (default: 'monthly')

Returns: Time-series data for compliance scores
```

### Export Compliance Report
```python
GET /api/method/api.compliance.export_compliance_report
Parameters:
  - company: Company name (optional)
  - format: 'pdf' or 'excel' (default: 'pdf')

Returns: Report file download
```

---

## Integration with Existing System

### Document Linking

All compliance documents can be linked to:
- Sales Invoice
- Sales Order
- Shipment
- Bill of Lading
- Certificate of Origin
- Letter of Credit

### Workflow Integration

Compliance tracking integrates with:
- Export documentation workflow
- Shipment tracking
- Financial accounting
- Customs clearance

---

## Permissions

### Role-Based Access

**Accounts User:**
- Read, Write, Create: GST Refund, LUT/Bond, Duty Drawback

**Accounts Manager:**
- Full access to all compliance documents

**Sales User:**
- Read, Write, Create: Export Incentive Scheme, DGFT Scheme

**Sales Manager:**
- Full access to export-related compliance

**System Manager:**
- Full access to all modules

---

## Maintenance

### Regular Tasks

**Daily:**
- Review compliance alerts
- Update application statuses

**Weekly:**
- Check Compliance Health Score
- Follow up on pending applications

**Monthly:**
- Review compliance metrics
- Analyze trends
- Generate reports

**Quarterly:**
- Audit compliance records
- Review and update processes
- Train users on new features

---

## Support & Resources

### Documentation
- ERPNext User Manual
- DGFT Handbook
- GST Refund Guidelines
- Duty Drawback Rules

### Training
- User training videos
- Process documentation
- Best practices guide

### Contact
- System Administrator
- Compliance Team
- IT Support

---

## Future Enhancements

### Planned Features
1. Automated email notifications
2. Integration with ICEGATE portal
3. OCR for document scanning
4. AI-powered compliance suggestions
5. Mobile app for alerts
6. Blockchain verification
7. Real-time GST portal integration
8. Automated report generation
9. Predictive analytics
10. Multi-currency support

---

## Conclusion

The Compliance & Regulatory Dashboard provides a comprehensive solution for managing all export-import compliance requirements. With automated tracking, alerts, and scoring, it ensures your organization maintains excellent compliance standards while minimizing manual effort.

**Key Benefits:**
- ✅ 100% compliance tracking coverage
- ✅ Automated alerts and notifications
- ✅ Real-time compliance health score
- ✅ Comprehensive audit trail
- ✅ Reduced manual effort
- ✅ Improved processing times
- ✅ Better decision making

---

**Document Version:** 1.0  
**Last Updated:** February 20, 2026  
**Status:** Production Ready ✅
