#!/bin/bash
# Universal White-Label Deployment Script
# Choose between TradeFlow ERP or GlobalEdge ERP

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ============================================================================
# BANNER
# ============================================================================

show_banner() {
    clear
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                                                                ║"
    echo "║           ERPNext White-Label Branding System                  ║"
    echo "║                                                                ║"
    echo "║           Complete Branding Transformation                     ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
}

# ============================================================================
# BRAND SELECTION
# ============================================================================

select_brand() {
    echo -e "${CYAN}Select Your Brand:${NC}\n"
    
    echo -e "${GREEN}1) TradeFlow ERP${NC}"
    echo "   - Global Trade Management Platform"
    echo "   - Modern blue/green design"
    echo "   - Trade-focused terminology"
    echo "   - Best for: Import/Export, Logistics, Freight"
    echo ""
    
    echo -e "${GREEN}2) GlobalEdge ERP${NC}"
    echo "   - Enterprise Trade Solutions"
    echo "   - Corporate deep blue design"
    echo "   - Enterprise terminology"
    echo "   - Best for: Large Enterprises, Corporations"
    echo ""
    
    echo -e "${GREEN}3) Custom Brand${NC}"
    echo "   - Create your own brand configuration"
    echo "   - Customize all settings"
    echo ""
    
    read -p "Enter your choice (1-3): " brand_choice
    
    case $brand_choice in
        1)
            BRAND_NAME="TradeFlow ERP"
            BRAND_SCRIPT="tradeflow_branding.py"
            CONFIG_SCRIPT="tradeflow_app_config.py"
            ;;
        2)
            BRAND_NAME="GlobalEdge ERP"
            BRAND_SCRIPT="globaledge_branding.py"
            CONFIG_SCRIPT="tradeflow_app_config.py"
            ;;
        3)
            echo -e "\n${YELLOW}Custom brand setup:${NC}"
            read -p "Enter brand name (e.g., 'MyBrand ERP'): " custom_name
            read -p "Enter company name (e.g., 'MyCompany Technologies'): " custom_company
            read -p "Enter tagline: " custom_tagline
            
            BRAND_NAME="$custom_name"
            BRAND_SCRIPT="custom_branding.py"
            CONFIG_SCRIPT="tradeflow_app_config.py"
            
            # Create custom branding script
            create_custom_brand "$custom_name" "$custom_company" "$custom_tagline"
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac
    
    echo -e "\n${GREEN}✓ Selected: $BRAND_NAME${NC}\n"
}

# ============================================================================
# DEPLOYMENT TYPE SELECTION
# ============================================================================

select_deployment() {
    echo -e "${CYAN}Select Deployment Type:${NC}\n"
    
    echo "1) Local (Bench installation)"
    echo "2) Docker (Docker Compose)"
    echo "3) GCP (Google Cloud Platform)"
    echo ""
    
    read -p "Enter your choice (1-3): " deploy_choice
    
    case $deploy_choice in
        1)
            DEPLOYMENT_TYPE="local"
            ;;
        2)
            DEPLOYMENT_TYPE="docker"
            ;;
        3)
            DEPLOYMENT_TYPE="gcp"
            read -p "Enter GCP Project ID: " GCP_PROJECT_ID
            read -p "Enter GCP Zone [us-central1-a]: " GCP_ZONE
            GCP_ZONE=${GCP_ZONE:-us-central1-a}
            read -p "Enter Instance Name [erpnext-server]: " GCP_INSTANCE
            GCP_INSTANCE=${GCP_INSTANCE:-erpnext-server}
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac
    
    echo -e "\n${GREEN}✓ Deployment type: $DEPLOYMENT_TYPE${NC}\n"
}

# ============================================================================
# CUSTOM BRAND CREATION
# ============================================================================

create_custom_brand() {
    local name="$1"
    local company="$2"
    local tagline="$3"
    
    echo -e "${YELLOW}Creating custom brand configuration...${NC}"
    
    # Copy TradeFlow script as template
    cp tradeflow_branding.py custom_branding.py
    
    # Replace brand config
    sed -i.bak "s/TradeFlow ERP/$name/g" custom_branding.py
    sed -i.bak "s/TradeFlow Technologies/$company/g" custom_branding.py
    sed -i.bak "s/Global Trade Management Platform/$tagline/g" custom_branding.py
    
    rm -f custom_branding.py.bak
    
    echo -e "${GREEN}✓ Custom brand configuration created${NC}"
}

# ============================================================================
# DEPLOYMENT FUNCTIONS
# ============================================================================

deploy_local() {
    echo -e "${BLUE}Deploying $BRAND_NAME (Local)...${NC}\n"
    
    if ! command -v bench &> /dev/null; then
        echo -e "${RED}✗ Bench not found${NC}"
        exit 1
    fi
    
    echo "→ Running branding script..."
    python3 "$BRAND_SCRIPT"
    
    echo "→ Applying configuration..."
    bench --site all execute tradeflow_app_config.apply_all_configurations
    
    echo "→ Building assets..."
    bench build
    
    echo "→ Clearing cache..."
    bench clear-cache
    bench clear-website-cache
    
    echo "→ Restarting services..."
    bench restart
    
    echo -e "\n${GREEN}✓ Local deployment complete!${NC}"
}

deploy_docker() {
    echo -e "${BLUE}Deploying $BRAND_NAME (Docker)...${NC}\n"
    
    # Find compose file
    if [ -f "frappe_docker/pwd.yml" ]; then
        COMPOSE_FILE="frappe_docker/pwd.yml"
    elif [ -f "frappe_docker/compose.yaml" ]; then
        COMPOSE_FILE="frappe_docker/compose.yaml"
    else
        echo -e "${RED}✗ Docker compose file not found${NC}"
        exit 1
    fi
    
    echo "→ Using: $COMPOSE_FILE"
    
    # Get container
    CONTAINER_ID=$(docker-compose -f $COMPOSE_FILE ps -q backend 2>/dev/null || docker compose -f $COMPOSE_FILE ps -q backend)
    
    if [ -z "$CONTAINER_ID" ]; then
        echo -e "${RED}✗ Backend container not found${NC}"
        exit 1
    fi
    
    echo "→ Container: $CONTAINER_ID"
    
    echo "→ Copying scripts..."
    docker cp "$BRAND_SCRIPT" $CONTAINER_ID:/home/frappe/
    docker cp "$CONFIG_SCRIPT" $CONTAINER_ID:/home/frappe/
    
    echo "→ Applying branding..."
    docker exec -u frappe $CONTAINER_ID python3 /home/frappe/"$BRAND_SCRIPT"
    
    echo "→ Applying configuration..."
    docker exec -u frappe $CONTAINER_ID bench --site all execute tradeflow_app_config.apply_all_configurations
    
    echo "→ Building assets..."
    docker exec -u frappe $CONTAINER_ID bench build
    
    echo "→ Clearing cache..."
    docker exec -u frappe $CONTAINER_ID bench clear-cache
    
    echo "→ Restarting..."
    docker-compose -f $COMPOSE_FILE restart backend || docker compose -f $COMPOSE_FILE restart backend
    
    echo -e "\n${GREEN}✓ Docker deployment complete!${NC}"
}

deploy_gcp() {
    echo -e "${BLUE}Deploying $BRAND_NAME (GCP)...${NC}\n"
    
    if ! command -v gcloud &> /dev/null; then
        echo -e "${RED}✗ gcloud not found${NC}"
        exit 1
    fi
    
    echo "→ Setting project: $GCP_PROJECT_ID"
    gcloud config set project $GCP_PROJECT_ID
    
    echo "→ Copying scripts to VM..."
    gcloud compute scp "$BRAND_SCRIPT" $GCP_INSTANCE:~/ --zone=$GCP_ZONE
    gcloud compute scp "$CONFIG_SCRIPT" $GCP_INSTANCE:~/ --zone=$GCP_ZONE
    
    echo "→ Applying branding on VM..."
    gcloud compute ssh $GCP_INSTANCE --zone=$GCP_ZONE --command="
        set -e
        cd ~/frappe_docker
        
        CONTAINER_ID=\$(sudo docker-compose -f pwd.yml ps -q backend 2>/dev/null || sudo docker compose -f pwd.yml ps -q backend)
        
        if [ -z \"\$CONTAINER_ID\" ]; then
            echo 'Error: Container not found'
            exit 1
        fi
        
        echo 'Container: '\$CONTAINER_ID
        
        sudo docker cp ~/$BRAND_SCRIPT \$CONTAINER_ID:/home/frappe/
        sudo docker cp ~/$CONFIG_SCRIPT \$CONTAINER_ID:/home/frappe/
        
        echo 'Applying branding...'
        sudo docker exec -u frappe \$CONTAINER_ID python3 /home/frappe/$BRAND_SCRIPT
        
        echo 'Applying configuration...'
        sudo docker exec -u frappe \$CONTAINER_ID bench --site all execute tradeflow_app_config.apply_all_configurations
        
        echo 'Building...'
        sudo docker exec -u frappe \$CONTAINER_ID bench build
        
        echo 'Clearing cache...'
        sudo docker exec -u frappe \$CONTAINER_ID bench clear-cache
        
        echo 'Restarting...'
        sudo docker-compose -f pwd.yml restart backend || sudo docker compose -f pwd.yml restart backend
        
        echo 'Complete!'
    "
    
    echo -e "\n${GREEN}✓ GCP deployment complete!${NC}"
}

# ============================================================================
# VERIFICATION
# ============================================================================

verify_deployment() {
    echo -e "\n${CYAN}Verification Checklist:${NC}\n"
    
    echo "□ Login screen shows $BRAND_NAME"
    echo "□ No 'ERPNext' text visible"
    echo "□ No 'Frappe' text visible"
    echo "□ Custom colors applied"
    echo "□ Module names updated"
    echo "□ Navigation customized"
    echo "□ Footer shows custom copyright"
    echo ""
    
    read -p "Press Enter to continue..."
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    show_banner
    
    # Check required files
    if [ ! -f "tradeflow_branding.py" ] || [ ! -f "globaledge_branding.py" ]; then
        echo -e "${RED}✗ Branding scripts not found${NC}"
        exit 1
    fi
    
    # Select brand
    select_brand
    
    # Select deployment
    select_deployment
    
    # Confirm
    echo -e "${YELLOW}Ready to deploy:${NC}"
    echo "  Brand: $BRAND_NAME"
    echo "  Deployment: $DEPLOYMENT_TYPE"
    echo ""
    read -p "Continue? (y/n): " confirm
    
    if [ "$confirm" != "y" ]; then
        echo "Cancelled"
        exit 0
    fi
    
    # Deploy
    case $DEPLOYMENT_TYPE in
        local)
            deploy_local
            ;;
        docker)
            deploy_docker
            ;;
        gcp)
            deploy_gcp
            ;;
    esac
    
    # Verify
    verify_deployment
    
    # Success
    echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║                  Deployment Successful!                        ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  Your system is now branded as: $BRAND_NAME${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}\n"
    
    echo -e "${CYAN}Next Steps:${NC}"
    echo "1. Access your site and verify branding"
    echo "2. Upload custom logo files"
    echo "3. Test all modules and features"
    echo "4. Train users on new terminology"
    echo ""
}

# Run
main
