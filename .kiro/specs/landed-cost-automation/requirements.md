# Requirements Document: Landed Cost Automation

## Introduction

This feature enhances ERPNext's existing landed cost functionality with intelligent automation for import/export shipments. The system automatically calculates and distributes various cost components (freight, insurance, customs duties, clearing agent fees, port handling charges) across shipment items to determine accurate final product costs. This automation integrates with ERPNext's Ocean Shipment, Purchase Receipt, and Stock Entry doctypes, supporting multiple allocation methods and real-time cost updates.

## Glossary

- **System**: The Landed Cost Automation module within ERPNext
- **Ocean_Shipment**: ERPNext doctype representing an import/export shipment
- **Purchase_Receipt**: ERPNext doctype for recording received goods
- **Stock_Entry**: ERPNext doctype for inventory movements
- **Landed_Cost_Voucher**: ERPNext doctype for distributing additional costs
- **HS_Code**: Harmonized System Code for product classification
- **CHA**: Customs House Agent
- **Allocation_Method**: Method for distributing costs (weight, volume, value, quantity)
- **Duty_Rate**: Percentage or fixed amount of customs duty per product/country
- **Cost_Component**: Individual cost element (freight, insurance, duty, CHA fees, port charges)
- **Shipment_Item**: Individual product line within a shipment
- **Landed_Cost**: Total cost of product including purchase price and all additional costs

## Requirements

### Requirement 1: Freight Cost Auto-Allocation

**User Story:** As an import manager, I want freight costs to be automatically distributed across shipment items, so that each product reflects its proportional share of transportation costs.

#### Acceptance Criteria

1. WHEN a freight cost is entered on an Ocean_Shipment, THE System SHALL calculate the allocation basis for each Shipment_Item based on the selected Allocation_Method
2. WHERE the Allocation_Method is "by weight", THE System SHALL distribute freight costs proportionally to each item's total weight
3. WHERE the Allocation_Method is "by volume", THE System SHALL distribute freight costs proportionally to each item's total volume
4. WHERE the Allocation_Method is "by value", THE System SHALL distribute freight costs proportionally to each item's purchase value
5. WHERE the Allocation_Method is "by quantity", THE System SHALL distribute freight costs equally across all item quantities
6. WHEN freight allocation is calculated, THE System SHALL update each Shipment_Item with its allocated freight cost amount
7. WHEN the total allocated freight costs are calculated, THE System SHALL equal the original freight cost amount entered

### Requirement 2: Insurance Cost Allocation

**User Story:** As a finance manager, I want insurance costs to be automatically allocated to shipment items, so that product valuations include insurance expenses.

#### Acceptance Criteria

1. WHEN an insurance cost is entered on an Ocean_Shipment, THE System SHALL calculate insurance allocation for each Shipment_Item based on the item's declared value
2. WHEN insurance allocation is calculated, THE System SHALL distribute costs proportionally to each item's percentage of total shipment value
3. WHEN insurance allocation is complete, THE System SHALL update each Shipment_Item with its allocated insurance cost amount
4. WHEN the total allocated insurance costs are calculated, THE System SHALL equal the original insurance cost amount entered

### Requirement 3: Customs Duty Auto-Calculation

**User Story:** As a customs compliance officer, I want customs duties to be automatically calculated based on HS codes and duty rates, so that duty costs are accurate and compliant.

#### Acceptance Criteria

1. WHEN a Shipment_Item has an HS_Code assigned, THE System SHALL retrieve the applicable Duty_Rate for that HS_Code and destination country
2. WHEN a Duty_Rate is retrieved, THE System SHALL calculate the customs duty amount by applying the rate to the item's assessable value
3. WHERE the Duty_Rate is a percentage, THE System SHALL calculate duty as (assessable_value × duty_rate / 100)
4. WHERE the Duty_Rate is a fixed amount per unit, THE System SHALL calculate duty as (quantity × duty_rate)
5. WHEN customs duty is calculated, THE System SHALL update the Shipment_Item with the calculated duty amount
6. IF no Duty_Rate is found for an HS_Code and country combination, THEN THE System SHALL set the duty amount to zero and log a warning

### Requirement 4: Clearing Agent Fees Distribution

**User Story:** As a logistics coordinator, I want CHA fees to be automatically distributed across shipment items, so that clearing costs are properly allocated.

#### Acceptance Criteria

1. WHEN CHA fees are entered on an Ocean_Shipment, THE System SHALL distribute the fees across all Shipment_Items based on the selected Allocation_Method
2. WHEN CHA fee allocation is calculated, THE System SHALL use the same Allocation_Method as freight costs
3. WHEN CHA fee allocation is complete, THE System SHALL update each Shipment_Item with its allocated CHA fee amount
4. WHEN the total allocated CHA fees are calculated, THE System SHALL equal the original CHA fee amount entered

### Requirement 5: Port Handling Cost Distribution

**User Story:** As a supply chain analyst, I want port handling charges to be automatically allocated to items, so that all landing costs are captured.

#### Acceptance Criteria

1. WHEN port handling charges are entered on an Ocean_Shipment, THE System SHALL distribute the charges across all Shipment_Items based on the selected Allocation_Method
2. WHEN port handling allocation is calculated, THE System SHALL use the same Allocation_Method as freight costs
3. WHEN port handling allocation is complete, THE System SHALL update each Shipment_Item with its allocated port handling cost amount
4. WHEN the total allocated port handling costs are calculated, THE System SHALL equal the original port handling charge amount entered

### Requirement 6: Final Landed Cost Calculation

**User Story:** As a product manager, I want the system to automatically calculate the total landed cost per item, so that I can make informed pricing decisions.

#### Acceptance Criteria

1. WHEN all Cost_Components are allocated to a Shipment_Item, THE System SHALL calculate the total Landed_Cost as the sum of purchase price plus all allocated costs
2. WHEN Landed_Cost is calculated, THE System SHALL include freight, insurance, customs duty, CHA fees, and port handling charges
3. WHEN Landed_Cost calculation is complete, THE System SHALL update the Shipment_Item with the final landed cost per unit
4. WHEN a Purchase_Receipt is created from the Ocean_Shipment, THE System SHALL create a Landed_Cost_Voucher with all calculated cost allocations
5. WHEN the Landed_Cost_Voucher is submitted, THE System SHALL update the stock valuation for each item to reflect the landed cost

### Requirement 7: Allocation Method Configuration

**User Story:** As a system administrator, I want to configure default allocation methods for different cost types, so that the system uses appropriate distribution logic.

#### Acceptance Criteria

1. THE System SHALL provide configuration options for default Allocation_Method per Cost_Component type
2. WHEN an Ocean_Shipment is created, THE System SHALL apply the configured default Allocation_Method for each Cost_Component
3. WHEN a user changes the Allocation_Method on an Ocean_Shipment, THE System SHALL recalculate all cost allocations using the new method
4. THE System SHALL support the following Allocation_Methods: by weight, by volume, by value, by quantity

### Requirement 8: HS Code and Duty Rate Master Data

**User Story:** As a trade compliance manager, I want to maintain HS codes and duty rates in the system, so that duty calculations are based on current tariff schedules.

#### Acceptance Criteria

1. THE System SHALL provide a master data table for HS_Code entries with fields for code, description, and product category
2. THE System SHALL provide a master data table for Duty_Rate entries with fields for HS_Code, country, rate type (percentage or fixed), and rate value
3. WHEN a Duty_Rate is created or updated, THE System SHALL validate that the HS_Code exists in the HS_Code master table
4. WHEN a Duty_Rate is queried for calculation, THE System SHALL return the most specific matching rate (HS_Code + country combination)
5. IF multiple Duty_Rates exist for the same HS_Code and country, THEN THE System SHALL use the most recently created rate

### Requirement 9: Real-Time Cost Updates

**User Story:** As a finance controller, I want cost allocations to update automatically when shipment costs change, so that landed costs remain accurate throughout the shipment lifecycle.

#### Acceptance Criteria

1. WHEN any Cost_Component amount is modified on an Ocean_Shipment, THE System SHALL automatically recalculate all cost allocations for affected Shipment_Items
2. WHEN a Shipment_Item is added or removed from an Ocean_Shipment, THE System SHALL recalculate cost allocations for all remaining items
3. WHEN an Allocation_Method is changed, THE System SHALL recalculate all cost allocations using the new method
4. WHEN cost allocations are recalculated, THE System SHALL update all dependent fields immediately without requiring manual refresh

### Requirement 10: Integration with Purchase Receipt and Stock Entry

**User Story:** As an inventory manager, I want landed costs to automatically flow to purchase receipts and stock entries, so that inventory valuation is accurate.

#### Acceptance Criteria

1. WHEN a Purchase_Receipt is created from an Ocean_Shipment with calculated landed costs, THE System SHALL automatically create a linked Landed_Cost_Voucher
2. WHEN the Landed_Cost_Voucher is created, THE System SHALL populate it with all Cost_Components and their allocations from the Ocean_Shipment
3. WHEN the Landed_Cost_Voucher is submitted, THE System SHALL update the Purchase_Receipt item valuations with the landed costs
4. WHEN a Stock_Entry is created from the Purchase_Receipt, THE System SHALL use the updated landed cost valuations
5. WHEN landed costs are applied, THE System SHALL maintain audit trail linking Ocean_Shipment, Purchase_Receipt, and Landed_Cost_Voucher

### Requirement 11: Validation and Error Handling

**User Story:** As a data quality manager, I want the system to validate cost allocations and handle errors gracefully, so that data integrity is maintained.

#### Acceptance Criteria

1. WHEN cost allocation is performed, THE System SHALL validate that the sum of allocated costs equals the original cost amount within a tolerance of 0.01
2. IF the sum of allocated costs differs from the original amount due to rounding, THEN THE System SHALL adjust the largest allocation to balance the total
3. WHEN an Allocation_Method requires specific item attributes (weight, volume), THE System SHALL validate that all Shipment_Items have the required attributes populated
4. IF required attributes are missing for the selected Allocation_Method, THEN THE System SHALL display an error message identifying the missing data and prevent allocation
5. WHEN a Duty_Rate lookup fails for an HS_Code, THE System SHALL log a warning message with the HS_Code and country details
6. WHEN cost allocation calculations encounter errors, THE System SHALL display user-friendly error messages and prevent saving invalid data

### Requirement 12: Reporting and Audit Trail

**User Story:** As an auditor, I want to view detailed cost allocation breakdowns and audit trails, so that I can verify the accuracy of landed cost calculations.

#### Acceptance Criteria

1. THE System SHALL provide a detailed cost allocation report showing each Cost_Component, Allocation_Method, and per-item allocations
2. WHEN a cost allocation report is generated, THE System SHALL include the calculation basis (weight, volume, value, or quantity) for each item
3. THE System SHALL maintain an audit log of all cost allocation calculations including timestamp, user, and calculation parameters
4. WHEN cost allocations are recalculated, THE System SHALL log the previous values and new values for audit purposes
5. THE System SHALL provide a summary view showing total landed cost per item with breakdown by cost component type
