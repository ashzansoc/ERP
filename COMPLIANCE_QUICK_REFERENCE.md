# Compliance Dashboard - Quick Reference

## 📊 Compliance Health Score

### Score Breakdown (100 Points)
- **IEC Validation**: 20 points
- **GST Refund**: 15 points
- **LUT/Bond**: 15 points
- **Export Incentives**: 15 points
- **Duty Drawback**: 15 points
- **DGFT Schemes**: 20 points

### Score Ratings
- 90-100: ✅ Excellent
- 75-89: 🟢 Good
- 60-74: 🟡 Fair
- <60: 🔴 Needs Improvement

---

## 🚀 Quick Access

### Search Terms in ERPNext
- `GST Export Refund`
- `LUT Bond Tracking`
- `Export Incentive Scheme`
- `Duty Drawback Claim`
- `DGFT Scheme Tracking`
- `IEC Registration`

---

## 📝 Common Tasks

### 1. File GST Refund
1. New GST Export Refund
2. Enter Shipping Bill Number
3. Link Sales Invoice
4. Enter IGST/Cess amounts
5. Submit

### 2. Create LUT/Bond
1. New LUT Bond Tracking
2. Select Type (LUT/Bond)
3. Enter Number & Validity
4. Save

### 3. Apply for MEIS/RoDTEP
1. New Export Incentive Scheme
2. Select Scheme Type
3. Enter Shipping Bill Details
4. Enter Incentive Rate
5. Submit

### 4. File Duty Drawback
1. New Duty Drawback Claim
2. Select Drawback Type
3. Enter Export Details
4. Enter Drawback Rate
5. Submit

### 5. Track DGFT Scheme
1. New DGFT Scheme Tracking
2. Select Scheme Name
3. Enter Authorization Number
4. Enter Import/Export Values
5. Save

---

## ⚠️ Alert Types

### Critical (🔴)
- IEC expiring in <30 days
- LUT/Bond expiring in <30 days
- DGFT obligation deadline <30 days

### Warning (🟡)
- IEC expiring in 30-90 days
- LUT/Bond expiring in 30-60 days
- DGFT obligation deadline 30-90 days

### Info (🔵)
- >5 pending GST refunds
- >10 pending duty drawback claims

---

## 📈 Key Metrics

### IEC
- Total | Active | Expiring Soon

### GST Refund
- Total | Processed | Pending
- Claimed Amount | Sanctioned Amount

### LUT/Bond
- Total | Active | Expiring Soon

### Export Incentives
- Total | Scrip Issued
- Incentive Amount | Approved Amount

### Duty Drawback
- Total | Processed
- Claimed Amount | Sanctioned Amount

### DGFT Schemes
- Total | Active | Obligation Pending
- Import Value | Duty Saved

---

## 🔄 Status Workflows

### GST Refund
Draft → Submitted → Under Review → Query Raised → Approved → Refund Processed

### LUT/Bond
Active → Expiring Soon → Expired → Renewed

### Export Incentive
Draft → Submitted → Under Review → Approved → Scrip Issued → Scrip Utilized

### Duty Drawback
Draft → Submitted → Under Verification → Approved → Payment Processed

### DGFT Scheme
Applied → Issued → Partially Utilized → Fully Utilized → Export Obligation Fulfilled

---

## 🔗 Document Links

All compliance documents can link to:
- Sales Invoice
- Sales Order
- Shipment
- Bill of Lading
- Certificate of Origin
- Letter of Credit

---

## 📞 API Endpoints

```javascript
// Get Compliance Score
frappe.call({
    method: 'api.compliance.get_compliance_health_score',
    args: { company: 'Your Company' }
});

// Get Compliance Trend
frappe.call({
    method: 'api.compliance.get_compliance_trend',
    args: { company: 'Your Company', period: 'monthly' }
});

// Export Report
frappe.call({
    method: 'api.compliance.export_compliance_report',
    args: { company: 'Your Company', format: 'pdf' }
});
```

---

## 🎯 Best Practices

1. ✅ Update statuses promptly
2. ✅ Check dashboard weekly
3. ✅ Review alerts daily
4. ✅ Start renewals 60 days early
5. ✅ Attach all documents
6. ✅ Use remarks for notes
7. ✅ Monitor export obligations monthly
8. ✅ Track processing times
9. ✅ Analyze rejection reasons
10. ✅ Maintain audit trail

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Score not updating | Refresh dashboard |
| Alerts not showing | Check date fields |
| Auto-calc not working | Fill required fields |
| Cannot link docs | Verify doc exists |

---

## 📅 Maintenance Schedule

### Daily
- Review alerts
- Update statuses

### Weekly
- Check health score
- Follow up pending items

### Monthly
- Review metrics
- Analyze trends
- Generate reports

### Quarterly
- Audit records
- Update processes
- Train users

---

## 🎓 Training Resources

- User Manual: See COMPLIANCE_DASHBOARD_GUIDE.md
- Video Tutorials: Coming soon
- Process Docs: Available in system
- Support: Contact IT team

---

## 📊 Report Types

1. GST Refund Summary
2. LUT/Bond Status Report
3. Export Incentive Analysis
4. Duty Drawback Analysis
5. DGFT Compliance Report

---

## 🔐 Permissions

| Role | Access |
|------|--------|
| Accounts User | GST, LUT, Drawback (RWC) |
| Accounts Manager | All Accounts (Full) |
| Sales User | Incentives, DGFT (RWC) |
| Sales Manager | All Sales (Full) |
| System Manager | All (Full) |

RWC = Read, Write, Create

---

## 📱 Quick Links

- [Full Guide](COMPLIANCE_DASHBOARD_GUIDE.md)
- [Installation](install_compliance_dashboard.sh)
- [API Documentation](api/compliance.py)
- [Export System Guide](EXPORT_DOCUMENTATION_GUIDE.md)

---

**Version:** 1.0  
**Updated:** February 20, 2026
