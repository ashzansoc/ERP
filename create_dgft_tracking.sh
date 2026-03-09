#!/bin/bash
cd frappe_docker
docker compose -f compose.yaml -f overrides/compose.redis.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.noproxy.yaml exec -T backend bench --site localhost console <<'PYTHON'
import frappe

# Create DGFT Scheme Tracking DocType
if not frappe.db.exists('DocType', 'DGFT Scheme Tracking'):
    dgft_scheme = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'DGFT Scheme Tracking',
        'module': 'Selling',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:DGFT-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'scheme_name', 'fieldtype': 'Select', 'label': 'Scheme Name', 'options': 'Advance Authorization\nDFIA (Duty Free Import Authorization)\nEPCG (Export Promotion Capital Goods)\nEOU (Export Oriented Unit)\nSEZ (Special Economic Zone)\nAdvance Authorization for Annual Requirement\nDuty Exemption Scheme\nDuty Remission Scheme', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'authorization_number', 'fieldtype': 'Data', 'label': 'Authorization Number', 'unique': 1, 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Applied\nIssued\nPartially Utilized\nFully Utilized\nExport Obligation Pending\nExport Obligation Fulfilled\nExpired\nCancelled', 'default': 'Applied', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'application_date', 'fieldtype': 'Date', 'label': 'Application Date', 'default': 'Today', 'reqd': 1},
            
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Company Details'},
            {'fieldname': 'company', 'fieldtype': 'Link', 'label': 'Company', 'options': 'Company', 'reqd': 1},
            {'fieldname': 'iec_number', 'fieldtype': 'Link', 'label': 'IEC Number', 'options': 'IEC Registration', 'reqd': 1},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'gstin', 'fieldtype': 'Data', 'label': 'GSTIN'},
            {'fieldname': 'pan_number', 'fieldtype': 'Data', 'label': 'PAN Number'},
            
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Authorization Details'},
            {'fieldname': 'issue_date', 'fieldtype': 'Date', 'label': 'Issue Date', 'in_list_view': 1},
            {'fieldname': 'valid_from', 'fieldtype': 'Date', 'label': 'Valid From'},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'valid_till', 'fieldtype': 'Date', 'label': 'Valid Till', 'in_list_view': 1},
            {'fieldname': 'days_to_expiry', 'fieldtype': 'Int', 'label': 'Days to Expiry', 'read_only': 1},
            
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Import Details'},
            {'fieldname': 'import_value_allowed', 'fieldtype': 'Currency', 'label': 'Import Value Allowed', 'reqd': 1},
            {'fieldname': 'import_value_utilized', 'fieldtype': 'Currency', 'label': 'Import Value Utilized', 'default': 0},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'import_value_balance', 'fieldtype': 'Currency', 'label': 'Import Value Balance', 'read_only': 1},
            {'fieldname': 'duty_saved', 'fieldtype': 'Currency', 'label': 'Duty Saved'},
            
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Export Obligation'},
            {'fieldname': 'export_obligation_value', 'fieldtype': 'Currency', 'label': 'Export Obligation Value', 'reqd': 1},
            {'fieldname': 'export_obligation_fulfilled', 'fieldtype': 'Currency', 'label': 'Export Obligation Fulfilled', 'default': 0},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'export_obligation_pending', 'fieldtype': 'Currency', 'label': 'Export Obligation Pending', 'read_only': 1},
            {'fieldname': 'export_obligation_deadline', 'fieldtype': 'Date', 'label': 'Export Obligation Deadline', 'reqd': 1},
            {'fieldname': 'export_obligation_percentage', 'fieldtype': 'Percent', 'label': 'Export Obligation Fulfilled (%)', 'read_only': 1},
            
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Product Details'},
            {'fieldname': 'import_items', 'fieldtype': 'Text', 'label': 'Import Items Description'},
            {'fieldname': 'export_product', 'fieldtype': 'Text', 'label': 'Export Product Description'},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'hs_code_import', 'fieldtype': 'Link', 'label': 'HS Code (Import)', 'options': 'Customs Tariff Number'},
            {'fieldname': 'hs_code_export', 'fieldtype': 'Link', 'label': 'HS Code (Export)', 'options': 'Customs Tariff Number'},
            
            {'fieldname': 'section_break_12', 'fieldtype': 'Section Break', 'label': 'Bond Details'},
            {'fieldname': 'bond_number', 'fieldtype': 'Data', 'label': 'Bond Number'},
            {'fieldname': 'bond_amount', 'fieldtype': 'Currency', 'label': 'Bond Amount'},
            {'fieldname': 'column_break_13', 'fieldtype': 'Column Break'},
            {'fieldname': 'bank_guarantee_number', 'fieldtype': 'Data', 'label': 'Bank Guarantee Number'},
            {'fieldname': 'bg_amount', 'fieldtype': 'Currency', 'label': 'BG Amount'},
            {'fieldname': 'bg_expiry_date', 'fieldtype': 'Date', 'label': 'BG Expiry Date'},
            
            {'fieldname': 'section_break_14', 'fieldtype': 'Section Break', 'label': 'Extension & Amendments'},
            {'fieldname': 'extension_applied', 'fieldtype': 'Check', 'label': 'Extension Applied'},
            {'fieldname': 'extension_granted_till', 'fieldtype': 'Date', 'label': 'Extension Granted Till'},
            {'fieldname': 'column_break_15', 'fieldtype': 'Column Break'},
            {'fieldname': 'amendment_count', 'fieldtype': 'Int', 'label': 'Amendment Count', 'default': 0},
            {'fieldname': 'last_amendment_date', 'fieldtype': 'Date', 'label': 'Last Amendment Date'},
            
            {'fieldname': 'section_break_16', 'fieldtype': 'Section Break', 'label': 'Compliance Status'},
            {'fieldname': 'compliance_status', 'fieldtype': 'Select', 'label': 'Compliance Status', 'options': 'Compliant\nNon-Compliant\nUnder Review\nPenalty Imposed', 'default': 'Compliant'},
            {'fieldname': 'penalty_amount', 'fieldtype': 'Currency', 'label': 'Penalty Amount'},
            {'fieldname': 'column_break_17', 'fieldtype': 'Column Break'},
            {'fieldname': 'redemption_date', 'fieldtype': 'Date', 'label': 'Redemption Date'},
            {'fieldname': 'redemption_status', 'fieldtype': 'Select', 'label': 'Redemption Status', 'options': 'Pending\nIn Progress\nCompleted'},
            
            {'fieldname': 'section_break_18', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'column_break_19', 'fieldtype': 'Column Break'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
        ],
        'permissions': [
            {'role': 'Sales User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Sales Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Accounts User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Accounts Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    dgft_scheme.insert(ignore_permissions=True)
    print("Created DGFT Scheme Tracking DocType")

frappe.db.commit()
print("Phase 3 Complete: Created DGFT Scheme Tracking")
exit()
PYTHON
