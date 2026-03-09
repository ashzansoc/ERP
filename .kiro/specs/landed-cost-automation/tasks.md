# Implementation Tasks: Landed Cost Automation

## Phase 1: Foundation - DocType Creation

### Task 1.1: Create Cost Component Child DocType
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: None

**Subtasks**:
- [ ] Create `Cost Component` DocType with istable=1
- [ ] Add fields: cost_type, description, amount, currency, exchange_rate, amount_in_base_currency
- [ ] Add fields: is_estimated, actual_amount, supplier, invoice_reference
- [ ] Set up field validations (amount > 0, required fields)
- [ ] Test DocType creation and field behavior

**Acceptance Criteria**:
- Cost Component DocType exists and is usable as child table
- All fields are properly configured with correct types
- Validation prevents negative amounts

---

### Task 1.2: Create Shipment Item Child DocType
**Priority**: High  
**Estimated Time**: 3 hours  
**Dependencies**: None

**Subtasks**:
- [ ] Create `Shipment Item` DocType with istable=1
- [ ] Add item identification fields: item_code, item_name, description, quantity, uom
- [ ] Add physical attribute fields: weight_per_unit, total_weight, volume_per_unit, total_volume
- [ ] Add value fields: base_cost, customs_value, declared_value
- [ ] Add HS code fields: hs_code, duty_rate, customs_duty
- [ ] Add allocated cost fields: allocated_freight, allocated_insurance, allocated_cha_fees, allocated_port_charges
- [ ] Add landed cost fields: total_landed_cost, unit_landed_cost
- [ ] Add container_no field for linking
- [ ] Set up computed fields (total_weight = weight_per_unit * quantity)
- [ ] Test DocType creation and calculations

**Acceptance Criteria**:
- Shipment Item DocType exists with all required fields
- Computed fields calculate correctly
- Can be used as child table in Ocean Shipment

---

### Task 1.3: Create HS Code Master DocType
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.4

**Subtasks**:
- [ ] Create `HS Code` DocType as master
- [ ] Add fields: hs_code (unique), description
- [ ] Add child table field: duty_rates
- [ ] Set up naming rule (use hs_code as name)
- [ ] Add validation for HS code format (6-10 digits)
- [ ] Create list view with search functionality
- [ ] Test DocType creation and uniqueness constraint

**Acceptance Criteria**:
- HS Code DocType exists and can store codes
- HS codes are unique
- Format validation works correctly

---

### Task 1.4: Create HS Code Duty Rate Child DocType
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: None

**Subtasks**:
- [ ] Create `HS Code Duty Rate` DocType with istable=1
- [ ] Add fields: country_of_origin, destination_country, duty_rate, additional_duty
- [ ] Add validity fields: valid_from, valid_to
- [ ] Add notes field for additional information
- [ ] Set up validation (duty_rate >= 0, valid_from < valid_to)
- [ ] Test DocType creation

**Acceptance Criteria**:
- HS Code Duty Rate DocType exists
- Can store multiple rates per HS code
- Date validations work correctly

---

### Task 1.5: Create Landed Cost Calculation Log DocType
**Priority**: Medium  
**Estimated Time**: 1.5 hours  
**Dependencies**: None

**Subtasks**:
- [ ] Create `Landed Cost Calculation Log` DocType
- [ ] Add fields: shipment, calculation_date, triggered_by, trigger_reason
- [ ] Add fields: calculation_details, previous_total, new_total
- [ ] Set up auto-naming (LOG-{####})
- [ ] Add permissions (read-only for most users)
- [ ] Test DocType creation

**Acceptance Criteria**:
- Log DocType exists and can record calculations
- Auto-naming works
- Proper permissions are set

---

### Task 1.6: Enhance Ocean Shipment DocType
**Priority**: High  
**Estimated Time**: 3 hours  
**Dependencies**: Tasks 1.1, 1.2

**Subtasks**:
- [ ] Add `items` child table field (Shipment Item)
- [ ] Add `cost_components` child table field (Cost Component)
- [ ] Add cost summary fields: total_freight, total_insurance, total_customs_duty, total_cha_fees, total_port_charges, total_landed_cost
- [ ] Add allocation method fields: freight_allocation_method, cha_allocation_method, port_allocation_method
- [ ] Add integration fields: landed_cost_voucher, auto_calculate_landed_cost
- [ ] Add base_currency field
- [ ] Create new section "Landed Cost Automation" in form
- [ ] Arrange fields in logical groups
- [ ] Test field additions and form layout

**Acceptance Criteria**:
- Ocean Shipment has all new fields
- Child tables are properly linked
- Form layout is user-friendly

---

## Phase 2: Calculation Engine - Core Algorithms

### Task 2.1: Implement Currency Conversion Utility
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.6

**Subtasks**:
- [ ] Create `landed_cost_utils.py` module
- [ ] Implement `convert_to_base_currency(amount, from_currency, to_currency, date)` function
- [ ] Integrate with ERPNext's exchange rate system
- [ ] Handle missing exchange rate scenarios
- [ ] Add error handling and logging
- [ ] Write unit tests

**Acceptance Criteria**:
- Currency conversion works correctly
- Uses ERPNext exchange rates
- Handles edge cases gracefully

---

### Task 2.2: Implement Weight-Based Allocation Algorithm
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.6

**Subtasks**:
- [ ] Create `allocation_algorithms.py` module
- [ ] Implement `allocate_by_weight(total_cost, items, target_field)` function
- [ ] Handle zero total weight scenario
- [ ] Add rounding logic to prevent allocation mismatches
- [ ] Write unit tests with various scenarios
- [ ] Document algorithm with examples

**Acceptance Criteria**:
- Weight-based allocation distributes costs correctly
- Sum of allocated costs equals total cost
- Handles edge cases (zero weight, single item)

---

### Task 2.3: Implement Volume-Based Allocation Algorithm
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 2.2

**Subtasks**:
- [ ] Implement `allocate_by_volume(total_cost, items, target_field)` function
- [ ] Handle zero total volume scenario
- [ ] Add rounding logic
- [ ] Write unit tests
- [ ] Document algorithm

**Acceptance Criteria**:
- Volume-based allocation works correctly
- Proper handling of edge cases
- Tests pass

---

### Task 2.4: Implement Value-Based Allocation Algorithm
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 2.2

**Subtasks**:
- [ ] Implement `allocate_by_value(total_cost, items, target_field)` function
- [ ] Handle zero total value scenario
- [ ] Add rounding logic
- [ ] Write unit tests
- [ ] Document algorithm

**Acceptance Criteria**:
- Value-based allocation works correctly
- Proper handling of edge cases
- Tests pass

---

### Task 2.5: Implement Equal Distribution Algorithm
**Priority**: Medium  
**Estimated Time**: 1 hour  
**Dependencies**: Task 2.2

**Subtasks**:
- [ ] Implement `allocate_equally(total_cost, items, target_field)` function
- [ ] Handle rounding for uneven divisions
- [ ] Write unit tests
- [ ] Document algorithm

**Acceptance Criteria**:
- Equal distribution works correctly
- Rounding handled properly
- Tests pass

---

### Task 2.6: Implement HS Code Duty Rate Lookup
**Priority**: High  
**Estimated Time**: 3 hours  
**Dependencies**: Tasks 1.3, 1.4

**Subtasks**:
- [ ] Create `hs_code_utils.py` module
- [ ] Implement `get_duty_rate(hs_code, origin_country, dest_country, date)` function
- [ ] Query duty rates with date range validation
- [ ] Handle missing HS code scenarios
- [ ] Handle missing duty rate scenarios
- [ ] Add caching for performance
- [ ] Write unit tests
- [ ] Document function

**Acceptance Criteria**:
- Duty rate lookup returns correct rate for date
- Handles missing data gracefully
- Caching improves performance

---

### Task 2.7: Implement Customs Duty Calculator
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 2.6

**Subtasks**:
- [ ] Implement `calculate_customs_duty(item, origin_country, dest_country, date)` function
- [ ] Calculate duty as customs_value * duty_rate
- [ ] Handle items without HS codes
- [ ] Add validation for customs value
- [ ] Write unit tests
- [ ] Document function

**Acceptance Criteria**:
- Customs duty calculated correctly
- Items without HS codes flagged
- Tests pass

---

### Task 2.8: Implement Main Calculation Orchestrator
**Priority**: High  
**Estimated Time**: 4 hours  
**Dependencies**: Tasks 2.1-2.7

**Subtasks**:
- [ ] Create `LandedCostCalculator` class in `landed_cost_calculator.py`
- [ ] Implement `__init__(shipment)` method
- [ ] Implement `convert_currencies()` method
- [ ] Implement `calculate_customs_duties()` method
- [ ] Implement `allocate_freight()` method
- [ ] Implement `allocate_insurance()` method
- [ ] Implement `allocate_cha_fees()` method
- [ ] Implement `allocate_port_charges()` method
- [ ] Implement `calculate_total_landed_cost()` method
- [ ] Implement `update_shipment_totals()` method
- [ ] Implement `calculate_all()` orchestrator method
- [ ] Add error handling and validation
- [ ] Write integration tests
- [ ] Document class and methods

**Acceptance Criteria**:
- Calculator orchestrates all calculation steps
- All costs are allocated correctly
- Total landed cost is accurate
- Integration tests pass

---

## Phase 3: User Interface & Interaction

### Task 3.1: Design Shipment Items Table UI
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.6

**Subtasks**:
- [ ] Configure grid columns for Shipment Item table
- [ ] Set up editable grid with inline editing
- [ ] Add computed field displays (total_weight, total_landed_cost)
- [ ] Add color coding for items missing HS codes
- [ ] Configure column widths and visibility
- [ ] Test grid functionality

**Acceptance Criteria**:
- Items table is easy to use
- Computed fields update in real-time
- Visual indicators for missing data

---

### Task 3.2: Design Cost Components Table UI
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.6

**Subtasks**:
- [ ] Configure grid columns for Cost Component table
- [ ] Set up editable grid
- [ ] Add currency selector with exchange rate display
- [ ] Add estimated vs actual cost indicators
- [ ] Configure column widths
- [ ] Test grid functionality

**Acceptance Criteria**:
- Cost components table is intuitive
- Currency conversion visible
- Easy to distinguish estimated vs actual

---

### Task 3.3: Create Landed Cost Settings Section
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.6

**Subtasks**:
- [ ] Add "Landed Cost Settings" section to form
- [ ] Add allocation method dropdowns with descriptions
- [ ] Add "Auto Calculate" checkbox
- [ ] Add "Calculate Landed Cost" button
- [ ] Add "Create Landed Cost Voucher" button
- [ ] Style section for visibility
- [ ] Test UI elements

**Acceptance Criteria**:
- Settings section is clear and accessible
- Buttons are properly positioned
- Tooltips explain allocation methods

---

### Task 3.4: Create Landed Cost Summary Section
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.6

**Subtasks**:
- [ ] Add "Landed Cost Summary" section to form
- [ ] Display total for each cost type (read-only)
- [ ] Display grand total landed cost
- [ ] Add visual formatting (borders, bold totals)
- [ ] Make section collapsible
- [ ] Test summary updates

**Acceptance Criteria**:
- Summary displays all cost totals
- Updates automatically after calculation
- Visually distinct and easy to read

---

### Task 3.5: Create Item-Level Landed Cost Detail View
**Priority**: Medium  
**Estimated Time**: 3 hours  
**Dependencies**: Task 3.1

**Subtasks**:
- [ ] Create custom dialog for item landed cost breakdown
- [ ] Show all cost components with allocation percentages
- [ ] Display calculation formulas
- [ ] Add "View Breakdown" button to each item row
- [ ] Style dialog for clarity
- [ ] Test dialog functionality

**Acceptance Criteria**:
- Dialog shows complete cost breakdown
- Allocation logic is transparent
- Easy to access from item row

---

### Task 3.6: Add Validation Messages and Warnings
**Priority**: Medium  
**Estimated Time**: 2 hours  
**Dependencies**: Task 1.6

**Subtasks**:
- [ ] Add validation for missing item weights/volumes
- [ ] Add warning for items without HS codes
- [ ] Add warning for missing exchange rates
- [ ] Add validation for negative costs
- [ ] Display validation messages in form
- [ ] Test all validation scenarios

**Acceptance Criteria**:
- Users see clear validation messages
- Cannot save with critical errors
- Warnings don't block save but inform user

---

## Phase 4: API & Server-Side Logic

### Task 4.1: Create Calculate Landed Cost API Endpoint
**Priority**: High  
**Estimated Time**: 2 hours  
**Dependencies**: Task 2.8

**Subtasks**:
- [ ] Create `api/landed_cost.py` module
- [ ] Implement `@frappe.whitelist() calculate_landed_cost(shipment_name)` function
- [ ] Add permission checks
- [ ] Call LandedCostCalculator
- [ ] Return updated shipment data
- [ ] Add error handling
- [ ] Write API tests
- [ ] Document endpoint

**Acceptance Criteria**:
- API endpoint triggers calculation
- Returns updated shipment
- Proper error handling
- Tests pass

---

### Task 4.2: Create Get Duty Rate API Endpoint
**Priority**: High  
**Estimated Time**: 1.5 hours  
**Dependencies**: Task 2.6

**Subtasks**:
- [ ] Implement `@frappe.whitelist() get_duty_rate(hs_code, origin, dest, date)` function
- [ ] Add permission checks
- [ ] Return duty rate with metadata
- [ ] Handle missing data
- [ ] Write API tests
- [ ] Document endpoint

**Acceptance Criteria**:
- API returns correct duty rate
- Handles missing data gracefully
- Tests pass

---

### Task 4.3: Create Landed Cost Voucher Integration API
**Priority**: High  
**Estimated Time**: 4 hours  
**Dependencies**: Task 2.8

**Subtasks**:
- [ ] Implement `create_landed_cost_voucher_from_shipment(shipment_name)` function
- [ ] Map shipment items to voucher items
- [ ] Map cost components to voucher taxes
- [ ] Link voucher back to shipment
- [ ] Handle voucher updates (if already exists)
- [ ] Add validation before voucher creation
- [ ] Write integration tests
- [ ] Document function

**Acceptance Criteria**:
- Voucher created correctly from shipment
- All costs mapped properly
- Bidirectional linking works
- Tests pass

---

### Task 4.4: Implement Auto-Calculate on Save Hook
**Priority**: Medium  
**Estimated Time**: 2 hours  
**Dependencies**: Tasks 2.8, 4.1

**Subtasks**:
- [ ] Add `before_save` hook to Ocean Shipment
- [ ] Check if auto_calculate_landed_cost is enabled
- [ ] Trigger calculation if cost components or items changed
- [ ] Update totals
- [ ] Add logging
- [ ] Test hook behavior

**Acceptance Criteria**:
- Auto-calculation triggers on save when enabled
- Only recalculates when necessary
- Performance is acceptable

---

### Task 4.5: Implement Calculation Logging
**Priority**: Medium  
**Estimated Time**: 2 hours  
**Dependencies**: Tasks 1.5, 2.8

**Subtasks**:
- [ ] Add logging to LandedCostCalculator
- [ ] Create log entry for each calculation
- [ ] Record trigger reason and user
- [ ] Store calculation details (JSON)
- [ ] Record before/after totals
- [ ] Test logging functionality

**Acceptance Criteria**:
- All calculations are logged
- Log entries contain complete information
- Audit trail is maintained

---

## Phase 5: Integration & Testing

### Task 5.1: Test End-to-End Calculation Flow
**Priority**: High  
**Estimated Time**: 4 hours  
**Dependencies**: All Phase 2 and 4 tasks

**Subtasks**:
- [ ] Create test shipment with multiple items
- [ ] Add various cost components
- [ ] Test weight-based allocation
- [ ] Test volume-based allocation
- [ ] Test value-based allocation
- [ ] Verify customs duty calculation
- [ ] Verify total landed cost
- [ ] Test with different currencies
- [ ] Document test cases

**Acceptance Criteria**:
- All allocation methods work correctly
- Customs duties calculated accurately
- Multi-currency handling works
- All test cases pass

---

### Task 5.2: Test Landed Cost Voucher Integration
**Priority**: High  
**Estimated Time**: 3 hours  
**Dependencies**: Task 4.3

**Subtasks**:
- [ ] Create shipment and calculate costs
- [ ] Generate Landed Cost Voucher
- [ ] Verify voucher items match shipment items
- [ ] Verify voucher taxes match cost components
- [ ] Submit voucher and check inventory valuation
- [ ] Cancel voucher and verify reversal
- [ ] Test voucher update scenario
- [ ] Document test cases

**Acceptance Criteria**:
- Voucher creation works correctly
- Inventory valuation updates properly
- Cancellation reverses changes
- All test cases pass

---

### Task 5.3: Test Edge Cases and Error Handling
**Priority**: High  
**Estimated Time**: 3 hours  
**Dependencies**: All Phase 2 and 4 tasks

**Subtasks**:
- [ ] Test with zero-weight items
- [ ] Test with missing HS codes
- [ ] Test with missing exchange rates
- [ ] Test with single-item shipment
- [ ] Test with no cost components
- [ ] Test with negative values (should fail)
- [ ] Test with very large numbers
- [ ] Verify error messages are clear
- [ ] Document edge cases

**Acceptance Criteria**:
- All edge cases handled gracefully
- Error messages are user-friendly
- System doesn't crash
- Data integrity maintained

---

### Task 5.4: Performance Testing with Large Shipments
**Priority**: Medium  
**Estimated Time**: 2 hours  
**Dependencies**: Task 2.8

**Subtasks**:
- [ ] Create test shipment with 100+ items
- [ ] Measure calculation time
- [ ] Identify performance bottlenecks
- [ ] Optimize slow operations
- [ ] Add progress indicators if needed
- [ ] Consider async processing for large shipments
- [ ] Document performance characteristics

**Acceptance Criteria**:
- Calculation completes in reasonable time (<5 seconds for 100 items)
- No timeout errors
- User experience is acceptable

---

## Phase 6: Data Setup & Configuration

### Task 6.1: Create HS Code Import Utility
**Priority**: High  
**Estimated Time**: 3 hours  
**Dependencies**: Tasks 1.3, 1.4

**Subtasks**:
- [ ] Create `import_hs_codes.py` script
- [ ] Support CSV import format
- [ ] Validate HS code format
- [ ] Handle duplicate codes
- [ ] Import duty rates with country mappings
- [ ] Add progress logging
- [ ] Create sample HS code data file
- [ ] Test import with sample data
- [ ] Document import process

**Acceptance Criteria**:
- Import script works correctly
- Can import hundreds of HS codes
- Validation prevents bad data
- Documentation is clear

---

### Task 6.2: Create Default Allocation Method Configuration
**Priority**: Medium  
**Estimated Time**: 1 hour  
**Dependencies**: Task 1.6

**Subtasks**:
- [ ] Add company-level settings for default allocation methods
- [ ] Create configuration UI or use Custom Settings
- [ ] Set sensible defaults (Freight: Weight, Insurance: Value, etc.)
- [ ] Test configuration persistence
- [ ] Document configuration options

**Acceptance Criteria**:
- Default allocation methods can be configured
- Defaults apply to new shipments
- Configuration is persistent

---

### Task 6.3: Create Sample Data for Testing
**Priority**: Medium  
**Estimated Time**: 2 hours  
**Dependencies**: Tasks 1.3, 1.4

**Subtasks**:
- [ ] Create sample HS codes (20-30 common codes)
- [ ] Add duty rates for major countries
- [ ] Create sample shipment with realistic data
- [ ] Create sample cost components
- [ ] Document sample data
- [ ] Provide import script for sample data

**Acceptance Criteria**:
- Sample data is realistic
- Covers common scenarios
- Easy to import for testing/demo

---

## Phase 7: Documentation & Training

### Task 7.1: Create User Guide
**Priority**: High  
**Estimated Time**: 4 hours  
**Dependencies**: All implementation tasks

**Subtasks**:
- [ ] Write "Getting Started" section
- [ ] Document how to add shipment items
- [ ] Document how to add cost components
- [ ] Explain allocation methods with examples
- [ ] Document how to calculate landed costs
- [ ] Document how to create Landed Cost Voucher
- [ ] Add screenshots and examples
- [ ] Create troubleshooting section
- [ ] Review and edit for clarity

**Acceptance Criteria**:
- User guide is comprehensive
- Includes practical examples
- Easy to follow for new users

---

### Task 7.2: Create Administrator Guide
**Priority**: Medium  
**Estimated Time**: 3 hours  
**Dependencies**: All implementation tasks

**Subtasks**:
- [ ] Document HS code management
- [ ] Document duty rate updates
- [ ] Explain allocation method configuration
- [ ] Document permission setup
- [ ] Explain audit trail and logging
- [ ] Add troubleshooting for admins
- [ ] Document backup and maintenance

**Acceptance Criteria**:
- Admin guide covers all admin tasks
- Clear instructions for configuration
- Troubleshooting section is helpful

---

### Task 7.3: Create API Documentation
**Priority**: Medium  
**Estimated Time**: 2 hours  
**Dependencies**: All Phase 4 tasks

**Subtasks**:
- [ ] Document all API endpoints
- [ ] Provide request/response examples
- [ ] Document error codes and messages
- [ ] Add authentication requirements
- [ ] Create Postman collection or similar
- [ ] Add integration examples

**Acceptance Criteria**:
- API documentation is complete
- Examples are working
- Easy for developers to integrate

---

### Task 7.4: Create Video Tutorial
**Priority**: Low  
**Estimated Time**: 4 hours  
**Dependencies**: Task 7.1

**Subtasks**:
- [ ] Script tutorial content
- [ ] Record screen capture
- [ ] Demonstrate creating shipment with landed costs
- [ ] Show calculation process
- [ ] Show Landed Cost Voucher creation
- [ ] Add voiceover or captions
- [ ] Edit and publish video

**Acceptance Criteria**:
- Video is clear and professional
- Covers key workflows
- Accessible to users

---

## Phase 8: Deployment & Rollout

### Task 8.1: Create Installation Script
**Priority**: High  
**Estimated Time**: 3 hours  
**Dependencies**: All Phase 1 tasks

**Subtasks**:
- [ ] Create `install_landed_cost_automation.py` script
- [ ] Check for existing DocTypes
- [ ] Create all DocTypes in correct order
- [ ] Add default allocation methods
- [ ] Create sample HS codes (optional)
- [ ] Add success/failure logging
- [ ] Test installation on clean system
- [ ] Document installation process

**Acceptance Criteria**:
- Installation script works on clean ERPNext
- Handles existing installations gracefully
- Clear success/failure messages

---

### Task 8.2: Create Migration Script for Existing Shipments
**Priority**: Medium  
**Estimated Time**: 2 hours  
**Dependencies**: Task 8.1

**Subtasks**:
- [ ] Create migration script for existing Ocean Shipments
- [ ] Add empty items and cost_components tables
- [ ] Preserve existing data
- [ ] Add logging for migration
- [ ] Test on sample data
- [ ] Document migration process

**Acceptance Criteria**:
- Existing shipments are not broken
- New fields are added
- No data loss

---

### Task 8.3: Create Rollback Script
**Priority**: Medium  
**Estimated Time**: 2 hours  
**Dependencies**: Task 8.1

**Subtasks**:
- [ ] Create rollback script to remove landed cost features
- [ ] Remove added fields from Ocean Shipment
- [ ] Optionally delete new DocTypes
- [ ] Preserve data if possible
- [ ] Test rollback process
- [ ] Document rollback procedure

**Acceptance Criteria**:
- Rollback script works correctly
- System returns to previous state
- Critical data is preserved

---

### Task 8.4: Conduct User Acceptance Testing (UAT)
**Priority**: High  
**Estimated Time**: 8 hours  
**Dependencies**: All implementation tasks

**Subtasks**:
- [ ] Prepare UAT environment
- [ ] Create UAT test cases
- [ ] Train UAT users
- [ ] Conduct UAT sessions
- [ ] Collect feedback
- [ ] Document issues and enhancement requests
- [ ] Prioritize fixes
- [ ] Implement critical fixes
- [ ] Re-test

**Acceptance Criteria**:
- UAT users can complete all workflows
- Critical issues are resolved
- Users are satisfied with functionality

---

### Task 8.5: Production Deployment
**Priority**: High  
**Estimated Time**: 4 hours  
**Dependencies**: Task 8.4

**Subtasks**:
- [ ] Create deployment checklist
- [ ] Backup production database
- [ ] Schedule maintenance window
- [ ] Run installation script on production
- [ ] Verify all DocTypes created
- [ ] Test basic functionality
- [ ] Import HS codes and duty rates
- [ ] Configure default allocation methods
- [ ] Train support team
- [ ] Monitor for issues
- [ ] Document deployment

**Acceptance Criteria**:
- System deployed successfully
- All features working in production
- No critical issues
- Users can access new features

---

## Summary

**Total Estimated Time**: ~110 hours (approximately 3-4 weeks for one developer)

**Critical Path**:
1. Phase 1: DocType Creation (15 hours)
2. Phase 2: Calculation Engine (18 hours)
3. Phase 4: API & Server Logic (11.5 hours)
4. Phase 5: Integration Testing (12 hours)
5. Phase 8: Deployment (19 hours)

**Recommended Team**:
- 1 Backend Developer (Frappe/ERPNext expert)
- 1 Frontend Developer (UI/UX)
- 1 QA Engineer (Testing)
- 1 Technical Writer (Documentation)

**Key Milestones**:
- Week 1: Complete Phase 1 (Foundation)
- Week 2: Complete Phase 2 (Calculation Engine)
- Week 3: Complete Phases 3-5 (UI, API, Testing)
- Week 4: Complete Phases 6-8 (Data Setup, Documentation, Deployment)
