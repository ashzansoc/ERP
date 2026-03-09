#!/bin/bash
# Enhance Ocean Shipment with Landed Cost fields

cd frappe_docker

echo "🔧 Enhancing Ocean Shipment DocType..."

docker-compose exec -T backend bench --site localhost console <<'PYTHON'
import frappe

if not frappe.db.exists("DocType", "Ocean Shipment"):
    print("❌ Ocean Shipment not found. Please install it first.")
else:
    print("📦 Enhancing Ocean Shipment...")
    doc = frappe.get_doc("DocType", "Ocean Shipment")
    
    existing = [f.fieldname for f in doc.fields]
    if "items" in existing:
        print("ℹ️  Already enhanced")
    else:
        # Find insert position after containers
        insert_idx = len(doc.fields)
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
             "options": "Weight\\nVolume\\nValue", "default": "Weight"},
            {"fieldname": "cha_allocation_method", "fieldtype": "Select", "label": "CHA Allocation",
             "options": "Customs Value\\nEqual", "default": "Customs Value"},
            {"fieldname": "port_allocation_method", "fieldtype": "Select", "label": "Port Allocation",
             "options": "Weight\\nVolume", "default": "Weight"},
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

PYTHON

echo ""
echo "✅ Done!"
