#!/bin/bash

# Simple one-command analytics installation
# Usage: ./install_analytics_now.sh

SITE_NAME=${1:-site1.local}

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         ANALYTICS SYSTEM - QUICK INSTALLATION              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Site: $SITE_NAME"
echo ""

# Check if bench command exists
if ! command -v bench &> /dev/null; then
    echo "❌ Error: bench command not found"
    echo "   Please run from frappe-bench directory or install bench"
    exit 1
fi

# Check if site exists
if ! bench --site $SITE_NAME list-apps &> /dev/null; then
    echo "❌ Error: Site '$SITE_NAME' not found"
    echo "   Available sites:"
    ls -1 sites/*/site_config.json 2>/dev/null | cut -d'/' -f2
    exit 1
fi

echo "Installing analytics system..."
echo ""

# Run the Python setup script
bench --site $SITE_NAME execute quick_analytics_setup.setup_analytics

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                  ✓ INSTALLATION COMPLETE!                 ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Analytics system is now live in your ERP!"
    echo ""
    echo "📊 Access your reports:"
    echo ""
    echo "   Method 1: From Modules"
    echo "   ├─ Selling > Reports > Country-wise Sales Analysis"
    echo "   ├─ Selling > Reports > HS Code Profitability"
    echo "   ├─ Stock > Reports > Shipment Delay Analytics"
    echo "   ├─ Stock > Reports > Port Performance Analysis"
    echo "   ├─ Stock > Reports > Freight Forwarder Comparison"
    echo "   ├─ Accounts > Reports > Duty Cost Trend Analysis"
    echo "   └─ Accounts > Reports > FX Exposure Analysis"
    echo ""
    echo "   Method 2: Search Bar"
    echo "   └─ Press Ctrl+K (or Cmd+K) and type 'Analytics'"
    echo ""
    echo "   Method 3: Direct URLs"
    echo "   └─ http://localhost:8000/app/query-report/Country-wise%20Sales%20Analysis"
    echo ""
    echo "📝 Sample data has been created for testing"
    echo ""
    echo "📖 Read ANALYTICS_IMPLEMENTATION.md for detailed usage"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Check the error messages above."
    echo ""
    echo "Common fixes:"
    echo "  1. Make sure you're in the frappe-bench directory"
    echo "  2. Ensure the site is running: bench start"
    echo "  3. Check permissions: bench --site $SITE_NAME console"
    echo "  4. View logs: tail -f logs/$SITE_NAME/error.log"
    echo ""
    exit 1
fi
