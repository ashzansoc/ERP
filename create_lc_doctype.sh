#!/bin/bash
docker compose -f compose.yaml -f overrides/compose.redis.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.noproxy.yaml exec -T backend bench --site localhost console <<'PYTHON'
import frappe

# Create LC Document child table
if not frappe.db.exists('DocType', 'LC Document'):
    lc_doc_table = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'LC Document',
        'module': 'Accounts',
        'custom': 1,
        'istable': 1,
        'editable_grid': 1,
        'fields': [
            {'fieldname': 'document_type', 'fieldtype': 'Select', 'label': 'Document Type', 'options': 'Commercial Invoice\nPacking List\nBill of Lading\nAirway Bill\nCertificate of Origin\nInsurance Certificate\nInspection Certificate\nHealth Certificate\nPhytosanitary Certificate\nOther', 'in_list_view': 1, 'reqd': 1},
            {'fieldname': 'document_number', 'fieldtype': 'Data', 'label': 'Document Number', 'in_list_view': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'required_copies', 'fieldtype': 'Int', 'label': 'Required Copies', 'in_list_view': 1, 'default': 1},
            {'fieldname': 'submitted_copies', 'fieldtype': 'Int', 'label': 'Submitted Copies', 'in_list_view': 1, 'default': 0},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Pending\nSubmitted\nAccepted\nRejected', 'in_list_view': 1, 'default': 'Pending'},
            {'fieldname': 'column_break_2', 'fieldtype': 'Column Break'},
            {'fieldname': 'submission_date', 'fieldtype': 'Date', 'label': 'Submission Date'},
            {'fieldname': 'remarks', 'fieldtype': 'Small Text', 'label': 'Remarks'}
        ]
    })
    lc_doc_table.insert(ignore_permissions=True)
    print("Created LC Document DocType")

# Create LC Amendment child table
if not frappe.db.exists('DocType', 'LC Amendment'):
    lc_amendment_table = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'LC Amendment',
        'module': 'Accounts',
        'custom': 1,
        'istable': 1,
        'editable_grid': 1,
        'fields': [
            {'fieldname': 'amendment_number', 'fieldtype': 'Data', 'label': 'Amendment Number', 'in_list_view': 1, 'reqd': 1},
            {'fieldname': 'amendment_date', 'fieldtype': 'Date', 'label': 'Amendment Date', 'in_list_view': 1, 'reqd': 1},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'amendment_type', 'fieldtype': 'Select', 'label': 'Amendment Type', 'options': 'Amount Increase\nAmount Decrease\nExpiry Extension\nShipment Extension\nTerms Change\nBeneficiary Change\nOther', 'in_list_view': 1},
            {'fieldname': 'description', 'fieldtype': 'Text', 'label': 'Description', 'reqd': 1},
            {'fieldname': 'column_break_2', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Pending\nApproved\nRejected', 'in_list_view': 1, 'default': 'Pending'}
        ]
    })
    lc_amendment_table.insert(ignore_permissions=True)
    print("Created LC Amendment DocType")

# Create Letter of Credit main DocType
if not frappe.db.exists('DocType', 'Letter of Credit'):
    lc_doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Letter of Credit',
        'module': 'Accounts',
        'custom': 1,
        'naming_rule': 'Expression',
        'autoname': 'format:LC-{####}',
        'track_changes': 1,
        'fields': [
            {'fieldname': 'lc_number', 'fieldtype': 'Data', 'label': 'LC Number', 'reqd': 1, 'unique': 1, 'in_list_view': 1},
            {'fieldname': 'lc_date', 'fieldtype': 'Date', 'label': 'LC Date', 'reqd': 1, 'in_list_view': 1, 'default': 'Today'},
            {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
            {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Draft\nIssued\nAdvised\nConfirmed\nDocuments Submitted\nDocuments Accepted\nPayment Released\nCompleted\nCancelled\nExpired', 'default': 'Draft', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'lc_type', 'fieldtype': 'Select', 'label': 'LC Type', 'options': 'Sight LC\nUsance LC\nRevocable LC\nIrrevocable LC\nConfirmed LC\nUnconfirmed LC\nTransferable LC\nBack-to-Back LC\nRed Clause LC\nGreen Clause LC\nStandby LC', 'reqd': 1},
            {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Banking Details'},
            {'fieldname': 'issuing_bank', 'fieldtype': 'Data', 'label': 'Issuing Bank', 'reqd': 1},
            {'fieldname': 'issuing_bank_address', 'fieldtype': 'Small Text', 'label': 'Issuing Bank Address'},
            {'fieldname': 'issuing_bank_swift', 'fieldtype': 'Data', 'label': 'SWIFT Code'},
            {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
            {'fieldname': 'advising_bank', 'fieldtype': 'Data', 'label': 'Advising Bank'},
            {'fieldname': 'advising_bank_address', 'fieldtype': 'Small Text', 'label': 'Advising Bank Address'},
            {'fieldname': 'advising_bank_swift', 'fieldtype': 'Data', 'label': 'SWIFT Code'},
            {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Applicant Details'},
            {'fieldname': 'applicant', 'fieldtype': 'Link', 'label': 'Applicant (Buyer)', 'options': 'Customer', 'reqd': 1},
            {'fieldname': 'applicant_name', 'fieldtype': 'Data', 'label': 'Applicant Name', 'fetch_from': 'applicant.customer_name'},
            {'fieldname': 'applicant_address', 'fieldtype': 'Small Text', 'label': 'Applicant Address'},
            {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
            {'fieldname': 'applicant_country', 'fieldtype': 'Link', 'label': 'Country', 'options': 'Country'},
            {'fieldname': 'applicant_contact', 'fieldtype': 'Data', 'label': 'Contact Person'},
            {'fieldname': 'applicant_email', 'fieldtype': 'Data', 'label': 'Email'},
            {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Beneficiary Details'},
            {'fieldname': 'beneficiary', 'fieldtype': 'Link', 'label': 'Beneficiary (Seller)', 'options': 'Supplier', 'reqd': 1},
            {'fieldname': 'beneficiary_name', 'fieldtype': 'Data', 'label': 'Beneficiary Name', 'fetch_from': 'beneficiary.supplier_name'},
            {'fieldname': 'beneficiary_address', 'fieldtype': 'Small Text', 'label': 'Beneficiary Address'},
            {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
            {'fieldname': 'beneficiary_country', 'fieldtype': 'Link', 'label': 'Country', 'options': 'Country'},
            {'fieldname': 'beneficiary_contact', 'fieldtype': 'Data', 'label': 'Contact Person'},
            {'fieldname': 'beneficiary_email', 'fieldtype': 'Data', 'label': 'Email'},
            {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'LC Amount & Currency'},
            {'fieldname': 'lc_amount', 'fieldtype': 'Currency', 'label': 'LC Amount', 'reqd': 1, 'in_list_view': 1},
            {'fieldname': 'currency', 'fieldtype': 'Link', 'label': 'Currency', 'options': 'Currency', 'reqd': 1},
            {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
            {'fieldname': 'tolerance_percentage', 'fieldtype': 'Percent', 'label': 'Tolerance (+/-)'},
            {'fieldname': 'utilized_amount', 'fieldtype': 'Currency', 'label': 'Utilized Amount', 'read_only': 1},
            {'fieldname': 'balance_amount', 'fieldtype': 'Currency', 'label': 'Balance Amount', 'read_only': 1},
            {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Validity & Shipment'},
            {'fieldname': 'lc_expiry_date', 'fieldtype': 'Date', 'label': 'LC Expiry Date', 'reqd': 1},
            {'fieldname': 'latest_shipment_date', 'fieldtype': 'Date', 'label': 'Latest Shipment Date', 'reqd': 1},
            {'fieldname': 'column_break_11', 'fieldtype': 'Column Break'},
            {'fieldname': 'presentation_period', 'fieldtype': 'Int', 'label': 'Presentation Period (Days)', 'default': 21},
            {'fieldname': 'place_of_expiry', 'fieldtype': 'Data', 'label': 'Place of Expiry'},
            {'fieldname': 'section_break_12', 'fieldtype': 'Section Break', 'label': 'Shipment Details'},
            {'fieldname': 'port_of_loading', 'fieldtype': 'Data', 'label': 'Port of Loading'},
            {'fieldname': 'port_of_discharge', 'fieldtype': 'Data', 'label': 'Port of Discharge'},
            {'fieldname': 'column_break_13', 'fieldtype': 'Column Break'},
            {'fieldname': 'partial_shipment', 'fieldtype': 'Select', 'label': 'Partial Shipment', 'options': 'Allowed\nNot Allowed', 'default': 'Not Allowed'},
            {'fieldname': 'transhipment', 'fieldtype': 'Select', 'label': 'Transhipment', 'options': 'Allowed\nNot Allowed', 'default': 'Not Allowed'},
            {'fieldname': 'section_break_14', 'fieldtype': 'Section Break', 'label': 'Goods Description'},
            {'fieldname': 'goods_description', 'fieldtype': 'Text Editor', 'label': 'Description of Goods', 'reqd': 1},
            {'fieldname': 'quantity', 'fieldtype': 'Data', 'label': 'Quantity'},
            {'fieldname': 'column_break_15', 'fieldtype': 'Column Break'},
            {'fieldname': 'unit_price', 'fieldtype': 'Data', 'label': 'Unit Price'},
            {'fieldname': 'incoterms', 'fieldtype': 'Select', 'label': 'Incoterms', 'options': 'EXW\nFCA\nCPT\nCIP\nDAP\nDPU\nDDP\nFAS\nFOB\nCFR\nCIF'},
            {'fieldname': 'section_break_16', 'fieldtype': 'Section Break', 'label': 'Required Documents'},
            {'fieldname': 'documents', 'fieldtype': 'Table', 'label': 'Documents', 'options': 'LC Document'},
            {'fieldname': 'section_break_17', 'fieldtype': 'Section Break', 'label': 'Payment Terms'},
            {'fieldname': 'payment_terms', 'fieldtype': 'Select', 'label': 'Payment Terms', 'options': 'At Sight\nUsance 30 Days\nUsance 60 Days\nUsance 90 Days\nUsance 120 Days\nUsance 180 Days\nDeferred Payment', 'reqd': 1},
            {'fieldname': 'usance_days', 'fieldtype': 'Int', 'label': 'Usance Days'},
            {'fieldname': 'column_break_18', 'fieldtype': 'Column Break'},
            {'fieldname': 'charges_on', 'fieldtype': 'Select', 'label': 'Charges On', 'options': 'Applicant\nBeneficiary\nShared'},
            {'fieldname': 'reimbursement_bank', 'fieldtype': 'Data', 'label': 'Reimbursement Bank'},
            {'fieldname': 'section_break_19', 'fieldtype': 'Section Break', 'label': 'Amendments'},
            {'fieldname': 'amendments', 'fieldtype': 'Table', 'label': 'Amendments', 'options': 'LC Amendment'},
            {'fieldname': 'section_break_20', 'fieldtype': 'Section Break', 'label': 'Special Conditions'},
            {'fieldname': 'special_conditions', 'fieldtype': 'Text Editor', 'label': 'Special Conditions'},
            {'fieldname': 'column_break_21', 'fieldtype': 'Column Break'},
            {'fieldname': 'additional_instructions', 'fieldtype': 'Text', 'label': 'Additional Instructions'},
            {'fieldname': 'section_break_22', 'fieldtype': 'Section Break', 'label': 'Tracking & Status'},
            {'fieldname': 'document_submission_date', 'fieldtype': 'Date', 'label': 'Document Submission Date'},
            {'fieldname': 'document_acceptance_date', 'fieldtype': 'Date', 'label': 'Document Acceptance Date'},
            {'fieldname': 'column_break_23', 'fieldtype': 'Column Break'},
            {'fieldname': 'payment_release_date', 'fieldtype': 'Date', 'label': 'Payment Release Date'},
            {'fieldname': 'completion_date', 'fieldtype': 'Date', 'label': 'Completion Date'},
            {'fieldname': 'section_break_24', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
            {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
            {'fieldname': 'column_break_25', 'fieldtype': 'Column Break'},
            {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
        ],
        'permissions': [
            {'role': 'Accounts User', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Accounts Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
            {'role': 'Sales User', 'read': 1, 'write': 1, 'create': 1},
            {'role': 'Sales Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1}
        ]
    })
    lc_doc.insert(ignore_permissions=True)
    print("Created Letter of Credit DocType")

frappe.db.commit()
print("Successfully created Letter of Credit tracking system!")
exit()
PYTHON
