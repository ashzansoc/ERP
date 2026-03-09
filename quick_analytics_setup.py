#!/usr/bin/env python3
"""
Quick Analytics Setup - Run this directly in bench console
Usage: bench --site site1.local execute quick_analytics_setup.setup_analytics
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import json

def setup_analytics():
    """Complete analytics setup in one go"""
    
    print("\n" + "="*60)
    print("ANALYTICS SYSTEM SETUP")
    print("="*60 + "\n")
    
    # Step 1: Create HS Code Master
    create_hs_code_master()
    
    # Step 2: Add custom fields
    add_custom_fields()
    
    # Step 3: Create reports
    create_reports()
    
    # Step 4: Create workspace
    create_workspace()
    
    # Step 5: Add sample data
    create_sample_data()
    
    frappe.db.commit()
    
    print("\n" + "="*60)
    print("✓ ANALYTICS SYSTEM READY!")
    print("="*60)
    print("\nAccess reports from:")
    print("  • Selling > Reports")
    print("  • Stock > Reports")
    print("  • Accounts > Reports")
    print("  • Or search 'Analytics' in awesome bar")
    print("\n")

def create_hs_code_master():
    """Create HS Code Master DocType"""
    print("→ Creating HS Code Master DocType...")
    
    if frappe.db.exists('DocType', 'HS Code Master'):
        print("  ✓ Already exists")
        return
    
    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'HS Code Master',
        'module': 'Stock',
        'custom': 1,
        'autoname': 'format:HS-{hs_code}-{country}',
        'naming_rule': 'Expression',
        'fields': [
            {
                'fieldname': 'hs_code',
                'label': 'HS Code',
                'fieldtype': 'Data',
                'reqd': 1,
                'in_list_view': 1,
                'in_standard_filter': 1
            },
            {
                'fieldname': 'country',
                'label': 'Country',
                'fieldtype': 'Link',
                'options': 'Country',
                'reqd': 1,
                'in_list_view': 1,
                'in_standard_filter': 1
            },
            {
                'fieldname': 'section_break_1',
                'fieldtype': 'Section Break',
                'label': 'Duty Rates'
            },
            {
                'fieldname': 'duty_rate',
                'label': 'Duty Rate (%)',
                'fieldtype': 'Percent',
                'in_list_view': 1
            },
            {
                'fieldname': 'additional_duty_rate',
                'label': 'Additional Duty Rate (%)',
                'fieldtype': 'Percent'
            },
            {
                'fieldname': 'section_break_2',
                'fieldtype': 'Section Break',
                'label': 'Details'
            },
            {
                'fieldname': 'description',
                'label': 'Description',
                'fieldtype': 'Text'
            }
        ],
        'permissions': [
            {
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1
            },
            {
                'role': 'Sales User',
                'read': 1
            },
            {
                'role': 'Stock User',
                'read': 1
            }
        ]
    })
    doc.insert(ignore_permissions=True)
    print("  ✓ HS Code Master created")

def add_custom_fields():
    """Add custom fields to existing doctypes"""
    print("→ Adding custom fields...")
    
    custom_fields = {
        'Sales Invoice': [
            {
                'fieldname': 'country_of_destination',
                'label': 'Country of Destination',
                'fieldtype': 'Link',
                'options': 'Country',
                'insert_after': 'customer',
                'in_list_view': 0,
                'in_standard_filter': 1
            }
        ],
        'Sales Invoice Item': [
            {
                'fieldname': 'hs_code',
                'label': 'HS Code',
                'fieldtype': 'Data',
                'insert_after': 'item_code',
                'in_list_view': 0
            }
        ]
    }
    
    # Add Ocean Shipment fields if it exists
    if frappe.db.exists('DocType', 'Ocean Shipment'):
        custom_fields['Ocean Shipment'] = [
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
    
    create_custom_fields(custom_fields, update=True)
    print("  ✓ Custom fields added")

def create_reports():
    """Create all analytics reports"""
    print("→ Creating analytics reports...")
    
    reports = [
        {
            'name': 'Country-wise Sales Analysis',
            'ref_doctype': 'Sales Invoice',
            'module': 'Selling',
            'report_type': 'Script Report',
            'description': 'Analyze sales by destination country with trends'
        },
        {
            'name': 'HS Code Profitability',
            'ref_doctype': 'Sales Invoice',
            'module': 'Selling',
            'report_type': 'Script Report',
            'description': 'Product profitability by HS code classification'
        },
        {
            'name': 'Shipment Delay Analytics',
            'ref_doctype': 'Ocean Shipment',
            'module': 'Stock',
            'report_type': 'Script Report',
            'description': 'Track shipment delays by carrier and route'
        },
        {
            'name': 'Port Performance Analysis',
            'ref_doctype': 'Ocean Shipment',
            'module': 'Stock',
            'report_type': 'Script Report',
            'description': 'Evaluate port efficiency and throughput'
        },
        {
            'name': 'Freight Forwarder Comparison',
            'ref_doctype': 'Ocean Shipment',
            'module': 'Stock',
            'report_type': 'Script Report',
            'description': 'Compare freight forwarders on cost and performance'
        },
        {
            'name': 'Duty Cost Trend Analysis',
            'ref_doctype': 'Sales Invoice',
            'module': 'Accounts',
            'report_type': 'Script Report',
            'description': 'Track customs duty costs over time'
        },
        {
            'name': 'FX Exposure Analysis',
            'ref_doctype': 'Sales Invoice',
            'module': 'Accounts',
            'report_type': 'Script Report',
            'description': 'Analyze foreign exchange exposure and risk'
        }
    ]
    
    for report_data in reports:
        if not frappe.db.exists('Report', report_data['name']):
            report = frappe.get_doc({
                'doctype': 'Report',
                'name': report_data['name'],
                'ref_doctype': report_data['ref_doctype'],
                'report_name': report_data['name'],
                'report_type': report_data['report_type'],
                'is_standard': 'No',
                'module': report_data['module'],
                'disabled': 0
            })
            report.insert(ignore_permissions=True)
            print(f"  ✓ {report_data['name']}")
        else:
            print(f"  ✓ {report_data['name']} (already exists)")

def create_workspace():
    """Create Analytics workspace"""
    print("→ Creating Analytics workspace...")
    
    if frappe.db.exists('Workspace', 'Analytics'):
        print("  ✓ Already exists")
        return
    
    workspace = frappe.get_doc({
        'doctype': 'Workspace',
        'name': 'Analytics',
        'title': 'Analytics',
        'icon': 'chart-line',
        'module': 'Selling',
        'is_standard': 0,
        'public': 1
    })
    workspace.insert(ignore_permissions=True)
    print("  ✓ Analytics workspace created")

def create_sample_data():
    """Create sample data for testing"""
    print("→ Creating sample data...")
    
    import random
    from frappe.utils import today, add_days, add_months
    
    # Sample countries
    countries = ['United States', 'United Kingdom', 'Germany', 'Japan', 'Australia']
    
    # Sample HS codes
    hs_codes = [
        {'code': '8471.30', 'desc': 'Portable computers', 'duty': 5.5},
        {'code': '8517.12', 'desc': 'Smartphones', 'duty': 0.0},
        {'code': '8528.72', 'desc': 'LCD monitors', 'duty': 3.9},
        {'code': '9403.60', 'desc': 'Wooden furniture', 'duty': 0.0},
        {'code': '6204.62', 'desc': 'Cotton trousers', 'duty': 16.6}
    ]
    
    # Create HS Code Master records
    count = 0
    for country in countries[:3]:  # Limit to 3 countries for speed
        for hs in hs_codes[:3]:  # Limit to 3 HS codes
            key = f"{hs['code']}-{country}"
            if not frappe.db.exists('HS Code Master', {'hs_code': hs['code'], 'country': country}):
                try:
                    frappe.get_doc({
                        'doctype': 'HS Code Master',
                        'hs_code': hs['code'],
                        'country': country,
                        'duty_rate': hs['duty'],
                        'additional_duty_rate': 2.0,
                        'description': hs['desc']
                    }).insert(ignore_permissions=True)
                    count += 1
                except Exception as e:
                    pass
    
    if count > 0:
        print(f"  ✓ Created {count} HS Code Master records")
    else:
        print("  ✓ Sample HS codes already exist")
    
    print("  ✓ Sample data ready")

if __name__ == '__main__':
    setup_analytics()
