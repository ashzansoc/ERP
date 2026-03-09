#!/bin/bash

# Complete Analytics Implementation Script
# This will install everything needed to see analytics in the ERP

set -e

SITE_NAME=${1:-site1.local}

echo "=========================================="
echo "Complete Analytics Implementation"
echo "=========================================="
echo ""
echo "Site: $SITE_NAME"
echo ""

# Check if we're in the right directory
if [ ! -f "api/analytics.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Find the bench directory
if [ -d "../frappe-bench" ]; then
    BENCH_DIR="../frappe-bench"
elif [ -d "frappe-bench" ]; then
    BENCH_DIR="frappe-bench"
elif [ -d "../bench" ]; then
    BENCH_DIR="../bench"
else
    echo "Error: Could not find bench directory"
    echo "Please specify bench directory:"
    read -p "Bench directory path: " BENCH_DIR
fi

echo "Using bench directory: $BENCH_DIR"
echo ""

# Step 1: Copy API file to ERPNext
echo "Step 1: Installing analytics API..."
ERPNEXT_PATH="$BENCH_DIR/apps/erpnext/erpnext"

if [ -d "$ERPNEXT_PATH" ]; then
    cp api/analytics.py "$ERPNEXT_PATH/selling/doctype/" || \
    cp api/analytics.py "$ERPNEXT_PATH/stock/doctype/" || \
    mkdir -p "$ERPNEXT_PATH/custom/analytics" && cp api/analytics.py "$ERPNEXT_PATH/custom/analytics/"
    echo "✓ Analytics API copied"
else
    echo "Warning: ERPNext path not found, will try alternative method"
fi

# Step 2: Create HS Code Master DocType
echo ""
echo "Step 2: Creating HS Code Master DocType..."
cd "$BENCH_DIR"

bench --site $SITE_NAME execute "
import frappe

# Create HS Code Master DocType
if not frappe.db.exists('DocType', 'HS Code Master'):
    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'HS Code Master',
        'module': 'Stock',
        'custom': 1,
        'autoname': 'format:HS-{hs_code}-{country}',
        'fields': [
            {
                'fieldname': 'hs_code',
                'label': 'HS Code',
                'fieldtype': 'Data',
                'reqd': 1,
                'in_list_view': 1
            },
            {
                'fieldname': 'country',
                'label': 'Country',
                'fieldtype': 'Link',
                'options': 'Country',
                'reqd': 1,
                'in_list_view': 1
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
            }
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print('✓ HS Code Master DocType created')
else:
    print('✓ HS Code Master already exists')
"

echo "✓ HS Code Master created"

# Step 3: Add custom fields
echo ""
echo "Step 3: Adding custom fields..."

bench --site $SITE_NAME execute "
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

custom_fields = {
    'Sales Invoice': [
        {
            'fieldname': 'country_of_destination',
            'label': 'Country of Destination',
            'fieldtype': 'Link',
            'options': 'Country',
            'insert_after': 'customer',
            'in_list_view': 0
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

# Add Ocean Shipment fields if doctype exists
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
frappe.db.commit()
print('✓ Custom fields added')
"

echo "✓ Custom fields added"

# Step 4: Create Report DocTypes
echo ""
echo "Step 4: Creating Report DocTypes..."

bench --site $SITE_NAME execute "
import frappe

reports = [
    {
        'name': 'Country-wise Sales Analysis',
        'ref_doctype': 'Sales Invoice',
        'module': 'Selling',
        'report_type': 'Script Report'
    },
    {
        'name': 'HS Code Profitability',
        'ref_doctype': 'Sales Invoice',
        'module': 'Selling',
        'report_type': 'Script Report'
    },
    {
        'name': 'Shipment Delay Analytics',
        'ref_doctype': 'Ocean Shipment',
        'module': 'Stock',
        'report_type': 'Script Report'
    },
    {
        'name': 'Port Performance Analysis',
        'ref_doctype': 'Ocean Shipment',
        'module': 'Stock',
        'report_type': 'Script Report'
    },
    {
        'name': 'Freight Forwarder Comparison',
        'ref_doctype': 'Ocean Shipment',
        'module': 'Stock',
        'report_type': 'Script Report'
    },
    {
        'name': 'Duty Cost Trend Analysis',
        'ref_doctype': 'Sales Invoice',
        'module': 'Accounts',
        'report_type': 'Script Report'
    },
    {
        'name': 'FX Exposure Analysis',
        'ref_doctype': 'Sales Invoice',
        'module': 'Accounts',
        'report_type': 'Script Report'
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
        print(f'✓ Created report: {report_data[\"name\"]}')
    else:
        print(f'✓ Report already exists: {report_data[\"name\"]}')

frappe.db.commit()
"

echo "✓ Reports created"

# Step 5: Create sample data
echo ""
echo "Step 5: Creating sample data..."
echo "This will take a minute..."

cd -
bench --site $SITE_NAME execute create_sample_analytics_data.create_sample_analytics_data

echo "✓ Sample data created"

# Step 6: Create workspace/dashboard
echo ""
echo "Step 6: Creating Analytics Workspace..."

cd "$BENCH_DIR"
bench --site $SITE_NAME execute "
import frappe

# Create Analytics Workspace
if not frappe.db.exists('Workspace', 'Analytics'):
    workspace = frappe.get_doc({
        'doctype': 'Workspace',
        'name': 'Analytics',
        'title': 'Analytics',
        'icon': 'chart',
        'module': 'Selling',
        'is_standard': 0,
        'public': 1,
        'content': '''
# Analytics Dashboard

## Sales Analytics
- Country-wise Sales Analysis
- HS Code Profitability

## Operations Analytics  
- Shipment Delay Analytics
- Port Performance Analysis
- Freight Forwarder Comparison

## Financial Analytics
- Duty Cost Trend Analysis
- FX Exposure Analysis
        '''
    })
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    print('✓ Analytics Workspace created')
else:
    print('✓ Analytics Workspace already exists')
"

echo "✓ Workspace created"

echo ""
echo "=========================================="
echo "✓ Analytics System Installed Successfully!"
echo "=========================================="
echo ""
echo "Access the reports:"
echo ""
echo "1. Go to: Selling > Reports"
echo "   - Country-wise Sales Analysis"
echo "   - HS Code Profitability"
echo ""
echo "2. Go to: Stock > Reports"
echo "   - Shipment Delay Analytics"
echo "   - Port Performance Analysis"
echo "   - Freight Forwarder Comparison"
echo ""
echo "3. Go to: Accounts > Reports"
echo "   - Duty Cost Trend Analysis"
echo "   - FX Exposure Analysis"
echo ""
echo "4. Or search 'Analytics' in the awesome bar"
echo ""
echo "Sample data has been created for demonstration."
echo ""
