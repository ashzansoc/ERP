#!/usr/bin/env python3
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_bill_of_lading_doctypes():
    frappe.connect()
    frappe.init(site='localhost')
    frappe.connect()
    
    # Create Bill of Lading Container child table first
    if not frappe.db.exists('DocType', 'Bill of Lading Container'):
        container_doc = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Bill of Lading Container',
            'module': 'Stock',
            'custom': 1,
            'istable': 1,
            'editable_grid': 1,
            'fields': [
                {
                    'fieldname': 'container_number',
                    'fieldtype': 'Data',
                    'label': 'Container Number',
                    'in_list_view': 1,
                    'reqd': 1
                },
                {
                    'fieldname': 'container_type',
                    'fieldtype': 'Select',
                    'label': 'Container Type',
                    'options': "20' Standard\n40' Standard\n40' High Cube\n45' High Cube\n20' Refrigerated\n40' Refrigerated\n20' Open Top\n40' Open Top\n20' Flat Rack\n40' Flat Rack",
                    'in_list_view': 1
                },
                {
                    'fieldname': 'seal_number',
                    'fieldtype': 'Data',
                    'label': 'Seal Number',
                    'in_list_view': 1
                },
                {
                    'fieldname': 'column_break_1',
                    'fieldtype': 'Column Break'
                },
                {
                    'fieldname': 'packages',
                    'fieldtype': 'Int',
                    'label': 'Number of Packages',
                    'in_list_view': 1
                },
                {
                    'fieldname': 'weight',
                    'fieldtype': 'Float',
                    'label': 'Weight (KG)',
                    'in_list_view': 1
                },
                {
                    'fieldname': 'volume',
                    'fieldtype': 'Float',
                    'label': 'Volume (CBM)'
                }
            ]
        })
        container_doc.insert(ignore_permissions=True)
        print("Created Bill of Lading Container DocType")
    
    # Create Bill of Lading main DocType
    if not frappe.db.exists('DocType', 'Bill of Lading'):
        bl_doc = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Bill of Lading',
            'module': 'Stock',
            'custom': 1,
            'naming_rule': 'Expression',
            'autoname': 'format:BL-{####}',
            'track_changes': 1,
            'fields': [
                {'fieldname': 'bl_number', 'fieldtype': 'Data', 'label': 'B/L Number', 'reqd': 1, 'unique': 1, 'in_list_view': 1},
                {'fieldname': 'bl_date', 'fieldtype': 'Date', 'label': 'B/L Date', 'reqd': 1, 'in_list_view': 1},
                {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'},
                {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Draft\nBooked\nIn Transit\nArrived at Port\nCustoms Clearance\nOut for Delivery\nDelivered\nCancelled', 'default': 'Draft', 'reqd': 1, 'in_list_view': 1},
                {'fieldname': 'shipment_type', 'fieldtype': 'Select', 'label': 'Shipment Type', 'options': 'FCL (Full Container Load)\nLCL (Less than Container Load)\nBreak Bulk\nRo-Ro'},
                {'fieldname': 'section_break_2', 'fieldtype': 'Section Break', 'label': 'Shipper & Consignee Details'},
                {'fieldname': 'shipper', 'fieldtype': 'Link', 'label': 'Shipper', 'options': 'Supplier'},
                {'fieldname': 'shipper_address', 'fieldtype': 'Small Text', 'label': 'Shipper Address'},
                {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'},
                {'fieldname': 'consignee', 'fieldtype': 'Link', 'label': 'Consignee', 'options': 'Customer'},
                {'fieldname': 'consignee_address', 'fieldtype': 'Small Text', 'label': 'Consignee Address'},
                {'fieldname': 'section_break_4', 'fieldtype': 'Section Break', 'label': 'Notify Party & Delivery Agent'},
                {'fieldname': 'notify_party', 'fieldtype': 'Data', 'label': 'Notify Party'},
                {'fieldname': 'notify_address', 'fieldtype': 'Small Text', 'label': 'Notify Address'},
                {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'},
                {'fieldname': 'delivery_agent', 'fieldtype': 'Data', 'label': 'Delivery Agent / CHA'},
                {'fieldname': 'delivery_agent_contact', 'fieldtype': 'Data', 'label': 'Agent Contact'},
                {'fieldname': 'section_break_6', 'fieldtype': 'Section Break', 'label': 'Port Details'},
                {'fieldname': 'port_of_loading', 'fieldtype': 'Data', 'label': 'Port of Loading', 'reqd': 1, 'in_list_view': 1},
                {'fieldname': 'port_of_discharge', 'fieldtype': 'Data', 'label': 'Port of Discharge', 'reqd': 1, 'in_list_view': 1},
                {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'},
                {'fieldname': 'place_of_receipt', 'fieldtype': 'Data', 'label': 'Place of Receipt'},
                {'fieldname': 'place_of_delivery', 'fieldtype': 'Data', 'label': 'Place of Delivery'},
                {'fieldname': 'section_break_8', 'fieldtype': 'Section Break', 'label': 'Vessel & Carrier Details'},
                {'fieldname': 'vessel_name', 'fieldtype': 'Data', 'label': 'Vessel Name'},
                {'fieldname': 'voyage_number', 'fieldtype': 'Data', 'label': 'Voyage Number'},
                {'fieldname': 'column_break_9', 'fieldtype': 'Column Break'},
                {'fieldname': 'shipping_line', 'fieldtype': 'Data', 'label': 'Shipping Line'},
                {'fieldname': 'carrier_booking_number', 'fieldtype': 'Data', 'label': 'Carrier Booking Number'},
                {'fieldname': 'section_break_10', 'fieldtype': 'Section Break', 'label': 'Container Details'},
                {'fieldname': 'container_details', 'fieldtype': 'Table', 'label': 'Container Details', 'options': 'Bill of Lading Container'},
                {'fieldname': 'section_break_11', 'fieldtype': 'Section Break', 'label': 'Cargo Details'},
                {'fieldname': 'goods_description', 'fieldtype': 'Text Editor', 'label': 'Description of Goods'},
                {'fieldname': 'column_break_12', 'fieldtype': 'Column Break'},
                {'fieldname': 'total_packages', 'fieldtype': 'Int', 'label': 'Total Packages'},
                {'fieldname': 'gross_weight', 'fieldtype': 'Float', 'label': 'Gross Weight (KG)'},
                {'fieldname': 'measurement', 'fieldtype': 'Float', 'label': 'Measurement (CBM)'},
                {'fieldname': 'section_break_13', 'fieldtype': 'Section Break', 'label': 'Freight & Payment'},
                {'fieldname': 'freight_terms', 'fieldtype': 'Select', 'label': 'Freight Terms', 'options': 'Prepaid\nCollect\nThird Party'},
                {'fieldname': 'payment_terms', 'fieldtype': 'Data', 'label': 'Payment Terms'},
                {'fieldname': 'column_break_14', 'fieldtype': 'Column Break'},
                {'fieldname': 'freight_amount', 'fieldtype': 'Currency', 'label': 'Freight Amount'},
                {'fieldname': 'currency', 'fieldtype': 'Link', 'label': 'Currency', 'options': 'Currency'},
                {'fieldname': 'section_break_15', 'fieldtype': 'Section Break', 'label': 'Tracking Information'},
                {'fieldname': 'tracking_status', 'fieldtype': 'Select', 'label': 'Tracking Status', 'options': 'Not Started\nDeparted from Origin\nIn Transit\nArrived at Destination Port\nCustoms Processing\nReleased from Customs\nOut for Delivery\nDelivered'},
                {'fieldname': 'tracking_url', 'fieldtype': 'Data', 'label': 'Tracking URL'},
                {'fieldname': 'column_break_16', 'fieldtype': 'Column Break'},
                {'fieldname': 'estimated_arrival_date', 'fieldtype': 'Date', 'label': 'Estimated Arrival Date'},
                {'fieldname': 'actual_arrival_date', 'fieldtype': 'Date', 'label': 'Actual Arrival Date'},
                {'fieldname': 'section_break_17', 'fieldtype': 'Section Break', 'label': 'Additional Information'},
                {'fieldname': 'remarks', 'fieldtype': 'Text', 'label': 'Remarks'},
                {'fieldname': 'column_break_18', 'fieldtype': 'Column Break'},
                {'fieldname': 'attachments', 'fieldtype': 'Attach', 'label': 'Attachments'}
            ],
            'permissions': [
                {
                    'role': 'Stock User',
                    'read': 1,
                    'write': 1,
                    'create': 1,
                    'delete': 1,
                    'submit': 0,
                    'cancel': 0,
                    'amend': 0
                },
                {
                    'role': 'Stock Manager',
                    'read': 1,
                    'write': 1,
                    'create': 1,
                    'delete': 1,
                    'submit': 0,
                    'cancel': 0,
                    'amend': 0
                }
            ]
        })
        bl_doc.insert(ignore_permissions=True)
        print("Created Bill of Lading DocType")
    
    frappe.db.commit()
    print("Successfully created Bill of Lading tracking system!")

if __name__ == '__main__':
    create_bill_of_lading_doctypes()
