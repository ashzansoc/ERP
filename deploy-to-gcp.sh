#!/bin/bash

# ERPNext GCP Deployment Script
# Usage: ./deploy-to-gcp.sh

set -e

# Configuration
PROJECT_ID="ashutosh-a2720"
ZONE="us-central1-a"
INSTANCE_NAME="erpnext-server"
MACHINE_TYPE="e2-standard-4"
DISK_SIZE="50GB"

echo "🚀 Starting ERPNext deployment on GCP..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK first."
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs with retry logic
echo "🔧 Enabling required APIs..."
enable_api_with_retry() {
    local api=$1
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt: Enabling $api..."
        if gcloud services enable $api --quiet; then
            echo "✅ Successfully enabled $api"
            return 0
        else
            echo "❌ Failed to enable $api (attempt $attempt/$max_attempts)"
            if [ $attempt -lt $max_attempts ]; then
                echo "⏳ Waiting 30 seconds before retry..."
                sleep 30
            fi
        fi
        ((attempt++))
    done
    
    echo "❌ Failed to enable $api after $max_attempts attempts"
    return 1
}

# Enable APIs
enable_api_with_retry "compute.googleapis.com"
enable_api_with_retry "cloudresourcemanager.googleapis.com"

# Wait for APIs to be fully enabled
echo "⏳ Waiting for APIs to be fully enabled..."
sleep 60

# Create firewall rules
echo "🔥 Creating firewall rules..."
gcloud compute firewall-rules create allow-erpnext-http \
    --allow tcp:80,tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow ERPNext HTTP traffic" \
    --quiet || echo "Firewall rule already exists"

gcloud compute firewall-rules create allow-erpnext-https \
    --allow tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow ERPNext HTTPS traffic" \
    --quiet || echo "Firewall rule already exists"

# Create VM instance
echo "💻 Checking VM instance..."
if gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE &> /dev/null; then
    echo "✅ Instance $INSTANCE_NAME already exists, skipping creation..."
else
    echo "💻 Creating VM instance..."
    gcloud compute instances create $INSTANCE_NAME \
        --zone=$ZONE \
        --machine-type=$MACHINE_TYPE \
        --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
        --maintenance-policy=MIGRATE \
        --provisioning-model=STANDARD \
        --tags=http-server,https-server \
        --create-disk=auto-delete=yes,boot=yes,device-name=$INSTANCE_NAME,image=projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20240319,mode=rw,size=50,type=projects/$PROJECT_ID/zones/$ZONE/diskTypes/pd-standard \
        --labels=environment=production,app=erpnext
fi

# Wait for instance to be ready
echo "⏳ Waiting for instance to be ready..."
sleep 30

# Get external IP
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

# Create startup script
cat > startup-script.sh << 'EOF'
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
EOF

# Copy and execute startup script
echo "📦 Installing ERPNext on the VM..."
gcloud compute scp startup-script.sh $INSTANCE_NAME:~/startup-script.sh --zone=$ZONE
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="chmod +x ~/startup-script.sh && ~/startup-script.sh"

echo ""
echo "🎉 Deployment completed successfully!"
echo "🌐 Access your ERPNext at: http://$EXTERNAL_IP:8080"
echo "👤 Username: Administrator"
echo "🔑 Password: admin"
echo ""
echo "📝 Next steps:"
echo "1. Configure your domain name to point to $EXTERNAL_IP"
echo "2. Set up SSL certificate using Let's Encrypt"
echo "3. Configure backup strategy"
echo "4. Set up monitoring and alerts"
echo ""
echo "💰 Estimated monthly cost: ~$140-180"