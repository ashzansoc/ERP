#!/bin/bash

# Vendor & Freight Forwarder Portal Installation Script
# This script installs the complete portal system with all features

set -e

echo "🌍 Installing Vendor & Freight Forwarder Portal..."
echo "=================================================="

# Check if bench is available
if ! command -v bench &> /dev/null; then
    echo "❌ Error: bench command not found. Please ensure you're in a Frappe environment."
    exit 1
fi

# Get site name
SITE_NAME=${1:-$(bench --site)}

if [ -z "$SITE_NAME" ]; then
    echo "Usage: $0 <site-name>"
    echo "Or run from within a site directory"
    exit 1
fi

echo "📍 Installing on site: $SITE_NAME"
echo ""

# Run Python installation script
echo "📦 Creating DocTypes and custom fields..."
bench --site $SITE_NAME execute install_vendor_portal.install_vendor_portal

# Clear cache
echo "🧹 Clearing cache..."
bench --site $SITE_NAME clear-cache

# Migrate database
echo "🔄 Running database migrations..."
bench --site $SITE_NAME migrate

# Build assets
echo "🏗️  Building assets..."
bench build --app frappe

echo ""
echo "✅ Installation Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Configure portal branding:"
echo "   bench --site $SITE_NAME console"
echo "   >>> frappe.db.set_value('Website Settings', None, 'brand_html', '<img src=\"/files/logo.png\">')"
echo ""
echo "2. Create vendor/forwarder users:"
echo "   - Go to User List"
echo "   - Create new user with role 'Vendor' or 'Freight Forwarder'"
echo "   - Link user to Supplier record"
echo ""
echo "3. Access portals:"
echo "   - Vendor Portal: https://$SITE_NAME/vendor-portal"
echo "   - Freight Portal: https://$SITE_NAME/freight-portal"
echo ""
echo "4. Test workflows:"
echo "   - Document upload"
echo "   - Quote submission"
echo "   - Invoice approval"
echo "   - Milestone updates"
echo ""
echo "📚 Documentation: See VENDOR_PORTAL_GUIDE.md"
