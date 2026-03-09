#!/bin/bash
# Fix Shipment Item creation

cd frappe_docker

echo "🔧 Creating Shipment Item DocType..."

docker-compose exec -T backend bench --site localhost console <<'PYTHON'
import frappe

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
    print("ℹ️  Shipment Item already exists")

PYTHON

echo ""
echo "✅ Done!"
