#!/bin/bash
# Install Landed Cost Automation inline

cd frappe_docker

echo "🚢 Installing Landed Cost Automation..."
echo ""

docker-compose exec -T backend bench --site localhost console <<'PYTHON'
import frappe

print("\n" + "="*60)
print("🚢 Landed Cost Automation Installation")
print("="*60 + "\n")

# Phase 1: Cost Component
if not frappe.db.exists("DocType", "Cost Component"):
    print("📦 Creating Cost Component...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Cost Component",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {"fieldname": "cost_type", "fieldtype": "Select", "label": "Cost Type", 
             "options": "Freight\\nInsurance\\nCustoms Duty\\nCHA Fees\\nPort Charges\\nOther",
             "reqd": 1, "in_list_view": 1},
            {"fieldname": "description", "fieldtype": "Data", "label": "Description", "in_list_view": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "reqd": 1, "in_list_view": 1},
            {"fieldname": "currency", "fieldtype": "Link", "label": "Currency", "options": "Currency", "default": "USD", "in_list_view": 1},
            {"fieldname": "section_break_1", "fieldtype": "Section Break"},
            {"fieldname": "exchange_rate", "fieldtype": "Float", "label": "Exchange Rate", "precision": 6},
            {"fieldname": "amount_in_base_currency", "fieldtype": "Currency", "label": "Amount in Base Currency", "read_only": 1},
            {"fieldname": "column_break_2", "fieldtype": "Column Break"},
            {"fieldname": "is_estimated", "fieldtype": "Check", "label": "Is Estimated", "default": 1},
            {"fieldname": "actual_amount", "fieldtype": "Currency", "label": "Actual Amount"},
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Cost Component created")
else:
    print("ℹ️  Cost Component exists")

# Phase 2: Shipment Item
if not frappe.db.exists("DocType", "Shipment Item"):
    print("📦 Creating Shipment Item...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Shipment Item",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {"fieldname": "item_code", "fieldtype": "Link", "label": "Item Code", "options": "Item", "reqd": 1, "in_list_view": 1},
            {"fieldname": "item_name", "fieldtype": "Data", "label": "Item Name"},
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
            {"fieldname": "total_landed_cost", "fieldtype": "Currency", "label": "Total Landed Cost", "read_only": 1, "in_list_view": 1, "bold": 1},
            {"fieldname": "column_break_4", "fieldtype": "Column Break"},
            {"fieldname": "unit_landed_cost", "fieldtype": "Currency", "label": "Unit Landed Cost", "read_only": 1},
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✅ Shipment Item created")
else:
    print("ℹ️  Shipment Item exists")

# Phase 3: HS Code Duty Rate
if not frappe.db.exists("DocType", "HS Code Duty Rate"):
    print("📦 Creating HS Code Duty Rate...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "HS Code Duty Rate",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {"fieldname": "country_of_origin", "fieldtype": "Link", "label": "Country of Origin", "options": "Country", "in_list_view": 1},
            {"fieldname": "destination_country", "fieldtype": "Link", "label": "Destination Country", "options": "Country", "in_list_view": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "duty_rate", "fieldtype": "Percent", "label": "Duty Rate (%)", "reqd": 1, "in_list_view": 1},
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
else:
    print("ℹ️  HS Code Duty Rate exists")

# Phase 4: HS Code
if not frappe.db.exists("DocType", "HS Code"):
    print("📦 Creating HS Code...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "HS Code",
        "module": "Stock",
        "custom": 1,
        "autoname": "field:hs_code",
        "naming_rule": "By fieldname",
        "fields": [
            {"fieldname": "hs_code", "fieldtype": "Data", "label": "HS Code", "reqd": 1, "unique": 1},
            {"fieldname": "description", "fieldtype": "Text", "label": "Description", "reqd": 1},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Duty Rates"},
            {"fieldname": "duty_rates", "fieldtype": "Table", "label": "Duty Rates", "options": "HS Code Duty Rate"},
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
else:
    print("ℹ️  HS Code exists")

# Phase 5: Calculation Log
if not frappe.db.exists("DocType", "Landed Cost Calculation Log"):
    print("📦 Creating Calculation Log...")
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Landed Cost Calculation Log",
        "module": "Stock",
        "custom": 1,
        "autoname": "format:LCCLOG-{####}",
        "naming_rule": "Expression",
        "fields": [
            {"fieldname": "shipment", "fieldtype": "Link", "label": "Shipment", "options": "Ocean Shipment", "reqd": 1, "in_list_view": 1},
            {"fieldname": "calculation_date", "fieldtype": "Datetime", "label": "Calculation Date", "default": "Now", "reqd": 1, "in_list_view": 1},
            {"fieldname": "column_break_1", "fieldtype": "Column Break"},
            {"fieldname": "triggered_by", "fieldtype": "Link", "label": "Triggered By", "options": "User"},
            {"fieldname": "trigger_reason", "fieldtype": "Select", "label": "Trigger Reason", "options": "Manual\\nCost Component Changed\\nItem Changed\\nAllocation Method Changed", "in_list_view": 1},
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
else:
    print("ℹ️  Calculation Log exists")

print("\n✅ All DocTypes created successfully!")
print("\n" + "="*60)

PYTHON

echo ""
echo "✅ Installation complete!"
echo "📍 Access at: http://localhost:8080"
echo ""
