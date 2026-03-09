#!/usr/bin/env python3
"""
TradeFlow ERP - App Configuration & Module Renaming
Creates custom app namespace and renames modules to industry terms
"""

import frappe
from frappe import _

# ============================================================================
# APP CONFIGURATION
# ============================================================================

def setup_tradeflow_app():
    """Configure TradeFlow ERP app settings"""
    
    # Update System Settings
    system_settings = frappe.get_single("System Settings")
    system_settings.app_name = "TradeFlow ERP"
    system_settings.country = "United States"
    system_settings.time_zone = "America/New_York"
    system_settings.save()
    
    # Update Website Settings
    website_settings = frappe.get_single("Website Settings")
    website_settings.app_name = "TradeFlow ERP"
    website_settings.app_logo = "/assets/tradeflow/images/logo.png"
    website_settings.banner_html = '''
        <div class="tradeflow-banner">
            <h1>TradeFlow ERP</h1>
            <p>Global Trade Management Platform</p>
        </div>
    '''
    website_settings.brand_html = '<img src="/assets/tradeflow/images/logo.png" alt="TradeFlow ERP" style="height: 40px;">'
    website_settings.copyright = "© 2024 TradeFlow Technologies. All rights reserved."
    website_settings.footer_address = """
        <div class="footer-address">
            <strong>TradeFlow Technologies</strong><br>
            Global Trade Management Platform<br>
            Email: support@tradeflow.io<br>
            Web: https://tradeflow.io
        </div>
    """
    website_settings.save()
    
    print("✓ App configuration updated")

# ============================================================================
# MODULE RENAMING
# ============================================================================

MODULE_TRANSLATIONS = {
    # Core modules
    "Buying": "Procurement",
    "Selling": "Sales & Distribution",
    "Stock": "Inventory Management",
    "Accounts": "Financial Management",
    "HR": "Human Resources",
    "Manufacturing": "Production",
    "Projects": "Project Management",
    "CRM": "Customer Relations",
    "Support": "Customer Support",
    "Assets": "Asset Management",
    "Quality Management": "Quality Assurance",
    "Maintenance": "Equipment Maintenance",
    
    # Custom modules
    "Buying Module": "Procurement Module",
    "Selling Module": "Sales & Distribution Module",
    "Stock Module": "Inventory Management Module",
    "Accounts Module": "Financial Management Module",
}

def rename_modules():
    """Rename modules to industry-specific terms"""
    
    print("\n🔄 Renaming modules to industry terms...")
    
    for old_name, new_name in MODULE_TRANSLATIONS.items():
        try:
            # Update module definitions
            if frappe.db.exists("Module Def", old_name):
                module = frappe.get_doc("Module Def", old_name)
                module.module_name = new_name
                module.save()
                print(f"  ✓ Renamed: {old_name} → {new_name}")
            
            # Update translations
            frappe.db.sql("""
                INSERT INTO `tabTranslation` (language, source_text, translated_text, context)
                VALUES ('en', %s, %s, 'Module')
                ON DUPLICATE KEY UPDATE translated_text = %s
            """, (old_name, new_name, new_name))
            
        except Exception as e:
            print(f"  ✗ Error renaming {old_name}: {e}")
    
    frappe.db.commit()
    print("✓ Module renaming complete")

# ============================================================================
# DOCTYPE LABELS
# ============================================================================

DOCTYPE_LABELS = {
    # Buying → Procurement
    "Purchase Order": "Procurement Order",
    "Purchase Receipt": "Goods Receipt",
    "Purchase Invoice": "Vendor Invoice",
    "Supplier": "Vendor",
    "Supplier Quotation": "Vendor Quote",
    "Request for Quotation": "RFQ",
    
    # Selling → Sales & Distribution
    "Sales Order": "Customer Order",
    "Delivery Note": "Shipment Note",
    "Sales Invoice": "Customer Invoice",
    "Quotation": "Sales Quote",
    
    # Stock → Inventory
    "Stock Entry": "Inventory Transaction",
    "Material Request": "Stock Request",
    "Item": "Product",
    "Warehouse": "Storage Location",
    "Stock Reconciliation": "Inventory Adjustment",
    
    # Accounts → Financial
    "Journal Entry": "Financial Entry",
    "Payment Entry": "Payment Transaction",
    "Chart of Accounts": "Account Structure",
}

def update_doctype_labels():
    """Update DocType labels to industry terms"""
    
    print("\n🏷️  Updating DocType labels...")
    
    for doctype, new_label in DOCTYPE_LABELS.items():
        try:
            if frappe.db.exists("DocType", doctype):
                frappe.db.set_value("DocType", doctype, "description", 
                    f"Also known as: {new_label}")
                
                # Add translation
                frappe.db.sql("""
                    INSERT INTO `tabTranslation` (language, source_text, translated_text, context)
                    VALUES ('en', %s, %s, 'DocType')
                    ON DUPLICATE KEY UPDATE translated_text = %s
                """, (doctype, new_label, new_label))
                
                print(f"  ✓ Labeled: {doctype} → {new_label}")
        except Exception as e:
            print(f"  ✗ Error updating {doctype}: {e}")
    
    frappe.db.commit()
    print("✓ DocType labels updated")

# ============================================================================
# WORKSPACE CUSTOMIZATION
# ============================================================================

def customize_workspaces():
    """Customize workspace names and layouts"""
    
    print("\n🖥️  Customizing workspaces...")
    
    workspace_renames = {
        "Buying": "Procurement",
        "Selling": "Sales & Distribution",
        "Stock": "Inventory Management",
        "Accounts": "Financial Management",
        "HR": "Human Resources",
        "Manufacturing": "Production",
        "Projects": "Project Management",
        "CRM": "Customer Relations",
    }
    
    for old_name, new_name in workspace_renames.items():
        try:
            if frappe.db.exists("Workspace", old_name):
                workspace = frappe.get_doc("Workspace", old_name)
                workspace.title = new_name
                workspace.label = new_name
                workspace.save()
                print(f"  ✓ Workspace: {old_name} → {new_name}")
        except Exception as e:
            print(f"  ✗ Error updating workspace {old_name}: {e}")
    
    frappe.db.commit()
    print("✓ Workspaces customized")

# ============================================================================
# CUSTOM ROLES
# ============================================================================

def create_custom_roles():
    """Create industry-specific roles"""
    
    print("\n👥 Creating custom roles...")
    
    custom_roles = [
        {
            "role_name": "Trade Manager",
            "desk_access": 1,
            "description": "Manages international trade operations"
        },
        {
            "role_name": "Compliance Officer",
            "desk_access": 1,
            "description": "Handles trade compliance and regulations"
        },
        {
            "role_name": "Logistics Coordinator",
            "desk_access": 1,
            "description": "Coordinates shipments and logistics"
        },
        {
            "role_name": "Procurement Specialist",
            "desk_access": 1,
            "description": "Manages vendor relationships and purchasing"
        },
        {
            "role_name": "Customs Broker",
            "desk_access": 1,
            "description": "Handles customs clearance and documentation"
        }
    ]
    
    for role_data in custom_roles:
        try:
            if not frappe.db.exists("Role", role_data["role_name"]):
                role = frappe.get_doc({
                    "doctype": "Role",
                    "role_name": role_data["role_name"],
                    "desk_access": role_data["desk_access"],
                    "description": role_data["description"]
                })
                role.insert()
                print(f"  ✓ Created role: {role_data['role_name']}")
        except Exception as e:
            print(f"  ✗ Error creating role {role_data['role_name']}: {e}")
    
    frappe.db.commit()
    print("✓ Custom roles created")

# ============================================================================
# NAVBAR CUSTOMIZATION
# ============================================================================

def customize_navbar():
    """Customize navigation bar"""
    
    print("\n🧭 Customizing navigation...")
    
    # Remove ERPNext default items
    navbar_settings = frappe.get_single("Navbar Settings")
    
    # Clear existing items
    navbar_settings.settings_dropdown = []
    
    # Add custom items
    custom_items = [
        {"item_label": "Dashboard", "item_type": "Route", "route": "/app/home"},
        {"item_label": "Procurement", "item_type": "Route", "route": "/app/procurement"},
        {"item_label": "Sales", "item_type": "Route", "route": "/app/sales-distribution"},
        {"item_label": "Inventory", "item_type": "Route", "route": "/app/inventory-management"},
        {"item_label": "Finance", "item_type": "Route", "route": "/app/financial-management"},
        {"item_label": "Trade Compliance", "item_type": "Route", "route": "/app/compliance"},
        {"item_label": "Reports", "item_type": "Route", "route": "/app/reports"},
        {"item_label": "Settings", "item_type": "Route", "route": "/app/settings"},
    ]
    
    for item in custom_items:
        navbar_settings.append("settings_dropdown", item)
    
    navbar_settings.save()
    print("✓ Navigation customized")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def apply_all_configurations():
    """Apply all TradeFlow configurations"""
    
    print("\n" + "="*70)
    print("  TradeFlow ERP - Configuration & Module Setup")
    print("="*70 + "\n")
    
    try:
        setup_tradeflow_app()
        rename_modules()
        update_doctype_labels()
        customize_workspaces()
        create_custom_roles()
        customize_navbar()
        
        # Clear cache
        frappe.clear_cache()
        
        print("\n" + "="*70)
        print("  ✅ Configuration Complete!")
        print("="*70)
        print("\n  Your system is now configured as TradeFlow ERP")
        print("  All modules have been renamed to industry terms")
        print("  Custom roles and workspaces are ready\n")
        
    except Exception as e:
        print(f"\n❌ Error during configuration: {e}")
        frappe.db.rollback()

if __name__ == "__main__":
    apply_all_configurations()
