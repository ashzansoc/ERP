#!/bin/bash
# Run Landed Cost Automation Installation

cd frappe_docker

echo "🚢 Installing Landed Cost Automation System..."
echo ""

# Copy files to container
echo "📦 Copying installation files..."
docker cp ../install_landed_cost_automation.py frappe_docker-backend-1:/tmp/
docker cp ../api/landed_cost.py frappe_docker-backend-1:/tmp/

# Run installation using bench execute
echo ""
echo "🔧 Running installation script..."
docker-compose exec -T backend bash -c "cd /home/frappe/frappe-bench && bench --site localhost execute /tmp/install_landed_cost_automation.py"

# Copy API file to proper location
echo ""
echo "📁 Setting up API files..."
docker-compose exec -T backend bash -c "mkdir -p /home/frappe/frappe-bench/sites/localhost/api && cp /tmp/landed_cost.py /home/frappe/frappe-bench/sites/localhost/api/"

# Clear cache
echo ""
echo "🧹 Clearing cache..."
docker-compose exec -T backend bench --site localhost clear-cache

echo ""
echo "✅ Installation complete!"
echo ""
echo "📍 Access your ERP at: http://localhost:8080"
echo ""
