"""
Freight Forwarder Portal API
Handles freight quotes, shipment updates, and milestone tracking
"""

import frappe
from frappe import _
from frappe.utils import now, get_datetime, flt
import json


@frappe.whitelist()
def get_freight_dashboard(forwarder_id=None):
    """Get freight forwarder dashboard"""
    if not forwarder_id:
        forwarder_id = frappe.session.user
    
    forwarder = frappe.get_doc("Supplier", {"email_id": forwarder_id, "supplier_type": "Freight Forwarder"})
    
    dashboard_data = {
        "forwarder_name": forwarder.supplier_name,
        "forwarder_id": forwarder.name,
        "statistics": {
            "active_shipments": get_active_shipments_count(forwarder.name),
            "pending_quotes": get_pending_quotes_count(forwarder.name),
            "pending_updates": get_pending_updates_count(forwarder.name),
            "completed_shipments": get_completed_shipments_count(forwarder.name)
        },
        "recent_shipments": get_recent_shipments(forwarder.name),
        "quote_requests": get_quote_requests(forwarder.name)
    }
    
    return dashboard_data


@frappe.whitelist()
def submit_freight_quote(forwarder_id, quote_request_id, quote_data):
    """Submit freight quote for comparison"""
    try:
        quote_data = json.loads(quote_data) if isinstance(quote_data, str) else quote_data
        
        quote = frappe.get_doc({
            "doctype": "Freight Quote",
            "freight_forwarder": forwarder_id,
            "quote_request": quote_request_id,
            "quote_number": quote_data.get("quote_number"),
            "quote_date": now(),
            "valid_until": quote_data.get("valid_until"),
            "origin_port": quote_data.get("origin_port"),
            "destination_port": quote_data.get("destination_port"),
            "shipping_mode": quote_data.get("shipping_mode"),
            "transit_time_days": quote_data.get("transit_time_days"),
            "base_freight_cost": quote_data.get("base_freight_cost"),
            "fuel_surcharge": quote_data.get("fuel_surcharge", 0),
            "documentation_fee": quote_data.get("documentation_fee", 0),
            "handling_charges": quote_data.get("handling_charges", 0),
            "insurance_cost": quote_data.get("insurance_cost", 0),
            "other_charges": quote_data.get("other_charges", 0),
            "total_cost": calculate_total_quote_cost(quote_data),
            "currency": quote_data.get("currency", "USD"),
            "service_level": quote_data.get("service_level"),
            "special_notes": quote_data.get("special_notes"),
            "status": "Submitted"
        })
        quote.insert(ignore_permissions=True)
        
        # Notify customer about new quote
        notify_new_quote(quote_request_id, forwarder_id)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Quote submitted successfully"),
            "quote_id": quote.name
        }
    
    except Exception as e:
        frappe.log_error(f"Freight quote submission failed: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_shipment_milestone(shipment_id, milestone_data):
    """Update shipment milestone with documents"""
    try:
        milestone_data = json.loads(milestone_data) if isinstance(milestone_data, str) else milestone_data
        
        milestone = frappe.get_doc({
            "doctype": "Shipment Milestone",
            "shipment": shipment_id,
            "milestone_type": milestone_data.get("milestone_type"),
            "milestone_date": milestone_data.get("milestone_date", now()),
            "location": milestone_data.get("location"),
            "status": milestone_data.get("status"),
            "notes": milestone_data.get("notes"),
            "updated_by": frappe.session.user,
            "eta_update": milestone_data.get("eta_update"),
            "delay_reason": milestone_data.get("delay_reason")
        })
        milestone.insert(ignore_permissions=True)
        
        # Update shipment status
        update_shipment_status(shipment_id, milestone_data.get("milestone_type"))
        
        # Send notifications
        notify_milestone_update(shipment_id, milestone_data.get("milestone_type"))
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Milestone updated successfully"),
            "milestone_id": milestone.name
        }
    
    except Exception as e:
        frappe.log_error(f"Milestone update failed: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_quote_comparison(quote_request_id):
    """Get all quotes for comparison"""
    quotes = frappe.get_all(
        "Freight Quote",
        filters={"quote_request": quote_request_id, "status": ["!=", "Rejected"]},
        fields=[
            "name", "freight_forwarder", "quote_number", "total_cost", 
            "transit_time_days", "service_level", "valid_until", "quote_date",
            "base_freight_cost", "fuel_surcharge", "documentation_fee",
            "handling_charges", "insurance_cost", "currency"
        ],
        order_by="total_cost asc"
    )
    
    # Add forwarder details
    for quote in quotes:
        forwarder = frappe.get_doc("Supplier", quote.freight_forwarder)
        quote["forwarder_name"] = forwarder.supplier_name
        quote["forwarder_rating"] = get_forwarder_rating(quote.freight_forwarder)
    
    # Calculate comparison metrics
    if quotes:
        costs = [q.total_cost for q in quotes]
        transit_times = [q.transit_time_days for q in quotes]
        
        comparison_summary = {
            "total_quotes": len(quotes),
            "lowest_cost": min(costs),
            "highest_cost": max(costs),
            "average_cost": sum(costs) / len(costs),
            "fastest_transit": min(transit_times),
            "slowest_transit": max(transit_times)
        }
    else:
        comparison_summary = {}
    
    return {
        "quotes": quotes,
        "summary": comparison_summary
    }


@frappe.whitelist()
def get_shipment_details(shipment_id):
    """Get detailed shipment information with milestones"""
    shipment = frappe.get_doc("Shipment", shipment_id)
    
    milestones = frappe.get_all(
        "Shipment Milestone",
        filters={"shipment": shipment_id},
        fields=["milestone_type", "milestone_date", "location", "status", "notes", "eta_update"],
        order_by="milestone_date desc"
    )
    
    documents = frappe.get_all(
        "File",
        filters={"attached_to_doctype": "Shipment", "attached_to_name": shipment_id},
        fields=["file_name", "file_url", "creation"]
    )
    
    return {
        "shipment": {
            "name": shipment.name,
            "status": shipment.status,
            "origin": shipment.origin_port,
            "destination": shipment.destination_port,
            "shipping_mode": shipment.shipping_mode,
            "estimated_arrival": shipment.estimated_arrival_date,
            "actual_arrival": shipment.actual_arrival_date
        },
        "milestones": milestones,
        "documents": documents,
        "container_details": get_container_details(shipment_id)
    }


@frappe.whitelist()
def upload_shipment_document(shipment_id, document_type, file_data):
    """Upload document for shipment"""
    try:
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": file_data.get("filename"),
            "attached_to_doctype": "Shipment",
            "attached_to_name": shipment_id,
            "is_private": 0,
            "content": file_data.get("content")
        })
        file_doc.insert(ignore_permissions=True)
        
        # Log document upload
        frappe.get_doc({
            "doctype": "Shipment Document Log",
            "shipment": shipment_id,
            "document_type": document_type,
            "file_url": file_doc.file_url,
            "uploaded_by": frappe.session.user,
            "upload_date": now()
        }).insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Document uploaded successfully"),
            "file_url": file_doc.file_url
        }
    
    except Exception as e:
        frappe.log_error(f"Shipment document upload failed: {str(e)}")
        return {"success": False, "message": str(e)}


# Helper functions

def get_active_shipments_count(forwarder):
    """Count active shipments"""
    return frappe.db.count("Shipment", {
        "freight_forwarder": forwarder,
        "status": ["not in", ["Delivered", "Cancelled"]]
    })


def get_pending_quotes_count(forwarder):
    """Count pending quote requests"""
    return frappe.db.count("Freight Quote Request", {
        "freight_forwarder": forwarder,
        "status": "Pending"
    })


def get_pending_updates_count(forwarder):
    """Count shipments needing updates"""
    return frappe.db.count("Shipment", {
        "freight_forwarder": forwarder,
        "status": ["in", ["In Transit", "At Port"]],
        "last_update": ["<", frappe.utils.add_days(now(), -2)]
    })


def get_completed_shipments_count(forwarder):
    """Count completed shipments this month"""
    return frappe.db.count("Shipment", {
        "freight_forwarder": forwarder,
        "status": "Delivered",
        "actual_arrival_date": [">=", frappe.utils.get_first_day(now())]
    })


def get_recent_shipments(forwarder):
    """Get recent shipments"""
    return frappe.get_all(
        "Shipment",
        filters={"freight_forwarder": forwarder},
        fields=["name", "status", "origin_port", "destination_port", "estimated_arrival_date"],
        order_by="creation desc",
        limit=10
    )


def get_quote_requests(forwarder):
    """Get pending quote requests"""
    return frappe.get_all(
        "Freight Quote Request",
        filters={"freight_forwarder": forwarder, "status": "Pending"},
        fields=["name", "origin_port", "destination_port", "cargo_type", "required_by_date"],
        order_by="required_by_date asc"
    )


def calculate_total_quote_cost(quote_data):
    """Calculate total quote cost"""
    total = flt(quote_data.get("base_freight_cost", 0))
    total += flt(quote_data.get("fuel_surcharge", 0))
    total += flt(quote_data.get("documentation_fee", 0))
    total += flt(quote_data.get("handling_charges", 0))
    total += flt(quote_data.get("insurance_cost", 0))
    total += flt(quote_data.get("other_charges", 0))
    return total


def notify_new_quote(quote_request_id, forwarder_id):
    """Notify customer about new quote"""
    request = frappe.get_doc("Freight Quote Request", quote_request_id)
    frappe.sendmail(
        recipients=request.requested_by,
        subject=f"New Freight Quote Received - {quote_request_id}",
        message=f"A new quote has been submitted by {forwarder_id}. Please review in the portal.",
        reference_doctype="Freight Quote Request",
        reference_name=quote_request_id
    )


def update_shipment_status(shipment_id, milestone_type):
    """Update shipment status based on milestone"""
    status_map = {
        "Booking Confirmed": "Booked",
        "Cargo Loaded": "In Transit",
        "Departed Origin": "In Transit",
        "Arrived at Port": "At Port",
        "Customs Cleared": "Cleared",
        "Out for Delivery": "In Transit",
        "Delivered": "Delivered"
    }
    
    new_status = status_map.get(milestone_type)
    if new_status:
        frappe.db.set_value("Shipment", shipment_id, "status", new_status)


def notify_milestone_update(shipment_id, milestone_type):
    """Send notification on milestone update"""
    shipment = frappe.get_doc("Shipment", shipment_id)
    
    frappe.sendmail(
        recipients=shipment.customer_email,
        subject=f"Shipment Update - {shipment_id}",
        message=f"Milestone: {milestone_type}<br>Your shipment has been updated. Check the portal for details.",
        reference_doctype="Shipment",
        reference_name=shipment_id
    )


def get_forwarder_rating(forwarder_id):
    """Get forwarder performance rating"""
    # Calculate based on on-time delivery, customer feedback
    return 4.5  # Placeholder


def get_container_details(shipment_id):
    """Get container tracking details"""
    return frappe.get_all(
        "Shipment Container",
        filters={"parent": shipment_id},
        fields=["container_number", "container_type", "seal_number", "weight"]
    )
