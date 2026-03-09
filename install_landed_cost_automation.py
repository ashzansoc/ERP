#!/usr/bin/env python3
"""
Landed Cost Automation Installation Script
Installs all DocTypes and configurations for automated landed cost calculation
"""
import sys
import frappe

def init_frappe():
    """Initialize Frappe connection"""
    frappe.init(site='localhost')
    frappe.connect()
    frappe.set_user('Administrator')

def create_cost_component_doctype():
    """Create Cost Component child DocType"""
    if frappe.db.exists("DocType", "Cost Component"):
        print("ℹ️  Cost Component already exists")
        return
    
    print("📦 Creating Cost Component DocType...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Cost Component",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "editable_grid": 1,
        "track_changes": 1,
        "fields": [
            {"fieldname": "cost_type", "fieldtype": "Select", "label": "Cost Type", 
             "options": "Freight\nInsurance\nCustoms Duty\nCHA Fees\nPort Charges\nOther",
             "reqd": 1, "in_list_view": 1},
            {"fieldname": "description", "fieldtype": "Data", "label": "Description", "in_list_view": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "reqd": 1, "in_list_view": 1},
            {"fieldname": "currency", "fieldtype": "Link", "label": "Currency", "options": "Currency", 
             "default": "USD", "in_list_view": 1},
            {"fieldname": "section_break_1", "fieldtype": "Section Break"},
            {"fieldname": "exchange_rate", "fieldtype": "Float", "label": "Exchange Rate", "precision": 6},
            {"fieldname": "amount_in_base_currency", "fieldtype": "Currency", "label": "Amount in Base Currency", "read_only": 1},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "is_estimated", "fieldtype": "Check", "label": "Is Estimated", "default": 1},
            {"fieldname": "actual_amount", "fieldtype": "Currency", "label": "Actual Amount"},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "collapsible": 1, "label": "Additional Details"},
            {"fieldname": "supplier", "fieldtype": "Link", "label": "Supplier", "options": "Supplier"},
            {"fieldname": "column_break_3", "fieldtype": "Column Break"},
            {"fieldname": "invoice_reference", "fieldtype": "Data", "label": "Invoice Reference"},
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Cost Component DocType created")

def create_shipment_item_doctype():
    """Create Shipment Item child DocType"""
    if frappe.db.exists("DocType", "Shipment Item"):
        print("ℹ️  Shipment Item already exists")
        return
    
    print("📦 Creating Shipment Item DocType...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Shipment Item",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "editable_grid": 1,
        "track_changes": 1,
        "fields": [
            # Item Details
            {"fieldname": "item_section", "fieldtype": "Section Break", "label": "Item Details"},
            {"fieldname": "item_code", "fieldtype": "Link", "label": "Item Code", "options": "Item", 
             "reqd": 1, "in_list_view": 1},
            {"fieldname": "item_name", "fieldtype": "Data", "label": "Item Name", "fetch_from": "item_code.item_name"},
            {"fieldname": "description", "fieldtype": "Text Editor", "label": "Description"},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "quantity", "fieldtype": "Float", "label": "Quantity", "reqd": 1, "in_list_view": 1},
            {"fieldname": "uom", "fieldtype": "Link", "label": "UOM", "options": "UOM", 
             "fetch_from": "item_code.stock_uom"},
            
            # Physical Attributes
            {"fieldname": "physical_section", "fieldtype": "Section Break", "label": "Physical Attributes"},
            {"fieldname": "weight_per_unit", "fieldtype": "Float", "label": "Weight per Unit (KG)", "precision": 3},
            {"fieldname": "total_weight", "fieldtype": "Float", "label": "Total Weight (KG)", "read_only": 1, "in_list_view": 1},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "volume_per_unit", "fieldtype": "Float", "label": "Volume per Unit (CBM)", "precision": 3},
            {"fieldname": "total_volume", "fieldtype": "Float", "label": "Total Volume (CBM)", "read_only": 1},
            
            # Values
            {"fieldname": "value_section", "fieldtype": "Section Break", "label": "Values"},
            {"fieldname": "base_cost", "fieldtype": "Currency", "label": "Base Cost", "reqd": 1, "in_list_view": 1},
            {"fieldname": "column_break_3", "fieldtype": "Column Break"},
            {"fieldname": "customs_value", "fieldtype": "Currency", "label": "Customs Value"},
            {"fieldname": "declared_value", "fieldtype": "Currency", "label": "Declared Value (for Insurance)"},
            
            # HS Code & Duty
            {"fieldname": "hs_section", "fieldtype": "Section Break", "label": "HS Code & Customs Duty"},
            {"fieldname": "hs_code", "fieldtype": "Link", "label": "HS Code", "options": "HS Code"},
            {"fieldname": "duty_rate", "fieldtype": "Percent", "label": "Duty Rate (%)", "read_only": 1},
            {"fieldname": "column_break_4", "fieldtype": "Column Break"},
            {"fieldname": "customs_duty", "fieldtype": "Currency", "label": "Customs Duty", "read_only": 1},
            
            # Allocated Costs
            {"fieldname": "allocated_section", "fieldtype": "Section Break", "label": "Allocated Costs"},
            {"fieldname": "allocated_freight", "fieldtype": "Currency", "label": "Allocated Freight", "read_only": 1},
            {"fieldname": "allocated_insurance", "fieldtype": "Currency", "label": "Allocated Insurance", "read_only": 1},
            {"fieldname": "column_break_5", "fieldtype": "Column Break"},
            {"fieldname": "allocated_cha_fees", "fieldtype": "Currency", "label": "Allocated CHA Fees", "read_only": 1},
            {"fieldname": "allocated_port_charges", "fieldtype": "Currency", "label": "Allocated Port Charges", "read_only": 1},
            
            # Landed Cost
            {"fieldname": "landed_cost_section", "fieldtype": "Section Break", "label": "Landed Cost"},
            {"fieldname": "total_landed_cost", "fieldtype": "Currency", "label": "Total Landed Cost", 
             "read_only": 1, "in_list_view": 1, "bold": 1},
            {"fieldname": "column_break_6", "fieldtype": "Column Break"},
            {"fieldname": "unit_landed_cost", "fieldtype": "Currency", "label": "Unit Landed Cost", "read_only": 1},
            
            # Container Reference
            {"fieldname": "container_section", "fieldtype": "Section Break", "label": "Container"},
            {"fieldname": "container_no", "fieldtype": "Data", "label": "Container No"},
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Shipment Item DocType created")

def create_hs_code_duty_rate_doctype():
    """Create HS Code Duty Rate child DocType"""
    if frappe.db.exists("DocType", "HS Code Duty Rate"):
        print("ℹ️  HS Code Duty Rate already exists")
        return
    
    print("📦 Creating HS Code Duty Rate DocType...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "HS Code Duty Rate",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {"fieldname": "country_of_origin", "fieldtype": "Link", "label": "Country of Origin", 
             "options": "Country", "in_list_view": 1},
            {"fieldname": "destination_country", "fieldtype": "Link", "label": "Destination Country", 
             "options": "Country", "in_list_view": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "duty_rate", "fieldtype": "Percent", "label": "Duty Rate (%)", 
             "reqd": 1, "in_list_view": 1},
            {"fieldname": "additional_duty", "fieldtype": "Percent", "label": "Additional Duty (%)"},
            {"fieldname": "section_break_1", "fieldtype": "Section Break"},
            {"fieldname": "valid_from", "fieldtype": "Date", "label": "Valid From", "reqd": 1},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "valid_to", "fieldtype": "Date", "label": "Valid To"},
            {"fieldname": "section_break_2", "fieldtype": "Section Break"},
            {"fieldname": "notes", "fieldtype": "Text", "label": "Notes"},
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ HS Code Duty Rate DocType created")

def create_hs_code_doctype():
    """Create HS Code master DocType"""
    if frappe.db.exists("DocType", "HS Code"):
        print("ℹ️  HS Code already exists")
        return
    
    print("📦 Creating HS Code DocType...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "HS Code",
        "module": "Stock",
        "custom": 1,
        "autoname": "field:hs_code",
        "naming_rule": "By fieldname",
        "track_changes": 1,
        "fields": [
            {"fieldname": "hs_code", "fieldtype": "Data", "label": "HS Code", "reqd": 1, "unique": 1},
            {"fieldname": "description", "fieldtype": "Text", "label": "Description", "reqd": 1},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Duty Rates"},
            {"fieldname": "duty_rates", "fieldtype": "Table", "label": "Duty Rates", 
             "options": "HS Code Duty Rate"},
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Stock Manager", "read": 1, "write": 1, "create": 1},
            {"role": "Stock User", "read": 1},
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ HS Code DocType created")

def create_landed_cost_calculation_log_doctype():
    """Create Landed Cost Calculation Log DocType"""
    if frappe.db.exists("DocType", "Landed Cost Calculation Log"):
        print("ℹ️  Landed Cost Calculation Log already exists")
        return
    
    print("📦 Creating Landed Cost Calculation Log DocType...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Landed Cost Calculation Log",
        "module": "Stock",
        "custom": 1,
        "autoname": "format:LCCLOG-{####}",
        "naming_rule": "Expression",
        "track_changes": 1,
        "fields": [
            {"fieldname": "shipment", "fieldtype": "Link", "label": "Shipment", 
             "options": "Ocean Shipment", "reqd": 1, "in_list_view": 1},
            {"fieldname": "calculation_date", "fieldtype": "Datetime", "label": "Calculation Date", 
             "default": "Now", "reqd": 1, "in_list_view": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "triggered_by", "fieldtype": "Link", "label": "Triggered By", 
             "options": "User", "default": "user"},
            {"fieldname": "trigger_reason", "fieldtype": "Select", "label": "Trigger Reason",
             "options": "Manual\nCost Component Changed\nItem Changed\nAllocation Method Changed\nAuto Calculate on Save",
             "in_list_view": 1},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Calculation Details"},
            {"fieldname": "calculation_details", "fieldtype": "Long Text", "label": "Calculation Details"},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Totals"},
            {"fieldname": "previous_total", "fieldtype": "Currency", "label": "Previous Total"},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "new_total", "fieldtype": "Currency", "label": "New Total"},
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Stock Manager", "read": 1},
            {"role": "Stock User", "read": 1},
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Landed Cost Calculation Log DocType created")

def enhance_ocean_shipment_doctype():
    """Add landed cost fields to Ocean Shipment DocType"""
    if not frappe.db.exists("DocType", "Ocean Shipment"):
        print("❌ Ocean Shipment DocType not found. Please install Ocean Shipment module first.")
        return False
    
    print("🔧 Enhancing Ocean Shipment DocType with Landed Cost fields...")
    
    # Get the Ocean Shipment DocType
    doc = frappe.get_doc("DocType", "Ocean Shipment")
    
    # Check if already enhanced
    existing_fields = [f.fieldname for f in doc.fields]
    if "items" in existing_fields:
        print("ℹ️  Ocean Shipment already enhanced with Landed Cost fields")
        return True
    
    # Add new fields
    new_fields = [
        # Shipment Items Section
        {"fieldname": "items_section", "fieldtype": "Section Break", "label": "Shipment Items", "insert_after": "containers"},
        {"fieldname": "items", "fieldtype": "Table", "label": "Items", "options": "Shipment Item", "insert_after": "items_section"},
        
        # Cost Components Section
        {"fieldname": "cost_components_section", "fieldtype": "Section Break", "label": "Cost Components", "insert_after": "items"},
        {"fieldname": "cost_components", "fieldtype": "Table", "label": "Cost Components", "options": "Cost Component", "insert_after": "cost_components_section"},
        
        # Landed Cost Settings Section
        {"fieldname": "landed_cost_settings_section", "fieldtype": "Section Break", "label": "Landed Cost Settings", "insert_after": "cost_components"},
        {"fieldname": "auto_calculate_landed_cost", "fieldtype": "Check", "label": "Auto Calculate Landed Cost", "default": 1, "insert_after": "landed_cost_settings_section"},
        {"fieldname": "column_break_lc1", "fieldtype": "Column Break", "insert_after": "auto_calculate_landed_cost"},
        {"fieldname": "base_currency", "fieldtype": "Link", "label": "Base Currency", "options": "Currency", "default": "USD", "insert_after": "column_break_lc1"},
        
        {"fieldname": "allocation_methods_section", "fieldtype": "Section Break", "label": "Allocation Methods", "collapsible": 1, "insert_after": "base_currency"},
        {"fieldname": "freight_allocation_method", "fieldtype": "Select", "label": "Freight Allocation Method", 
         "options": "Weight\nVolume\nValue", "default": "Weight", "insert_after": "allocation_methods_section"},
        {"fieldname": "column_break_lc2", "fieldtype": "Column Break", "insert_after": "freight_allocation_method"},
        {"fieldname": "cha_allocation_method", "fieldtype": "Select", "label": "CHA Allocation Method",
         "options": "Customs Value\nEqual", "default": "Customs Value", "insert_after": "column_break_lc2"},
        {"fieldname": "column_break_lc3", "fieldtype": "Column Break", "insert_after": "cha_allocation_method"},
        {"fieldname": "port_allocation_method", "fieldtype": "Select", "label": "Port Allocation Method",
         "options": "Weight\nVolume", "default": "Weight", "insert_after": "column_break_lc3"},
        
        # Landed Cost Summary Section
        {"fieldname": "landed_cost_summary_section", "fieldtype": "Section Break", "label": "Landed Cost Summary", "insert_after": "port_allocation_method"},
        {"fieldname": "total_freight", "fieldtype": "Currency", "label": "Total Freight", "read_only": 1, "insert_after": "landed_cost_summary_section"},
        {"fieldname": "total_insurance", "fieldtype": "Currency", "label": "Total Insurance", "read_only": 1, "insert_after": "total_freight"},
        {"fieldname": "total_customs_duty", "fieldtype": "Currency", "label": "Total Customs Duty", "read_only": 1, "insert_after": "total_insurance"},
        {"fieldname": "column_break_lc4", "fieldtype": "Column Break", "insert_after": "total_customs_duty"},
        {"fieldname": "total_cha_fees", "fieldtype": "Currency", "label": "Total CHA Fees", "read_only": 1, "insert_after": "column_break_lc4"},
        {"fieldname": "total_port_charges", "fieldtype": "Currency", "label": "Total Port Charges", "read_only": 1, "insert_after": "total_cha_fees"},
        {"fieldname": "total_landed_cost", "fieldtype": "Currency", "label": "Total Landed Cost", "read_only": 1, "bold": 1, "insert_after": "total_port_charges"},
        
        # Integration Section
        {"fieldname": "integration_section", "fieldtype": "Section Break", "label": "Integration", "collapsible": 1, "insert_after": "total_landed_cost"},
        {"fieldname": "landed_cost_voucher", "fieldtype": "Link", "label": "Landed Cost Voucher", 
         "options": "Landed Cost Voucher", "read_only": 1, "insert_after": "integration_section"},
    ]
    
    for field in new_fields:
        doc.append("fields", field)
    
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Ocean Shipment DocType enhanced successfully")
    return True

def create_sample_hs_codes():
    """Create sample HS codes for testing"""
    print("📝 Creating sample HS codes...")
    
    sample_codes = [
        {"hs_code": "8517.62", "description": "Machines for reception, conversion and transmission of voice, images or other data"},
        {"hs_code": "8471.30", "description": "Portable automatic data processing machines, weighing not more than 10 kg"},
        {"hs_code": "8528.72", "description": "Reception apparatus for television, color"},
        {"hs_code": "6203.42", "description": "Men's or boys' trousers, breeches and shorts, of cotton"},
        {"hs_code": "6204.62", "description": "Women's or girls' trousers, breeches and shorts, of cotton"},
    ]
    
    for code_data in sample_codes:
        if not frappe.db.exists("HS Code", code_data["hs_code"]):
            hs_code = frappe.get_doc({
                "doctype": "HS Code",
                "hs_code": code_data["hs_code"],
                "description": code_data["description"],
                "duty_rates": [
                    {
                        "country_of_origin": "China",
                        "destination_country": "United States",
                        "duty_rate": 10.0,
                        "valid_from": "2024-01-01",
                    },
                    {
                        "country_of_origin": "India",
                        "destination_country": "United States",
                        "duty_rate": 8.0,
                        "valid_from": "2024-01-01",
                    }
                ]
            })
            hs_code.insert(ignore_permissions=True)
    
    frappe.db.commit()
    print(f"✅ Created {len(sample_codes)} sample HS codes")

def main():
    """Main installation function"""
    print("\n" + "="*60)
    print("🚢 Landed Cost Automation Installation")
    print("="*60 + "\n")
    
    try:
        init_frappe()
        
        # Phase 1: Create child DocTypes first
        print("\n📦 Phase 1: Creating Child DocTypes...")
        create_cost_component_doctype()
        create_shipment_item_doctype()
        create_hs_code_duty_rate_doctype()
        
        # Phase 2: Create master DocTypes
        print("\n📦 Phase 2: Creating Master DocTypes...")
        create_hs_code_doctype()
        create_landed_cost_calculation_log_doctype()
        
        # Phase 3: Enhance Ocean Shipment
        print("\n🔧 Phase 3: Enhancing Ocean Shipment...")
        if not enhance_ocean_shipment_doctype():
            print("\n❌ Installation failed: Ocean Shipment DocType not found")
            print("Please install Ocean Shipment module first using install_ocean_shipment.py")
            return
        
        # Phase 4: Create sample data
        print("\n📝 Phase 4: Creating Sample Data...")
        create_sample_hs_codes()
        
        # Clear cache
        frappe.clear_cache()
        
        print("\n" + "="*60)
        print("✅ Installation Complete!")
        print("="*60)
        print("\n📍 Next Steps:")
        print("1. Access Ocean Shipment: Desk → Stock → Ocean Shipment")
        print("2. Manage HS Codes: Desk → Stock → HS Code")
        print("3. View Calculation Logs: Desk → Stock → Landed Cost Calculation Log")
        print("\n💡 Features Installed:")
        print("   ✓ Shipment Items with physical attributes")
        print("   ✓ Cost Components with multi-currency support")
        print("   ✓ HS Code master with duty rates")
        print("   ✓ Automated cost allocation (Weight/Volume/Value)")
        print("   ✓ Customs duty auto-calculation")
        print("   ✓ Landed cost calculation and tracking")
        print("   ✓ Audit trail and logging")
        print("\n📚 Documentation:")
        print("   - User Guide: .kiro/specs/landed-cost-automation/requirements.md")
        print("   - Design Doc: .kiro/specs/landed-cost-automation/design.md")
        print("   - Tasks: .kiro/specs/landed-cost-automation/tasks.md")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Installation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
