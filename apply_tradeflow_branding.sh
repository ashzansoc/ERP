#!/bin/bash
# TradeFlow ERP - Complete Branding Application Script
# Applies white-label branding to live or local ERPNext installation

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

BRAND_NAME="TradeFlow ERP"
PROJECT_ID="${GCP_PROJECT_ID:-ashutosh-a2720}"
ZONE="${GCP_ZONE:-us-central1-a}"
INSTANCE_NAME="${GCP_INSTANCE:-erpnext-server}"
DEPLOYMENT_TYPE="${1:-local}"  # local, docker, or gcp

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# ============================================================================
# DEPLOYMENT FUNCTIONS
# ============================================================================

apply_local_branding() {
    print_header "Applying $BRAND_NAME Branding (Local)"
    
    # Check if bench is available
    if ! command -v bench &> /dev/null; then
        print_error "Bench command not found. Please install Frappe Bench first."
        exit 1
    fi
    
    # Get bench path
    BENCH_PATH=$(bench --site $(ls -1 sites | grep -v common | grep -v assets | head -1) get-app-path frappe 2>/dev/null || echo "/home/frappe/frappe-bench")
    
    print_info "Bench path: $BENCH_PATH"
    
    # Apply branding
    print_info "Running branding script..."
    python3 tradeflow_branding.py
    
    # Apply configuration
    print_info "Applying app configuration..."
    bench --site all execute tradeflow_app_config.apply_all_configurations
    
    # Build assets
    print_info "Building assets..."
    bench build
    
    # Clear cache
    print_info "Clearing cache..."
    bench clear-cache
    bench clear-website-cache
    
    # Restart
    print_info "Restarting services..."
    bench restart
    
    print_success "Local branding applied successfully!"
}

apply_docker_branding() {
    print_header "Applying $BRAND_NAME Branding (Docker)"
    
    # Find docker-compose file
    if [ -f "frappe_docker/pwd.yml" ]; then
        COMPOSE_FILE="frappe_docker/pwd.yml"
    elif [ -f "frappe_docker/compose.yaml" ]; then
        COMPOSE_FILE="frappe_docker/compose.yaml"
    elif [ -f "docker-compose.yml" ]; then
        COMPOSE_FILE="docker-compose.yml"
    else
        print_error "Docker compose file not found"
        exit 1
    fi
    
    print_info "Using compose file: $COMPOSE_FILE"
    
    # Get backend container
    CONTAINER_ID=$(docker-compose -f $COMPOSE_FILE ps -q backend 2>/dev/null || docker compose -f $COMPOSE_FILE ps -q backend)
    
    if [ -z "$CONTAINER_ID" ]; then
        print_error "Backend container not found. Is ERPNext running?"
        exit 1
    fi
    
    print_success "Found backend container: $CONTAINER_ID"
    
    # Copy branding scripts to container
    print_info "Copying branding scripts..."
    docker cp tradeflow_branding.py $CONTAINER_ID:/home/frappe/
    docker cp tradeflow_app_config.py $CONTAINER_ID:/home/frappe/
    
    # Apply branding
    print_info "Applying branding..."
    docker exec -u frappe $CONTAINER_ID python3 /home/frappe/tradeflow_branding.py
    
    # Apply configuration
    print_info "Applying configuration..."
    docker exec -u frappe $CONTAINER_ID bench --site all execute tradeflow_app_config.apply_all_configurations
    
    # Build and restart
    print_info "Building assets..."
    docker exec -u frappe $CONTAINER_ID bench build
    
    print_info "Clearing cache..."
    docker exec -u frappe $CONTAINER_ID bench clear-cache
    
    print_info "Restarting services..."
    docker-compose -f $COMPOSE_FILE restart backend || docker compose -f $COMPOSE_FILE restart backend
    
    print_success "Docker branding applied successfully!"
}

apply_gcp_branding() {
    print_header "Applying $BRAND_NAME Branding (GCP)"
    
    # Check gcloud
    if ! command -v gcloud &> /dev/null; then
        print_error "gcloud command not found. Please install Google Cloud SDK."
        exit 1
    fi
    
    # Set project
    print_info "Setting GCP project: $PROJECT_ID"
    gcloud config set project $PROJECT_ID
    
    # Copy scripts to VM
    print_info "Copying branding scripts to VM..."
    gcloud compute scp tradeflow_branding.py $INSTANCE_NAME:~/ --zone=$ZONE
    gcloud compute scp tradeflow_app_config.py $INSTANCE_NAME:~/ --zone=$ZONE
    
    # Apply branding on VM
    print_info "Applying branding on GCP VM..."
    gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="
        set -e
        cd ~/frappe_docker
        
        # Find container
        CONTAINER_ID=\$(sudo docker-compose -f pwd.yml ps -q backend 2>/dev/null || sudo docker compose -f pwd.yml ps -q backend)
        
        if [ -z \"\$CONTAINER_ID\" ]; then
            echo 'Error: Backend container not found'
            exit 1
        fi
        
        echo 'Found container: '\$CONTAINER_ID
        
        # Copy scripts
        sudo docker cp ~/tradeflow_branding.py \$CONTAINER_ID:/home/frappe/
        sudo docker cp ~/tradeflow_app_config.py \$CONTAINER_ID:/home/frappe/
        
        # Apply branding
        echo 'Applying branding...'
        sudo docker exec -u frappe \$CONTAINER_ID python3 /home/frappe/tradeflow_branding.py
        
        # Apply configuration
        echo 'Applying configuration...'
        sudo docker exec -u frappe \$CONTAINER_ID bench --site all execute tradeflow_app_config.apply_all_configurations
        
        # Build and restart
        echo 'Building assets...'
        sudo docker exec -u frappe \$CONTAINER_ID bench build
        
        echo 'Clearing cache...'
        sudo docker exec -u frappe \$CONTAINER_ID bench clear-cache
        
        echo 'Restarting services...'
        sudo docker-compose -f pwd.yml restart backend || sudo docker compose -f pwd.yml restart backend
        
        echo 'Branding applied successfully!'
    "
    
    print_success "GCP branding applied successfully!"
}

# ============================================================================
# VERIFICATION
# ============================================================================

verify_branding() {
    print_header "Verifying Branding"
    
    print_info "Checking for TradeFlow branding..."
    
    case $DEPLOYMENT_TYPE in
        local)
            if bench --site all execute "frappe.db.get_single_value('System Settings', 'app_name')" | grep -q "TradeFlow"; then
                print_success "Branding verified in database"
            else
                print_error "Branding not found in database"
            fi
            ;;
        docker)
            if docker exec -u frappe $CONTAINER_ID bench --site all execute "frappe.db.get_single_value('System Settings', 'app_name')" | grep -q "TradeFlow"; then
                print_success "Branding verified in database"
            else
                print_error "Branding not found in database"
            fi
            ;;
        gcp)
            print_info "Please verify branding by accessing your site"
            ;;
    esac
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    print_header "$BRAND_NAME - White-Label Branding System"
    
    # Check if branding scripts exist
    if [ ! -f "tradeflow_branding.py" ]; then
        print_error "tradeflow_branding.py not found in current directory"
        exit 1
    fi
    
    if [ ! -f "tradeflow_app_config.py" ]; then
        print_error "tradeflow_app_config.py not found in current directory"
        exit 1
    fi
    
    # Apply branding based on deployment type
    case $DEPLOYMENT_TYPE in
        local)
            apply_local_branding
            ;;
        docker)
            apply_docker_branding
            ;;
        gcp)
            apply_gcp_branding
            ;;
        *)
            print_error "Invalid deployment type: $DEPLOYMENT_TYPE"
            echo "Usage: $0 [local|docker|gcp]"
            exit 1
            ;;
    esac
    
    # Verify
    verify_branding
    
    # Final message
    print_header "Branding Complete!"
    echo -e "${GREEN}Your system is now branded as: $BRAND_NAME${NC}"
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Access your site and verify the branding"
    echo "  2. Upload custom logo to /assets/tradeflow/images/"
    echo "  3. Customize colors in tradeflow_branding.py if needed"
    echo "  4. Test all modules and workspaces"
    echo ""
}

# Run main function
main
