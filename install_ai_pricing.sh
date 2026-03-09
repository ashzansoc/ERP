#!/bin/bash

# Smart Pricing Engine (AI Layer) Installation Script
# This script installs AI-powered pricing features for the ERP system

set -e

echo "🤖 Smart Pricing Engine (AI Layer) Installation"
echo "=============================================="
echo ""

# Check if bench command exists
if ! command -v bench &> /dev/null; then
    echo "❌ Error: bench command not found"
    echo "Please run this script from your Frappe bench directory"
    exit 1
fi

# Get site name
if [ -z "$1" ]; then
    echo "Usage: ./install_ai_pricing.sh <site-name>"
    echo "Example: ./install_ai_pricing.sh mysite.local"
    exit 1
fi

SITE=$1

echo "📦 Installing on site: $SITE"
echo ""

# Run the Python installation script
echo "🔧 Creating DocTypes and configurations..."
bench --site $SITE execute install_ai_pricing_engine.install_ai_pricing_engine

echo ""
echo "✅ Installation Complete!"
echo ""
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. Configure LLM Settings:"
echo "   - Each user should go to User Settings"
echo "   - Select their preferred LLM provider (OpenAI, Anthropic, Google, Azure)"
echo "   - Enter their API key"
echo "   - Choose the model to use"
echo ""
echo "2. AI Features Available:"
echo "   ✨ Margin Suggestions - AI-powered margin recommendations based on landed cost"
echo "   📊 Historical Comparison - Compare pricing against historical data"
echo "   🌍 Country Analytics - Country-wise pricing analysis"
echo "   📦 Volume Discounts - AI-recommended volume discount tiers"
echo "   💱 FX Risk Alerts - Currency risk monitoring and hedging recommendations"
echo ""
echo "3. Access AI Features:"
echo "   - Ocean Shipment: Click 'Get AI Pricing Suggestions' button"
echo "   - Sales Invoice: AI price checks appear automatically"
echo "   - Dashboard: View AI Pricing Dashboard for insights"
echo ""
echo "4. API Endpoints Available:"
echo "   - /api/method/api.ai_pricing.get_margin_suggestion"
echo "   - /api/method/api.ai_pricing.compare_historical_pricing"
echo "   - /api/method/api.ai_pricing.analyze_country_pricing"
echo "   - /api/method/api.ai_pricing.get_volume_discount_recommendations"
echo "   - /api/method/api.ai_pricing.analyze_fx_risk"
echo ""
echo "📚 For detailed documentation, see: AI_PRICING_ENGINE_GUIDE.md"
echo ""
