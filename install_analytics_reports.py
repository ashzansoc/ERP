#!/usr/bin/env python3
"""
Analytics Reports Installation Script
Creates report doctypes and dashboards for business intelligence
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def install_analytics_reports():
    """Install all analytics reports and dashboards"""
    print("Installing Analytics Reports System...")
    
    # Create custom fields for analytics
    create_analytics_custom_fields()
    
    # Create report doctypes
    create_country_sales_report()
    create_hs_code_profitability_report()
    create_shipment_delay_report()
    create_port_performance_report()
    create_freight_forwarder_report()
    create_duty_cost_trend_report()
    create_fx_exposure_report()
    
    # Create executive dashboard
    create_executive_dashboard()
    
    print("✓ Analytics Reports System installed successfully!")

def create_analytics_custom_fields():
    """Add custom fields needed for analytics"""
    custom_fields = {
        'Sales Invoice': [
            {
                'fieldname': 'country_of_destination',
                'label': 'Country of Destination',
                'fieldtype': 'Link',
                'options': 'Country',
                'insert_after': 'customer'
            }
        ],
        'Sales Invoice Item': [
            {
                'fieldname': 'hs_code',
                'label': 'HS Code',
                'fieldtype': 'Data',
                'insert_after': 'item_code'
            }
        ],
        'Ocean Shipment': [
            {
                'fieldname': 'freight_forwarder',
                'label': 'Freight Forwarder',
                'fieldtype': 'Link',
                'options': 'Supplier',
                'insert_after': 'carrier'
            },
            {
                'fieldname': 'freight_cost',
                'label': 'Freight Cost',
                'fieldtype': 'Currency',
                'insert_after': 'freight_forwarder'
            }
        ]
    }
    
    create_custom_fields(custom_fields, update=True)
    print("✓ Custom fields created")

def create_country_sales_report():
    """Create Country-wise Sales Report"""
    if not frappe.db.exists('Report', 'Country-wise Sales Analysis'):
        report = frappe.get_doc({
            'doctype': 'Report',
            'name': 'Country-wise Sales Analysis',
            'ref_doctype': 'Sales Invoice',
            'report_name': 'Country-wise Sales Analysis',
            'report_type': 'Script Report',
            'is_standard': 'No',
            'module': 'Selling',
            'disabled': 0,
            'json': '''
{
    "filters": [
        {"fieldname": "from_date", "label": "From Date", "fieldtype": "Date", "default": "Today", "reqd": 1},
        {"fieldname": "to_date", "label": "To Date", "fieldtype": "Date", "default": "Today", "reqd": 1},
        {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "options": "Customer"}
    ],
    "columns": [
        {"fieldname": "country", "label": "Country", "fieldtype": "Data", "width": 150},
        {"fieldname": "shipment_count", "label": "Shipments", "fieldtype": "Int", "width": 100},
        {"fieldname": "total_revenue", "label": "Revenue", "fieldtype": "Currency", "width": 150},
        {"fieldname": "total_quantity", "label": "Quantity", "fieldtype": "Float", "width": 120},
        {"fieldname": "avg_order_value", "label": "Avg Order Value", "fieldtype": "Currency", "width": 150}
    ]
}
            '''
        })
        report.insert(ignore_permissions=True)
        print("✓ Country-wise Sales Report created")

def create_hs_code_profitability_report():
    """Create HS Code Profitability Report"""
    if not frappe.db.exists('Report', 'HS Code Profitability'):
        report = frappe.get_doc({
            'doctype': 'Report',
            'name': 'HS Code Profitability',
            'ref_doctype': 'Sales Invoice',
            'report_name': 'HS Code Profitability',
            'report_type': 'Script Report',
            'is_standard': 'No',
            'module': 'Selling',
            'disabled': 0
        })
        report.insert(ignore_permissions=True)
        print("✓ HS Code Profitability Report created")

def create_shipment_delay_report():
    """Create Shipment Delay Analytics Report"""
    if not frappe.db.exists('Report', 'Shipment Delay Analytics'):
        report = frappe.get_doc({
            'doctype': 'Report',
            'name': 'Shipment Delay Analytics',
            'ref_doctype': 'Ocean Shipment',
            'report_name': 'Shipment Delay Analytics',
            'report_type': 'Script Report',
            'is_standard': 'No',
            'module': 'Stock',
            'disabled': 0
        })
        report.insert(ignore_permissions=True)
        print("✓ Shipment Delay Analytics Report created")

def create_port_performance_report():
    """Create Port Performance Analysis Report"""
    if not frappe.db.exists('Report', 'Port Performance Analysis'):
        report = frappe.get_doc({
            'doctype': 'Report',
            'name': 'Port Performance Analysis',
            'ref_doctype': 'Ocean Shipment',
            'report_name': 'Port Performance Analysis',
            'report_type': 'Script Report',
            'is_standard': 'No',
            'module': 'Stock',
            'disabled': 0
        })
        report.insert(ignore_permissions=True)
        print("✓ Port Performance Report created")

def create_freight_forwarder_report():
    """Create Freight Forwarder Comparison Report"""
    if not frappe.db.exists('Report', 'Freight Forwarder Comparison'):
        report = frappe.get_doc({
            'doctype': 'Report',
            'name': 'Freight Forwarder Comparison',
            'ref_doctype': 'Ocean Shipment',
            'report_name': 'Freight Forwarder Comparison',
            'report_type': 'Script Report',
            'is_standard': 'No',
            'module': 'Stock',
            'disabled': 0
        })
        report.insert(ignore_permissions=True)
        print("✓ Freight Forwarder Comparison Report created")

def create_duty_cost_trend_report():
    """Create Duty Cost Trend Report"""
    if not frappe.db.exists('Report', 'Duty Cost Trend Analysis'):
        report = frappe.get_doc({
            'doctype': 'Report',
            'name': 'Duty Cost Trend Analysis',
            'ref_doctype': 'Sales Invoice',
            'report_name': 'Duty Cost Trend Analysis',
            'report_type': 'Script Report',
            'is_standard': 'No',
            'module': 'Accounts',
            'disabled': 0
        })
        report.insert(ignore_permissions=True)
        print("✓ Duty Cost Trend Report created")

def create_fx_exposure_report():
    """Create FX Exposure Report"""
    if not frappe.db.exists('Report', 'FX Exposure Analysis'):
        report = frappe.get_doc({
            'doctype': 'Report',
            'name': 'FX Exposure Analysis',
            'ref_doctype': 'Sales Invoice',
            'report_name': 'FX Exposure Analysis',
            'report_type': 'Script Report',
            'is_standard': 'No',
            'module': 'Accounts',
            'disabled': 0
        })
        report.insert(ignore_permissions=True)
        print("✓ FX Exposure Report created")

def create_executive_dashboard():
    """Create Executive Dashboard"""
    if not frappe.db.exists('Dashboard', 'Export-Import Executive Dashboard'):
        dashboard = frappe.get_doc({
            'doctype': 'Dashboard',
            'name': 'Export-Import Executive Dashboard',
            'dashboard_name': 'Export-Import Executive Dashboard',
            'module': 'Selling',
            'is_default': 0,
            'charts': []
        })
        dashboard.insert(ignore_permissions=True)
        print("✓ Executive Dashboard created")

if __name__ == '__main__':
    frappe.init(site='site1.local')
    frappe.connect()
    install_analytics_reports()
    frappe.db.commit()
