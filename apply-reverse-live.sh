#!/bin/bash
set -e

PROJECT_ID="ashutosh-a2720"
ZONE="us-central1-a"
INSTANCE_NAME="erpnext-server"

echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

echo "📦 Copying reverse whitelabel script to VM..."
gcloud compute scp reverse_whitelabel.py $INSTANCE_NAME:~/reverse_whitelabel.py --zone=$ZONE

echo "🎨 Reverting changes on the live server..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="
    cd ~/frappe_docker
    CONTAINER_ID=\$(sudo docker-compose -f pwd.yml ps -q backend)
    if [ -n \"\$CONTAINER_ID\" ]; then
        echo \"Found backend container: \$CONTAINER_ID\"
        sudo docker cp ~/reverse_whitelabel.py \$CONTAINER_ID:/home/frappe/reverse_whitelabel.py
        sudo docker exec -u frappe \$CONTAINER_ID python3 /home/frappe/reverse_whitelabel.py
        echo \"✅ Reversion applied successfully!\"
    else
        echo \"❌ Could not find backend container. Is ERPNext running?\"
        exit 1
    fi
"
