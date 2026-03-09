#!/bin/bash

# Workflow Enhancements Installation Script
# Installs customized workflows for Export Sales and Import Purchase flows

set -e

echo "=========================================="
echo "Workflow Enhancements Installation"
echo "=========================================="
echo ""

# Check if bench command exists
if ! command -v bench &> /dev/null; then
    echo "Error: bench command not found. Please run this script from your Frappe bench directory."
    exit 1
fi

# Get site name
SITE_NAME=${1:-$(bench --site currentsite 2>/dev/null || echo "")}

if [ -z "$SITE_NAME" ]; then
    echo "Usage: $0 <site-name>"
    echo "Or run from bench directory with a default site configured"
    exit 1
fi

echo "Installing on site: $SITE_NAME"
echo ""

# Run the Python installation script
echo "Step 1: Installing workflow enhancements..."
bench --site "$SITE_NAME" execute install_workflow_enhancements.install_workflow_enhancements

echo ""
echo "Step 2: Creating workflow permissions..."

# Set up role permissions for workflows
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Sales User" --doctype "Sales Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Sales Manager" --doctype "Sales Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Purchase User" --doctype "Purchase Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Purchase Manager" --doctype "Purchase Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Manufacturing User" --doctype "Sales Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Manufacturing Manager" --doctype "Sales Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Stock User" --doctype "Sales Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Stock User" --doctype "Purchase Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Stock Manager" --doctype "Sales Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Stock Manager" --doctype "Purchase Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Accounts User" --doctype "Sales Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Accounts User" --doctype "Purchase Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Accounts Manager" --doctype "Sales Order"
bench --site "$SITE_NAME" execute frappe.commands.utils.add_to_role --role "Accounts Manager" --doctype "Purchase Order"

echo ""
echo "Step 3: Clearing cache..."
bench --site "$SITE_NAME" clear-cache

echo ""
echo "=========================================="
echo "✓ Workflow Enhancements Installed!"
echo "=========================================="
echo ""
echo "Workflows Created:"
echo "  1. Export Sales Flow (Sales Order)"
echo "  2. Import Purchase Flow (Purchase Order)"
echo ""
echo "Next Steps:"
echo "  1. Assign users to appropriate roles"
echo "  2. Test workflow transitions"
echo "  3. Configure email notifications"
echo "  4. Review and customize approval rules"
echo ""
