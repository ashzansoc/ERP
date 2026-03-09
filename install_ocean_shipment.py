#!/usr/bin/env python3
import sys
import frappe

# Initialize Frappe
frappe.init(site='localhost')
frappe.connect()
frappe.set_user('Administrator')

print("🚢 Creating Ocean Shipment & Container Tracking Module...")

# First, create the child table DocType
if not frappe.db.exists("DocType", "Ocean Shipment Container"):
    container_doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Ocean Shipment Container",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "editable_grid": 1,
        "track_changes": 1,
        "fields": [
            {"fieldname": "container_no", "fieldtype": "Data", "label": "Container No", "reqd": 1, "in_list_view": 1},
            {"fieldname": "container_type", "fieldtype": "Select", "label": "Container Type", "options": "20ft Standard\n40ft Standard\n40ft High Cube\n20ft Refrigerated\n40ft Refrigerated", "in_list_view": 1},
            {"fieldname": "seal_no", "fieldtype": "Data", "label": "Seal No", "in_list_view": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "gross_weight", "fieldtype": "Float", "label": "Gross Weight (KG)"},
            {"fieldname": "net_weight", "fieldtype": "Float", "label": "Net Weight (KG)"},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "container_status", "fieldtype": "Select", "label": "Container Status", "options": "Empty\nLoaded\nIn Transit\nDischarged\nReturned", "default": "Empty"}
        ]
    })
    container_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Ocean Shipment Container DocType created")
else:
    print("ℹ️  Ocean Shipment Container already exists")

# Create the main Ocean Shipment DocType
if not frappe.db.exists("DocType", "Ocean Shipment"):
    shipment_doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Ocean Shipment",
        "module": "Stock",
        "custom": 1,
        "is_submittable": 1,
        "autoname": "format:OSHIP-{####}",
        "naming_rule": "Expression",
        "track_changes": 1,
        "allow_rename": 1,
        "fields": [
            {"fieldname": "shipment_details_section", "fieldtype": "Section Break", "label": "Shipment Details"},
            {"fieldname": "shipment_type", "fieldtype": "Select", "label": "Shipment Type", "options": "Import\nExport", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "shipment_date", "fieldtype": "Date", "label": "Shipment Date", "default": "Today", "reqd": 1},
            {"fieldname": "customer", "fieldtype": "Link", "label": "Customer", "options": "Customer", "in_list_view": 1},
            
            {"fieldname": "port_details_section", "fieldtype": "Section Break", "label": "Port & Route Details"},
            {"fieldname": "port_of_loading", "fieldtype": "Data", "label": "Port of Loading", "reqd": 1, "in_list_view": 1},
            {"fieldname": "port_of_discharge", "fieldtype": "Data", "label": "Port of Discharge", "reqd": 1, "in_list_view": 1},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "etd", "fieldtype": "Datetime", "label": "ETD (Estimated Time of Departure)", "reqd": 1},
            {"fieldname": "eta", "fieldtype": "Datetime", "label": "ETA (Estimated Time of Arrival)", "reqd": 1},
            
            {"fieldname": "shipping_details_section", "fieldtype": "Section Break", "label": "Shipping Details"},
            {"fieldname": "shipping_line", "fieldtype": "Data", "label": "Shipping Line", "reqd": 1},
            {"fieldname": "vessel_name", "fieldtype": "Data", "label": "Vessel Name", "reqd": 1},
            {"fieldname": "column_break_3", "fieldtype": "Column Break"},
            {"fieldname": "freight_forwarder", "fieldtype": "Data", "label": "Freight Forwarder"},
            {"fieldname": "booking_number", "fieldtype": "Data", "label": "Booking Number"},
            
            {"fieldname": "container_section", "fieldtype": "Section Break", "label": "Container Information"},
            {"fieldname": "containers", "fieldtype": "Table", "label": "Containers", "options": "Ocean Shipment Container", "reqd": 1},
            
            {"fieldname": "status_section", "fieldtype": "Section Break", "label": "Status & Tracking"},
            {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nBooked\nIn Transit\nCustoms\nDelivered\nCancelled", "default": "Draft", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
            {"fieldname": "column_break_4", "fieldtype": "Column Break"},
            {"fieldname": "actual_departure_date", "fieldtype": "Datetime", "label": "Actual Departure Date"},
            {"fieldname": "actual_arrival_date", "fieldtype": "Datetime", "label": "Actual Arrival Date"},
            
            {"fieldname": "additional_info_section", "fieldtype": "Section Break", "label": "Additional Information", "collapsible": 1},
            {"fieldname": "bill_of_lading", "fieldtype": "Link", "label": "Bill of Lading", "options": "Bill of Lading"},
            {"fieldname": "tracking_notes", "fieldtype": "Text Editor", "label": "Tracking Notes"},
            
            {"fieldname": "amended_from", "fieldtype": "Link", "label": "Amended From", "options": "Ocean Shipment", "read_only": 1, "no_copy": 1}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "amend": 1},
            {"role": "Stock User", "read": 1, "write": 1, "create": 1, "submit": 1}
        ]
    })
    shipment_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Ocean Shipment DocType created")
else:
    print("ℹ️  Ocean Shipment already exists")

frappe.clear_cache()
print("\n✅ Installation complete! Access at: Desk → Stock → Ocean Shipment")
