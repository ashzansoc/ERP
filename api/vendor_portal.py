"""
Vendor Portal API
Handles vendor document uploads, invoice submissions, and PO tracking
"""

import frappe
from frappe import _
from frappe.utils import now, get_datetime, add_days
import json


@frappe.whitelist()
def get_vendor_dashboard(vendor_id=None):
    """Get vendor dashboard with key metrics and recent activities"""
    if not vendor_id:
        vendor_id = frappe.session.user
    
    # Get vendor details
    vendor = frappe.get_doc("Supplier", {"email_id": vendor_id})
    
    dashboard_data = {
        "vendor_name": vendor.supplier_name,
        "vendor_id": vendor.name,
        "statistics": {
            "open_pos": get_open_purchase_orders(vendor.name),
            "pending_invoices": get_pending_invoices(vendor.name),
            "pending_documents": get_pending_documents(vendor.name),
            "total_shipments": get_active_shipments(vendor.name)
        },
        "recent_activities": get_recent_activities(vendor.name),
        "pending_actions": get_pending_actions(vendor.name)
    }
    
    return dashboard_data


@frappe.whitelist()
def upload_vendor_document(vendor_id, document_type, reference_doc, reference_name, file_data):
    """Upload vendor document with categorization"""
    try:
        # Create file attachment
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": file_data.get("filename"),
            "attached_to_doctype": reference_doc,
            "attached_to_name": reference_name,
            "is_private": 1,
            "content": file_data.get("content")
        })
        file_doc.insert(ignore_permissions=True)
        
        # Create document log
        doc_log = frappe.get_doc({
            "doctype": "Vendor Document Log",
            "vendor": vendor_id,
            "document_type": document_type,
            "reference_doctype": reference_doc,
            "reference_name": reference_name,
            "file_url": file_doc.file_url,
            "upload_date": now(),
            "status": "Submitted",
            "uploaded_by": frappe.session.user
        })
        doc_log.insert(ignore_permissions=True)
        
        # Send notification to internal team
        notify_document_upload(vendor_id, document_type, reference_name)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Document uploaded successfully"),
            "document_id": doc_log.name,
            "file_url": file_doc.file_url
        }
    
    except Exception as e:
        frappe.log_error(f"Vendor document upload failed: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def submit_invoice(vendor_id, purchase_order, invoice_data):
    """Submit invoice for approval"""
    try:
        invoice_data = json.loads(invoice_data) if isinstance(invoice_data, str) else invoice_data
        
        # Create Purchase Invoice
        invoice = frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": vendor_id,
            "bill_no": invoice_data.get("invoice_number"),
            "bill_date": invoice_data.get("invoice_date"),
            "purchase_order": purchase_order,
            "items": invoice_data.get("items", []),
            "workflow_state": "Pending Approval",
            "submitted_via_portal": 1
        })
        invoice.insert(ignore_permissions=True)
        
        # Create approval workflow
        create_invoice_approval_workflow(invoice.name, vendor_id)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Invoice submitted for approval"),
            "invoice_id": invoice.name
        }
    
    except Exception as e:
        frappe.log_error(f"Invoice submission failed: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_purchase_orders(vendor_id, status=None):
    """Get purchase orders for vendor"""
    filters = {"supplier": vendor_id}
    if status:
        filters["status"] = status
    
    pos = frappe.get_all(
        "Purchase Order",
        filters=filters,
        fields=["name", "transaction_date", "grand_total", "status", "delivery_date"],
        order_by="transaction_date desc"
    )
    
    return pos


@frappe.whitelist()
def get_invoice_status(invoice_id):
    """Get invoice approval status and history"""
    invoice = frappe.get_doc("Purchase Invoice", invoice_id)
    
    approval_history = frappe.get_all(
        "Invoice Approval Log",
        filters={"invoice": invoice_id},
        fields=["approver", "status", "comments", "approval_date"],
        order_by="approval_date desc"
    )
    
    return {
        "invoice_number": invoice.bill_no,
        "status": invoice.workflow_state,
        "current_approver": get_current_approver(invoice_id),
        "approval_history": approval_history,
        "payment_status": invoice.status
    }


# Helper functions

def get_open_purchase_orders(vendor):
    """Count open purchase orders"""
    return frappe.db.count("Purchase Order", {
        "supplier": vendor,
        "status": ["in", ["To Receive and Bill", "To Receive", "To Bill"]]
    })


def get_pending_invoices(vendor):
    """Count pending invoices"""
    return frappe.db.count("Purchase Invoice", {
        "supplier": vendor,
        "workflow_state": ["in", ["Pending Approval", "Under Review"]]
    })


def get_pending_documents(vendor):
    """Count pending document submissions"""
    return frappe.db.count("Vendor Document Log", {
        "vendor": vendor,
        "status": "Pending"
    })


def get_active_shipments(vendor):
    """Count active shipments"""
    return frappe.db.count("Shipment", {
        "supplier": vendor,
        "status": ["not in", ["Delivered", "Cancelled"]]
    })


def get_recent_activities(vendor):
    """Get recent activities for vendor"""
    activities = []
    
    # Recent POs
    recent_pos = frappe.get_all(
        "Purchase Order",
        filters={"supplier": vendor},
        fields=["name", "transaction_date", "grand_total"],
        order_by="transaction_date desc",
        limit=5
    )
    
    for po in recent_pos:
        activities.append({
            "type": "Purchase Order",
            "reference": po.name,
            "date": po.transaction_date,
            "description": f"PO {po.name} - {po.grand_total}"
        })
    
    return activities


def get_pending_actions(vendor):
    """Get pending actions for vendor"""
    actions = []
    
    # Documents needed
    pending_docs = frappe.get_all(
        "Vendor Document Request",
        filters={"vendor": vendor, "status": "Pending"},
        fields=["name", "document_type", "due_date", "reference_name"]
    )
    
    for doc in pending_docs:
        actions.append({
            "type": "Document Required",
            "description": f"{doc.document_type} needed for {doc.reference_name}",
            "due_date": doc.due_date,
            "priority": "High" if get_datetime(doc.due_date) < get_datetime(add_days(now(), 2)) else "Medium"
        })
    
    return actions


def notify_document_upload(vendor, document_type, reference):
    """Send notification on document upload"""
    # Get relevant users to notify
    users = frappe.get_all(
        "User",
        filters={"role": ["in", ["Purchase Manager", "Purchase User"]]},
        fields=["email"]
    )
    
    for user in users:
        frappe.sendmail(
            recipients=user.email,
            subject=f"New Document Uploaded by {vendor}",
            message=f"Document Type: {document_type}<br>Reference: {reference}",
            reference_doctype="Vendor Document Log",
            reference_name=reference
        )


def create_invoice_approval_workflow(invoice_id, vendor):
    """Create approval workflow for invoice"""
    # Get approval hierarchy
    approvers = get_invoice_approvers(vendor)
    
    for idx, approver in enumerate(approvers):
        frappe.get_doc({
            "doctype": "Invoice Approval Log",
            "invoice": invoice_id,
            "approver": approver,
            "approval_level": idx + 1,
            "status": "Pending" if idx == 0 else "Waiting",
            "created_date": now()
        }).insert(ignore_permissions=True)


def get_invoice_approvers(vendor):
    """Get list of approvers for vendor invoices"""
    # Default approval hierarchy
    return ["purchase.manager@company.com", "finance.manager@company.com"]


def get_current_approver(invoice_id):
    """Get current approver for invoice"""
    approval = frappe.get_value(
        "Invoice Approval Log",
        {"invoice": invoice_id, "status": "Pending"},
        "approver"
    )
    return approval
