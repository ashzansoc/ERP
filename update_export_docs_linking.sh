#!/bin/bash
docker compose -f compose.yaml -f overrides/compose.redis.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.noproxy.yaml exec -T backend bench --site localhost console <<'PYTHON'
import frappe

# Update Bill of Lading with linking fields
if frappe.db.exists('DocType', 'Bill of Lading'):
    bl_doc = frappe.get_doc('DocType', 'Bill of Lading')
    
    # Add linking section after section_break_17
    new_fields = [
        {
            'fieldname': 'section_break_links',
            'fieldtype': 'Section Break',
            'label': 'Document Links',
            'insert_after': 'section_break_17'
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
            'fieldname': 'column_break_links',
            'fieldtype': 'Column Break',
            'insert_after': 'purchase_order'
        },
        {
            'fieldname': 'shipment',
            'fieldtype': 'Link',
            'label': 'Shipment',
            'options': 'Shipment',
            'insert_after': 'column_break_links'
        },
        {
            'fieldname': 'container_number_ref',
            'fieldtype': 'Data',
            'label': 'Container Number Reference',
            'insert_after': 'shipment'
        }
    ]
    
    for field in new_fields:
        if not any(f.fieldname == field['fieldname'] for f in bl_doc.fields):
            bl_doc.append('fields', field)
    
    bl_doc.save(ignore_permissions=True)
    print("Updated Bill of Lading with linking fields")

# Update Certificate of Origin with linking fields
if frappe.db.exists('DocType', 'Certificate of Origin'):
    coo_doc = frappe.get_doc('DocType', 'Certificate of Origin')
    
    new_fields = [
        {
            'fieldname': 'section_break_links',
            'fieldtype': 'Section Break',
            'label': 'Document Links',
            'insert_after': 'section_break_17'
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
            'fieldname': 'column_break_links',
            'fieldtype': 'Column Break',
            'insert_after': 'purchase_order'
        },
        {
            'fieldname': 'shipment',
            'fieldtype': 'Link',
            'label': 'Shipment',
            'options': 'Shipment',
            'insert_after': 'column_break_links'
        },
        {
            'fieldname': 'bill_of_lading',
            'fieldtype': 'Link',
            'label': 'Bill of Lading',
            'options': 'Bill of Lading',
            'insert_after': 'shipment'
        }
    ]
    
    for field in new_fields:
        if not any(f.fieldname == field['fieldname'] for f in coo_doc.fields):
            coo_doc.append('fields', field)
    
    coo_doc.save(ignore_permissions=True)
    print("Updated Certificate of Origin with linking fields")

# Update Letter of Credit with linking fields
if frappe.db.exists('DocType', 'Letter of Credit'):
    lc_doc = frappe.get_doc('DocType', 'Letter of Credit')
    
    new_fields = [
        {
            'fieldname': 'section_break_links',
            'fieldtype': 'Section Break',
            'label': 'Document Links',
            'insert_after': 'section_break_24'
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
            'fieldname': 'column_break_links',
            'fieldtype': 'Column Break',
            'insert_after': 'purchase_order'
        },
        {
            'fieldname': 'shipment',
            'fieldtype': 'Link',
            'label': 'Shipment',
            'options': 'Shipment',
            'insert_after': 'column_break_links'
        },
        {
            'fieldname': 'bill_of_lading',
            'fieldtype': 'Link',
            'label': 'Bill of Lading',
            'options': 'Bill of Lading',
            'insert_after': 'shipment'
        }
    ]
    
    for field in new_fields:
        if not any(f.fieldname == field['fieldname'] for f in lc_doc.fields):
            lc_doc.append('fields', field)
    
    lc_doc.save(ignore_permissions=True)
    print("Updated Letter of Credit with linking fields")

# Create Shipment Document Bundle DocType
if not frappe.db.exists('DocType', 'Shipment Document Bundle'):
    bundle_doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Shipment Document Bundle',
        'module': 'Stock',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:SDB-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'bundle_name', 'fieldtype': 'Data', 'label': 'Bundle Name', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'bundle_date', 'fieldtype': 'Date', 'label': 'Bundle Date', 'default': 'Today', 'reqd': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Draft\nGenerated\nDownloaded\nArchived', 'default': 'Draft', 'in_list_view': 1},
            {'fieldname': 'bundle_type', 'fieldtype': 'Select', 'label': 'Bundle Type', 'options': 'Export\nImport\nCustoms\nComplete', 'default': 'Complete'},
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Reference Documents'},
            {'fieldname': 'sales_order', 'fieldtype': 'Link', 'label': 'Sales Order', 'options': 'Sales Order'},
            {'fieldname': 'purchase_order', 'fieldtype': 'Link', 'label': 'Purchase Order', 'options': 'Purchase Order'},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'shipment', 'fieldtype': 'Link', 'label': 'Shipment', 'options': 'Shipment', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'delivery_note', 'fieldtype': 'Link', 'label': 'Delivery Note', 'options': 'Delivery Note'},
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Export Documents'},
            {'fieldname': 'bill_of_lading', 'fieldtype': 'Link', 'label': 'Bill of Lading', 'options': 'Bill of Lading'},
            {'fieldname': 'certificate_of_origin', 'fieldtype': 'Link', 'label': 'Certificate of Origin', 'options': 'Certificate of Origin'},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'letter_of_credit', 'fieldtype': 'Link', 'label': 'Letter of Credit', 'options': 'Letter of Credit'},
            {'fieldname': 'commercial_invoice', 'fieldtype': 'Link', 'label': 'Commercial Invoice', 'options': 'Sales Invoice'},
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Additional Documents'},
            {'fieldname': 'packing_slip', 'fieldtype': 'Link', 'label': 'Packing Slip', 'options': 'Packing Slip'},
            {'fieldname': 'customs_declaration', 'fieldtype': 'Data', 'label': 'Customs Declaration Number'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'insurance_certificate', 'fieldtype': 'Data', 'label': 'Insurance Certificate Number'},
            {'fieldname': 'inspection_certificate', 'fieldtype': 'Data', 'label': 'Inspection Certificate Number'},
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Bundle Generation'},
            {'fieldname': 'include_attachments', 'fieldtype': 'Check', 'label': 'Include Attachments', 'default': 1},
            {'fieldname': 'include_print_formats', 'fieldtype': 'Check', 'label': 'Include Print Formats', 'default': 1},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'generated_file', 'fieldtype': 'Attach', 'label': 'Generated Bundle (ZIP)', 'read_only': 1},
            {'fieldname': 'generation_date', 'fieldtype': 'Datetime', 'label': 'Generation Date', 'read_only': 1},
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'generated_by', 'fieldtype': 'Link', 'label': 'Generated By', 'options': 'User', 'read_only': 1}
        ],
        'permissions': [
            {'role': 'Stock User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Stock Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Sales User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Sales Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    bundle_doc.insert(ignore_permissions=True)
    print("Created Shipment Document Bundle DocType")

frappe.db.commit()
print("Successfully updated all export documents with linking fields and created Document Bundle system!")
exit()
PYTHON
