#!/bin/bash

# Analytics Reports Installation Script
# Installs comprehensive reporting system for export-import business

set -e

SITE_NAME=${1:-site1.local}

echo "=========================================="
echo "Analytics Reports Installation"
echo "=========================================="
echo ""

# Check if bench command exists
if ! command -v bench &> /dev/null; then
    echo "Error: bench command not found. Please run from Frappe bench directory."
    exit 1
fi

echo "Installing on site: $SITE_NAME"
echo ""

# Copy API file
echo "→ Installing analytics API..."
cp api/analytics.py ../frappe-bench/apps/erpnext/erpnext/selling/doctype/ 2>/dev/null || \
cp api/analytics.py ../apps/erpnext/erpnext/selling/doctype/ || \
echo "  Note: Copy analytics.py to your ERPNext app manually"

# Run installation script
echo "→ Creating report doctypes..."
bench --site $SITE_NAME execute install_analytics_reports.install_analytics_reports

# Create HS Code Master doctype if not exists
echo "→ Setting up HS Code Master..."
bench --site $SITE_NAME execute "frappe.get_doc({
    'doctype': 'DocType',
    'name': 'HS Code Master',
    'module': 'Stock',
    'custom': 1,
    'fields': [
        {'fieldname': 'hs_code', 'label': 'HS Code', 'fieldtype': 'Data', 'reqd': 1},
        {'fieldname': 'country', 'label': 'Country', 'fieldtype': 'Link', 'options': 'Country'},
        {'fieldname': 'duty_rate', 'label': 'Duty Rate (%)', 'fieldtype': 'Percent'},
        {'fieldname': 'additional_duty_rate', 'label': 'Additional Duty Rate (%)', 'fieldtype': 'Percent'},
        {'fieldname': 'description', 'label': 'Description', 'fieldtype': 'Text'}
    ],
    'permissions': [{'role': 'System Manager', 'read': 1, 'write': 1, 'create': 1}]
}).insert(ignore_if_duplicate=True)"

echo ""
echo "=========================================="
echo "✓ Analytics Reports Installed Successfully!"
echo "=========================================="
echo ""
echo "Available Reports:"
echo "  1. Country-wise Sales Analysis"
echo "  2. HS Code Profitability"
echo "  3. Shipment Delay Analytics"
echo "  4. Port Performance Analysis"
echo "  5. Freight Forwarder Comparison"
echo "  6. Duty Cost Trend Analysis"
echo "  7. FX Exposure Analysis"
echo ""
echo "Access via: Selling > Reports or Stock > Reports"
echo ""
