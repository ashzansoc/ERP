# Workflow Enhancements - Quick Reference

## Installation

```bash
chmod +x install_workflow_enhancements.sh
./install_workflow_enhancements.sh <site-name>
```

## Export Sales Flow - Quick Guide

### Stage Progression

```
Lead → Quotation Pending → Quotation Approved → Sales Order Created → 
Proforma Invoice Issued → Production In Progress → Production Complete → 
Packing In Progress → Ready for Shipment → Shipment Dispatched → 
Export Invoice Generated → Payment Received → Forex Realized → Export Complete
```

### Key Actions by Role

**Sales User**
- Create quotations
- Submit for approval

**Sales Manager**
- Approve/reject quotations
- Create sales orders

**Manufacturing User**
- Start production
- Update production status

**Manufacturing Manager**
- Complete production
- Approve production completion

**Stock User**
- Start packing
- Update packing status

**Stock Manager**
- Complete packing
- Dispatch shipments

**Accounts User**
- Generate proforma invoices
- Generate export invoices

**Accounts Manager**
- Confirm payments
- Realize forex

## Import Purchase Flow - Quick Guide

### Stage Progression

```
Purchase Request → PR Approved → PO Created → PO Approved → 
Shipment In Transit → Customs Clearance → Customs Cleared → 
GRN Pending → GRN Completed → Landed Cost Calculated → 
Inventory Updated → Payment Pending → Payment Completed → Import Complete
```

### Key Actions by Role

**Purchase User**
- Create purchase requests
- Create purchase orders

**Purchase Manager**
- Approve purchase requests
- Approve purchase orders

**Stock User**
- Track shipments
- Initiate customs clearance
- Create GRN

**Stock Manager**
- Clear customs
- Complete GRN
- Update inventory

**Accounts User**
- Calculate landed costs
- Request payments

**Accounts Manager**
- Process payments
- Complete import

## API Endpoints

### Get Workflow Status
```javascript
frappe.call({
    method: 'api.workflow_automation.get_workflow_status',
    args: {
        doctype: 'Sales Order',
        docname: 'SO-00001'
    }
});
```

### Apply Workflow Action
```javascript
frappe.call({
    method: 'api.workflow_automation.apply_workflow_action',
    args: {
        doctype: 'Sales Order',
        docname: 'SO-00001',
        action: 'Approve'
    }
});
```

### Get Pending Approvals
```javascript
frappe.call({
    method: 'api.workflow_automation.get_pending_approvals'
});
```

### Get Workflow Analytics
```javascript
frappe.call({
    method: 'api.workflow_automation.get_workflow_analytics',
    args: {
        doctype: 'Sales Order',
        from_date: '2024-01-01',
        to_date: '2024-12-31'
    }
});
```

## Required Fields by Stage

### Export Sales

**Quotation Approved → Sales Order Created**
- Customer details
- Items with quantities
- Pricing

**Sales Order Created → Proforma Invoice Issued**
- Proforma invoice number

**Proforma Invoice Issued → Production In Progress**
- Production order reference

**Production Complete → Packing In Progress**
- Production status = "Completed"

**Packing In Progress → Ready for Shipment**
- Packing status = "Completed"

**Ready for Shipment → Shipment Dispatched**
- Shipment reference

**Payment Received → Forex Realized**
- Forex realization date

### Import Purchase

**PO Approved → Shipment In Transit**
- Shipment tracking details

**Customs Clearance → Customs Cleared**
- Customs clearance date
- Customs status = "Cleared"

**Customs Cleared → GRN Pending**
- GRN reference

**GRN Pending → GRN Completed**
- GRN status = "Completed"

**GRN Completed → Landed Cost Calculated**
- All cost components

**Landed Cost Calculated → Inventory Updated**
- Landed cost voucher

## Common Issues & Solutions

### Issue: Cannot transition to next state
**Solution**: Check required fields are filled and user has appropriate role

### Issue: Workflow actions not visible
**Solution**: Clear cache and reload page

### Issue: Email notifications not sent
**Solution**: Verify email settings and user email addresses

### Issue: Self-approval error
**Solution**: Different user with appropriate role must approve

## Keyboard Shortcuts

- `Ctrl + Shift + W` - Open workflow actions menu
- `Ctrl + Shift + A` - View pending approvals
- `Ctrl + Shift + H` - View workflow history

## Reports

Access from: Reports > Workflow

- Workflow State Report
- Pending Approvals by User
- Stage Duration Analysis
- Workflow Bottlenecks
- Approval Turnaround Time

## Best Practices

1. Complete all required fields before transitioning
2. Attach supporting documents at each stage
3. Add comments when rejecting or requesting changes
4. Review pending approvals daily
5. Monitor workflow analytics weekly
6. Update status fields in real-time
7. Use bulk actions for multiple documents
8. Set up email notifications for critical stages

## Support Commands

```bash
# Check workflow status
bench --site <site> console
>>> frappe.get_doc('Sales Order', 'SO-00001').workflow_state

# Reset workflow state (use with caution)
>>> doc = frappe.get_doc('Sales Order', 'SO-00001')
>>> doc.workflow_state = 'Lead'
>>> doc.save()

# Clear workflow cache
bench --site <site> clear-cache
```

## Configuration Files

- Workflow definitions: `install_workflow_enhancements.py`
- API endpoints: `api/workflow_automation.py`
- UI enhancements: `workflow_ui_enhancements.js`
- Documentation: `WORKFLOW_ENHANCEMENTS_GUIDE.md`
