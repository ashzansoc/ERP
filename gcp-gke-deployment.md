# ERPNext Deployment on Google Kubernetes Engine (GKE)

## Step 1: Create GKE Cluster

```bash
export PROJECT_ID="your-project-id"
export CLUSTER_NAME="erpnext-cluster"
export ZONE="us-central1-a"

# Create GKE cluster
gcloud container clusters create $CLUSTER_NAME \
    --zone $ZONE \
    --num-nodes 3 \
    --machine-type e2-standard-4 \
    --disk-size 50GB \
    --enable-autoscaling \
    --min-nodes 1 \
    --max-nodes 10 \
    --enable-autorepair \
    --enable-autoupgrade

# Get credentials
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE
```

## Step 2: Install Helm

```bash
# Install Helm
curl https://get.helm.sh/helm-v3.12.0-linux-amd64.tar.gz | tar xz
sudo mv linux-amd64/helm /usr/local/bin/helm
```

## Step 3: Deploy using Frappe Helm Chart

```bash
# Add Frappe Helm repository
helm repo add frappe https://helm.erpnext.com
helm repo update

# Create values file
cat > values.yaml << EOF
# Database configuration
mariadb:
  enabled: true
  auth:
    rootPassword: "your-secure-password"
    database: "erpnext"
  primary:
    persistence:
      size: 100Gi

# Redis configuration
redis:
  enabled: true
  auth:
    enabled: false

# ERPNext configuration
erpnext:
  image:
    repository: frappe/erpnext
    tag: v15.95.0
  
  # Site configuration
  sites:
    - name: "your-domain.com"
      adminPassword: "admin"
      installApps:
        - "erpnext"

# Ingress configuration
ingress:
  enabled: true
  className: "gce"
  annotations:
    kubernetes.io/ingress.global-static-ip-name: "erpnext-ip"
    networking.gke.io/managed-certificates: "erpnext-ssl-cert"
  hosts:
    - host: your-domain.com
      paths:
        - path: /
          pathType: Prefix

# SSL Certificate
managedCertificate:
  enabled: true
  domains:
    - your-domain.com
EOF

# Install ERPNext
helm install erpnext frappe/erpnext -f values.yaml
```

## Step 4: Configure Load Balancer and SSL

```bash
# Reserve static IP
gcloud compute addresses create erpnext-ip --global

# Create managed SSL certificate
cat > ssl-cert.yaml << EOF
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: erpnext-ssl-cert
spec:
  domains:
    - your-domain.com
EOF

kubectl apply -f ssl-cert.yaml
```

## Step 5: Monitor and Scale

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Scale deployment
kubectl scale deployment erpnext --replicas=3

# Check logs
kubectl logs -f deployment/erpnext
```

## Estimated Costs (Monthly)
- GKE cluster (3 e2-standard-4 nodes): ~$360/month
- Load Balancer: ~$20/month
- Persistent disks: ~$20/month
- **Total: ~$400/month**