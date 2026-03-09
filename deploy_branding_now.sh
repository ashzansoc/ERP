#!/bin/bash
# Quick Deploy TradeFlow ERP Branding to Docker
set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║           TradeFlow ERP - White-Label Deployment               ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
COMPOSE_FILE="frappe_docker/pwd.yml"
CONTAINER_NAME="frappe_docker-backend-1"

echo "→ Checking Docker container..."
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "✗ Container not running. Starting containers..."
    docker compose -f $COMPOSE_FILE up -d
    sleep 10
fi

echo "✓ Container is running"
echo ""

echo "→ Copying branding scripts to container..."
docker cp tradeflow_branding.py $CONTAINER_NAME:/home/frappe/
docker cp tradeflow_app_config.py $CONTAINER_NAME:/home/frappe/
echo "✓ Scripts copied"
echo ""

echo "→ Applying TradeFlow ERP branding..."
docker exec -u frappe $CONTAINER_NAME python3 /home/frappe/tradeflow_branding.py
echo ""

echo "→ Applying configuration and module renaming..."
docker exec -u frappe $CONTAINER_NAME bench --site all execute tradeflow_app_config.apply_all_configurations
echo ""

echo "→ Building assets..."
docker exec -u frappe $CONTAINER_NAME bench build
echo ""

echo "→ Clearing cache..."
docker exec -u frappe $CONTAINER_NAME bench clear-cache
docker exec -u frappe $CONTAINER_NAME bench clear-website-cache
echo ""

echo "→ Restarting services..."
docker compose -f $COMPOSE_FILE restart backend frontend
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║                  ✓ Deployment Complete!                        ║"
echo "║                                                                ║"
echo "║  Your ERP is now branded as: TradeFlow ERP                     ║"
echo "║                                                                ║"
echo "║  Access your site at: http://localhost:8080                    ║"
echo "║                                                                ║"
echo "║  Login and verify:                                             ║"
echo "║  • Custom login screen                                         ║"
echo "║  • No 'ERPNext' branding                                       ║"
echo "║  • Renamed modules (Procurement, etc.)                         ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
