#!/bin/bash
cd frappe_docker
docker compose -f compose.yaml -f overrides/compose.redis.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.noproxy.yaml exec -T backend bench --site localhost console <<'PYTHON'
import frappe

# Create MEIS/RoDTEP Benefit Tracking DocType
if not frappe.db.exists('DocType', 'Export Incentive Scheme'):
    export_scheme = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Export Incentive Scheme',
        'module': 'Selling',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:EIS-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'scheme_type', 'fieldtype': 'Select', 'label': 'Scheme Type', 'options': 'MEIS (Merchandise Exports from India Scheme)\nRoDTEP (Remission of Duties and Taxes on Exported Products)\nSEIS (Service Exports from India Scheme)\nRoSCTL (Rebate of State and Central Taxes and Levies)', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'application_number', 'fieldtype': 'Data', 'label': 'Application Number', 'unique': 1, 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Draft\nSubmitted\nUnder Review\nApproved\nRejected\nScrip Issued\nScrip Utilized\nCancelled', 'default': 'Draft', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'application_date', 'fieldtype': 'Date', 'label': 'Application Date', 'default': 'Today', 'reqd': 1},
            
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Company Details'},
            {'fieldname': 'company', 'fieldtype': 'Link', 'label': 'Company', 'options': 'Company', 'reqd': 1},
            {'fieldname': 'iec_number', 'fieldtype': 'Link', 'label': 'IEC Number', 'options': 'IEC Registration', 'reqd': 1},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'gstin', 'fieldtype': 'Data', 'label': 'GSTIN'},
            {'fieldname': 'pan_number', 'fieldtype': 'Data', 'label': 'PAN Number'},
            
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Export Details'},
            {'fieldname': 'shipping_bill_number', 'fieldtype': 'Data', 'label': 'Shipping Bill Number', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'shipping_bill_date', 'fieldtype': 'Date', 'label': 'Shipping Bill Date', 'reqd': 1},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'invoice_number', 'fieldtype': 'Link', 'label': 'Invoice Number', 'options': 'Sales Invoice'},
            {'fieldname': 'invoice_date', 'fieldtype': 'Date', 'label': 'Invoice Date'},
            {'fieldname': 'fob_value', 'fieldtype': 'Currency', 'label': 'FOB Value', 'reqd': 1},
            
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Product Details'},
            {'fieldname': 'hs_code', 'fieldtype': 'Link', 'label': 'HS Code', 'options': 'Customs Tariff Number'},
            {'fieldname': 'product_description', 'fieldtype': 'Small Text', 'label': 'Product Description'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'destination_country', 'fieldtype': 'Link', 'label': 'Destination Country', 'options': 'Country'},
            {'fieldname': 'port_of_export', 'fieldtype': 'Data', 'label': 'Port of Export'},
            
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Incentive Calculation'},
            {'fieldname': 'incentive_rate', 'fieldtype': 'Percent', 'label': 'Incentive Rate (%)', 'reqd': 1},
            {'fieldname': 'eligible_value', 'fieldtype': 'Currency', 'label': 'Eligible Value', 'reqd': 1},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'incentive_amount', 'fieldtype': 'Currency', 'label': 'Incentive Amount', 'read_only': 1},
            {'fieldname': 'approved_amount', 'fieldtype': 'Currency', 'label': 'Approved Amount'},
            
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Scrip Details'},
            {'fieldname': 'scrip_number', 'fieldtype': 'Data', 'label': 'Scrip Number'},
            {'fieldname': 'scrip_issue_date', 'fieldtype': 'Date', 'label': 'Scrip Issue Date'},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'scrip_value', 'fieldtype': 'Currency', 'label': 'Scrip Value'},
            {'fieldname': 'scrip_expiry_date', 'fieldtype': 'Date', 'label': 'Scrip Expiry Date'},
            {'fieldname': 'scrip_utilized_amount', 'fieldtype': 'Currency', 'label': 'Scrip Utilized Amount'},
            
            {'fieldname': 'section_break_12', 'fieldtype': 'Section Break', 'label': 'Processing Timeline'},
            {'fieldname': 'submission_date', 'fieldtype': 'Date', 'label': 'Submission Date'},
            {'fieldname': 'approval_date', 'fieldtype': 'Date', 'label': 'Approval Date'},
            {'fieldname': 'column_break_13', 'fieldtype': 'Column Break'},
            {'fieldname': 'processing_time_days', 'fieldtype': 'Int', 'label': 'Processing Time (Days)', 'read_only': 1},
            {'fieldname': 'rejection_reason', 'fieldtype': 'Text', 'label': 'Rejection Reason'},
            
            {'fieldname': 'section_break_14', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'column_break_15', 'fieldtype': 'Column Break'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
        ],
        'permissions': [
            {'role': 'Sales User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Sales Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Accounts User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Accounts Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    export_scheme.insert(ignore_permissions=True)
    print("Created Export Incentive Scheme DocType")

# Create Duty Drawback Module DocType
if not frappe.db.exists('DocType', 'Duty Drawback Claim'):
    duty_drawback = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Duty Drawback Claim',
        'module': 'Accounts',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:DDB-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'claim_number', 'fieldtype': 'Data', 'label': 'Claim Number', 'read_only': 1, 'in_list_view': 1},
            {'fieldname': 'claim_date', 'fieldtype': 'Date', 'label': 'Claim Date', 'default': 'Today', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Draft\nSubmitted\nUnder Verification\nApproved\nRejected\nPayment Processed\nCancelled', 'default': 'Draft', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'drawback_type', 'fieldtype': 'Select', 'label': 'Drawback Type', 'options': 'All Industry Rate (AIR)\nBrand Rate\nSpecial Brand Rate', 'reqd': 1},
            
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Company Details'},
            {'fieldname': 'company', 'fieldtype': 'Link', 'label': 'Company', 'options': 'Company', 'reqd': 1},
            {'fieldname': 'iec_number', 'fieldtype': 'Link', 'label': 'IEC Number', 'options': 'IEC Registration', 'reqd': 1},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'gstin', 'fieldtype': 'Data', 'label': 'GSTIN'},
            {'fieldname': 'pan_number', 'fieldtype': 'Data', 'label': 'PAN Number'},
            
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Export Details'},
            {'fieldname': 'shipping_bill_number', 'fieldtype': 'Data', 'label': 'Shipping Bill Number', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'shipping_bill_date', 'fieldtype': 'Date', 'label': 'Shipping Bill Date', 'reqd': 1},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'invoice_number', 'fieldtype': 'Link', 'label': 'Invoice Number', 'options': 'Sales Invoice'},
            {'fieldname': 'invoice_date', 'fieldtype': 'Date', 'label': 'Invoice Date'},
            {'fieldname': 'fob_value', 'fieldtype': 'Currency', 'label': 'FOB Value', 'reqd': 1},
            
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Product Details'},
            {'fieldname': 'hs_code', 'fieldtype': 'Link', 'label': 'HS Code', 'options': 'Customs Tariff Number'},
            {'fieldname': 'product_description', 'fieldtype': 'Small Text', 'label': 'Product Description'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'quantity_exported', 'fieldtype': 'Float', 'label': 'Quantity Exported'},
            {'fieldname': 'uom', 'fieldtype': 'Link', 'label': 'UOM', 'options': 'UOM'},
            
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Drawback Calculation'},
            {'fieldname': 'drawback_rate', 'fieldtype': 'Currency', 'label': 'Drawback Rate (per unit)'},
            {'fieldname': 'drawback_percentage', 'fieldtype': 'Percent', 'label': 'Drawback Percentage'},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'calculated_drawback', 'fieldtype': 'Currency', 'label': 'Calculated Drawback', 'read_only': 1},
            {'fieldname': 'claimed_amount', 'fieldtype': 'Currency', 'label': 'Claimed Amount', 'reqd': 1},
            {'fieldname': 'sanctioned_amount', 'fieldtype': 'Currency', 'label': 'Sanctioned Amount'},
            
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Customs Details'},
            {'fieldname': 'customs_port', 'fieldtype': 'Data', 'label': 'Customs Port'},
            {'fieldname': 'customs_officer', 'fieldtype': 'Data', 'label': 'Customs Officer'},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'verification_date', 'fieldtype': 'Date', 'label': 'Verification Date'},
            {'fieldname': 'approval_date', 'fieldtype': 'Date', 'label': 'Approval Date'},
            
            {'fieldname': 'section_break_12', 'fieldtype': 'Section Break', 'label': 'Payment Details'},
            {'fieldname': 'bank_name', 'fieldtype': 'Data', 'label': 'Bank Name'},
            {'fieldname': 'account_number', 'fieldtype': 'Data', 'label': 'Account Number'},
            {'fieldname': 'column_break_13', 'fieldtype': 'Column Break'},
            {'fieldname': 'ifsc_code', 'fieldtype': 'Data', 'label': 'IFSC Code'},
            {'fieldname': 'payment_date', 'fieldtype': 'Date', 'label': 'Payment Date'},
            {'fieldname': 'utr_number', 'fieldtype': 'Data', 'label': 'UTR Number'},
            
            {'fieldname': 'section_break_14', 'fieldtype': 'Section Break', 'label': 'Processing Timeline'},
            {'fieldname': 'submission_date', 'fieldtype': 'Date', 'label': 'Submission Date'},
            {'fieldname': 'processing_time_days', 'fieldtype': 'Int', 'label': 'Processing Time (Days)', 'read_only': 1},
            {'fieldname': 'column_break_15', 'fieldtype': 'Column Break'},
            {'fieldname': 'rejection_reason', 'fieldtype': 'Text', 'label': 'Rejection Reason'},
            
            {'fieldname': 'section_break_16', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'column_break_17', 'fieldtype': 'Column Break'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
        ],
        'permissions': [
            {'role': 'Accounts User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Accounts Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    duty_drawback.insert(ignore_permissions=True)
    print("Created Duty Drawback Claim DocType")

frappe.db.commit()
print("Phase 2 Complete: Created Export Incentive Scheme and Duty Drawback")
exit()
PYTHON
