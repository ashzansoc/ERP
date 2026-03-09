# Workflow Enhancements - Access Guide

## ✅ Installation Complete!

Your workflow enhancements have been successfully installed in your ERP system.

## Access Your ERP

**URL**: http://localhost:8080

## What's Been Installed

### 1. Workflows
- **Export Sales Flow** - Applied to Sales Order
- **Import Purchase Flow** - Applied to Purchase Order

### 2. Workflow States (28 total)
Export Sales: 14 stages from Lead to Export Complete
Import Purchase: 14 stages from Purchase Request to Import Complete

### 3. Custom Fields
**Sales Order**:
- Export Workflow Section
- Workflow Stage
- Production Status
- Packing Status
- Forex Realization Date
- Proforma Invoice No
- Export Invoice No
- Shipment Reference

**Purchase Order**:
- Import Workflow Section
- Workflow Stage
- Customs Status
- GRN Status
- Landed Cost Status
- Shipment Reference
- Customs Clearance Date
- GRN Reference
- Landed Cost Voucher

### 4. UI Enhancements
- Visual progress indicators
- Workflow timeline
- Quick action buttons
- Client-side scripts for both doctypes

## How to Test

### Test Export Sales Workflow

1. **Login to ERP** at http://localhost:8080

2. **Go to Sales Order**
   - Navigate to: Selling > Sales Order > New

3. **Create a New Sales Order**
   - Select a customer
   - Add items
   - Save the document

4. **Check Workflow**
   - You should see the "Export Workflow" section
   - Current state will be shown
   - Workflow actions will appear in the menu

5. **Progress Through Stages**
   - Use workflow actions to move through stages
   - Each stage requires specific role permissions

### Test Import Purchase Workflow

1. **Go to Purchase Order**
   - Navigate to: Buying > Purchase Order > New

2. **Create a New Purchase Order**
   - Select a supplier
   - Add items
   - Save the document

3. **Check Workflow**
   - You should see the "Import Workflow" section
   - Current state will be shown
   - Workflow actions will appear

4. **Progress Through Stages**
   - Use workflow actions to move through stages

## Viewing Workflows

### Method 1: Through Document
1. Open any Sales Order or Purchase Order
2. Look for the workflow section
3. Click on workflow actions in the menu

### Method 2: Through Workflow List
1. Go to: Setup > Workflow > Workflow
2. You'll see:
   - Export Sales Flow
   - Import Purchase Flow
3. Click to view/edit workflow details

### Method 3: Through Workflow States
1. Go to: Setup > Workflow > Workflow State
2. View all 28 workflow states
3. See their colors and styles

## Workflow Actions

### Export Sales Flow Actions
- Submit for Approval
- Approve / Reject
- Start Production
- Complete Production
- Start Packing
- Complete Packing
- Dispatch Shipment
- Generate Invoice
- Confirm Payment
- Realize Forex
- Complete

### Import Purchase Flow Actions
- Approve / Reject
- Create PO
- Request Changes
- Dispatch Shipment
- Start Customs
- Clear Customs
- Create GRN
- Complete GRN
- Calculate Landed Cost
- Update Inventory
- Request Payment
- Process Payment
- Complete

## Role Requirements

Make sure users have these roles assigned:

**For Export Sales**:
- Sales User
- Sales Manager
- Manufacturing User
- Manufacturing Manager
- Stock User
- Stock Manager
- Accounts User
- Accounts Manager

**For Import Purchase**:
- Purchase User
- Purchase Manager
- Stock User
- Stock Manager
- Accounts User
- Accounts Manager

## Assigning Roles

1. Go to: Users and Permissions > User
2. Select a user
3. Scroll to "Roles" section
4. Add required roles
5. Save

## Troubleshooting

### Workflow Not Visible
- Clear browser cache (Ctrl+Shift+R)
- Clear ERPNext cache: `docker compose -f frappe_docker/compose.yaml exec backend bench --site localhost clear-cache`
- Reload the page

### Cannot See Workflow Actions
- Check if user has required role
- Verify workflow is active
- Check document status (Draft/Submitted)

### Custom Fields Not Showing
- Reload the form
- Check if fields are hidden by permissions
- Clear cache

## API Access

The workflow automation API is available at:
- `api.workflow_automation.get_workflow_status`
- `api.workflow_automation.apply_workflow_action`
- `api.workflow_automation.get_pending_approvals`
- `api.workflow_automation.get_workflow_analytics`

## Next Steps

1. **Assign Roles**: Give users appropriate roles
2. **Test Workflows**: Create test documents and progress through stages
3. **Customize**: Modify workflows as needed through UI
4. **Setup Notifications**: Create email notifications for state changes
5. **Train Users**: Show team members how to use workflows

## Customization

### To Modify Workflows
1. Go to: Setup > Workflow > Workflow
2. Select the workflow
3. Edit states and transitions
4. Save changes

### To Add More States
1. Go to: Setup > Workflow > Workflow State
2. Create new state
3. Add to workflow transitions

### To Change Permissions
1. Edit the workflow
2. Modify "Allow Edit" for each state
3. Update transition permissions

## Support Commands

```bash
# Clear cache
docker compose -f frappe_docker/compose.yaml exec backend bench --site localhost clear-cache

# Restart services
docker compose -f frappe_docker/compose.yaml restart

# View logs
docker compose -f frappe_docker/compose.yaml logs -f backend

# Access console
docker compose -f frappe_docker/compose.yaml exec backend bench --site localhost console
```

## Documentation Files

- `WORKFLOW_ENHANCEMENTS_GUIDE.md` - Complete guide
- `WORKFLOW_QUICK_REFERENCE.md` - Quick reference
- `WORKFLOW_IMPLEMENTATION_SUMMARY.md` - Technical details
- `WORKFLOW_ACCESS_GUIDE.md` - This file

## Success! 🎉

Your workflow enhancements are now live and ready to use. Access your ERP at http://localhost:8080 and start testing!
