"""
Workflow Automation API
Handles automated workflow transitions and validations
"""

import frappe
from frappe import _
from frappe.model.workflow import apply_workflow

@frappe.whitelist()
def get_workflow_status(doctype, docname):
    """Get current workflow status for a document"""
    doc = frappe.get_doc(doctype, docname)
    
    workflow_state = doc.get("workflow_state")
    workflow_name = frappe.get_value("Workflow", {"document_type": doctype, "is_active": 1}, "name")
    
    if not workflow_name:
        return {"error": "No active workflow found"}
    
    # Get available actions
    workflow = frappe.get_doc("Workflow", workflow_name)
    available_actions = []
    
    for transition in workflow.transitions:
        if transition.state == workflow_state:
            if frappe.has_permission(doctype, "write") and transition.allowed in frappe.get_roles():
                available_actions.append({
                    "action": transition.action,
                    "next_state": transition.next_state,
                    "allowed_role": transition.allowed
                })
    
    return {
        "current_state": workflow_state,
        "workflow_name": workflow_name,
        "available_actions": available_actions,
        "document": doc.as_dict()
    }

@frappe.whitelist()
def apply_workflow_action(doctype, docname, action):
    """Apply a workflow action to a document"""
    try:
        doc = frappe.get_doc(doctype, docname)
        
        # Validate before transition
        validate_workflow_transition(doc, action)
        
        # Apply workflow
        apply_workflow(doc, action)
        
        # Post-transition actions
        post_workflow_actions(doc, action)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": f"Workflow action '{action}' applied successfully",
            "new_state": doc.workflow_state
        }
    
    except Exception as e:
        frappe.log_error(f"Workflow Action Error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def validate_workflow_transition(doc, action):
    """Validate document before workflow transition"""
    
    if doc.doctype == "Sales Order":
        validate_sales_order_transition(doc, action)
    elif doc.doctype == "Purchase Order":
        validate_purchase_order_transition(doc, action)

def validate_sales_order_transition(doc, action):
    """Validate Sales Order workflow transitions"""
    
    if action == "Start Production":
        if not doc.get("proforma_invoice_no"):
            frappe.throw(_("Proforma Invoice is required before starting production"))
    
    elif action == "Complete Production":
        if doc.get("production_status") != "Completed":
            frappe.throw(_("Production must be marked as completed"))
    
    elif action == "Complete Packing":
        if doc.get("packing_status") != "Completed":
            frappe.throw(_("Packing must be marked as completed"))
    
    elif action == "Dispatch Shipment":
        if not doc.get("shipment_reference"):
            frappe.throw(_("Shipment reference is required"))
    
    elif action == "Realize Forex":
        if not doc.get("forex_realization_date"):
            frappe.throw(_("Forex realization date is required"))

def validate_purchase_order_transition(doc, action):
    """Validate Purchase Order workflow transitions"""
    
    if action == "Clear Customs":
        if doc.get("customs_status") != "Cleared":
            frappe.throw(_("Customs must be marked as cleared"))
        if not doc.get("customs_clearance_date"):
            frappe.throw(_("Customs clearance date is required"))
    
    elif action == "Complete GRN":
        if not doc.get("grn_reference"):
            frappe.throw(_("GRN reference is required"))
        if doc.get("grn_status") != "Completed":
            frappe.throw(_("GRN must be marked as completed"))

    elif action == "Calculate Landed Cost":
        if not doc.get("grn_reference"):
            frappe.throw(_("GRN must be completed before calculating landed cost"))
    
    elif action == "Process Payment":
        if doc.get("landed_cost_status") != "Applied":
            frappe.throw(_("Landed cost must be applied before payment"))

def post_workflow_actions(doc, action):
    """Execute post-transition actions"""
    
    if doc.doctype == "Sales Order":
        post_sales_order_actions(doc, action)
    elif doc.doctype == "Purchase Order":
        post_purchase_order_actions(doc, action)

def post_sales_order_actions(doc, action):
    """Post-transition actions for Sales Order"""
    
    if action == "Start Production":
        doc.production_status = "In Progress"
        doc.save()
    
    elif action == "Complete Production":
        doc.production_status = "Completed"
        doc.save()
    
    elif action == "Start Packing":
        doc.packing_status = "In Progress"
        doc.save()
    
    elif action == "Complete Packing":
        doc.packing_status = "Completed"
        doc.save()

def post_purchase_order_actions(doc, action):
    """Post-transition actions for Purchase Order"""
    
    if action == "Start Customs":
        doc.customs_status = "In Progress"
        doc.save()
    
    elif action == "Clear Customs":
        doc.customs_status = "Cleared"
        doc.save()
    
    elif action == "Complete GRN":
        doc.grn_status = "Completed"
        doc.save()
    
    elif action == "Calculate Landed Cost":
        doc.landed_cost_status = "Calculated"
        doc.save()
    
    elif action == "Update Inventory":
        doc.landed_cost_status = "Applied"
        doc.save()

@frappe.whitelist()
def get_pending_approvals(user=None):
    """Get list of documents pending approval for user"""
    
    if not user:
        user = frappe.session.user
    
    user_roles = frappe.get_roles(user)
    pending = []
    
    # Get Sales Orders pending approval
    sales_orders = frappe.get_all(
        "Sales Order",
        filters={
            "workflow_state": ["in", ["Quotation Pending", "Proforma Invoice Issued"]],
            "docstatus": ["<", 2]
        },
        fields=["name", "customer", "grand_total", "workflow_state", "transaction_date"]
    )
    
    for so in sales_orders:
        pending.append({
            "doctype": "Sales Order",
            "name": so.name,
            "title": f"{so.customer} - {so.grand_total}",
            "state": so.workflow_state,
            "date": so.transaction_date
        })
    
    # Get Purchase Orders pending approval
    purchase_orders = frappe.get_all(
        "Purchase Order",
        filters={
            "workflow_state": ["in", ["Purchase Request", "PO Created"]],
            "docstatus": ["<", 2]
        },
        fields=["name", "supplier", "grand_total", "workflow_state", "transaction_date"]
    )
    
    for po in purchase_orders:
        pending.append({
            "doctype": "Purchase Order",
            "name": po.name,
            "title": f"{po.supplier} - {po.grand_total}",
            "state": po.workflow_state,
            "date": po.transaction_date
        })
    
    return pending

@frappe.whitelist()
def get_workflow_analytics(doctype, from_date=None, to_date=None):
    """Get workflow analytics and metrics"""
    
    if not from_date:
        from_date = frappe.utils.add_days(frappe.utils.today(), -30)
    if not to_date:
        to_date = frappe.utils.today()
    
    # Get workflow state distribution
    state_distribution = frappe.db.sql(f"""
        SELECT workflow_state, COUNT(*) as count
        FROM `tab{doctype}`
        WHERE creation BETWEEN %s AND %s
        AND docstatus < 2
        GROUP BY workflow_state
    """, (from_date, to_date), as_dict=True)
    
    # Get average time in each state
    # This would require workflow history tracking
    
    # Get bottlenecks (states with most documents)
    bottlenecks = sorted(state_distribution, key=lambda x: x['count'], reverse=True)[:3]
    
    return {
        "state_distribution": state_distribution,
        "bottlenecks": bottlenecks,
        "date_range": {"from": from_date, "to": to_date}
    }

@frappe.whitelist()
def bulk_workflow_action(doctype, docnames, action):
    """Apply workflow action to multiple documents"""
    
    if isinstance(docnames, str):
        import json
        docnames = json.loads(docnames)
    
    results = []
    
    for docname in docnames:
        try:
            result = apply_workflow_action(doctype, docname, action)
            results.append({
                "docname": docname,
                "success": result.get("success"),
                "message": result.get("message") or result.get("error")
            })
        except Exception as e:
            results.append({
                "docname": docname,
                "success": False,
                "message": str(e)
            })
    
    return results

@frappe.whitelist()
def get_workflow_history(doctype, docname):
    """Get workflow transition history for a document"""
    
    # Get from Version doctype
    versions = frappe.get_all(
        "Version",
        filters={
            "ref_doctype": doctype,
            "docname": docname
        },
        fields=["name", "owner", "creation", "data"],
        order_by="creation desc"
    )
    
    history = []
    
    for version in versions:
        import json
        data = json.loads(version.data)
        
        if "changed" in data:
            for change in data["changed"]:
                if change[0] == "workflow_state":
                    history.append({
                        "date": version.creation,
                        "user": version.owner,
                        "from_state": change[1],
                        "to_state": change[2]
                    })
    
    return history
