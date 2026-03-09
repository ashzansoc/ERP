#!/bin/bash
docker compose -f compose.yaml -f overrides/compose.redis.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.noproxy.yaml exec -T backend bench --site localhost console <<'PYTHON'
import frappe

# Create Certificate of Origin Item child table first
if not frappe.db.exists('DocType', 'Certificate of Origin Item'):
    coo_item_doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Certificate of Origin Item',
        'module': 'Stock',
        'custom': 1,
        'istable': 1,
        'editable_grid': 1,
        'fields': [
            {'fieldname': 'item_code', 'fieldtype': 'Link', 'label': 'Item Code', 'options': 'Item', 'in_list_view': 1, 'reqd': 1},
            {'fieldname': 'item_name', 'fieldtype': 'Data', 'label': 'Item Name', 'fetch_from': 'item_code.item_name', 'in_list_view': 1, 'read_only': 1},
            {'fieldname': 'description', 'fieldtype': 'Text Editor', 'label': 'Description'},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'hs_code', 'fieldtype': 'Link', 'label': 'HS Code', 'options': 'Customs Tariff Number', 'in_list_view': 1},
            {'fieldname': 'quantity', 'fieldtype': 'Float', 'label': 'Quantity', 'in_list_view': 1, 'reqd': 1},
            {'fieldname': 'uom', 'fieldtype': 'Link', 'label': 'UOM', 'options': 'UOM', 'in_list_view': 1},
            {'fieldname': 'column_break_2', 'fieldtype': 'Column Break'},
            {'fieldname': 'unit_price', 'fieldtype': 'Currency', 'label': 'Unit Price'},
            {'fieldname': 'amount', 'fieldtype': 'Currency', 'label': 'Amount', 'read_only': 1},
            {'fieldname': 'origin_criteria', 'fieldtype': 'Select', 'label': 'Origin Criteria', 'options': 'Wholly Obtained\nProduced Entirely\nSubstantial Transformation\nValue Added\nChange in Tariff Classification'}
        ]
    })
    coo_item_doc.insert(ignore_permissions=True)
    print("Created Certificate of Origin Item DocType")

# Create Certificate of Origin main DocType
if not frappe.db.exists('DocType', 'Certificate of Origin'):
    coo_doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Certificate of Origin',
        'module': 'Stock',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:COO-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'certificate_number', 'fieldtype': 'Data', 'label': 'Certificate Number', 'reqd': 1, 'unique': 1, 'in_list_view': 1},
            {'fieldname': 'certificate_date', 'fieldtype': 'Date', 'label': 'Certificate Date', 'reqd': 1, 'in_list_view': 1, 'default': 'Today'},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Draft\nPending Approval\nApproved\nIssued\nRejected\nCancelled', 'default': 'Draft', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'certificate_type', 'fieldtype': 'Select', 'label': 'Certificate Type', 'options': 'Non-Preferential\nGSP (Generalized System of Preferences)\nFTA (Free Trade Agreement)\nForm A\nForm B\nForm E\nForm D\nOther', 'reqd': 1},
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Exporter Details'},
            {'fieldname': 'exporter', 'fieldtype': 'Link', 'label': 'Exporter', 'options': 'Supplier', 'reqd': 1},
            {'fieldname': 'exporter_name', 'fieldtype': 'Data', 'label': 'Exporter Name', 'fetch_from': 'exporter.supplier_name'},
            {'fieldname': 'exporter_address', 'fieldtype': 'Small Text', 'label': 'Exporter Address'},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'exporter_country', 'fieldtype': 'Link', 'label': 'Exporter Country', 'options': 'Country', 'reqd': 1},
            {'fieldname': 'exporter_tax_id', 'fieldtype': 'Data', 'label': 'Exporter Tax ID / IEC'},
            {'fieldname': 'exporter_contact', 'fieldtype': 'Data', 'label': 'Contact Person'},
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Consignee Details'},
            {'fieldname': 'consignee', 'fieldtype': 'Link', 'label': 'Consignee', 'options': 'Customer', 'reqd': 1},
            {'fieldname': 'consignee_name', 'fieldtype': 'Data', 'label': 'Consignee Name', 'fetch_from': 'consignee.customer_name'},
            {'fieldname': 'consignee_address', 'fieldtype': 'Small Text', 'label': 'Consignee Address'},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'consignee_country', 'fieldtype': 'Link', 'label': 'Consignee Country', 'options': 'Country', 'reqd': 1},
            {'fieldname': 'consignee_tax_id', 'fieldtype': 'Data', 'label': 'Consignee Tax ID'},
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Shipment Details'},
            {'fieldname': 'invoice_number', 'fieldtype': 'Link', 'label': 'Invoice Number', 'options': 'Sales Invoice'},
            {'fieldname': 'invoice_date', 'fieldtype': 'Date', 'label': 'Invoice Date'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'bl_awb_number', 'fieldtype': 'Data', 'label': 'B/L / AWB Number'},
            {'fieldname': 'shipment_date', 'fieldtype': 'Date', 'label': 'Shipment Date'},
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Transport Details'},
            {'fieldname': 'port_of_loading', 'fieldtype': 'Data', 'label': 'Port of Loading', 'reqd': 1},
            {'fieldname': 'port_of_discharge', 'fieldtype': 'Data', 'label': 'Port of Discharge', 'reqd': 1},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'vessel_flight', 'fieldtype': 'Data', 'label': 'Vessel / Flight'},
            {'fieldname': 'transport_mode', 'fieldtype': 'Select', 'label': 'Mode of Transport', 'options': 'Sea\nAir\nRoad\nRail\nMultimodal'},
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Items'},
            {'fieldname': 'items', 'fieldtype': 'Table', 'label': 'Items', 'options': 'Certificate of Origin Item', 'reqd': 1},
            {'fieldname': 'section_break_11', 'fieldtype': 'Section Break', 'label': 'Totals'},
            {'fieldname': 'total_quantity', 'fieldtype': 'Float', 'label': 'Total Quantity', 'read_only': 1},
            {'fieldname': 'column_break_12', 'fieldtype': 'Column Break'},
            {'fieldname': 'total_amount', 'fieldtype': 'Currency', 'label': 'Total Amount', 'read_only': 1},
            {'fieldname': 'currency', 'fieldtype': 'Link', 'label': 'Currency', 'options': 'Currency'},
            {'fieldname': 'section_break_13', 'fieldtype': 'Section Break', 'label': 'Origin Declaration'},
            {'fieldname': 'country_of_origin', 'fieldtype': 'Link', 'label': 'Country of Origin', 'options': 'Country', 'reqd': 1},
            {'fieldname': 'origin_criteria', 'fieldtype': 'Select', 'label': 'Origin Criteria', 'options': 'Wholly Obtained\nProduced Entirely\nSubstantial Transformation\nValue Added\nChange in Tariff Classification'},
            {'fieldname': 'column_break_14', 'fieldtype': 'Column Break'},
            {'fieldname': 'declaration_text', 'fieldtype': 'Text', 'label': 'Declaration Text', 'default': 'We hereby certify that the goods described above originate in the country stated and comply with the origin requirements specified for those goods.'},
            {'fieldname': 'section_break_15', 'fieldtype': 'Section Break', 'label': 'Issuing Authority'},
            {'fieldname': 'issuing_authority', 'fieldtype': 'Data', 'label': 'Issuing Authority'},
            {'fieldname': 'authority_address', 'fieldtype': 'Small Text', 'label': 'Authority Address'},
            {'fieldname': 'column_break_16', 'fieldtype': 'Column Break'},
            {'fieldname': 'authorized_signatory', 'fieldtype': 'Data', 'label': 'Authorized Signatory'},
            {'fieldname': 'signatory_designation', 'fieldtype': 'Data', 'label': 'Designation'},
            {'fieldname': 'signature_date', 'fieldtype': 'Date', 'label': 'Signature Date'},
            {'fieldname': 'section_break_17', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'column_break_18', 'fieldtype': 'Column Break'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'},
            {'fieldname': 'validity_date', 'fieldtype': 'Date', 'label': 'Validity Date'}
        ],
        'permissions': [
            {'role': 'Stock User', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Stock Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Sales User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Sales Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    coo_doc.insert(ignore_permissions=True)
    print("Created Certificate of Origin DocType")

frappe.db.commit()
print("Successfully created Certificate of Origin system!")
exit()
PYTHON
