#!/bin/bash
docker compose -f compose.yaml -f overrides/compose.redis.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.noproxy.yaml exec -T backend bench --site localhost console <<'PYTHON'
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# Define custom fields for Bill of Lading
bl_fields = {
    'Bill of Lading': [
        {
            'fieldname': 'section_break_links',
            'fieldtype': 'Section Break',
            'label': 'Document Links',
            'insert_after': 'attachments'
        },
        {
            'fieldname': 'sales_order',
            'fieldtype': 'Link',
            'label': 'Sales Order',
            'options': 'Sales Order',
            'insert_after': 'section_break_links'
        },
        {
            'fieldname': 'purchase_order',
            'fieldtype': 'Link',
            'label': 'Purchase Order',
            'options': 'Purchase Order',
            'insert_after': 'sales_order'
        },
        {
            'fieldname': 'column_break_links_1',
            'fieldtype': 'Column Break',
            'insert_after': 'purchase_order'
        },
        {
            'fieldname': 'shipment_link',
            'fieldtype': 'Link',
            'label': 'Shipment',
            'options': 'Shipment',
            'insert_after': 'column_break_links_1'
        },
        {
            'fieldname': 'delivery_note',
            'fieldtype': 'Link',
            'label': 'Delivery Note',
            'options': 'Delivery Note',
            'insert_after': 'shipment_link'
        }
    ]
}

# Define custom fields for Certificate of Origin
coo_fields = {
    'Certificate of Origin': [
        {
            'fieldname': 'section_break_doc_links',
            'fieldtype': 'Section Break',
            'label': 'Document Links',
            'insert_after': 'attachments'
        },
        {
            'fieldname': 'sales_order_link',
            'fieldtype': 'Link',
            'label': 'Sales Order',
            'options': 'Sales Order',
            'insert_after': 'section_break_doc_links'
        },
        {
            'fieldname': 'purchase_order_link',
            'fieldtype': 'Link',
            'label': 'Purchase Order',
            'options': 'Purchase Order',
            'insert_after': 'sales_order_link'
        },
        {
            'fieldname': 'column_break_doc_links',
            'fieldtype': 'Column Break',
            'insert_after': 'purchase_order_link'
        },
        {
            'fieldname': 'shipment_ref',
            'fieldtype': 'Link',
            'label': 'Shipment',
            'options': 'Shipment',
            'insert_after': 'column_break_doc_links'
        },
        {
            'fieldname': 'bill_of_lading_ref',
            'fieldtype': 'Link',
            'label': 'Bill of Lading',
            'options': 'Bill of Lading',
            'insert_after': 'shipment_ref'
        }
    ]
}

# Define custom fields for Letter of Credit
lc_fields = {
    'Letter of Credit': [
        {
            'fieldname': 'section_break_doc_refs',
            'fieldtype': 'Section Break',
            'label': 'Document References',
            'insert_after': 'attachments'
        },
        {
            'fieldname': 'sales_order_ref',
            'fieldtype': 'Link',
            'label': 'Sales Order',
            'options': 'Sales Order',
            'insert_after': 'section_break_doc_refs'
        },
        {
            'fieldname': 'purchase_order_ref',
            'fieldtype': 'Link',
            'label': 'Purchase Order',
            'options': 'Purchase Order',
            'insert_after': 'sales_order_ref'
        },
        {
            'fieldname': 'column_break_doc_refs',
            'fieldtype': 'Column Break',
            'insert_after': 'purchase_order_ref'
        },
        {
            'fieldname': 'shipment_reference',
            'fieldtype': 'Link',
            'label': 'Shipment',
            'options': 'Shipment',
            'insert_after': 'column_break_doc_refs'
        },
        {
            'fieldname': 'bl_reference',
            'fieldtype': 'Link',
            'label': 'Bill of Lading',
            'options': 'Bill of Lading',
            'insert_after': 'shipment_reference'
        }
    ]
}

# Create all custom fields
try:
    create_custom_fields(bl_fields, update=True)
    print("Added linking fields to Bill of Lading")
except Exception as e:
    print(f"Error adding fields to Bill of Lading: {str(e)}")

try:
    create_custom_fields(coo_fields, update=True)
    print("Added linking fields to Certificate of Origin")
except Exception as e:
    print(f"Error adding fields to Certificate of Origin: {str(e)}")

try:
    create_custom_fields(lc_fields, update=True)
    print("Added linking fields to Letter of Credit")
except Exception as e:
    print(f"Error adding fields to Letter of Credit: {str(e)}")

frappe.db.commit()
print("Successfully added all linking fields!")
exit()
PYTHON
