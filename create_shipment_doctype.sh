#!/bin/bash

# Script to create Shipment and Container Tracking DocTypes in Frappe

echo "🚢 Creating Shipment & Container Tracking Module..."

# Generate JSON files
python3 create_shipment_doctype.py

# Check if bench command is available
if ! command -v bench &> /dev/null; then
    echo "❌ Error: bench command not found. Please run this script from your Frappe bench directory."
    exit 1
fi

# Get site name (you may need to modify this)
SITE_NAME=${1:-"site1.local"}

echo "📦 Installing Shipment Container DocType..."
bench --site $SITE_NAME import-doc shipment_container_doctype.json

echo "📦 Installing Shipment DocType..."
bench --site $SITE_NAME import-doc shipment_doctype.json

echo "🔄 Clearing cache..."
bench --site $SITE_NAME clear-cache

echo "✅ Shipment & Container Tracking module created successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Login to your Frappe/ERPNext instance"
echo "2. Go to: Desk → Stock → Shipment"
echo "3. Create your first shipment record"
echo ""
echo "🎯 Features included:"
echo "   ✓ Shipment Type (Import/Export)"
echo "   ✓ Port of Loading & Discharge"
echo "   ✓ ETD/ETA tracking"
echo "   ✓ Multiple containers per shipment"
echo "   ✓ Shipping Line & Vessel details"
echo "   ✓ Freight Forwarder information"
echo "   ✓ Status Workflow: Draft → Booked → In Transit → Customs → Delivered"
echo "   ✓ Link to Bill of Lading"
