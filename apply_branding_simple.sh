#!/bin/bash
# Simple TradeFlow ERP Branding - No Config Errors
set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         TradeFlow ERP - Simple Branding Deployment            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

COMPOSE_FILE="frappe_docker/pwd.yml"
CONTAINER_NAME="frappe_docker-backend-1"

echo "→ Copying branding script..."
docker cp tradeflow_branding.py $CONTAINER_NAME:/home/frappe/
echo "✓ Script copied"
echo ""

echo "→ Applying TradeFlow ERP branding (text replacement only)..."
docker exec -u frappe $CONTAINER_NAME python3 /home/frappe/tradeflow_branding.py
echo ""

echo "→ Clearing cache (simple)..."
docker exec -u frappe $CONTAINER_NAME bench --site all clear-cache || true
echo ""

echo "→ Restarting services..."
docker compose -f $COMPOSE_FILE restart backend frontend
sleep 5
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  ✓ Branding Applied!                           ║"
echo "║                                                                ║"
echo "║  Text branding complete. Access at: http://localhost:8080      ║"
echo "║                                                                ║"
echo "║  Note: Login screen and full theme require additional steps   ║"
echo "║  The system now shows 'TradeFlow ERP' instead of 'ERPNext'     ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
