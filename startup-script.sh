#!/bin/bash
set -e

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone frappe_docker
if [ -d "frappe_docker" ]; then
    echo "Repo already exists, pulling latest changes..."
    cd frappe_docker
    git pull
else
    git clone https://github.com/frappe/frappe_docker.git
    cd frappe_docker
fi

# Start ERPNext
sudo docker-compose -f pwd.yml up -d

echo "✅ ERPNext installation completed!"
echo "🌐 Access your ERPNext at: http://$(curl -s ifconfig.me):8080"
echo "👤 Username: Administrator"
echo "🔑 Password: admin"
