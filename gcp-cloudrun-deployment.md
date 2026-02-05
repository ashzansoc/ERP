# ERPNext Deployment on Google Cloud Run

## Prerequisites
- Google Cloud Project with billing enabled
- Cloud SQL for database
- Cloud Memorystore for Redis
- Container Registry or Artifact Registry

## Step 1: Set up Cloud SQL (MariaDB)

```bash
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export DB_INSTANCE="erpnext-db"

# Create Cloud SQL instance
gcloud sql instances create $DB_INSTANCE \
    --database-version=MYSQL_8_0 \
    --tier=db-n1-standard-2 \
    --region=$REGION \
    --storage-size=100GB \
    --storage-type=SSD \
    --storage-auto-increase

# Set root password
gcloud sql users set-password root \
    --host=% \
    --instance=$DB_INSTANCE \
    --password=your-secure-password

# Create database
gcloud sql databases create erpnext --instance=$DB_INSTANCE
```

## Step 2: Set up Cloud Memorystore (Redis)

```bash
# Create Redis instance
gcloud redis instances create erpnext-redis \
    --size=1 \
    --region=$REGION \
    --redis-version=redis_6_x
```

## Step 3: Build and Push Custom Docker Image

```bash
# Create Dockerfile for Cloud Run
cat > Dockerfile.cloudrun << EOF
FROM frappe/erpnext:v15.95.0

# Install Cloud SQL Proxy
RUN apt-get update && apt-get install -y wget
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
RUN chmod +x cloud_sql_proxy && mv cloud_sql_proxy /usr/local/bin/

# Copy startup script
COPY start-cloudrun.sh /start-cloudrun.sh
RUN chmod +x /start-cloudrun.sh

EXPOSE 8080
CMD ["/start-cloudrun.sh"]
EOF

# Create startup script
cat > start-cloudrun.sh << 'EOF'
#!/bin/bash

# Start Cloud SQL Proxy
/usr/local/bin/cloud_sql_proxy -instances=$CLOUD_SQL_CONNECTION_NAME=tcp:3306 &

# Wait for database connection
sleep 10

# Configure Frappe
bench set-config -g db_host 127.0.0.1
bench set-config -g db_port 3306
bench set-config -g redis_cache $REDIS_URL
bench set-config -g redis_queue $REDIS_URL

# Start Frappe
exec /home/frappe/frappe-bench/env/bin/gunicorn -b 0.0.0.0:8080 frappe.app:application
EOF

# Build and push image
docker build -f Dockerfile.cloudrun -t gcr.io/$PROJECT_ID/erpnext-cloudrun .
docker push gcr.io/$PROJECT_ID/erpnext-cloudrun
```

## Step 4: Deploy to Cloud Run

```bash
# Get connection details
DB_CONNECTION=$(gcloud sql instances describe $DB_INSTANCE --format="value(connectionName)")
REDIS_IP=$(gcloud redis instances describe erpnext-redis --region=$REGION --format="value(host)")

# Deploy to Cloud Run
gcloud run deploy erpnext \
    --image gcr.io/$PROJECT_ID/erpnext-cloudrun \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --concurrency 80 \
    --set-env-vars="CLOUD_SQL_CONNECTION_NAME=$DB_CONNECTION,REDIS_URL=redis://$REDIS_IP:6379" \
    --add-cloudsql-instances $DB_CONNECTION
```

## Limitations of Cloud Run Approach
- **Stateless only**: Background workers and schedulers need separate deployment
- **Cold starts**: May have latency issues
- **File storage**: Requires Cloud Storage integration
- **WebSocket**: Limited support

## Estimated Costs (Monthly)
- Cloud SQL (db-n1-standard-2): ~$150/month
- Cloud Memorystore (1GB): ~$40/month
- Cloud Run: ~$20-100/month (depending on usage)
- **Total: ~$210-290/month**