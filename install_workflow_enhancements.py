#!/usr/bin/env python3
"""
Workflow Enhancements Installation Script
Creates customized workflows for Export Sales and Import Purchase flows
with strict stage-based approval mechanisms.
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.workflow.doctype.workflow.workflow import Workflow

def install_workflow_enhancements():
    """Main installation function"""
    print("Installing Workflow Enhancements...")
    
    # Create workflow states
    create_workflow_states()
    
    # Create workflow actions
    create_workflow_actions()
    
    # Create Export Sales Workflow
    create_export_sales_workflow()
    
    # Create Import Purchase Workflow
    create_import_purchase_workflow()
    
    # Add custom fields for workflow tracking
    add_workflow_custom_fields()
    
    # Create workflow notification templates
    create_workflow_notifications()
    
    frappe.db.commit()
    print("✓ Workflow Enhancements installed successfully!")

def create_workflow_states():
    """Create workflow states for both flows"""
    
    # Export Sales Flow States
    export_states = [
        {"name": "Lead", "style": "Info"},
        {"name": "Quotation Pending", "style": "Warning"},
        {"name": "Quotation Approved", "style": "Success"},
        {"name": "Sales Order Created", "style": "Primary"},
        {"name": "Proforma Invoice Issued", "style": "Info"},
        {"name": "Production In Progress", "style": "Warning"},
        {"name": "Production Complete", "style": "Success"},
        {"name": "Packing In Progress", "style": "Warning"},
        {"name": "Ready for Shipment", "style": "Success"},
        {"name": "Shipment Dispatched", "style": "Primary"},
        {"name": "Export Invoice Generated", "style": "Info"},
        {"name": "Payment Received", "style": "Success"},
        {"name": "Forex Realized", "style": "Success"},
        {"name": "Export Complete", "style": "Success"},
    ]
    
    # Import Purchase Flow States
    import_states = [
        {"name": "Purchase Request", "style": "Info"},
        {"name": "PR Approved", "style": "Success"},
        {"name": "PO Created", "style": "Primary"},
        {"name": "PO Approved", "style": "Success"},
        {"name": "Shipment In Transit", "style": "Warning"},
        {"name": "Customs Clearance", "style": "Warning"},
        {"name": "Customs Cleared", "style": "Success"},
        {"name": "GRN Pending", "style": "Warning"},
        {"name": "GRN Completed", "style": "Success"},
        {"name": "Landed Cost Calculated", "style": "Info"},
        {"name": "Inventory Updated", "style": "Success"},
        {"name": "Payment Pending", "style": "Warning"},
        {"name": "Payment Completed", "style": "Success"},
        {"name": "Import Complete", "style": "Success"},
    ]
    
    all_states = export_states + import_states
    
    for state in all_states:
        if not frappe.db.exists("Workflow State", state["name"]):
            doc = frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state["name"],
                "style": state["style"]
            })
            doc.insert(ignore_permissions=True)
            print(f"  Created Workflow State: {state['name']}")

def create_workflow_actions():
    """Create workflow actions"""
    
    actions = [
        "Submit for Approval",
        "Approve",
        "Reject",
        "Request Changes",
        "Start Production",
        "Complete Production",
        "Start Packing",
        "Complete Packing",
        "Dispatch Shipment",
        "Generate Invoice",
        "Confirm Payment",
        "Realize Forex",
        "Create PO",
        "Clear Customs",
        "Complete GRN",
        "Calculate Landed Cost",
        "Update Inventory",
        "Process Payment",
        "Submit",
        "Complete",
        "Start Customs",
        "Create GRN",
        "Request Payment"
    ]
    
    for action in actions:
        if not frappe.db.exists("Workflow Action Master", action):
            doc = frappe.get_doc({
                "doctype": "Workflow Action Master",
                "workflow_action_name": action
            })
            doc.insert(ignore_permissions=True)
            print(f"  Created Workflow Action: {action}")

def create_export_sales_workflow():
    """Create Export Sales Workflow"""
    
    workflow_name = "Export Sales Flow"
    
    if frappe.db.exists("Workflow", workflow_name):
        frappe.delete_doc("Workflow", workflow_name)
    
    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": workflow_name,
        "document_type": "Sales Order",
        "is_active": 1,
        "send_email_alert": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Lead",
                "doc_status": "0",
                "allow_edit": "Sales User",
                "is_optional_state": 0
            },
            {
                "state": "Quotation Pending",
                "doc_status": "0",
                "allow_edit": "Sales User",
                "is_optional_state": 0
            },
            {
                "state": "Quotation Approved",
                "doc_status": "0",
                "allow_edit": "Sales Manager",
                "is_optional_state": 0
            },
            {
                "state": "Sales Order Created",
                "doc_status": "1",
                "allow_edit": "Sales Manager",
                "is_optional_state": 0
            },
            {
                "state": "Proforma Invoice Issued",
                "doc_status": "1",
                "allow_edit": "Accounts User",
                "is_optional_state": 0
            },
            {
                "state": "Production In Progress",
                "doc_status": "1",
                "allow_edit": "Manufacturing User",
                "is_optional_state": 0
            },
            {
                "state": "Production Complete",
                "doc_status": "1",
                "allow_edit": "Manufacturing Manager",
                "is_optional_state": 0
            },
            {
                "state": "Packing In Progress",
                "doc_status": "1",
                "allow_edit": "Stock User",
                "is_optional_state": 0
            },
            {
                "state": "Ready for Shipment",
                "doc_status": "1",
                "allow_edit": "Stock Manager",
                "is_optional_state": 0
            },
            {
                "state": "Shipment Dispatched",
                "doc_status": "1",
                "allow_edit": "Stock Manager",
                "is_optional_state": 0
            },
            {
                "state": "Export Invoice Generated",
                "doc_status": "1",
                "allow_edit": "Accounts User",
                "is_optional_state": 0
            },
            {
                "state": "Payment Received",
                "doc_status": "1",
                "allow_edit": "Accounts Manager",
                "is_optional_state": 0
            },
            {
                "state": "Forex Realized",
                "doc_status": "1",
                "allow_edit": "Accounts Manager",
                "is_optional_state": 0
            },
            {
                "state": "Export Complete",
                "doc_status": "1",
                "allow_edit": "System Manager",
                "is_optional_state": 0
            },
        ],
        "transitions": [
            {
                "state": "Lead",
                "action": "Submit for Approval",
                "next_state": "Quotation Pending",
                "allowed": "Sales User",
                "allow_self_approval": 0
            },
            {
                "state": "Quotation Pending",
                "action": "Approve",
                "next_state": "Quotation Approved",
                "allowed": "Sales Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Quotation Pending",
                "action": "Reject",
                "next_state": "Lead",
                "allowed": "Sales Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Quotation Approved",
                "action": "Submit",
                "next_state": "Sales Order Created",
                "allowed": "Sales Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Sales Order Created",
                "action": "Generate Invoice",
                "next_state": "Proforma Invoice Issued",
                "allowed": "Accounts User",
                "allow_self_approval": 0
            },
            {
                "state": "Proforma Invoice Issued",
                "action": "Start Production",
                "next_state": "Production In Progress",
                "allowed": "Manufacturing User",
                "allow_self_approval": 0
            },
            {
                "state": "Production In Progress",
                "action": "Complete Production",
                "next_state": "Production Complete",
                "allowed": "Manufacturing Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Production Complete",
                "action": "Start Packing",
                "next_state": "Packing In Progress",
                "allowed": "Stock User",
                "allow_self_approval": 0
            },
            {
                "state": "Packing In Progress",
                "action": "Complete Packing",
                "next_state": "Ready for Shipment",
                "allowed": "Stock Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Ready for Shipment",
                "action": "Dispatch Shipment",
                "next_state": "Shipment Dispatched",
                "allowed": "Stock Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Shipment Dispatched",
                "action": "Generate Invoice",
                "next_state": "Export Invoice Generated",
                "allowed": "Accounts User",
                "allow_self_approval": 0
            },
            {
                "state": "Export Invoice Generated",
                "action": "Confirm Payment",
                "next_state": "Payment Received",
                "allowed": "Accounts Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Payment Received",
                "action": "Realize Forex",
                "next_state": "Forex Realized",
                "allowed": "Accounts Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Forex Realized",
                "action": "Complete",
                "next_state": "Export Complete",
                "allowed": "Accounts Manager",
                "allow_self_approval": 0
            },
        ]
    })
    
    workflow.insert(ignore_permissions=True)
    print(f"  Created Workflow: {workflow_name}")

def create_import_purchase_workflow():
    """Create Import Purchase Workflow"""
    
    workflow_name = "Import Purchase Flow"
    
    if frappe.db.exists("Workflow", workflow_name):
        frappe.delete_doc("Workflow", workflow_name)
    
    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": workflow_name,
        "document_type": "Purchase Order",
        "is_active": 1,
        "send_email_alert": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Purchase Request",
                "doc_status": "0",
                "allow_edit": "Purchase User",
                "is_optional_state": 0
            },
            {
                "state": "PR Approved",
                "doc_status": "0",
                "allow_edit": "Purchase Manager",
                "is_optional_state": 0
            },
            {
                "state": "PO Created",
                "doc_status": "0",
                "allow_edit": "Purchase User",
                "is_optional_state": 0
            },
            {
                "state": "PO Approved",
                "doc_status": "1",
                "allow_edit": "Purchase Manager",
                "is_optional_state": 0
            },
            {
                "state": "Shipment In Transit",
                "doc_status": "1",
                "allow_edit": "Stock User",
                "is_optional_state": 0
            },
            {
                "state": "Customs Clearance",
                "doc_status": "1",
                "allow_edit": "Stock User",
                "is_optional_state": 0
            },
            {
                "state": "Customs Cleared",
                "doc_status": "1",
                "allow_edit": "Stock Manager",
                "is_optional_state": 0
            },
            {
                "state": "GRN Pending",
                "doc_status": "1",
                "allow_edit": "Stock User",
                "is_optional_state": 0
            },
            {
                "state": "GRN Completed",
                "doc_status": "1",
                "allow_edit": "Stock Manager",
                "is_optional_state": 0
            },
            {
                "state": "Landed Cost Calculated",
                "doc_status": "1",
                "allow_edit": "Accounts User",
                "is_optional_state": 0
            },
            {
                "state": "Inventory Updated",
                "doc_status": "1",
                "allow_edit": "Stock Manager",
                "is_optional_state": 0
            },
            {
                "state": "Payment Pending",
                "doc_status": "1",
                "allow_edit": "Accounts User",
                "is_optional_state": 0
            },
            {
                "state": "Payment Completed",
                "doc_status": "1",
                "allow_edit": "Accounts Manager",
                "is_optional_state": 0
            },
            {
                "state": "Import Complete",
                "doc_status": "1",
                "allow_edit": "System Manager",
                "is_optional_state": 0
            },
        ],
        "transitions": [
            {
                "state": "Purchase Request",
                "action": "Approve",
                "next_state": "PR Approved",
                "allowed": "Purchase Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Purchase Request",
                "action": "Reject",
                "next_state": "Purchase Request",
                "allowed": "Purchase Manager",
                "allow_self_approval": 0
            },
            {
                "state": "PR Approved",
                "action": "Create PO",
                "next_state": "PO Created",
                "allowed": "Purchase User",
                "allow_self_approval": 0
            },
            {
                "state": "PO Created",
                "action": "Approve",
                "next_state": "PO Approved",
                "allowed": "Purchase Manager",
                "allow_self_approval": 0
            },
            {
                "state": "PO Created",
                "action": "Request Changes",
                "next_state": "PR Approved",
                "allowed": "Purchase Manager",
                "allow_self_approval": 0
            },
            {
                "state": "PO Approved",
                "action": "Dispatch Shipment",
                "next_state": "Shipment In Transit",
                "allowed": "Stock User",
                "allow_self_approval": 0
            },
            {
                "state": "Shipment In Transit",
                "action": "Start Customs",
                "next_state": "Customs Clearance",
                "allowed": "Stock User",
                "allow_self_approval": 0
            },
            {
                "state": "Customs Clearance",
                "action": "Clear Customs",
                "next_state": "Customs Cleared",
                "allowed": "Stock Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Customs Cleared",
                "action": "Create GRN",
                "next_state": "GRN Pending",
                "allowed": "Stock User",
                "allow_self_approval": 0
            },
            {
                "state": "GRN Pending",
                "action": "Complete GRN",
                "next_state": "GRN Completed",
                "allowed": "Stock Manager",
                "allow_self_approval": 0
            },
            {
                "state": "GRN Completed",
                "action": "Calculate Landed Cost",
                "next_state": "Landed Cost Calculated",
                "allowed": "Accounts User",
                "allow_self_approval": 0
            },
            {
                "state": "Landed Cost Calculated",
                "action": "Update Inventory",
                "next_state": "Inventory Updated",
                "allowed": "Stock Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Inventory Updated",
                "action": "Request Payment",
                "next_state": "Payment Pending",
                "allowed": "Accounts User",
                "allow_self_approval": 0
            },
            {
                "state": "Payment Pending",
                "action": "Process Payment",
                "next_state": "Payment Completed",
                "allowed": "Accounts Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Payment Completed",
                "action": "Complete",
                "next_state": "Import Complete",
                "allowed": "Accounts Manager",
                "allow_self_approval": 0
            },
        ]
    })
    
    workflow.insert(ignore_permissions=True)
    print(f"  Created Workflow: {workflow_name}")

def add_workflow_custom_fields():
    """Add custom fields for workflow tracking"""
    
    custom_fields = {
        "Sales Order": [
            {
                "fieldname": "export_workflow_section",
                "label": "Export Workflow",
                "fieldtype": "Section Break",
                "insert_after": "customer"
            },
            {
                "fieldname": "workflow_stage",
                "label": "Workflow Stage",
                "fieldtype": "Data",
                "read_only": 1,
                "insert_after": "export_workflow_section"
            },
            {
                "fieldname": "production_status",
                "label": "Production Status",
                "fieldtype": "Select",
                "options": "Not Started\nIn Progress\nCompleted",
                "insert_after": "workflow_stage"
            },
            {
                "fieldname": "packing_status",
                "label": "Packing Status",
                "fieldtype": "Select",
                "options": "Not Started\nIn Progress\nCompleted",
                "insert_after": "production_status"
            },
            {
                "fieldname": "forex_realization_date",
                "label": "Forex Realization Date",
                "fieldtype": "Date",
                "insert_after": "packing_status"
            },
            {
                "fieldname": "column_break_workflow",
                "fieldtype": "Column Break",
                "insert_after": "forex_realization_date"
            },
            {
                "fieldname": "proforma_invoice_no",
                "label": "Proforma Invoice No",
                "fieldtype": "Data",
                "insert_after": "column_break_workflow"
            },
            {
                "fieldname": "export_invoice_no",
                "label": "Export Invoice No",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "insert_after": "proforma_invoice_no"
            },
            {
                "fieldname": "shipment_reference",
                "label": "Shipment Reference",
                "fieldtype": "Link",
                "options": "Shipment",
                "insert_after": "export_invoice_no"
            },
        ],
        "Purchase Order": [
            {
                "fieldname": "import_workflow_section",
                "label": "Import Workflow",
                "fieldtype": "Section Break",
                "insert_after": "supplier"
            },
            {
                "fieldname": "workflow_stage",
                "label": "Workflow Stage",
                "fieldtype": "Data",
                "read_only": 1,
                "insert_after": "import_workflow_section"
            },
            {
                "fieldname": "customs_status",
                "label": "Customs Status",
                "fieldtype": "Select",
                "options": "Pending\nIn Progress\nCleared",
                "insert_after": "workflow_stage"
            },
            {
                "fieldname": "grn_status",
                "label": "GRN Status",
                "fieldtype": "Select",
                "options": "Pending\nPartial\nCompleted",
                "insert_after": "customs_status"
            },
            {
                "fieldname": "landed_cost_status",
                "label": "Landed Cost Status",
                "fieldtype": "Select",
                "options": "Not Calculated\nCalculated\nApplied",
                "insert_after": "grn_status"
            },
            {
                "fieldname": "column_break_import",
                "fieldtype": "Column Break",
                "insert_after": "landed_cost_status"
            },
            {
                "fieldname": "shipment_reference",
                "label": "Shipment Reference",
                "fieldtype": "Link",
                "options": "Shipment",
                "insert_after": "column_break_import"
            },
            {
                "fieldname": "customs_clearance_date",
                "label": "Customs Clearance Date",
                "fieldtype": "Date",
                "insert_after": "shipment_reference"
            },
            {
                "fieldname": "grn_reference",
                "label": "GRN Reference",
                "fieldtype": "Link",
                "options": "Purchase Receipt",
                "insert_after": "customs_clearance_date"
            },
            {
                "fieldname": "landed_cost_voucher",
                "label": "Landed Cost Voucher",
                "fieldtype": "Link",
                "options": "Landed Cost Voucher",
                "insert_after": "grn_reference"
            },
        ]
    }
    
    create_custom_fields(custom_fields, update=True)
    print("  Added workflow custom fields")

def create_workflow_notifications():
    """Create email notification templates for workflows"""
    
    # Skip notifications for now - they need to be created manually through UI
    # as the Workflow State Change event is not available in v15
    print("  Skipping notifications - create manually through Notification doctype")

if __name__ == "__main__":
    install_workflow_enhancements()
