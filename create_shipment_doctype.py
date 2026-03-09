#!/usr/bin/env python3
"""
Script to create Shipment DocType for tracking shipments and containers
"""

import json
from datetime import datetime

# Main Shipment DocType
shipment_doctype = {
    "actions": [],
    "creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    "doctype": "DocType",
    "engine": "InnoDB",
    "is_submittable": 1,
    "autoname": "format:SHIP-{####}",
    "naming_rule": "Expression",
    "track_changes": 1,
    "allow_rename": 1,
    "editable_grid": 1,
    "index_web_pages_for_search": 1,
    "links": [],
    "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    "modified_by": "Administrator",
    "module": "Stock",
    "name": "Shipment",
    "owner": "Administrator",
    "sort_field": "modified",
    "sort_order": "DESC",
    "states": [],
    "field_order": [
        "shipment_details_section",
        "shipment_type",
        "column_break_1",
        "shipment_date",
        "customer",
        "port_details_section",
        "port_of_loading",
        "port_of_discharge",
        "column_break_2",
        "etd",
        "eta",
        "shipping_details_section",
        "shipping_line",
        "vessel_name",
        "column_break_3",
        "freight_forwarder",
        "booking_number",
        "container_section",
        "containers",
        "status_section",
        "status",
        "column_break_4",
        "actual_departure_date",
        "actual_arrival_date",
        "additional_info_section",
        "bill_of_lading",
        "tracking_notes",
        "amended_from"
    ],
    "fields": [
        # Basic Information
        {
            "fieldname": "shipment_details_section",
            "fieldtype": "Section Break",
            "label": "Shipment Details"
        },
        {
            "fieldname": "shipment_type",
            "fieldtype": "Select",
            "label": "Shipment Type",
            "options": "Import\nExport",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "column_break_1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "shipment_date",
            "fieldtype": "Date",
            "label": "Shipment Date",
            "default": "Today",
            "reqd": 1
        },
        {
            "fieldname": "customer",
            "fieldtype": "Link",
            "label": "Customer",
            "options": "Customer",
            "in_list_view": 1
        },
        
        # Port Information
        {
            "fieldname": "port_details_section",
            "fieldtype": "Section Break",
            "label": "Port & Route Details"
        },
        {
            "fieldname": "port_of_loading",
            "fieldtype": "Data",
            "label": "Port of Loading",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "port_of_discharge",
            "fieldtype": "Data",
            "label": "Port of Discharge",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "column_break_2",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "etd",
            "fieldtype": "Datetime",
            "label": "ETD (Estimated Time of Departure)",
            "reqd": 1
        },
        {
            "fieldname": "eta",
            "fieldtype": "Datetime",
            "label": "ETA (Estimated Time of Arrival)",
            "reqd": 1
        },
        
        # Shipping Details
        {
            "fieldname": "shipping_details_section",
            "fieldtype": "Section Break",
            "label": "Shipping Details"
        },
        {
            "fieldname": "shipping_line",
            "fieldtype": "Data",
            "label": "Shipping Line",
            "reqd": 1
        },
        {
            "fieldname": "vessel_name",
            "fieldtype": "Data",
            "label": "Vessel Name",
            "reqd": 1
        },
        {
            "fieldname": "column_break_3",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "freight_forwarder",
            "fieldtype": "Data",
            "label": "Freight Forwarder"
        },
        {
            "fieldname": "booking_number",
            "fieldtype": "Data",
            "label": "Booking Number"
        },
        
        # Container Information
        {
            "fieldname": "container_section",
            "fieldtype": "Section Break",
            "label": "Container Information"
        },
        {
            "fieldname": "containers",
            "fieldtype": "Table",
            "label": "Containers",
            "options": "Shipment Container",
            "reqd": 1
        },
        
        # Status & Workflow
        {
            "fieldname": "status_section",
            "fieldtype": "Section Break",
            "label": "Status & Tracking"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "Status",
            "options": "Draft\nBooked\nIn Transit\nCustoms\nDelivered\nCancelled",
            "default": "Draft",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "column_break_4",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "actual_departure_date",
            "fieldtype": "Datetime",
            "label": "Actual Departure Date"
        },
        {
            "fieldname": "actual_arrival_date",
            "fieldtype": "Datetime",
            "label": "Actual Arrival Date"
        },
        
        # Additional Information
        {
            "fieldname": "additional_info_section",
            "fieldtype": "Section Break",
            "label": "Additional Information",
            "collapsible": 1
        },
        {
            "fieldname": "bill_of_lading",
            "fieldtype": "Link",
            "label": "Bill of Lading",
            "options": "Bill of Lading"
        },
        {
            "fieldname": "tracking_notes",
            "fieldtype": "Text Editor",
            "label": "Tracking Notes"
        },
        
        # Amended From
        {
            "fieldname": "amended_from",
            "fieldtype": "Link",
            "label": "Amended From",
            "options": "Shipment",
            "read_only": 1,
            "no_copy": 1
        }
    ],
    "permissions": [
        {
            "role": "System Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1
        },
        {
            "role": "Stock User",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1
        }
    ]
}

# Child DocType for Containers
shipment_container_doctype = {
    "actions": [],
    "creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    "doctype": "DocType",
    "editable_grid": 1,
    "engine": "InnoDB",
    "index_web_pages_for_search": 1,
    "istable": 1,
    "links": [],
    "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    "modified_by": "Administrator",
    "module": "Stock",
    "name": "Shipment Container",
    "owner": "Administrator",
    "permissions": [],
    "sort_field": "modified",
    "sort_order": "DESC",
    "states": [],
    "track_changes": 1,
    "field_order": [
        "container_no",
        "container_type",
        "seal_no",
        "column_break_1",
        "gross_weight",
        "net_weight",
        "column_break_2",
        "container_status"
    ],
    "fields": [
        {
            "fieldname": "container_no",
            "fieldtype": "Data",
            "label": "Container No",
            "reqd": 1,
            "in_list_view": 1
        },
        {
            "fieldname": "container_type",
            "fieldtype": "Select",
            "label": "Container Type",
            "options": "20ft Standard\n40ft Standard\n40ft High Cube\n20ft Refrigerated\n40ft Refrigerated",
            "in_list_view": 1
        },
        {
            "fieldname": "seal_no",
            "fieldtype": "Data",
            "label": "Seal No",
            "in_list_view": 1
        },
        {
            "fieldname": "column_break_1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "gross_weight",
            "fieldtype": "Float",
            "label": "Gross Weight (KG)"
        },
        {
            "fieldname": "net_weight",
            "fieldtype": "Float",
            "label": "Net Weight (KG)"
        },
        {
            "fieldname": "column_break_2",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "container_status",
            "fieldtype": "Select",
            "label": "Container Status",
            "options": "Empty\nLoaded\nIn Transit\nDischarged\nReturned",
            "default": "Empty"
        }
    ]
}

# Save to JSON files
with open('shipment_doctype.json', 'w') as f:
    json.dump(shipment_doctype, f, indent=2)

with open('shipment_container_doctype.json', 'w') as f:
    json.dump(shipment_container_doctype, f, indent=2)

print("✅ Shipment DocType JSON files created successfully!")
print("📄 Files created:")
print("   - shipment_doctype.json")
print("   - shipment_container_doctype.json")
