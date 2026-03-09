#!/bin/bash
# Add Landed Cost fields to Ocean Shipment using Custom Fields

cd frappe_docker

echo "🔧 Adding Landed Cost fields to Ocean Shipment..."

docker-compose exec -T backend bench --site localhost console <<'PYTHON'
import frappe

def create_custom_field(dt, fieldname, label, fieldtype, options=None, default=None, read_only=0, bold=0, insert_after=None):
    """Create a custom field if it doesn't exist"""
    if not frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fieldname}):
        cf = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": dt,
            "fieldname": fieldname,
            "label": label,
            "fieldtype": fieldtype,
            "options": options,
            "default": default,
            "read_only": read_only,
            "bold": bold,
            "insert_after": insert_after
        })
        cf.insert(ignore_permissions=True)
        print(f"✅ Created: {fieldname}")
        return True
    else:
        print(f"ℹ️  Exists: {fieldname}")
        return False

print("📦 Adding fields to Ocean Shipment...")

# Shipment Items Section
create_custom_field("Ocean Shipment", "items_section", "Shipment Items", "Section Break", insert_after="containers")
create_custom_field("Ocean Shipment", "items", "Items", "Table", options="Shipment Item", insert_after="items_section")

# Cost Components Section
create_custom_field("Ocean Shipment", "cost_section", "Cost Components", "Section Break", insert_after="items")
create_custom_field("Ocean Shipment", "cost_components", "Cost Components", "Table", options="Cost Component", insert_after="cost_section")

# Landed Cost Settings Section
create_custom_field("Ocean Shipment", "lc_settings", "Landed Cost Settings", "Section Break", insert_after="cost_components")
create_custom_field("Ocean Shipment", "auto_calculate_landed_cost", "Auto Calculate Landed Cost", "Check", default=1, insert_after="lc_settings")
create_custom_field("Ocean Shipment", "base_currency", "Base Currency", "Link", options="Currency", default="USD", insert_after="auto_calculate_landed_cost")

create_custom_field("Ocean Shipment", "column_break_lc1", "", "Column Break", insert_after="base_currency")
create_custom_field("Ocean Shipment", "freight_allocation_method", "Freight Allocation Method", "Select", 
                   options="Weight\\nVolume\\nValue", default="Weight", insert_after="column_break_lc1")
create_custom_field("Ocean Shipment", "cha_allocation_method", "CHA Allocation Method", "Select",
                   options="Customs Value\\nEqual", default="Customs Value", insert_after="freight_allocation_method")
create_custom_field("Ocean Shipment", "port_allocation_method", "Port Allocation Method", "Select",
                   options="Weight\\nVolume", default="Weight", insert_after="cha_allocation_method")

# Landed Cost Summary Section
create_custom_field("Ocean Shipment", "lc_summary", "Landed Cost Summary", "Section Break", insert_after="port_allocation_method")
create_custom_field("Ocean Shipment", "total_freight", "Total Freight", "Currency", read_only=1, insert_after="lc_summary")
create_custom_field("Ocean Shipment", "total_insurance", "Total Insurance", "Currency", read_only=1, insert_after="total_freight")
create_custom_field("Ocean Shipment", "total_customs_duty", "Total Customs Duty", "Currency", read_only=1, insert_after="total_insurance")

create_custom_field("Ocean Shipment", "column_break_lc2", "", "Column Break", insert_after="total_customs_duty")
create_custom_field("Ocean Shipment", "total_cha_fees", "Total CHA Fees", "Currency", read_only=1, insert_after="column_break_lc2")
create_custom_field("Ocean Shipment", "total_port_charges", "Total Port Charges", "Currency", read_only=1, insert_after="total_cha_fees")
create_custom_field("Ocean Shipment", "total_landed_cost", "Total Landed Cost", "Currency", read_only=1, bold=1, insert_after="total_port_charges")

# Integration Section
create_custom_field("Ocean Shipment", "integration_section", "Integration", "Section Break", insert_after="total_landed_cost")
create_custom_field("Ocean Shipment", "landed_cost_voucher", "Landed Cost Voucher", "Link", 
                   options="Landed Cost Voucher", read_only=1, insert_after="integration_section")

frappe.db.commit()
print("\\n✅ All fields added to Ocean Shipment!")

PYTHON

echo ""
echo "🧹 Clearing cache..."
docker-compose exec -T backend bench --site localhost clear-cache

echo ""
echo "✅ Installation complete!"
echo "📍 Access Ocean Shipment at: http://localhost:8080"
echo "   Desk → Stock → Ocean Shipment"
echo ""
