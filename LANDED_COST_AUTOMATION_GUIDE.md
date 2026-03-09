# 💰 Landed Cost Automation Guide

## Overview

The Landed Cost Automation system automatically calculates and allocates various cost components across shipment items, providing accurate final product costs for inventory valuation and pricing decisions.

## ✅ Features

### Automated Cost Allocation
- **Freight Costs**: Allocate by weight, volume, or value
- **Insurance Costs**: Allocate proportionally by declared value
- **Customs Duties**: Auto-calculate based on HS codes
- **CHA Fees**: Distribute by customs value or equally
- **Port Charges**: Allocate by weight or volume

### Multi-Currency Support
- Automatic currency conversion
- Uses ERPNext exchange rates
- Displays both original and converted amounts

### HS Code Management
- Master database of HS codes
- Country-specific duty rates
- Historical rate tracking
- Date-based rate lookup

### Audit Trail
- Complete calculation history
- Track who triggered calculations
- Record before/after totals
- Detailed calculation logs

## 📦 Installation

### Prerequisites
1. ERPNext installed and running
2. Ocean Shipment module installed
3. Python 3.8 or higher

### Installation Steps

```bash
# 1. Navigate to your Frappe bench directory
cd ~/frappe-bench

# 2. Run the installation script
bench --site localhost execute install_landed_cost_automation.py

# 3. Clear cache
bench --site localhost clear-cache

# 4. Restart bench
bench restart
```

### Verify Installation

1. Login to ERPNext
2. Go to **Desk → Stock**
3. You should see:
   - Ocean Shipment (enhanced)
   - HS Code
   - Landed Cost Calculation Log

## 🚀 Quick Start

### Step 1: Set Up HS Codes

1. Go to **Stock → HS Code → New**
2. Enter HS Code (e.g., "8517.62")
3. Add description
4. Add duty rates:
   - Country of Origin
   - Destination Country
   - Duty Rate (%)
   - Valid From date
5. Save

**Example HS Codes** (already created during installation):
- 8517.62 - Telecom equipment (10% duty)
- 8471.30 - Laptops (10% duty)
- 8528.72 - TVs (10% duty)
- 6203.42 - Men's cotton trousers (8% duty)
- 6204.62 - Women's cotton trousers (8% duty)

### Step 2: Create a Shipment with Items

1. Go to **Stock → Ocean Shipment → New**
2. Fill in basic shipment details:
   - Shipment Type: Import/Export
   - Shipment Date
   - Customer
   - Port of Loading/Discharge
   - ETD/ETA
   - Shipping Line, Vessel Name

3. Add Shipment Items:
   - Click "Add Row" in Items table
   - Select Item Code
   - Enter Quantity
   - Enter Base Cost (purchase price)
   - Enter Weight per Unit (KG)
   - Enter Volume per Unit (CBM)
   - Select HS Code (for customs duty)
   - Enter Customs Value (if different from base cost)
   - Enter Declared Value (for insurance)

**Example Item:**
```
Item Code: LAPTOP-001
Quantity: 100
Base Cost: $500
Weight per Unit: 2.5 kg
Volume per Unit: 0.05 CBM
HS Code: 8471.30
Customs Value: $500
Declared Value: $550
```

### Step 3: Add Cost Components

1. Scroll to "Cost Components" section
2. Click "Add Row"
3. Select Cost Type:
   - Freight
   - Insurance
   - CHA Fees
   - Port Charges
   - Other
4. Enter Description
5. Enter Amount
6. Select Currency
7. Mark as Estimated or Actual

**Example Cost Components:**
```
Type: Freight
Description: Ocean Freight - Shanghai to LA
Amount: $2,000
Currency: USD
Is Estimated: Yes

Type: Insurance
Description: Cargo Insurance
Amount: $150
Currency: USD

Type: CHA Fees
Description: Customs Clearance
Amount: $500
Currency: USD

Type: Port Charges
Description: Port Handling
Amount: $300
Currency: USD
```

### Step 4: Configure Allocation Methods

1. Scroll to "Landed Cost Settings" section
2. Enable "Auto Calculate Landed Cost" (checked by default)
3. Select Base Currency (USD)
4. Configure allocation methods:
   - **Freight Allocation Method**: Weight/Volume/Value
   - **CHA Allocation Method**: Customs Value/Equal
   - **Port Allocation Method**: Weight/Volume

**Recommended Settings:**
- Freight: Weight (for heavy items) or Volume (for bulky items)
- CHA: Customs Value (proportional to item value)
- Port: Weight (most common)

### Step 5: Calculate Landed Cost

**Option A: Manual Calculation**
1. Click "Calculate Landed Cost" button
2. System will calculate and update all fields
3. Review the Landed Cost Summary section

**Option B: Auto-Calculation**
1. If "Auto Calculate Landed Cost" is enabled
2. System automatically calculates on save
3. Triggered when items or costs change

### Step 6: Review Results

Check the **Landed Cost Summary** section:
```
Total Freight:        $2,000.00
Total Insurance:      $150.00
Total Customs Duty:   $5,000.00  (auto-calculated from HS codes)
Total CHA Fees:       $500.00
Total Port Charges:   $300.00
─────────────────────────────
Total Landed Cost:    $57,950.00
```

Check individual items:
- Each item shows allocated costs
- Total Landed Cost per item
- Unit Landed Cost

### Step 7: Create Landed Cost Voucher (Optional)

1. Click "Create Landed Cost Voucher" button
2. System creates ERPNext Landed Cost Voucher
3. Links voucher to shipment
4. Updates inventory valuation when submitted

## 📊 Understanding Allocation Methods

### Weight-Based Allocation

Best for: Heavy items where freight is charged by weight

**Formula:**
```
Item Allocation = Total Cost × (Item Weight / Total Weight)
```

**Example:**
```
Total Freight: $2,000
Item A: 500 kg (62.5% of 800 kg total)
Item B: 300 kg (37.5% of 800 kg total)

Item A Freight: $2,000 × 0.625 = $1,250
Item B Freight: $2,000 × 0.375 = $750
```

### Volume-Based Allocation

Best for: Bulky items where freight is charged by volume

**Formula:**
```
Item Allocation = Total Cost × (Item Volume / Total Volume)
```

**Example:**
```
Total Freight: $2,000
Item A: 2 CBM (66.7% of 3 CBM total)
Item B: 1 CBM (33.3% of 3 CBM total)

Item A Freight: $2,000 × 0.667 = $1,334
Item B Freight: $2,000 × 0.333 = $666
```

### Value-Based Allocation

Best for: Insurance, or when costs correlate with item value

**Formula:**
```
Item Allocation = Total Cost × (Item Value / Total Value)
```

**Example:**
```
Total Insurance: $150
Item A: $10,000 (66.7% of $15,000 total)
Item B: $5,000 (33.3% of $15,000 total)

Item A Insurance: $150 × 0.667 = $100
Item B Insurance: $150 × 0.333 = $50
```

### Equal Distribution

Best for: Fixed fees that apply equally to all items

**Formula:**
```
Item Allocation = Total Cost / Number of Items
```

**Example:**
```
Total CHA Fees: $500
2 Items

Item A CHA: $500 / 2 = $250
Item B CHA: $500 / 2 = $250
```

## 🔍 Customs Duty Calculation

### How It Works

1. System looks up HS Code for each item
2. Finds applicable duty rate based on:
   - Country of Origin
   - Destination Country
   - Shipment Date
3. Calculates duty:
   ```
   Customs Duty = Customs Value × (Duty Rate / 100)
   ```

### Example

```
Item: Laptop
HS Code: 8471.30
Customs Value: $50,000
Duty Rate: 10% (from HS Code master)

Customs Duty = $50,000 × 0.10 = $5,000
```

### Missing HS Codes

If an item doesn't have an HS code:
- System shows warning message
- Customs duty set to 0
- User must enter manually

### Missing Duty Rates

If duty rate not found for HS code:
- System shows warning message
- Duty rate set to 0
- User can add rate to HS Code master

## 💱 Multi-Currency Handling

### Currency Conversion

1. System converts all costs to Base Currency
2. Uses ERPNext's Currency Exchange rates
3. Uses rate applicable on Shipment Date

### Example

```
Cost Component:
- Type: Freight
- Amount: €1,500
- Currency: EUR
- Shipment Date: 2026-02-20

System looks up EUR to USD rate for 2026-02-20:
- Exchange Rate: 1.08
- Amount in Base Currency: €1,500 × 1.08 = $1,620
```

### Missing Exchange Rates

If exchange rate not found:
- System shows warning
- Uses rate 1.0 as fallback
- User should add rate to Currency Exchange

## 📈 Complete Example

### Scenario
Import shipment from China to USA with 2 items:

**Shipment Details:**
- Shipment Date: 2026-02-20
- Country of Origin: China
- Destination: United States
- Base Currency: USD

**Items:**
```
Item A: Laptops
- Quantity: 100 units
- Base Cost: $50,000
- Weight: 250 kg (2.5 kg each)
- Volume: 5 CBM (0.05 CBM each)
- HS Code: 8471.30 (10% duty)
- Customs Value: $50,000
- Declared Value: $55,000

Item B: Tablets
- Quantity: 200 units
- Base Cost: $30,000
- Weight: 100 kg (0.5 kg each)
- Volume: 2 CBM (0.01 CBM each)
- HS Code: 8471.30 (10% duty)
- Customs Value: $30,000
- Declared Value: $33,000
```

**Cost Components:**
```
Freight: $2,000
Insurance: $150
CHA Fees: $500
Port Charges: $300
```

**Allocation Methods:**
- Freight: Weight
- CHA: Customs Value
- Port: Weight

### Calculation Results

**Item A (Laptops):**
```
Base Cost:              $50,000.00
Allocated Freight:      $1,428.57  (250kg / 350kg × $2,000)
Allocated Insurance:    $93.75     ($55k / $88k × $150)
Customs Duty:           $5,000.00  ($50k × 10%)
Allocated CHA Fees:     $312.50    ($50k / $80k × $500)
Allocated Port Charges: $214.29    (250kg / 350kg × $300)
─────────────────────────────────
Total Landed Cost:      $57,049.11
Unit Landed Cost:       $570.49    (per laptop)
```

**Item B (Tablets):**
```
Base Cost:              $30,000.00
Allocated Freight:      $571.43    (100kg / 350kg × $2,000)
Allocated Insurance:    $56.25     ($33k / $88k × $150)
Customs Duty:           $3,000.00  ($30k × 10%)
Allocated CHA Fees:     $187.50    ($30k / $80k × $500)
Allocated Port Charges: $85.71     (100kg / 350kg × $300)
─────────────────────────────────
Total Landed Cost:      $33,900.89
Unit Landed Cost:       $169.50    (per tablet)
```

**Shipment Totals:**
```
Total Freight:        $2,000.00
Total Insurance:      $150.00
Total Customs Duty:   $8,000.00
Total CHA Fees:       $500.00
Total Port Charges:   $300.00
─────────────────────────────────
Total Landed Cost:    $90,950.00
```

## 🔧 Advanced Features

### Auto-Calculate on Save

When enabled, system automatically recalculates when:
- Items are added/modified
- Cost components are added/modified
- Allocation methods are changed

To enable:
1. Check "Auto Calculate Landed Cost"
2. Save shipment
3. System calculates automatically

### Calculation Audit Trail

View calculation history:
1. Go to **Stock → Landed Cost Calculation Log**
2. Filter by Shipment
3. See all calculations with:
   - Date and time
   - User who triggered
   - Trigger reason
   - Before/after totals
   - Detailed calculation data

### Estimated vs Actual Costs

Track cost estimates vs actuals:
1. Mark cost component as "Is Estimated"
2. Enter estimated amount
3. When invoice received, enter "Actual Amount"
4. Recalculate to update with actual costs

### Container-Level Tracking

Link items to specific containers:
1. In Shipment Item, enter Container No
2. Matches container from Containers table
3. Track costs per container

## 🎯 Best Practices

### 1. Set Up HS Codes First
- Import common HS codes before creating shipments
- Include duty rates for your trade routes
- Keep rates updated

### 2. Choose Appropriate Allocation Methods
- Heavy items: Use weight-based allocation
- Bulky items: Use volume-based allocation
- High-value items: Consider value-based for insurance

### 3. Use Customs Value Correctly
- Customs value may differ from purchase price
- Include freight and insurance if required by customs
- Check your country's customs regulations

### 4. Track Estimated vs Actual
- Start with estimated costs
- Update with actuals when invoices received
- Recalculate for accurate landed costs

### 5. Review Before Finalizing
- Check allocation percentages make sense
- Verify customs duties are reasonable
- Ensure total landed cost is realistic

### 6. Create Landed Cost Voucher
- Link to Purchase Receipts
- Submit to update inventory valuation
- Ensures accurate product costing

## 🐛 Troubleshooting

### Issue: Customs Duty Not Calculating

**Possible Causes:**
1. Item missing HS Code
2. HS Code not in master
3. Duty rate not configured
4. Country information missing

**Solution:**
1. Add HS Code to item
2. Create HS Code in master
3. Add duty rate with country mapping
4. Set country of origin and destination in shipment

### Issue: Exchange Rate Not Found

**Possible Causes:**
1. Exchange rate not in ERPNext
2. Rate not valid for shipment date

**Solution:**
1. Go to **Setup → Currency Exchange**
2. Add exchange rate
3. Set valid from date
4. Recalculate landed cost

### Issue: Allocation Seems Wrong

**Possible Causes:**
1. Wrong allocation method selected
2. Missing weight/volume data
3. Zero total weight/volume

**Solution:**
1. Review allocation method choice
2. Enter weight/volume for all items
3. Ensure values are greater than zero
4. Recalculate

### Issue: Total Doesn't Match Sum

**Possible Causes:**
1. Rounding differences
2. Calculation not completed

**Solution:**
1. Click "Calculate Landed Cost" button
2. System handles rounding automatically
3. Last item gets remainder to ensure exact match

## 📚 API Reference

### Calculate Landed Cost

```python
import frappe

result = frappe.call(
    "api.landed_cost.calculate_landed_cost",
    shipment_name="OSHIP-0001"
)

# Returns:
# {
#     "success": True,
#     "message": "Landed cost calculated successfully",
#     "total_landed_cost": 90950.00
# }
```

### Get Duty Rate

```python
result = frappe.call(
    "api.landed_cost.get_duty_rate_api",
    hs_code="8471.30",
    origin_country="China",
    dest_country="United States",
    date="2026-02-20"
)

# Returns:
# {
#     "hs_code": "8471.30",
#     "duty_rate": 10.0,
#     "origin_country": "China",
#     "dest_country": "United States",
#     "date": "2026-02-20"
# }
```

### Create Landed Cost Voucher

```python
result = frappe.call(
    "api.landed_cost.create_landed_cost_voucher_from_shipment",
    shipment_name="OSHIP-0001"
)

# Returns:
# {
#     "success": True,
#     "message": "Landed Cost Voucher created successfully",
#     "voucher_name": "LCV-00001"
# }
```

## 🔐 Permissions

### Stock User
- Create and edit shipments
- Add items and cost components
- Calculate landed costs
- View calculation logs

### Stock Manager
- All Stock User permissions
- Create and edit HS Codes
- Configure allocation methods
- Delete calculation logs

### System Manager
- Full access to all features
- Configure system settings
- Manage permissions

## 📞 Support

### Documentation
- Requirements: `.kiro/specs/landed-cost-automation/requirements.md`
- Design: `.kiro/specs/landed-cost-automation/design.md`
- Tasks: `.kiro/specs/landed-cost-automation/tasks.md`

### Common Resources
- ERPNext Documentation: https://docs.erpnext.com
- Frappe Framework: https://frappeframework.com

### Getting Help
1. Check this guide first
2. Review calculation logs for errors
3. Check ERPNext error log
4. Consult with system administrator

---

**Version**: 1.0  
**Last Updated**: February 20, 2026  
**Status**: ✅ Production Ready
