#!/bin/bash

echo "🌍 Quick Portal Installation..."

# Create DocTypes using bench console with heredoc
docker compose -f frappe_docker/compose.yaml exec -T backend bench --site localhost console <<'EOF'
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

print("Creating Vendor Document Log...")
if not frappe.db.exists("DocType", "Vendor Document Log"):
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Vendor Document Log",
        "module": "Buying",
        "custom": 1,
        "naming_rule": "Autoincrement",
        "autoname": "VDL-.#####",
        "fields": [
            {"fieldname": "vendor", "label": "Vendor", "fieldtype": "Link", "options": "Supplier", "reqd": 1, "in_list_view": 1},
            {"fieldname": "document_type", "label": "Document Type", "fieldtype": "Select", "options": "Invoice\\nPacking List\\nCertificate\\nTest Report\\nOther", "reqd": 1, "in_list_view": 1},
            {"fieldname": "reference_doctype", "label": "Reference DocType", "fieldtype": "Data"},
            {"fieldname": "reference_name", "label": "Reference Name", "fieldtype": "Dynamic Link", "options": "reference_doctype", "in_list_view": 1},
            {"fieldname": "file_url", "label": "File URL", "fieldtype": "Attach"},
            {"fieldname": "upload_date", "label": "Upload Date", "fieldtype": "Datetime", "default": "now"},
            {"fieldname": "uploaded_by", "label": "Uploaded By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Pending\\nSubmitted\\nApproved\\nRejected", "default": "Pending", "in_list_view": 1},
            {"fieldname": "reviewed_by", "label": "Reviewed By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "review_date", "label": "Review Date", "fieldtype": "Datetime"},
            {"fieldname": "comments", "label": "Comments", "fieldtype": "Text"}
        ],
        "permissions": [
            {"role": "Purchase Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Purchase User", "read": 1, "write": 1, "create": 1}
        ]
    })
    doc.insert()
    print("✓ Created Vendor Document Log")

print("Creating Freight Quote...")
if not frappe.db.exists("DocType", "Freight Quote"):
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Freight Quote",
        "module": "Stock",
        "custom": 1,
        "naming_rule": "By fieldname",
        "autoname": "field:quote_number",
        "fields": [
            {"fieldname": "quote_number", "label": "Quote Number", "fieldtype": "Data", "reqd": 1, "unique": 1},
            {"fieldname": "freight_forwarder", "label": "Freight Forwarder", "fieldtype": "Link", "options": "Supplier", "reqd": 1, "in_list_view": 1},
            {"fieldname": "quote_date", "label": "Quote Date", "fieldtype": "Date", "default": "Today", "in_list_view": 1},
            {"fieldname": "valid_until", "label": "Valid Until", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Route Details"},
            {"fieldname": "origin_port", "label": "Origin Port", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "destination_port", "label": "Destination Port", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "shipping_mode", "label": "Shipping Mode", "fieldtype": "Select", "options": "Sea\\nAir\\nRoad\\nRail", "reqd": 1},
            {"fieldname": "transit_time_days", "label": "Transit Time (Days)", "fieldtype": "Int"},
            {"fieldname": "service_level", "label": "Service Level", "fieldtype": "Select", "options": "Standard\\nExpress\\nEconomy"},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Cost Breakdown"},
            {"fieldname": "base_freight_cost", "label": "Base Freight Cost", "fieldtype": "Currency", "reqd": 1},
            {"fieldname": "fuel_surcharge", "label": "Fuel Surcharge", "fieldtype": "Currency"},
            {"fieldname": "documentation_fee", "label": "Documentation Fee", "fieldtype": "Currency"},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "handling_charges", "label": "Handling Charges", "fieldtype": "Currency"},
            {"fieldname": "insurance_cost", "label": "Insurance Cost", "fieldtype": "Currency"},
            {"fieldname": "other_charges", "label": "Other Charges", "fieldtype": "Currency"},
            {"fieldname": "section_break_3", "fieldtype": "Section Break"},
            {"fieldname": "total_cost", "label": "Total Cost", "fieldtype": "Currency", "read_only": 1, "in_list_view": 1},
            {"fieldname": "currency", "label": "Currency", "fieldtype": "Link", "options": "Currency", "default": "USD"},
            {"fieldname": "section_break_4", "fieldtype": "Section Break"},
            {"fieldname": "special_notes", "label": "Special Notes", "fieldtype": "Text"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Draft\\nSubmitted\\nAccepted\\nRejected", "default": "Draft", "in_list_view": 1}
        ],
        "permissions": [
            {"role": "Stock Manager", "read": 1, "write": 1, "create": 1},
            {"role": "Stock User", "read": 1, "write": 1, "create": 1}
        ]
    })
    doc.insert()
    print("✓ Created Freight Quote")

print("Creating Shipment Milestone...")
if not frappe.db.exists("DocType", "Shipment Milestone"):
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Shipment Milestone",
        "module": "Stock",
        "custom": 1,
        "naming_rule": "Autoincrement",
        "autoname": "SM-.#####",
        "fields": [
            {"fieldname": "shipment", "label": "Shipment", "fieldtype": "Link", "options": "Shipment", "reqd": 1, "in_list_view": 1},
            {"fieldname": "milestone_type", "label": "Milestone Type", "fieldtype": "Select", "options": "Booking Confirmed\\nCargo Loaded\\nDeparted Origin\\nIn Transit\\nArrived at Port\\nCustoms Cleared\\nOut for Delivery\\nDelivered", "reqd": 1, "in_list_view": 1},
            {"fieldname": "milestone_date", "label": "Milestone Date", "fieldtype": "Datetime", "reqd": 1, "in_list_view": 1},
            {"fieldname": "location", "label": "Location", "fieldtype": "Data"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "On Time\\nDelayed\\nCompleted", "default": "On Time", "in_list_view": 1},
            {"fieldname": "notes", "label": "Notes", "fieldtype": "Text"},
            {"fieldname": "updated_by", "label": "Updated By", "fieldtype": "Link", "options": "User"},
            {"fieldname": "eta_update", "label": "Updated ETA", "fieldtype": "Datetime"},
            {"fieldname": "delay_reason", "label": "Delay Reason", "fieldtype": "Text"}
        ],
        "permissions": [
            {"role": "Stock Manager", "read": 1, "write": 1, "create": 1},
            {"role": "Stock User", "read": 1, "write": 1, "create": 1}
        ]
    })
    doc.insert()
    print("✓ Created Shipment Milestone")

print("Adding custom fields to Supplier...")
custom_fields = {
    "Supplier": [
        {"fieldname": "portal_access_section", "label": "Portal Access", "fieldtype": "Section Break", "insert_after": "supplier_type"},
        {"fieldname": "portal_access", "label": "Enable Portal Access", "fieldtype": "Check", "insert_after": "portal_access_section"},
        {"fieldname": "portal_user", "label": "Portal User", "fieldtype": "Link", "options": "User", "insert_after": "portal_access"},
        {"fieldname": "portal_type", "label": "Portal Type", "fieldtype": "Select", "options": "\\nVendor Portal\\nFreight Forwarder Portal\\nBoth", "insert_after": "portal_user"}
    ]
}

create_custom_fields(custom_fields, update=True)
print("✓ Added custom fields")

frappe.db.commit()
print("\\n✅ Portal DocTypes created successfully!")
exit()
EOF

echo ""
echo "🧹 Clearing cache..."
docker compose -f frappe_docker/compose.yaml exec backend bench --site localhost clear-cache

echo ""
echo "✅ Portal Deployed Successfully!"
echo ""
echo "📋 New DocTypes Available:"
echo "  • Vendor Document Log"
echo "  • Freight Quote"
echo "  • Shipment Milestone"
echo ""
echo "🌐 Access at: http://localhost:8080"
echo ""
