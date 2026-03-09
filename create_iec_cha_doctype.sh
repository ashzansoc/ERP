#!/bin/bash
docker compose -f compose.yaml -f overrides/compose.redis.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.noproxy.yaml exec -T backend bench --site localhost console <<'PYTHON'
import frappe

# Create IEC Registration DocType
if not frappe.db.exists('DocType', 'IEC Registration'):
    iec_doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'IEC Registration',
        'module': 'Selling',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'field:iec_number',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'iec_number', 'fieldtype': 'Data', 'label': 'IEC Number', 'reqd': 1, 'unique': 1, 'in_list_view': 1},
            {'fieldname': 'company', 'fieldtype': 'Link', 'label': 'Company', 'options': 'Company', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Active\nSuspended\nCancelled\nExpired', 'default': 'Active', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'registration_type', 'fieldtype': 'Select', 'label': 'Registration Type', 'options': 'Importer\nExporter\nBoth', 'default': 'Both'},
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Registration Details'},
            {'fieldname': 'issue_date', 'fieldtype': 'Date', 'label': 'Issue Date', 'reqd': 1},
            {'fieldname': 'valid_from', 'fieldtype': 'Date', 'label': 'Valid From'},
            {'fieldname': 'valid_till', 'fieldtype': 'Date', 'label': 'Valid Till'},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'issuing_authority', 'fieldtype': 'Data', 'label': 'Issuing Authority', 'default': 'DGFT (Directorate General of Foreign Trade)'},
            {'fieldname': 'regional_authority', 'fieldtype': 'Data', 'label': 'Regional Authority'},
            {'fieldname': 'file_number', 'fieldtype': 'Data', 'label': 'File Number'},
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Company Information'},
            {'fieldname': 'company_name', 'fieldtype': 'Data', 'label': 'Company Name', 'reqd': 1},
            {'fieldname': 'company_address', 'fieldtype': 'Small Text', 'label': 'Registered Address'},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'pan_number', 'fieldtype': 'Data', 'label': 'PAN Number'},
            {'fieldname': 'gstin', 'fieldtype': 'Data', 'label': 'GSTIN'},
            {'fieldname': 'cin_number', 'fieldtype': 'Data', 'label': 'CIN Number'},
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Contact Details'},
            {'fieldname': 'contact_person', 'fieldtype': 'Data', 'label': 'Contact Person'},
            {'fieldname': 'designation', 'fieldtype': 'Data', 'label': 'Designation'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'email', 'fieldtype': 'Data', 'label': 'Email', 'options': 'Email'},
            {'fieldname': 'phone', 'fieldtype': 'Data', 'label': 'Phone'},
            {'fieldname': 'mobile', 'fieldtype': 'Data', 'label': 'Mobile'},
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Bank Details'},
            {'fieldname': 'bank_name', 'fieldtype': 'Data', 'label': 'Bank Name'},
            {'fieldname': 'bank_account_number', 'fieldtype': 'Data', 'label': 'Account Number'},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'ifsc_code', 'fieldtype': 'Data', 'label': 'IFSC Code'},
            {'fieldname': 'swift_code', 'fieldtype': 'Data', 'label': 'SWIFT Code'},
            {'fieldname': 'ad_code', 'fieldtype': 'Data', 'label': 'AD Code'},
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'nature_of_business', 'fieldtype': 'Small Text', 'label': 'Nature of Business'},
            {'fieldname': 'principal_products', 'fieldtype': 'Text', 'label': 'Principal Products'},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
        ],
        'permissions': [
            {'role': 'Sales User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Sales Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Accounts User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Accounts Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    iec_doc.insert(ignore_permissions=True)
    print("Created IEC Registration DocType")

# Create CHA Shipment child table
if not frappe.db.exists('DocType', 'CHA Shipment'):
    cha_shipment_table = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'CHA Shipment',
        'module': 'Stock',
        'custom': 1,
        'istable': 1,
        'editable_grid': 1,
        'fields': [
            {'fieldname': 'shipment_type', 'fieldtype': 'Select', 'label': 'Shipment Type', 'options': 'Import\nExport', 'in_list_view': 1, 'reqd': 1},
            {'fieldname': 'reference_number', 'fieldtype': 'Data', 'label': 'Reference Number', 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'bl_awb_number', 'fieldtype': 'Data', 'label': 'B/L / AWB Number', 'in_list_view': 1},
            {'fieldname': 'shipment_date', 'fieldtype': 'Date', 'label': 'Shipment Date', 'in_list_view': 1},
            {'fieldname': 'column_break_2', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Pending\nIn Progress\nCleared\nHeld\nCancelled', 'in_list_view': 1, 'default': 'Pending'},
            {'fieldname': 'clearance_date', 'fieldtype': 'Date', 'label': 'Clearance Date'},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'value', 'fieldtype': 'Currency', 'label': 'Shipment Value'},
            {'fieldname': 'cha_charges', 'fieldtype': 'Currency', 'label': 'CHA Charges'},
            {'fieldname': 'remarks', 'fieldtype': 'Small Text', 'label': 'Remarks'}
        ]
    })
    cha_shipment_table.insert(ignore_permissions=True)
    print("Created CHA Shipment DocType")

# Create Customs House Agent DocType
if not frappe.db.exists('DocType', 'Customs House Agent'):
    cha_doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Customs House Agent',
        'module': 'Stock',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:CHA-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'cha_name', 'fieldtype': 'Data', 'label': 'CHA Name', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'cha_license_number', 'fieldtype': 'Data', 'label': 'CHA License Number', 'reqd': 1, 'unique': 1, 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Active\nInactive\nSuspended', 'default': 'Active', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'rating', 'fieldtype': 'Rating', 'label': 'Rating'},
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'License Details'},
            {'fieldname': 'license_issue_date', 'fieldtype': 'Date', 'label': 'License Issue Date'},
            {'fieldname': 'license_valid_till', 'fieldtype': 'Date', 'label': 'License Valid Till'},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'issuing_customs_office', 'fieldtype': 'Data', 'label': 'Issuing Customs Office'},
            {'fieldname': 'customs_port', 'fieldtype': 'Data', 'label': 'Customs Port'},
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Company Information'},
            {'fieldname': 'company_name', 'fieldtype': 'Data', 'label': 'Company Name'},
            {'fieldname': 'address', 'fieldtype': 'Small Text', 'label': 'Address', 'reqd': 1},
            {'fieldname': 'city', 'fieldtype': 'Data', 'label': 'City'},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'state', 'fieldtype': 'Data', 'label': 'State'},
            {'fieldname': 'country', 'fieldtype': 'Link', 'label': 'Country', 'options': 'Country', 'default': 'India'},
            {'fieldname': 'pincode', 'fieldtype': 'Data', 'label': 'Pincode'},
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Contact Details'},
            {'fieldname': 'contact_person', 'fieldtype': 'Data', 'label': 'Contact Person', 'reqd': 1},
            {'fieldname': 'designation', 'fieldtype': 'Data', 'label': 'Designation'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'email', 'fieldtype': 'Data', 'label': 'Email', 'options': 'Email'},
            {'fieldname': 'phone', 'fieldtype': 'Data', 'label': 'Phone'},
            {'fieldname': 'mobile', 'fieldtype': 'Data', 'label': 'Mobile', 'reqd': 1},
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Tax & Registration'},
            {'fieldname': 'pan_number', 'fieldtype': 'Data', 'label': 'PAN Number'},
            {'fieldname': 'gstin', 'fieldtype': 'Data', 'label': 'GSTIN'},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'service_tax_number', 'fieldtype': 'Data', 'label': 'Service Tax Number'},
            {'fieldname': 'customs_code', 'fieldtype': 'Data', 'label': 'Customs Code'},
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Bank Details'},
            {'fieldname': 'bank_name', 'fieldtype': 'Data', 'label': 'Bank Name'},
            {'fieldname': 'bank_account_number', 'fieldtype': 'Data', 'label': 'Account Number'},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'ifsc_code', 'fieldtype': 'Data', 'label': 'IFSC Code'},
            {'fieldname': 'branch', 'fieldtype': 'Data', 'label': 'Branch'},
            {'fieldname': 'section_break_12', 'fieldtype': 'Section Break', 'label': 'Services & Charges'},
            {'fieldname': 'services_offered', 'fieldtype': 'Small Text', 'label': 'Services Offered'},
            {'fieldname': 'specialization', 'fieldtype': 'Select', 'label': 'Specialization', 'options': 'Import\nExport\nBoth', 'default': 'Both'},
            {'fieldname': 'column_break_13', 'fieldtype': 'Column Break'},
            {'fieldname': 'standard_charges', 'fieldtype': 'Currency', 'label': 'Standard Charges'},
            {'fieldname': 'payment_terms', 'fieldtype': 'Data', 'label': 'Payment Terms'},
            {'fieldname': 'section_break_14', 'fieldtype': 'Section Break', 'label': 'Shipment Tracking'},
            {'fieldname': 'shipments', 'fieldtype': 'Table', 'label': 'Shipments', 'options': 'CHA Shipment'},
            {'fieldname': 'section_break_15', 'fieldtype': 'Section Break', 'label': 'Performance Metrics'},
            {'fieldname': 'total_shipments_handled', 'fieldtype': 'Int', 'label': 'Total Shipments Handled', 'read_only': 1, 'default': 0},
            {'fieldname': 'average_clearance_time', 'fieldtype': 'Float', 'label': 'Average Clearance Time (Days)', 'read_only': 1},
            {'fieldname': 'column_break_16', 'fieldtype': 'Column Break'},
            {'fieldname': 'total_value_handled', 'fieldtype': 'Currency', 'label': 'Total Value Handled', 'read_only': 1},
            {'fieldname': 'last_shipment_date', 'fieldtype': 'Date', 'label': 'Last Shipment Date', 'read_only': 1},
            {'fieldname': 'section_break_17', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'column_break_18', 'fieldtype': 'Column Break'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
        ],
        'permissions': [
            {'role': 'Stock User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Stock Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Purchase User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Purchase Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    cha_doc.insert(ignore_permissions=True)
    print("Created Customs House Agent DocType")

frappe.db.commit()
print("Successfully created IEC Registration and CHA tracking systems!")
exit()
PYTHON
