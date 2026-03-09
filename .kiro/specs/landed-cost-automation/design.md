# Design Document: Landed Cost Automation

## System Architecture

### Overview
The Landed Cost Automation system extends ERPNext's Ocean Shipment module with automated cost calculation and allocation capabilities. It integrates with ERPNext's existing Landed Cost Voucher system while providing intelligent cost distribution algorithms.

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Ocean Shipment DocType                    │
│  (Enhanced with Landed Cost fields and calculations)         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├──► Cost Components Table (Child DocType)
                 │    - Freight, Insurance, Customs, CHA, Port
                 │
                 ├──► Shipment Items Table (Child DocType)
                 │    - Items with HS codes, weights, values
                 │
                 └──► Landed Cost Calculation Engine
                      │
                      ├──► Allocation Algorithms
                      │    - Weight-based
                      │    - Volume-based
                      │    - Value-based
                      │
                      ├──► HS Code & Duty Rate Master
                      │    - Country-specific rates
                      │    - Historical tracking
                      │
                      └──► Integration Layer
                           - Landed Cost Voucher creation
                           - Inventory valuation updates
```

## Data Model

### 1. Ocean Shipment (Enhanced)

**New Fields:**
```python
{
    # Cost Components Section
    "cost_components": "Table",  # Link to Cost Component child table
    "total_freight": "Currency",
    "total_insurance": "Currency",
    "total_customs_duty": "Currency",
    "total_cha_fees": "Currency",
    "total_port_charges": "Currency",
    "total_landed_cost": "Currency",
    
    # Allocation Settings
    "freight_allocation_method": "Select",  # Weight/Volume/Value
    "cha_allocation_method": "Select",  # Customs Value/Equal
    "port_allocation_method": "Select",  # Weight/Volume
    
    # Integration
    "landed_cost_voucher": "Link",  # Link to Landed Cost Voucher
    "auto_calculate_landed_cost": "Check",  # Enable auto-calculation
    
    # Currency
    "base_currency": "Link",  # Company currency
}
```

### 2. Cost Component (New Child DocType)

```python
{
    "doctype": "Cost Component",
    "istable": 1,
    "fields": [
        {"fieldname": "cost_type", "fieldtype": "Select", 
         "options": "Freight\nInsurance\nCustoms Duty\nCHA Fees\nPort Charges\nOther"},
        {"fieldname": "description", "fieldtype": "Data"},
        {"fieldname": "amount", "fieldtype": "Currency"},
        {"fieldname": "currency", "fieldtype": "Link", "options": "Currency"},
        {"fieldname": "exchange_rate", "fieldtype": "Float"},
        {"fieldname": "amount_in_base_currency", "fieldtype": "Currency"},
        {"fieldname": "is_estimated", "fieldtype": "Check"},
        {"fieldname": "actual_amount", "fieldtype": "Currency"},
        {"fieldname": "supplier", "fieldtype": "Link", "options": "Supplier"},
        {"fieldname": "invoice_reference", "fieldtype": "Data"},
    ]
}
```

### 3. Shipment Item (New Child DocType)

```python
{
    "doctype": "Shipment Item",
    "istable": 1,
    "fields": [
        # Item Details
        {"fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"fieldname": "item_name", "fieldtype": "Data"},
        {"fieldname": "description", "fieldtype": "Text Editor"},
        {"fieldname": "quantity", "fieldtype": "Float"},
        {"fieldname": "uom", "fieldtype": "Link", "options": "UOM"},
        
        # Physical Attributes
        {"fieldname": "weight_per_unit", "fieldtype": "Float"},
        {"fieldname": "total_weight", "fieldtype": "Float"},
        {"fieldname": "volume_per_unit", "fieldtype": "Float"},
        {"fieldname": "total_volume", "fieldtype": "Float"},
        
        # Values
        {"fieldname": "base_cost", "fieldtype": "Currency"},
        {"fieldname": "customs_value", "fieldtype": "Currency"},
        {"fieldname": "declared_value", "fieldtype": "Currency"},
        
        # HS Code & Duty
        {"fieldname": "hs_code", "fieldtype": "Link", "options": "HS Code"},
        {"fieldname": "duty_rate", "fieldtype": "Percent"},
        {"fieldname": "customs_duty", "fieldtype": "Currency"},
        
        # Allocated Costs
        {"fieldname": "allocated_freight", "fieldtype": "Currency"},
        {"fieldname": "allocated_insurance", "fieldtype": "Currency"},
        {"fieldname": "allocated_cha_fees", "fieldtype": "Currency"},
        {"fieldname": "allocated_port_charges", "fieldtype": "Currency"},
        
        # Landed Cost
        {"fieldname": "total_landed_cost", "fieldtype": "Currency"},
        {"fieldname": "unit_landed_cost", "fieldtype": "Currency"},
        
        # Container Reference
        {"fieldname": "container_no", "fieldtype": "Data"},
    ]
}
```

### 4. HS Code Master (New DocType)

```python
{
    "doctype": "HS Code",
    "fields": [
        {"fieldname": "hs_code", "fieldtype": "Data", "unique": 1},
        {"fieldname": "description", "fieldtype": "Text"},
        {"fieldname": "duty_rates", "fieldtype": "Table", "options": "HS Code Duty Rate"},
    ]
}
```

### 5. HS Code Duty Rate (New Child DocType)

```python
{
    "doctype": "HS Code Duty Rate",
    "istable": 1,
    "fields": [
        {"fieldname": "country_of_origin", "fieldtype": "Link", "options": "Country"},
        {"fieldname": "destination_country", "fieldtype": "Link", "options": "Country"},
        {"fieldname": "duty_rate", "fieldtype": "Percent"},
        {"fieldname": "valid_from", "fieldtype": "Date"},
        {"fieldname": "valid_to", "fieldtype": "Date"},
        {"fieldname": "additional_duty", "fieldtype": "Percent"},
        {"fieldname": "notes", "fieldtype": "Text"},
    ]
}
```

### 6. Landed Cost Calculation Log (New DocType)

```python
{
    "doctype": "Landed Cost Calculation Log",
    "fields": [
        {"fieldname": "shipment", "fieldtype": "Link", "options": "Ocean Shipment"},
        {"fieldname": "calculation_date", "fieldtype": "Datetime"},
        {"fieldname": "triggered_by", "fieldtype": "Link", "options": "User"},
        {"fieldname": "trigger_reason", "fieldtype": "Select",
         "options": "Manual\nCost Component Changed\nItem Changed\nAllocation Method Changed"},
        {"fieldname": "calculation_details", "fieldtype": "Long Text"},
        {"fieldname": "previous_total", "fieldtype": "Currency"},
        {"fieldname": "new_total", "fieldtype": "Currency"},
    ]
}
```

## Allocation Algorithms

### 1. Weight-Based Allocation

```python
def allocate_by_weight(total_cost, items):
    """
    Allocates cost proportionally based on item weight
    """
    total_weight = sum(item.total_weight for item in items)
    
    for item in items:
        if total_weight > 0:
            weight_ratio = item.total_weight / total_weight
            item.allocated_cost = total_cost * weight_ratio
        else:
            item.allocated_cost = 0
```

### 2. Volume-Based Allocation

```python
def allocate_by_volume(total_cost, items):
    """
    Allocates cost proportionally based on item volume
    """
    total_volume = sum(item.total_volume for item in items)
    
    for item in items:
        if total_volume > 0:
            volume_ratio = item.total_volume / total_volume
            item.allocated_cost = total_cost * volume_ratio
        else:
            item.allocated_cost = 0
```

### 3. Value-Based Allocation

```python
def allocate_by_value(total_cost, items):
    """
    Allocates cost proportionally based on item value
    """
    total_value = sum(item.customs_value or item.base_cost for item in items)
    
    for item in items:
        item_value = item.customs_value or item.base_cost
        if total_value > 0:
            value_ratio = item_value / total_value
            item.allocated_cost = total_cost * value_ratio
        else:
            item.allocated_cost = 0
```

### 4. Equal Distribution

```python
def allocate_equally(total_cost, items):
    """
    Distributes cost equally across all items
    """
    item_count = len(items)
    
    if item_count > 0:
        cost_per_item = total_cost / item_count
        for item in items:
            item.allocated_cost = cost_per_item
```

## Calculation Engine

### Main Calculation Flow

```python
class LandedCostCalculator:
    def __init__(self, shipment):
        self.shipment = shipment
        self.items = shipment.items
        self.cost_components = shipment.cost_components
        
    def calculate_all(self):
        """Main calculation orchestrator"""
        # Step 1: Convert all costs to base currency
        self.convert_currencies()
        
        # Step 2: Calculate customs duties
        self.calculate_customs_duties()
        
        # Step 3: Allocate freight costs
        self.allocate_freight()
        
        # Step 4: Allocate insurance costs
        self.allocate_insurance()
        
        # Step 5: Allocate CHA fees
        self.allocate_cha_fees()
        
        # Step 6: Allocate port charges
        self.allocate_port_charges()
        
        # Step 7: Calculate total landed cost per item
        self.calculate_total_landed_cost()
        
        # Step 8: Log the calculation
        self.log_calculation()
        
        # Step 9: Update shipment totals
        self.update_shipment_totals()
        
    def convert_currencies(self):
        """Convert all cost components to base currency"""
        for cost in self.cost_components:
            if cost.currency != self.shipment.base_currency:
                exchange_rate = get_exchange_rate(
                    cost.currency,
                    self.shipment.base_currency,
                    self.shipment.shipment_date
                )
                cost.exchange_rate = exchange_rate
                cost.amount_in_base_currency = cost.amount * exchange_rate
            else:
                cost.exchange_rate = 1.0
                cost.amount_in_base_currency = cost.amount
                
    def calculate_customs_duties(self):
        """Calculate customs duty for each item based on HS code"""
        for item in self.items:
            if item.hs_code:
                duty_rate = get_duty_rate(
                    item.hs_code,
                    self.shipment.country_of_origin,
                    self.shipment.destination_country,
                    self.shipment.shipment_date
                )
                item.duty_rate = duty_rate
                item.customs_duty = item.customs_value * (duty_rate / 100)
            else:
                item.customs_duty = 0
                item.duty_rate = 0
                
    def allocate_freight(self):
        """Allocate freight costs based on configured method"""
        freight_costs = sum(
            c.amount_in_base_currency 
            for c in self.cost_components 
            if c.cost_type == "Freight"
        )
        
        method = self.shipment.freight_allocation_method
        
        if method == "Weight":
            allocate_by_weight(freight_costs, self.items, "allocated_freight")
        elif method == "Volume":
            allocate_by_volume(freight_costs, self.items, "allocated_freight")
        elif method == "Value":
            allocate_by_value(freight_costs, self.items, "allocated_freight")
            
    def allocate_insurance(self):
        """Allocate insurance costs based on declared value"""
        insurance_costs = sum(
            c.amount_in_base_currency 
            for c in self.cost_components 
            if c.cost_type == "Insurance"
        )
        
        allocate_by_value(insurance_costs, self.items, "allocated_insurance")
        
    def allocate_cha_fees(self):
        """Allocate CHA fees based on configured method"""
        cha_costs = sum(
            c.amount_in_base_currency 
            for c in self.cost_components 
            if c.cost_type == "CHA Fees"
        )
        
        method = self.shipment.cha_allocation_method
        
        if method == "Customs Value":
            allocate_by_value(cha_costs, self.items, "allocated_cha_fees")
        elif method == "Equal":
            allocate_equally(cha_costs, self.items, "allocated_cha_fees")
            
    def allocate_port_charges(self):
        """Allocate port charges based on configured method"""
        port_costs = sum(
            c.amount_in_base_currency 
            for c in self.cost_components 
            if c.cost_type == "Port Charges"
        )
        
        method = self.shipment.port_allocation_method
        
        if method == "Weight":
            allocate_by_weight(port_costs, self.items, "allocated_port_charges")
        elif method == "Volume":
            allocate_by_volume(port_costs, self.items, "allocated_port_charges")
            
    def calculate_total_landed_cost(self):
        """Calculate total landed cost for each item"""
        for item in self.items:
            item.total_landed_cost = (
                item.base_cost +
                item.allocated_freight +
                item.allocated_insurance +
                item.customs_duty +
                item.allocated_cha_fees +
                item.allocated_port_charges
            )
            
            if item.quantity > 0:
                item.unit_landed_cost = item.total_landed_cost / item.quantity
            else:
                item.unit_landed_cost = 0
```

## Integration with ERPNext Landed Cost Voucher

### Voucher Creation Flow

```python
def create_landed_cost_voucher(shipment):
    """
    Creates or updates Landed Cost Voucher from shipment
    """
    # Check if voucher already exists
    if shipment.landed_cost_voucher:
        voucher = frappe.get_doc("Landed Cost Voucher", shipment.landed_cost_voucher)
    else:
        voucher = frappe.new_doc("Landed Cost Voucher")
        voucher.company = shipment.company
        voucher.posting_date = shipment.shipment_date
        
    # Clear existing items and taxes
    voucher.items = []
    voucher.taxes = []
    
    # Add shipment items to voucher
    for item in shipment.items:
        voucher.append("items", {
            "item_code": item.item_code,
            "quantity": item.quantity,
            "rate": item.base_cost,
            "amount": item.base_cost * item.quantity,
            "receipt_document_type": "Purchase Receipt",  # or Stock Entry
            "receipt_document": item.purchase_receipt,  # Link to source
        })
        
    # Add cost components as taxes
    for cost in shipment.cost_components:
        voucher.append("taxes", {
            "description": f"{cost.cost_type} - {cost.description}",
            "amount": cost.amount_in_base_currency,
            "account_head": get_expense_account(cost.cost_type),
        })
        
    voucher.save()
    
    # Link back to shipment
    shipment.landed_cost_voucher = voucher.name
    shipment.save()
    
    return voucher
```

## User Interface Design

### 1. Ocean Shipment Form Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Ocean Shipment: OSHIP-0001                                   │
├─────────────────────────────────────────────────────────────┤
│ [Shipment Details Section]                                   │
│ [Port & Route Details Section]                               │
│ [Shipping Details Section]                                   │
│ [Container Information Section]                              │
│                                                               │
│ ┌─ Shipment Items ─────────────────────────────────────────┐│
│ │ [Add Row]                                                 ││
│ │ Item | Qty | Weight | Volume | HS Code | Base Cost | ... ││
│ │ ───────────────────────────────────────────────────────── ││
│ │ Item A | 100 | 500kg | 2m³ | 8517.62 | $10,000 | ...     ││
│ │ Item B | 50  | 300kg | 1m³ | 8471.30 | $5,000  | ...     ││
│ └───────────────────────────────────────────────────────────┘│
│                                                               │
│ ┌─ Cost Components ────────────────────────────────────────┐│
│ │ [Add Row]                                                 ││
│ │ Type | Description | Amount | Currency | Base Amount     ││
│ │ ───────────────────────────────────────────────────────── ││
│ │ Freight | Ocean Freight | $2,000 | USD | $2,000         ││
│ │ Insurance | Cargo Insurance | $150 | USD | $150         ││
│ │ CHA Fees | Customs Clearance | $500 | USD | $500        ││
│ └───────────────────────────────────────────────────────────┘│
│                                                               │
│ ┌─ Landed Cost Settings ───────────────────────────────────┐│
│ │ ☑ Auto Calculate Landed Cost                             ││
│ │ Freight Allocation: [Weight ▼]                            ││
│ │ CHA Allocation: [Customs Value ▼]                         ││
│ │ Port Allocation: [Weight ▼]                               ││
│ │                                                            ││
│ │ [Calculate Landed Cost] [Create Landed Cost Voucher]     ││
│ └───────────────────────────────────────────────────────────┘│
│                                                               │
│ ┌─ Landed Cost Summary ────────────────────────────────────┐│
│ │ Total Freight:        $2,000.00                           ││
│ │ Total Insurance:      $150.00                             ││
│ │ Total Customs Duty:   $1,500.00                           ││
│ │ Total CHA Fees:       $500.00                             ││
│ │ Total Port Charges:   $300.00                             ││
│ │ ─────────────────────────────────                         ││
│ │ Total Landed Cost:    $19,450.00                          ││
│ └───────────────────────────────────────────────────────────┘│
│                                                               │
│ [Status & Tracking Section]                                  │
│ [Additional Information Section]                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Item-Level Landed Cost View

```
┌─────────────────────────────────────────────────────────────┐
│ Shipment Item: Item A                                        │
├─────────────────────────────────────────────────────────────┤
│ Base Cost:              $10,000.00                           │
│ Allocated Freight:      $1,250.00  (62.5% by weight)        │
│ Allocated Insurance:    $100.00    (66.7% by value)         │
│ Customs Duty:           $1,000.00  (10% of customs value)   │
│ Allocated CHA Fees:     $333.33    (66.7% by customs value) │
│ Allocated Port Charges: $187.50    (62.5% by weight)        │
│ ─────────────────────────────────────────────────────────    │
│ Total Landed Cost:      $12,870.83                           │
│ Unit Landed Cost:       $128.71    (for 100 units)          │
└─────────────────────────────────────────────────────────────┘
```

## API Endpoints

### 1. Calculate Landed Cost
```python
@frappe.whitelist()
def calculate_landed_cost(shipment_name):
    """
    Triggers landed cost calculation for a shipment
    """
    shipment = frappe.get_doc("Ocean Shipment", shipment_name)
    calculator = LandedCostCalculator(shipment)
    calculator.calculate_all()
    shipment.save()
    return shipment
```

### 2. Get Duty Rate
```python
@frappe.whitelist()
def get_duty_rate(hs_code, origin_country, dest_country, shipment_date):
    """
    Retrieves applicable duty rate for HS code
    """
    # Query HS Code Duty Rate table
    # Return rate valid for shipment_date
```

### 3. Create Landed Cost Voucher
```python
@frappe.whitelist()
def create_landed_cost_voucher_from_shipment(shipment_name):
    """
    Creates Landed Cost Voucher from Ocean Shipment
    """
    shipment = frappe.get_doc("Ocean Shipment", shipment_name)
    voucher = create_landed_cost_voucher(shipment)
    return voucher
```

## Validation Rules

### 1. Pre-Calculation Validations
- All items must have base cost
- All items must have weight or volume (depending on allocation method)
- All cost components must have valid amounts
- Currency exchange rates must be available
- Items with HS codes must have valid duty rates

### 2. Post-Calculation Validations
- Sum of allocated costs must equal total cost component
- Total landed cost must be greater than base cost
- Unit landed cost must be positive

## Performance Considerations

### 1. Caching
- Cache HS code duty rates
- Cache exchange rates for the day
- Cache allocation method preferences

### 2. Batch Processing
- Calculate all items in a single transaction
- Bulk update item records

### 3. Async Processing
- For large shipments (>100 items), use background job
- Show progress indicator to user

## Security & Permissions

### Role-Based Access
- **Logistics Coordinator**: Can enter cost components, trigger calculations
- **Finance Manager**: Can view all costs, approve landed cost vouchers
- **System Manager**: Full access to configuration and HS code master

### Audit Trail
- Log all calculation events
- Track changes to cost components
- Record who approved landed cost vouchers

## Testing Strategy

### Unit Tests
- Test each allocation algorithm independently
- Test customs duty calculation with various HS codes
- Test currency conversion logic

### Integration Tests
- Test full calculation flow end-to-end
- Test Landed Cost Voucher creation
- Test inventory valuation updates

### Edge Cases
- Zero-weight items
- Missing HS codes
- Missing exchange rates
- Single-item shipments
- Multi-currency scenarios

## Migration & Deployment

### Phase 1: DocType Creation
1. Create new child DocTypes (Cost Component, Shipment Item, etc.)
2. Create HS Code master DocType
3. Add new fields to Ocean Shipment

### Phase 2: Calculation Engine
1. Implement allocation algorithms
2. Implement calculation orchestrator
3. Add API endpoints

### Phase 3: UI Enhancement
1. Add cost component table to form
2. Add shipment items table to form
3. Add calculation buttons and summary section

### Phase 4: Integration
1. Implement Landed Cost Voucher creation
2. Test inventory valuation updates
3. Add audit logging

### Phase 5: Data Migration
1. Import HS codes and duty rates
2. Set default allocation methods
3. Train users

## Future Enhancements

1. **AI-Powered Cost Estimation**: Use historical data to predict costs
2. **Real-Time Duty Rate Updates**: Integration with customs APIs
3. **Multi-Leg Shipment Support**: Handle transshipment scenarios
4. **Cost Variance Analysis**: Compare estimated vs actual costs
5. **Automated Invoice Matching**: Match supplier invoices to cost components
