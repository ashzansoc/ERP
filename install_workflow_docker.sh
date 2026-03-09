#!/bin/bash

# Workflow Enhancements Installation for Docker Environment
set -e

echo "=========================================="
echo "Workflow Enhancements Installation (Docker)"
echo "=========================================="
echo ""

SITE_NAME=${1:-localhost}

echo "Installing on site: $SITE_NAME"
echo ""

# Copy files to Docker container
echo "Step 1: Copying files to Docker container..."
docker compose -f frappe_docker/compose.yaml cp install_workflow_enhancements.py backend:/tmp/
docker compose -f frappe_docker/compose.yaml cp api/workflow_automation.py backend:/tmp/
docker compose -f frappe_docker/compose.yaml cp workflow_ui_enhancements.js backend:/tmp/

# Create the API directory if it doesn't exist
echo "Step 2: Setting up API directory..."
docker compose -f frappe_docker/compose.yaml exec -T backend bash -c "
    mkdir -p /home/frappe/frappe-bench/sites/api
    cp /tmp/workflow_automation.py /home/frappe/frappe-bench/sites/api/
    touch /home/frappe/frappe-bench/sites/api/__init__.py
"

# Run the installation script
echo "Step 3: Installing workflow enhancements..."
docker compose -f frappe_docker/compose.yaml exec -T backend bash -c "
    cd /home/frappe/frappe-bench
    bench --site $SITE_NAME console <<EOF
import sys
sys.path.insert(0, '/tmp')
from install_workflow_enhancements import install_workflow_enhancements
install_workflow_enhancements()
EOF
"

# Install the client script
echo "Step 4: Installing UI enhancements..."
docker compose -f frappe_docker/compose.yaml exec -T backend bash -c "
    bench --site $SITE_NAME console <<EOF
import frappe

# Create Client Script for Sales Order
if not frappe.db.exists('Client Script', 'Sales Order Workflow UI'):
    doc = frappe.get_doc({
        'doctype': 'Client Script',
        'name': 'Sales Order Workflow UI',
        'dt': 'Sales Order',
        'enabled': 1,
        'view': 'Form',
        'script': open('/tmp/workflow_ui_enhancements.js').read()
    })
    doc.insert(ignore_permissions=True)
    print('Created Sales Order Client Script')

# Create Client Script for Purchase Order
if not frappe.db.exists('Client Script', 'Purchase Order Workflow UI'):
    doc = frappe.get_doc({
        'doctype': 'Client Script',
        'name': 'Purchase Order Workflow UI',
        'dt': 'Purchase Order',
        'enabled': 1,
        'view': 'Form',
        'script': open('/tmp/workflow_ui_enhancements.js').read()
    })
    doc.insert(ignore_permissions=True)
    print('Created Purchase Order Client Script')

frappe.db.commit()
EOF
"

# Clear cache
echo "Step 5: Clearing cache..."
docker compose -f frappe_docker/compose.yaml exec -T backend bench --site $SITE_NAME clear-cache

echo ""
echo "=========================================="
echo "✓ Workflow Enhancements Installed!"
echo "=========================================="
echo ""
echo "Access your ERP at: http://localhost:8080"
echo ""
echo "Next Steps:"
echo "  1. Login to your ERP"
echo "  2. Go to Sales Order or Purchase Order"
echo "  3. You'll see the new workflow features"
echo ""
