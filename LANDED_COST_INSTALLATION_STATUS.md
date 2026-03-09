# 🚢 Landed Cost Automation - Installation Status

## ✅ Successfully Installed Components

### 1. Cost Component (Child DocType) ✅
- **Status**: Installed
- **Type**: Child Table
- **Fields**: 15 fields including cost_type, amount, currency, exchange_rate
- **Usage**: Store cost components (Freight, Insurance, CHA Fees, etc.)

### 2. Shipment Item (Child DocType) ✅
- **Status**: Installed
- **Type**: Child Table
- **Fields**: 27 fields including item details, weights, volumes, costs, HS codes
- **Usage**: Store shipment items with landed cost calculations

### 3. HS Code Duty Rate (Child DocType) ✅
- **Status**: Installed
- **Type**: Child Table
- **Fields**: 9 fields for country-specific duty rates
- **Usage**: Store duty rates for HS codes

### 4. HS Code (Master DocType) ✅
- **Status**: Installed
- **Type**: Master
- **Fields**: hs_code, description, duty_rates table
- **Usage**: Master database of HS codes with duty rates

### 5. Landed Cost Calculation Log (DocType) ✅
- **Status**: Installed
- **Type**: Document
- **Fields**: shipment, calculation_date, triggered_by, details
- **Usage**: Audit trail for all calculations

### 6. Sample HS Codes ✅
- **Status**: Created
- **Count**: 5 sample HS codes
- **Codes**:
  - 8517.62 - Telecom equipment (10% duty)
  - 8471.30 - Laptops (10% duty)
  - 8528.72 - TVs (10% duty)
  - 6203.42 - Men's cotton trousers (10% duty)
  - 6204.62 - Women's cotton trousers (10% duty)

## 📋 Manual Steps Required

### Step 1: Add Fields to Ocean Shipment (via Customize Form)

Since Ocean Shipment is a custom DocType, we need to add the landed cost fields manually through the UI:

1. **Login to ERPNext**: http://localhost:8080
2. **Go to**: Desk → Customize → Customize Form
3. **Select DocType**: Ocean Shipment
4. **Add the following fields** (after the "Containers" section):

#### Shipment Items Section
```
Section Break: "Shipment Items"
Table: "items" → Options: "Shipment Item"
```

#### Cost Components Section
```
Section Break: "Cost Components"
Table: "cost_components" → Options: "Cost Component"
```

#### Landed Cost Settings Section
```
Section Break: "Landed Cost Settings"
Check: "auto_calculate_landed_cost" → Label: "Auto Calculate" → Default: 1
Link: "base_currency" → Options: "Currency" → Default: "USD"
Column Break
Select: "freight_allocation_method" → Options: "Weight\nVolume\nValue" → Default: "Weight"
Select: "cha_allocation_method" → Options: "Customs Value\nEqual" → Default: "Customs Value"
Select: "port_allocation_method" → Options: "Weight\nVolume" → Default: "Weight"
```

#### Landed Cost Summary Section
```
Section Break: "Landed Cost Summary"
Currency: "total_freight" → Read Only: 1
Currency: "total_insurance" → Read Only: 1
Currency: "total_customs_duty" → Read Only: 1
Column Break
Currency: "total_cha_fees" → Read Only: 1
Currency: "total_port_charges" → Read Only: 1
Currency: "total_landed_cost" → Read Only: 1 → Bold: 1
```

#### Integration Section
```
Section Break: "Integration" → Collapsible: 1
Link: "landed_cost_voucher" → Options: "Landed Cost Voucher" → Read Only: 1
```

5. **Click "Update"** to save changes

### Step 2: Install Calculation Engine (API)

The calculation engine (`api/landed_cost.py`) needs to be integrated into your ERPNext app. You have two options:

#### Option A: Create Custom App (Recommended for Production)
```bash
# In frappe_docker directory
docker-compose exec backend bench new-app landed_cost_automation
docker-compose exec backend bench --site localhost install-app landed_cost_automation

# Copy api/landed_cost.py to the app
# Add hooks for auto-calculation
```

#### Option B: Use Server Scripts (Quick Setup)
1. Go to: Desk → Automation → Server Script
2. Create new Server Script
3. **Script Type**: DocType Event
4. **DocType**: Ocean Shipment
5. **Event**: Before Save
6. **Script**: Copy the calculation logic from `api/landed_cost.py`

### Step 3: Test the System

1. **Create a Test Shipment**:
   - Go to: Stock → Ocean Shipment → New
   - Fill in basic shipment details
   
2. **Add Items**:
   - Click "Add Row" in Shipment Items
   - Select an item
   - Enter quantity, weight, volume, base cost
   - Select HS Code (e.g., 8471.30)
   - Enter customs value
   
3. **Add Cost Components**:
   - Click "Add Row" in Cost Components
   - Select cost type (Freight, Insurance, etc.)
   - Enter amount and currency
   
4. **Calculate Landed Cost**:
   - Currently manual calculation
   - After API integration, will auto-calculate on save

## 📊 What's Working Now

### ✅ Available in ERP
1. **HS Code Management**
   - Access: Desk → Stock → HS Code
   - Can create/edit HS codes
   - Can add duty rates by country
   
2. **Calculation Log**
   - Access: Desk → Stock → Landed Cost Calculation Log
   - View calculation history (after API integration)

3. **DocTypes Created**
   - Cost Component (child table)
   - Shipment Item (child table)
   - HS Code Duty Rate (child table)
   - HS Code (master)
   - Landed Cost Calculation Log

### ⏳ Pending Integration
1. **Ocean Shipment Enhancement**
   - Fields need to be added via Customize Form (manual step above)
   - Or use the provided installation script with proper permissions

2. **Calculation Engine**
   - API file created: `api/landed_cost.py`
   - Needs to be integrated as custom app or server script
   - Provides:
     - Auto currency conversion
     - HS code-based duty calculation
     - Cost allocation algorithms
     - Landed cost calculation

3. **Auto-Calculation**
   - Requires API integration
   - Will trigger on save when enabled

## 🎯 Quick Start (Current State)

### View HS Codes
1. Login: http://localhost:8080
2. Go to: Desk → Stock → HS Code
3. You'll see 5 sample HS codes
4. Click any to view/edit duty rates

### Create HS Code
1. Go to: Stock → HS Code → New
2. Enter HS Code (e.g., "8471.50")
3. Enter Description
4. Add Duty Rates:
   - Country of Origin
   - Destination Country
   - Duty Rate (%)
   - Valid From date
5. Save

### View Calculation Logs
1. Go to: Desk → Stock → Landed Cost Calculation Log
2. View all calculation history (after calculations are performed)

## 📚 Documentation

### User Guides
- **Complete Guide**: `LANDED_COST_AUTOMATION_GUIDE.md`
- **Requirements**: `.kiro/specs/landed-cost-automation/requirements.md`
- **Design**: `.kiro/specs/landed-cost-automation/design.md`
- **Tasks**: `.kiro/specs/landed-cost-automation/tasks.md`

### Installation Scripts
- **Main Installer**: `install_landed_cost_automation.py`
- **Direct Installer**: `install_lc_direct.py`
- **API Module**: `api/landed_cost.py`

### Helper Scripts
- `install_lc_inline.sh` - Install DocTypes
- `fix_shipment_item.sh` - Fix Shipment Item
- `enhance_ocean_shipment_v2.sh` - Add fields to Ocean Shipment
- `create_sample_hs_codes.sh` - Create sample HS codes

## 🔧 Troubleshooting

### Issue: Can't see new DocTypes
**Solution**: Clear cache
```bash
cd frappe_docker
docker-compose exec backend bench --site localhost clear-cache
```

### Issue: Ocean Shipment doesn't have new fields
**Solution**: Add fields manually via Customize Form (see Step 1 above)

### Issue: Calculations not working
**Solution**: API integration pending. Use manual calculation for now or integrate the API module.

## 🚀 Next Steps

### For Full Functionality:

1. **Add Fields to Ocean Shipment** (Manual via UI - see Step 1)
2. **Integrate Calculation Engine** (Create custom app or use server scripts)
3. **Test Complete Workflow**:
   - Create shipment with items
   - Add cost components
   - Calculate landed costs
   - Create Landed Cost Voucher
   - Update inventory valuation

### For Production Deployment:

1. Create proper custom app
2. Add hooks for auto-calculation
3. Add client-side scripts for UI enhancements
4. Add buttons for "Calculate Landed Cost"
5. Add buttons for "Create Landed Cost Voucher"
6. Set up proper permissions
7. Train users

## 📞 Support

- **Documentation**: See `LANDED_COST_AUTOMATION_GUIDE.md`
- **API Reference**: See `api/landed_cost.py`
- **Design Details**: See `.kiro/specs/landed-cost-automation/design.md`

---

**Installation Date**: February 20, 2026  
**Status**: Core DocTypes Installed ✅  
**Pending**: Ocean Shipment Enhancement & API Integration  
**Access URL**: http://localhost:8080
