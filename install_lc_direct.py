#!/usr/bin/env python3
"""
Direct installation script for Landed Cost Automation
Run with: bench --site localhost execute install_lc_direct.py
"""
import frappe

def create_cost_component():
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
    print("✅ Cost Component created")

def create_shipment_item():
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
            {"fieldname": "item_code", "fieldtype": "Link", "label": "Item Code", "options": "Item", 
             "reqd": 1, "in_list_view": 1},
            {"fieldname": "item_name", "fieldtype": "Data", "label": "Item Name", "fetch_from": "item_code.item_name"},
            {"fieldname": "quantity", "fieldtype": "Float", "label": "Quantity", "reqd": 1, "in_list_view": 1},
            {"fieldname": "uom", "fieldtype": "Link", "label": "UOM", "options": "UOM"},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "weight_per_unit", "fieldtype": "Float", "label": "Weight per Unit (KG)", "precision": 3},
            {"fieldname": "total_weight", "fieldtype": "Float", "label": "Total Weight (KG)", "read_only": 1},
            {"fieldname": "volume_per_unit", "fieldtype": "Float", "label": "Volume per Unit (CBM)", "precision": 3},
            {"fieldname": "total_volume", "fieldtype": "Float", "label": "Total Volume (CBM)", "read_only": 1},
            {"fieldname": "section_break_1", "fieldtype": "Section Break"},
            {"fieldname": "base_cost", "fieldtype": "Currency", "label": "Base Cost", "reqd": 1, "in_list_view": 1},
            {"fieldname": "customs_value", "fieldtype": "Currency", "label": "Customs Value"},
            {"fieldname": "declared_value", "fieldtype": "Currency", "label": "Declared Value"},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "hs_code", "fieldtype": "Link", "label": "HS Code", "options": "HS Code"},
            {"fieldname": "duty_rate", "fieldtype": "Percent", "label": "Duty Rate (%)", "read_only": 1},
            {"fieldname": "customs_duty", "fieldtype": "Currency", "label": "Customs Duty", "read_only": 1},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Allocated Costs"},
            {"fieldname": "allocated_freight", "fieldtype": "Currency", "label": "Allocated Freight", "read_only": 1},
            {"fieldname": "allocated_insurance", "fieldtype": "Currency", "label": "Allocated Insurance", "read_only": 1},
            {"fieldname": "column_break_3", "fieldtype": "Column Break"},
            {"fieldname": "allocated_cha_fees", "fieldtype": "Currency", "label": "Allocated CHA Fees", "read_only": 1},
            {"fieldname": "allocated_port_charges", "fieldtype": "Currency", "label": "Allocated Port Charges", "read_only": 1},
            {"fieldname": "section_break_3", "fieldtype": "Section Break", "label": "Landed Cost"},
            {"fieldname": "total_landed_cost", "fieldtype": "Currency", "label": "Total Landed Cost", 
             "read_only": 1, "in_list_view": 1, "bold": 1},
            {"fieldname": "column_break_4", "fieldtype": "Column Break"},
            {"fieldname": "unit_landed_cost", "fieldtype": "Currency", "label": "Unit Landed Cost", "read_only": 1},
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Shipment Item created")

def create_hs_code_duty_rate():
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
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ HS Code Duty Rate created")

def create_hs_code():
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
    print("✅ HS Code created")

def create_calculation_log():
    """Create Landed Cost Calculation Log DocType"""
    if frappe.db.exists("DocType", "Landed Cost Calculation Log"):
        print("ℹ️  Calculation Log already exists")
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
            {"fieldname": "section_break_1", "fieldtype": "Section Break"},
            {"fieldname": "calculation_details", "fieldtype": "Long Text", "label": "Calculation Details"},
            {"fieldname": "section_break_2", "fieldtype": "Section Break"},
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
    print("✅ Calculation Log created")

def enhance_ocean_shipment():
    """Add landed cost fields to Ocean Shipment"""
    if not frappe.db.exists("DocType", "Ocean Shipment"):
        print("❌ Ocean Shipment not found")
        return False
    
    print("🔧 Enhancing Ocean Shipment...")
    doc = frappe.get_doc("DocType", "Ocean Shipment")
    
    existing = [f.fieldname for f in doc.fields]
    if "items" in existing:
        print("ℹ️  Already enhanced")
        return True
    
    # Find insert position (after containers)
    insert_idx = 0
    for i, f in enumerate(doc.fields):
        if f.fieldname == "containers":
            insert_idx = i + 1
            break
    
    new_fields = [
        {"fieldname": "items_section", "fieldtype": "Section Break", "label": "Shipment Items"},
        {"fieldname": "items", "fieldtype": "Table", "label": "Items", "options": "Shipment Item"},
        {"fieldname": "cost_section", "fieldtype": "Section Break", "label": "Cost Components"},
        {"fieldname": "cost_components", "fieldtype": "Table", "label": "Cost Components", "options": "Cost Component"},
        {"fieldname": "lc_settings", "fieldtype": "Section Break", "label": "Landed Cost Settings"},
        {"fieldname": "auto_calculate_landed_cost", "fieldtype": "Check", "label": "Auto Calculate", "default": 1},
        {"fieldname": "base_currency", "fieldtype": "Link", "label": "Base Currency", "options": "Currency", "default": "USD"},
        {"fieldname": "column_break_lc1", "fieldtype": "Column Break"},
        {"fieldname": "freight_allocation_method", "fieldtype": "Select", "label": "Freight Allocation", 
         "options": "Weight\nVolume\nValue", "default": "Weight"},
        {"fieldname": "cha_allocation_method", "fieldtype": "Select", "label": "CHA Allocation",
         "options": "Customs Value\nEqual", "default": "Customs Value"},
        {"fieldname": "port_allocation_method", "fieldtype": "Select", "label": "Port Allocation",
         "options": "Weight\nVolume", "default": "Weight"},
        {"fieldname": "lc_summary", "fieldtype": "Section Break", "label": "Landed Cost Summary"},
        {"fieldname": "total_freight", "fieldtype": "Currency", "label": "Total Freight", "read_only": 1},
        {"fieldname": "total_insurance", "fieldtype": "Currency", "label": "Total Insurance", "read_only": 1},
        {"fieldname": "total_customs_duty", "fieldtype": "Currency", "label": "Total Customs Duty", "read_only": 1},
        {"fieldname": "column_break_lc2", "fieldtype": "Column Break"},
        {"fieldname": "total_cha_fees", "fieldtype": "Currency", "label": "Total CHA Fees", "read_only": 1},
        {"fieldname": "total_port_charges", "fieldtype": "Currency", "label": "Total Port Charges", "read_only": 1},
        {"fieldname": "total_landed_cost", "fieldtype": "Currency", "label": "Total Landed Cost", "read_only": 1, "bold": 1},
        {"fieldname": "integration_section", "fieldtype": "Section Break", "label": "Integration", "collapsible": 1},
        {"fieldname": "landed_cost_voucher", "fieldtype": "Link", "label": "Landed Cost Voucher", 
         "options": "Landed Cost Voucher", "read_only": 1},
    ]
    
    for field in new_fields:
        doc.insert(insert_idx, "fields", field)
        insert_idx += 1
    
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Ocean Shipment enhanced")
    return True

def create_sample_hs_codes():
    """Create sample HS codes"""
    print("📝 Creating sample HS codes...")
    
    samples = [
        {"hs_code": "8517.62", "description": "Telecom equipment - reception, conversion and transmission"},
        {"hs_code": "8471.30", "description": "Portable computers, weighing not more than 10 kg"},
        {"hs_code": "8528.72", "description": "Reception apparatus for television, color"},
        {"hs_code": "6203.42", "description": "Men's or boys' trousers, breeches and shorts, of cotton"},
        {"hs_code": "6204.62", "description": "Women's or girls' trousers, breeches and shorts, of cotton"},
    ]
    
    for s in samples:
        if not frappe.db.exists("HS Code", s["hs_code"]):
            hs = frappe.get_doc({
                "doctype": "HS Code",
                "hs_code": s["hs_code"],
                "description": s["description"],
                "duty_rates": [
                    {
                        "country_of_origin": "China",
                        "destination_country": "United States",
                        "duty_rate": 10.0,
                        "valid_from": "2024-01-01",
                    }
                ]
            })
            hs.insert(ignore_permissions=True)
    
    frappe.db.commit()
    print(f"✅ Created {len(samples)} sample HS codes")

def main():
    print("\n" + "="*60)
    print("🚢 Landed Cost Automation Installation")
    print("="*60 + "\n")
    
    try:
        print("Phase 1: Child DocTypes...")
        create_cost_component()
        create_shipment_item()
        create_hs_code_duty_rate()
        
        print("\nPhase 2: Master DocTypes...")
        create_hs_code()
        create_calculation_log()
        
        print("\nPhase 3: Enhance Ocean Shipment...")
        if not enhance_ocean_shipment():
            print("\n❌ Failed: Install Ocean Shipment first")
            return
        
        print("\nPhase 4: Sample Data...")
        create_sample_hs_codes()
        
        frappe.clear_cache()
        
        print("\n" + "="*60)
        print("✅ Installation Complete!")
        print("="*60)
        print("\n📍 Access: http://localhost:8080")
        print("   Desk → Stock → Ocean Shipment")
        print("   Desk → Stock → HS Code")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

main()
