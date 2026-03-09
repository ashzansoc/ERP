#!/bin/bash
cd frappe_docker
docker compose -f compose.yaml -f overrides/compose.redis.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.noproxy.yaml exec -T backend bench --site localhost console <<'PYTHON'
import frappe

# Create GST Export Refund Tracking DocType
if not frappe.db.exists('DocType', 'GST Export Refund'):
    gst_refund = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'GST Export Refund',
        'module': 'Accounts',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:GST-REF-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'refund_number', 'fieldtype': 'Data', 'label': 'Refund Number', 'read_only': 1, 'in_list_view': 1},
            {'fieldname': 'application_date', 'fieldtype': 'Date', 'label': 'Application Date', 'reqd': 1, 'default': 'Today', 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Draft\nSubmitted\nUnder Review\nQuery Raised\nApproved\nRejected\nRefund Processed\nCancelled', 'default': 'Draft', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'refund_type', 'fieldtype': 'Select', 'label': 'Refund Type', 'options': 'IGST Refund\nIGST + Cess Refund\nAccumulated ITC Refund', 'reqd': 1},
            
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Company Details'},
            {'fieldname': 'company', 'fieldtype': 'Link', 'label': 'Company', 'options': 'Company', 'reqd': 1},
            {'fieldname': 'gstin', 'fieldtype': 'Data', 'label': 'GSTIN', 'reqd': 1},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'iec_number', 'fieldtype': 'Link', 'label': 'IEC Number', 'options': 'IEC Registration'},
            {'fieldname': 'financial_year', 'fieldtype': 'Data', 'label': 'Financial Year', 'reqd': 1},
            
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Export Details'},
            {'fieldname': 'shipping_bill_number', 'fieldtype': 'Data', 'label': 'Shipping Bill Number', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'shipping_bill_date', 'fieldtype': 'Date', 'label': 'Shipping Bill Date', 'reqd': 1},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'invoice_number', 'fieldtype': 'Link', 'label': 'Invoice Number', 'options': 'Sales Invoice'},
            {'fieldname': 'invoice_date', 'fieldtype': 'Date', 'label': 'Invoice Date'},
            {'fieldname': 'invoice_value', 'fieldtype': 'Currency', 'label': 'Invoice Value', 'reqd': 1},
            
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Refund Calculation'},
            {'fieldname': 'igst_amount', 'fieldtype': 'Currency', 'label': 'IGST Amount', 'reqd': 1},
            {'fieldname': 'cess_amount', 'fieldtype': 'Currency', 'label': 'Cess Amount'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'total_refund_claimed', 'fieldtype': 'Currency', 'label': 'Total Refund Claimed', 'read_only': 1},
            {'fieldname': 'refund_sanctioned', 'fieldtype': 'Currency', 'label': 'Refund Sanctioned'},
            {'fieldname': 'refund_rejected', 'fieldtype': 'Currency', 'label': 'Refund Rejected'},
            
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Processing Details'},
            {'fieldname': 'arn_number', 'fieldtype': 'Data', 'label': 'ARN Number'},
            {'fieldname': 'submission_date', 'fieldtype': 'Date', 'label': 'Submission Date'},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'approval_date', 'fieldtype': 'Date', 'label': 'Approval Date'},
            {'fieldname': 'refund_processed_date', 'fieldtype': 'Date', 'label': 'Refund Processed Date'},
            {'fieldname': 'processing_time_days', 'fieldtype': 'Int', 'label': 'Processing Time (Days)', 'read_only': 1},
            
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Bank Details'},
            {'fieldname': 'bank_name', 'fieldtype': 'Data', 'label': 'Bank Name'},
            {'fieldname': 'account_number', 'fieldtype': 'Data', 'label': 'Account Number'},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'ifsc_code', 'fieldtype': 'Data', 'label': 'IFSC Code'},
            {'fieldname': 'utr_number', 'fieldtype': 'Data', 'label': 'UTR Number'},
            
            {'fieldname': 'section_break_12', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'query_details', 'fieldtype': 'Text', 'label': 'Query Details'},
            {'fieldname': 'column_break_13', 'fieldtype': 'Column Break'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
        ],
        'permissions': [
            {'role': 'Accounts User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Accounts Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    gst_refund.insert(ignore_permissions=True)
    print("Created GST Export Refund DocType")

# Create LUT/Bond Tracking DocType
if not frappe.db.exists('DocType', 'LUT Bond Tracking'):
    lut_bond = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'LUT Bond Tracking',
        'module': 'Accounts',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:LUT-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'document_type', 'fieldtype': 'Select', 'label': 'Document Type', 'options': 'LUT (Letter of Undertaking)\nBond', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'lut_bond_number', 'fieldtype': 'Data', 'label': 'LUT/Bond Number', 'reqd': 1, 'unique': 1, 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Active\nExpiring Soon\nExpired\nRenewed\nCancelled', 'default': 'Active', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'financial_year', 'fieldtype': 'Data', 'label': 'Financial Year', 'reqd': 1},
            
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Company Details'},
            {'fieldname': 'company', 'fieldtype': 'Link', 'label': 'Company', 'options': 'Company', 'reqd': 1},
            {'fieldname': 'gstin', 'fieldtype': 'Data', 'label': 'GSTIN', 'reqd': 1},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'iec_number', 'fieldtype': 'Link', 'label': 'IEC Number', 'options': 'IEC Registration'},
            {'fieldname': 'pan_number', 'fieldtype': 'Data', 'label': 'PAN Number'},
            
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Validity Details'},
            {'fieldname': 'issue_date', 'fieldtype': 'Date', 'label': 'Issue Date', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'valid_from', 'fieldtype': 'Date', 'label': 'Valid From', 'reqd': 1},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'valid_till', 'fieldtype': 'Date', 'label': 'Valid Till', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'days_to_expiry', 'fieldtype': 'Int', 'label': 'Days to Expiry', 'read_only': 1},
            {'fieldname': 'renewal_required', 'fieldtype': 'Check', 'label': 'Renewal Required', 'read_only': 1},
            
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Bond Details (If Applicable)'},
            {'fieldname': 'bond_amount', 'fieldtype': 'Currency', 'label': 'Bond Amount'},
            {'fieldname': 'bank_guarantee_number', 'fieldtype': 'Data', 'label': 'Bank Guarantee Number'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'issuing_bank', 'fieldtype': 'Data', 'label': 'Issuing Bank'},
            {'fieldname': 'bg_expiry_date', 'fieldtype': 'Date', 'label': 'BG Expiry Date'},
            
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Submission Details'},
            {'fieldname': 'submitted_to', 'fieldtype': 'Data', 'label': 'Submitted To', 'default': 'GST Department'},
            {'fieldname': 'submission_date', 'fieldtype': 'Date', 'label': 'Submission Date'},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'acknowledgement_number', 'fieldtype': 'Data', 'label': 'Acknowledgement Number'},
            {'fieldname': 'acknowledgement_date', 'fieldtype': 'Date', 'label': 'Acknowledgement Date'},
            
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Renewal Tracking'},
            {'fieldname': 'renewal_application_date', 'fieldtype': 'Date', 'label': 'Renewal Application Date'},
            {'fieldname': 'renewed_lut_number', 'fieldtype': 'Link', 'label': 'Renewed LUT Number', 'options': 'LUT Bond Tracking'},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'previous_lut_number', 'fieldtype': 'Link', 'label': 'Previous LUT Number', 'options': 'LUT Bond Tracking'},
            
            {'fieldname': 'section_break_12', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'column_break_13', 'fieldtype': 'Column Break'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
        ],
        'permissions': [
            {'role': 'Accounts User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Accounts Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    lut_bond.insert(ignore_permissions=True)
    print("Created LUT Bond Tracking DocType")

frappe.db.commit()
print("Phase 1 Complete: Created GST Refund and LUT/Bond Tracking")
exit()
PYTHON
