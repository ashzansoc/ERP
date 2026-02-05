# ERPNext Deployment on Google Compute Engine

## Step 1: Create a VM Instance

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
export ZONE="us-central1-a"
export INSTANCE_NAME="erpnext-server"

# Create VM instance
gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=e2-standard-4 \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=default \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=$INSTANCE_NAME,image=projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20240319,mode=rw,size=50,type=projects/$PROJECT_ID/zones/$ZONE/diskTypes/pd-standard \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=environment=production,app=erpnext \
    --reservation-affinity=any
```

## Step 2: Configure Firewall Rules

```bash
# Allow HTTP traffic
gcloud compute firewall-rules create allow-erpnext-http \
    --allow tcp:80,tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow ERPNext HTTP traffic"

# Allow HTTPS traffic
gcloud compute firewall-rules create allow-erpnext-https \
    --allow tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow ERPNext HTTPS traffic"
```

## Step 3: SSH into VM and Install Docker

```bash
# SSH into the instance
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for docker group to take effect
exit
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE
```

## Step 4: Deploy ERPNext

```bash
# Clone the repository
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker

# Copy your customized files if any
# cp your-custom-pwd.yml pwd.yml

# Start the services
docker-compose -f pwd.yml up -d

# Check status
docker-compose -f pwd.yml ps
```

## Step 5: Configure Domain and SSL (Optional)

```bash
# Install Nginx for reverse proxy
sudo apt install nginx -y

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/erpnext << EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/erpnext /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Estimated Costs (Monthly)
- e2-standard-4 VM: ~$120/month
- 50GB SSD: ~$8/month
- Network egress: ~$10-50/month
- **Total: ~$140-180/month**