# Workflow Enhancements Guide

## Overview

This system implements comprehensive workflow management for Export Sales and Import Purchase operations with strict stage-based approvals.

## Export Sales Flow

### Workflow Stages

```
Lead → Quotation → Sales Order → Proforma Invoice → Production → 
Packing → Shipment → Export Invoice → Payment → Forex Realization
```

### Stage Details

1. **Lead**: Initial customer inquiry
   - Role: Sales User
   - Action: Submit for Approval

2. **Quotation Pending**: Awaiting manager approval
   - Role: Sales Manager
   - Actions: Approve / Reject

3. **Quotation Approved**: Ready for order creation
   - Role: Sales Manager
   - Action: Submit (creates Sales Order)

4. **Sales Order Created**: Order confirmed
   - Role: Sales Manager
   - Action: Generate Proforma Invoice

5. **Proforma Invoice Issued**: PI sent to customer
   - Role: Accounts User
   - Action: Start Production

6. **Production In Progress**: Manufacturing underway
   - Role: Manufacturing User
   - Action: Complete Production

7. **Production Complete**: Ready for packing
   - Role: Manufacturing Manager
   - Action: Start Packing

8. **Packing In Progress**: Items being packed
   - Role: Stock User
   - Action: Complete Packing

9. **Ready for Shipment**: Packed and ready
   - Role: Stock Manager
   - Action: Dispatch Shipment

10. **Shipment Dispatched**: Goods shipped
    - Role: Stock Manager
    - Action: Generate Export Invoice

11. **Export Invoice Generated**: Final invoice created
    - Role: Accounts User
    - Action: Confirm Payment

12. **Payment Received**: Customer payment received
    - Role: Accounts Manager
    - Action: Realize Forex

13. **Forex Realized**: Foreign exchange completed
    - Role: Accounts Manager
    - Action: Complete

14. **Export Complete**: Transaction closed

## Import Purchase Flow

### Workflow Stages

```
Purchase Request → PO → Shipment → Customs → GRN → 
Landed Cost → Inventory → Vendor Payment
```

### Stage Details

1. **Purchase Request**: Initial requirement
   - Role: Purchase User
   - Action: Submit for Approval

2. **PR Approved**: Request approved
   - Role: Purchase Manager
   - Action: Create PO

3. **PO Created**: Purchase order drafted
   - Role: Purchase User
   - Action: Submit for Approval

4. **PO Approved**: Order confirmed with supplier
   - Role: Purchase Manager
   - Action: Track Shipment

5. **Shipment In Transit**: Goods in transit
   - Role: Stock User
   - Action: Start Customs Clearance

6. **Customs Clearance**: Clearing customs
   - Role: Stock User
   - Action: Clear Customs

7. **Customs Cleared**: Customs completed
   - Role: Stock Manager
   - Action: Create GRN

8. **GRN Pending**: Awaiting goods receipt
   - Role: Stock User
   - Action: Complete GRN

9. **GRN Completed**: Goods received
   - Role: Stock Manager
   - Action: Calculate Landed Cost

10. **Landed Cost Calculated**: Costs computed
    - Role: Accounts User
    - Action: Update Inventory

11. **Inventory Updated**: Stock updated
    - Role: Stock Manager
    - Action: Request Payment

12. **Payment Pending**: Awaiting payment approval
    - Role: Accounts User
    - Action: Process Payment

13. **Payment Completed**: Vendor paid
    - Role: Accounts Manager
    - Action: Complete

14. **Import Complete**: Transaction closed

## Installation

```bash
chmod +x install_workflow_enhancements.sh
./install_workflow_enhancements.sh <site-name>
```

## Configuration

### Role Assignment

Ensure users are assigned to appropriate roles:

- Sales User / Sales Manager
- Purchase User / Purchase Manager
- Manufacturing User / Manufacturing Manager
- Stock User / Stock Manager
- Accounts User / Accounts Manager

### Approval Rules

All transitions require approval from designated roles.
Self-approval is disabled for all critical transitions.

## Custom Fields

### Sales Order Fields

- Workflow Stage
- Production Status
- Packing Status
- Forex Realization Date
- Proforma Invoice No
- Export Invoice No
- Shipment Reference

### Purchase Order Fields

- Workflow Stage
- Customs Status
- GRN Status
- Landed Cost Status
- Shipment Reference
- Customs Clearance Date
- GRN Reference
- Landed Cost Voucher

## Email Notifications

Automatic notifications are sent for:

- Quotation approval requests
- Production start/completion
- PO approval requests
- Customs clearance updates
- Payment confirmations

## Usage

### For Sales Orders

1. Create Sales Order from Lead/Quotation
2. Submit for approval
3. Manager approves
4. System guides through each stage
5. Complete all stages to close

### For Purchase Orders

1. Create Purchase Request
2. Get approval
3. Create and approve PO
4. Track through customs and GRN
5. Calculate landed costs
6. Process payment

## Best Practices

1. Complete each stage before moving to next
2. Ensure all required documents are attached
3. Update status fields regularly
4. Review approval queues daily
5. Monitor workflow reports

## Troubleshooting

### Workflow Not Appearing

- Check if workflow is active
- Verify user has required role
- Clear cache and reload

### Cannot Transition

- Verify current state
- Check user permissions
- Ensure required fields are filled

### Email Notifications Not Sent

- Check notification settings
- Verify email configuration
- Check user email addresses

## Reports

Access workflow reports from:

- Workflow State Report
- Pending Approvals Report
- Stage Duration Analysis
- Bottleneck Identification

## Support

For issues or customization requests, contact your system administrator.
