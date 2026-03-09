#!/usr/bin/env python3
"""
Vendor & Freight Forwarder Portal Installation Script
Creates all necessary DocTypes, custom fields, and portal configurations
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def install_vendor_portal():
    """Main installation function"""
    print("🌍 Installing Vendor & Freight Forwarder Portal...")
    
    # Create DocTypes
    create_vendor_document_log()
    create_vendor_document_request()
    create_invoice_approval_log()
    create_freight_quote()
    create_freight_quote_request()
    create_shipment_milestone()
    create_shipment_document_log()
    
    # Add custom fields
    add_custom_fields()
    
    # Create portal pages
    create_portal_pages()
    
    # Set up roles and permissions
    setup_roles_and_permissions()
    
    # Create default workflows
    create_workflows()
    
    print("✅ Vendor & Freight Forwarder Portal installed successfully!")
    print("\nNext steps:")
    print("1. Configure portal branding in Portal Settings")
    print("2. Set up user roles for vendors and freight forwarders")
    print("3. Customize email templates")
    print("4. Test portal workflows")


def create_vendor_document_log():
    """Create Vendor Document Log DocType"""
    if frappe.db.exists("DocType", "Vendor Document Log"):
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Vendor Document Log",
        "module": "Buying",
        "custom": 1,
        "is_submittable": 0,
        "track_changes": 1,
        "fields": [
            {"fieldname": "vendor", "label": "Vendor", "fieldtype": "Link", "options": "Supplier", "reqd": 1},
            {"fieldname": "document_type", "label": "Document Type", "fieldtype": "Select", 
             "options": "Invoice\nPacking List\nCertificate\nTest Report\nOther", "reqd": 1},
            {"fieldname": "reference_doctype", "label": "Reference DocType", "fieldtype": "Data"},
            {"fieldname": "reference_name", "label": "Reference Name", "fieldtype": "Dynamic Link", 
             "options": "reference_doctype"},
            {"fieldname": "file_url", "label": "File URL", "fieldtype": "Attach"},
            {"fieldname": "upload_date", "label": "Upload Date", "fieldtype": "Datetime"},
            {"fieldname": "uploaded_by", "label": "Uploaded By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", 
             "options": "Pending\nSubmitted\nApproved\nRejected", "default": "Pending"},
            {"fieldname": "reviewed_by", "label": "Reviewed By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "review_date", "label": "Review Date", "fieldtype": "Datetime"},
            {"fieldname": "comments", "label": "Comments", "fieldtype": "Text"}
        ],
        "permissions": [
            {"role": "Vendor", "read": 1, "write": 1, "create": 1},
            {"role": "Purchase Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
        ]
    })
    doc.insert()
    print("✓ Created Vendor Document Log")


def create_vendor_document_request():
    """Create Vendor Document Request DocType"""
    if frappe.db.exists("DocType", "Vendor Document Request"):
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Vendor Document Request",
        "module": "Buying",
        "custom": 1,
        "fields": [
            {"fieldname": "vendor", "label": "Vendor", "fieldtype": "Link", "options": "Supplier", "reqd": 1},
            {"fieldname": "document_type", "label": "Document Type", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "reference_name", "label": "Reference", "fieldtype": "Data"},
            {"fieldname": "due_date", "label": "Due Date", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", 
             "options": "Pending\nReceived\nOverdue", "default": "Pending"},
            {"fieldname": "requested_by", "label": "Requested By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "request_date", "label": "Request Date", "fieldtype": "Date", "default": "Today"},
            {"fieldname": "description", "label": "Description", "fieldtype": "Text"}
        ],
        "permissions": [
            {"role": "Purchase Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Vendor", "read": 1}
        ]
    })
    doc.insert()
    print("✓ Created Vendor Document Request")


def create_invoice_approval_log():
    """Create Invoice Approval Log DocType"""
    if frappe.db.exists("DocType", "Invoice Approval Log"):
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Invoice Approval Log",
        "module": "Accounts",
        "custom": 1,
        "fields": [
            {"fieldname": "invoice", "label": "Invoice", "fieldtype": "Link", 
             "options": "Purchase Invoice", "reqd": 1},
            {"fieldname": "approver", "label": "Approver", "fieldtype": "Link", "options": "User", "reqd": 1},
            {"fieldname": "approval_level", "label": "Approval Level", "fieldtype": "Int"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", 
             "options": "Pending\nApproved\nRejected\nWaiting", "default": "Pending"},
            {"fieldname": "approval_date", "label": "Approval Date", "fieldtype": "Datetime"},
            {"fieldname": "comments", "label": "Comments", "fieldtype": "Text"},
            {"fieldname": "created_date", "label": "Created Date", "fieldtype": "Datetime"}
        ],
        "permissions": [
            {"role": "Purchase Manager", "read": 1, "write": 1},
            {"role": "Accounts Manager", "read": 1, "write": 1}
        ]
    })
    doc.insert()
    print("✓ Created Invoice Approval Log")


def create_freight_quote():
    """Create Freight Quote DocType"""
    if frappe.db.exists("DocType", "Freight Quote"):
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Freight Quote",
        "module": "Stock",
        "custom": 1,
        "is_submittable": 1,
        "fields": [
            {"fieldname": "freight_forwarder", "label": "Freight Forwarder", "fieldtype": "Link", 
             "options": "Supplier", "reqd": 1},
            {"fieldname": "quote_request", "label": "Quote Request", "fieldtype": "Link", 
             "options": "Freight Quote Request"},
            {"fieldname": "quote_number", "label": "Quote Number", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "quote_date", "label": "Quote Date", "fieldtype": "Date", "default": "Today"},
            {"fieldname": "valid_until", "label": "Valid Until", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Route Details"},
            {"fieldname": "origin_port", "label": "Origin Port", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "destination_port", "label": "Destination Port", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "shipping_mode", "label": "Shipping Mode", "fieldtype": "Select", 
             "options": "Sea\nAir\nRoad\nRail", "reqd": 1},
            {"fieldname": "transit_time_days", "label": "Transit Time (Days)", "fieldtype": "Int"},
            {"fieldname": "service_level", "label": "Service Level", "fieldtype": "Select", 
             "options": "Standard\nExpress\nEconomy"},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Cost Breakdown"},
            {"fieldname": "base_freight_cost", "label": "Base Freight Cost", "fieldtype": "Currency", "reqd": 1},
            {"fieldname": "fuel_surcharge", "label": "Fuel Surcharge", "fieldtype": "Currency"},
            {"fieldname": "documentation_fee", "label": "Documentation Fee", "fieldtype": "Currency"},
            {"fieldname": "handling_charges", "label": "Handling Charges", "fieldtype": "Currency"},
            {"fieldname": "insurance_cost", "label": "Insurance Cost", "fieldtype": "Currency"},
            {"fieldname": "other_charges", "label": "Other Charges", "fieldtype": "Currency"},
            {"fieldname": "total_cost", "label": "Total Cost", "fieldtype": "Currency", "read_only": 1},
            {"fieldname": "currency", "label": "Currency", "fieldtype": "Link", "options": "Currency", 
             "default": "USD"},
            {"fieldname": "section_break_3", "fieldtype": "Section Break"},
            {"fieldname": "special_notes", "label": "Special Notes", "fieldtype": "Text"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", 
             "options": "Draft\nSubmitted\nAccepted\nRejected", "default": "Draft"}
        ],
        "permissions": [
            {"role": "Freight Forwarder", "read": 1, "write": 1, "create": 1, "submit": 1},
            {"role": "Purchase Manager", "read": 1, "write": 1}
        ]
    })
    doc.insert()
    print("✓ Created Freight Quote")


def create_freight_quote_request():
    """Create Freight Quote Request DocType"""
    if frappe.db.exists("DocType", "Freight Quote Request"):
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Freight Quote Request",
        "module": "Stock",
        "custom": 1,
        "fields": [
            {"fieldname": "origin_port", "label": "Origin Port", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "destination_port", "label": "Destination Port", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "cargo_type", "label": "Cargo Type", "fieldtype": "Data"},
            {"fieldname": "cargo_weight", "label": "Cargo Weight (kg)", "fieldtype": "Float"},
            {"fieldname": "cargo_volume", "label": "Cargo Volume (cbm)", "fieldtype": "Float"},
            {"fieldname": "required_by_date", "label": "Required By Date", "fieldtype": "Date"},
            {"fieldname": "freight_forwarder", "label": "Freight Forwarder", "fieldtype": "Link", 
             "options": "Supplier"},
            {"fieldname": "requested_by", "label": "Requested By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", 
             "options": "Pending\nQuoted\nAccepted\nClosed", "default": "Pending"}
        ],
        "permissions": [
            {"role": "Purchase Manager", "read": 1, "write": 1, "create": 1},
            {"role": "Freight Forwarder", "read": 1}
        ]
    })
    doc.insert()
    print("✓ Created Freight Quote Request")


def create_shipment_milestone():
    """Create Shipment Milestone DocType"""
    if frappe.db.exists("DocType", "Shipment Milestone"):
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Shipment Milestone",
        "module": "Stock",
        "custom": 1,
        "fields": [
            {"fieldname": "shipment", "label": "Shipment", "fieldtype": "Link", "options": "Shipment", "reqd": 1},
            {"fieldname": "milestone_type", "label": "Milestone Type", "fieldtype": "Select", 
             "options": "Booking Confirmed\nCargo Loaded\nDeparted Origin\nIn Transit\nArrived at Port\nCustoms Cleared\nOut for Delivery\nDelivered", 
             "reqd": 1},
            {"fieldname": "milestone_date", "label": "Milestone Date", "fieldtype": "Datetime", "reqd": 1},
            {"fieldname": "location", "label": "Location", "fieldtype": "Data"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", 
             "options": "On Time\nDelayed\nCompleted", "default": "On Time"},
            {"fieldname": "notes", "label": "Notes", "fieldtype": "Text"},
            {"fieldname": "updated_by", "label": "Updated By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "eta_update", "label": "Updated ETA", "fieldtype": "Datetime"},
            {"fieldname": "delay_reason", "label": "Delay Reason", "fieldtype": "Text"}
        ],
        "permissions": [
            {"role": "Freight Forwarder", "read": 1, "write": 1, "create": 1},
            {"role": "Stock User", "read": 1}
        ]
    })
    doc.insert()
    print("✓ Created Shipment Milestone")


def create_shipment_document_log():
    """Create Shipment Document Log DocType"""
    if frappe.db.exists("DocType", "Shipment Document Log"):
        return
    
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Shipment Document Log",
        "module": "Stock",
        "custom": 1,
        "fields": [
            {"fieldname": "shipment", "label": "Shipment", "fieldtype": "Link", "options": "Shipment", "reqd": 1},
            {"fieldname": "document_type", "label": "Document Type", "fieldtype": "Select", 
             "options": "Bill of Lading\nPacking List\nCommercial Invoice\nCertificate of Origin\nCustoms Declaration\nOther"},
            {"fieldname": "file_url", "label": "File URL", "fieldtype": "Attach"},
            {"fieldname": "uploaded_by", "label": "Uploaded By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "upload_date", "label": "Upload Date", "fieldtype": "Datetime"}
        ],
        "permissions": [
            {"role": "Freight Forwarder", "read": 1, "write": 1, "create": 1},
            {"role": "Stock User", "read": 1}
        ]
    })
    doc.insert()
    print("✓ Created Shipment Document Log")


def add_custom_fields():
    """Add custom fields to existing DocTypes"""
    custom_fields = {
        "Supplier": [
            {
                "fieldname": "portal_access",
                "label": "Portal Access",
                "fieldtype": "Check",
                "insert_after": "supplier_type"
            },
            {
                "fieldname": "portal_user",
                "label": "Portal User",
                "fieldtype": "Link",
                "options": "User",
                "insert_after": "portal_access"
            }
        ],
        "Purchase Invoice": [
            {
                "fieldname": "submitted_via_portal",
                "label": "Submitted via Portal",
                "fieldtype": "Check",
                "insert_after": "bill_date"
            },
            {
                "fieldname": "workflow_state",
                "label": "Workflow State",
                "fieldtype": "Select",
                "options": "Draft\nPending Approval\nUnder Review\nApproved\nRejected",
                "insert_after": "submitted_via_portal"
            }
        ],
        "Shipment": [
            {
                "fieldname": "freight_forwarder",
                "label": "Freight Forwarder",
                "fieldtype": "Link",
                "options": "Supplier",
                "insert_after": "shipment_type"
            },
            {
                "fieldname": "last_update",
                "label": "Last Update",
                "fieldtype": "Datetime",
                "insert_after": "freight_forwarder"
            }
        ]
    }
    
    create_custom_fields(custom_fields, update=True)
    print("✓ Added custom fields")


def create_portal_pages():
    """Create portal web pages"""
    pages = [
        {
            "name": "vendor-portal",
            "title": "Vendor Portal",
            "route": "vendor-portal",
            "published": 1
        },
        {
            "name": "freight-portal",
            "title": "Freight Forwarder Portal",
            "route": "freight-portal",
            "published": 1
        }
    ]
    
    for page_data in pages:
        if not frappe.db.exists("Web Page", page_data["name"]):
            page = frappe.get_doc({
                "doctype": "Web Page",
                **page_data
            })
            page.insert()
    
    print("✓ Created portal pages")


def setup_roles_and_permissions():
    """Set up roles for portal users"""
    roles = ["Vendor", "Freight Forwarder"]
    
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 0
            }).insert()
    
    print("✓ Set up roles and permissions")


def create_workflows():
    """Create approval workflows"""
    # Invoice approval workflow
    if not frappe.db.exists("Workflow", "Invoice Approval"):
        workflow = frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Invoice Approval",
            "document_type": "Purchase Invoice",
            "is_active": 1,
            "states": [
                {"state": "Pending Approval", "doc_status": "0", "allow_edit": "Purchase Manager"},
                {"state": "Approved", "doc_status": "1", "allow_edit": "Accounts Manager"},
                {"state": "Rejected", "doc_status": "2"}
            ],
            "transitions": [
                {"state": "Pending Approval", "action": "Approve", "next_state": "Approved", 
                 "allowed": "Purchase Manager"},
                {"state": "Pending Approval", "action": "Reject", "next_state": "Rejected", 
                 "allowed": "Purchase Manager"}
            ]
        })
        workflow.insert()
    
    print("✓ Created workflows")


if __name__ == "__main__":
    install_vendor_portal()
