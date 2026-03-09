#!/usr/bin/env python3
"""
Smart Pricing Engine (AI Layer) Installation Script
Creates all necessary DocTypes and configurations for AI-powered pricing features
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import json


def install_ai_pricing_engine():
    """Main installation function"""
    print("🤖 Installing Smart Pricing Engine (AI Layer)...")
    
    # Step 1: Create User AI Settings DocType
    create_user_ai_settings_doctype()
    
    # Step 2: Create AI Pricing Log DocType
    create_ai_pricing_log_doctype()
    
    # Step 3: Create FX Risk Alert DocType
    create_fx_risk_alert_doctype()
    
    # Step 4: Create Competitor Price DocType
    create_competitor_price_doctype()
    
    # Step 5: Add custom fields to existing DocTypes
    add_custom_fields()
    
    # Step 6: Create AI Pricing Dashboard
    create_ai_pricing_dashboard()
    
    print("✅ Smart Pricing Engine installed successfully!")
    print("\n📋 Next Steps:")
    print("1. Users should configure their LLM settings in User Settings")
    print("2. Access AI Pricing features from Ocean Shipment and Sales Invoice")
    print("3. View AI insights in the AI Pricing Dashboard")


def create_user_ai_settings_doctype():
    """Create User AI Settings DocType"""
    print("Creating User AI Settings DocType...")
    
    if frappe.db.exists("DocType", "User AI Settings"):
        print("  ⚠️  User AI Settings already exists, skipping...")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "User AI Settings",
        "module": "Custom",
        "custom": 1,
        "is_submittable": 0,
        "track_changes": 1,
        "naming_rule": "Expression",
        "autoname": "format:AI-SET-{user}",
        "fields": [
            {
                "fieldname": "user",
                "label": "User",
                "fieldtype": "Link",
                "options": "User",
                "reqd": 1,
                "unique": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "enabled",
                "label": "Enable AI Features",
                "fieldtype": "Check",
                "default": "1",
                "in_list_view": 1
            },
            {
                "fieldname": "section_break_1",
                "fieldtype": "Section Break",
                "label": "LLM Configuration"
            },
            {
                "fieldname": "llm_provider",
                "label": "LLM Provider",
                "fieldtype": "Select",
                "options": "\nOpenAI\nAnthropic\nGoogle\nAzure OpenAI",
                "reqd": 1,
                "in_list_view": 1,
                "description": "Select your preferred AI model provider"
            },
            {
                "fieldname": "llm_model",
                "label": "Model Name",
                "fieldtype": "Data",
                "description": "e.g., gpt-4, claude-3-sonnet-20240229, gemini-pro, or Azure endpoint URL"
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "llm_api_key",
                "label": "API Key",
                "fieldtype": "Password",
                "reqd": 1,
                "description": "Your API key for the selected provider"
            },
            {
                "fieldname": "section_break_2",
                "fieldtype": "Section Break",
                "label": "Feature Settings"
            },
            {
                "fieldname": "enable_margin_suggestions",
                "label": "Enable Margin Suggestions",
                "fieldtype": "Check",
                "default": "1"
            },
            {
                "fieldname": "enable_historical_comparison",
                "label": "Enable Historical Comparison",
                "fieldtype": "Check",
                "default": "1"
            },
            {
                "fieldname": "column_break_2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "enable_country_analytics",
                "label": "Enable Country Analytics",
                "fieldtype": "Check",
                "default": "1"
            },
            {
                "fieldname": "enable_volume_discounts",
                "label": "Enable Volume Discount Recommendations",
                "fieldtype": "Check",
                "default": "1"
            },
            {
                "fieldname": "enable_fx_alerts",
                "label": "Enable FX Risk Alerts",
                "fieldtype": "Check",
                "default": "1"
            },
            {
                "fieldname": "section_break_3",
                "fieldtype": "Section Break",
                "label": "Usage Statistics"
            },
            {
                "fieldname": "total_api_calls",
                "label": "Total API Calls",
                "fieldtype": "Int",
                "read_only": 1,
                "default": "0"
            },
            {
                "fieldname": "last_used",
                "label": "Last Used",
                "fieldtype": "Datetime",
                "read_only": 1
            }
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            },
            {
                "role": "All",
                "read": 1,
                "write": 1,
                "create": 1,
                "if_owner": 1
            }
        ]
    })
    
    doctype.insert(ignore_permissions=True)
    frappe.db.commit()
    print("  ✅ User AI Settings created")


def create_ai_pricing_log_doctype():
    """Create AI Pricing Log DocType"""
    print("Creating AI Pricing Log DocType...")
    
    if frappe.db.exists("DocType", "AI Pricing Log"):
        print("  ⚠️  AI Pricing Log already exists, skipping...")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "AI Pricing Log",
        "module": "Custom",
        "custom": 1,
        "is_submittable": 0,
        "track_changes": 0,
        "naming_rule": "Expression",
        "autoname": "format:AI-LOG-{#####}",
        "fields": [
            {
                "fieldname": "log_date",
                "label": "Log Date",
                "fieldtype": "Datetime",
                "reqd": 1,
                "in_list_view": 1,
                "default": "Now"
            },
            {
                "fieldname": "user",
                "label": "User",
                "fieldtype": "Link",
                "options": "User",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "suggestion_type",
                "label": "Suggestion Type",
                "fieldtype": "Select",
                "options": "Margin Suggestion\nHistorical Comparison\nCountry Pricing Analysis\nVolume Discount Recommendation\nFX Risk Analysis",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "reference",
                "label": "Reference",
                "fieldtype": "Data",
                "in_list_view": 1,
                "description": "Item code, currency, or other reference"
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "shipment",
                "label": "Shipment",
                "fieldtype": "Link",
                "options": "Ocean Shipment"
            },
            {
                "fieldname": "llm_provider",
                "label": "LLM Provider",
                "fieldtype": "Data",
                "read_only": 1
            },
            {
                "fieldname": "llm_model",
                "label": "LLM Model",
                "fieldtype": "Data",
                "read_only": 1
            },
            {
                "fieldname": "section_break_1",
                "fieldtype": "Section Break",
                "label": "Suggestion Data"
            },
            {
                "fieldname": "suggestion_data",
                "label": "Suggestion Data",
                "fieldtype": "Long Text",
                "description": "JSON data of the AI suggestion"
            }
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            },
            {
                "role": "Sales User",
                "read": 1
            }
        ]
    })
    
    doctype.insert(ignore_permissions=True)
    frappe.db.commit()
    print("  ✅ AI Pricing Log created")


def create_fx_risk_alert_doctype():
    """Create FX Risk Alert DocType"""
    print("Creating FX Risk Alert DocType...")
    
    if frappe.db.exists("DocType", "FX Risk Alert"):
        print("  ⚠️  FX Risk Alert already exists, skipping...")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "FX Risk Alert",
        "module": "Custom",
        "custom": 1,
        "is_submittable": 0,
        "track_changes": 1,
        "naming_rule": "Expression",
        "autoname": "format:FX-ALERT-{#####}",
        "fields": [
            {
                "fieldname": "alert_date",
                "label": "Alert Date",
                "fieldtype": "Date",
                "reqd": 1,
                "in_list_view": 1,
                "default": "Today"
            },
            {
                "fieldname": "user",
                "label": "User",
                "fieldtype": "Link",
                "options": "User",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "currencies",
                "label": "Currencies",
                "fieldtype": "Data",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "risk_level",
                "label": "Risk Level",
                "fieldtype": "Select",
                "options": "Low\nMedium\nHigh",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "exposure_amount",
                "label": "Exposure Amount",
                "fieldtype": "Currency"
            },
            {
                "fieldname": "status",
                "label": "Status",
                "fieldtype": "Select",
                "options": "Open\nAcknowledged\nMitigated\nClosed",
                "default": "Open",
                "in_list_view": 1
            },
            {
                "fieldname": "section_break_1",
                "fieldtype": "Section Break",
                "label": "Recommendation"
            },
            {
                "fieldname": "recommendation",
                "label": "Hedging Recommendation",
                "fieldtype": "Long Text"
            },
            {
                "fieldname": "section_break_2",
                "fieldtype": "Section Break",
                "label": "Actions Taken"
            },
            {
                "fieldname": "action_taken",
                "label": "Action Taken",
                "fieldtype": "Text"
            },
            {
                "fieldname": "action_date",
                "label": "Action Date",
                "fieldtype": "Date"
            }
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            },
            {
                "role": "Accounts User",
                "read": 1,
                "write": 1
            }
        ]
    })
    
    doctype.insert(ignore_permissions=True)
    frappe.db.commit()
    print("  ✅ FX Risk Alert created")


def create_competitor_price_doctype():
    """Create Competitor Price DocType"""
    print("Creating Competitor Price DocType...")
    
    if frappe.db.exists("DocType", "Competitor Price"):
        print("  ⚠️  Competitor Price already exists, skipping...")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Competitor Price",
        "module": "Custom",
        "custom": 1,
        "is_submittable": 0,
        "track_changes": 1,
        "naming_rule": "Expression",
        "autoname": "format:COMP-{item_code}-{#####}",
        "fields": [
            {
                "fieldname": "item_code",
                "label": "Item Code",
                "fieldtype": "Link",
                "options": "Item",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "competitor",
                "label": "Competitor",
                "fieldtype": "Data",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "price",
                "label": "Price",
                "fieldtype": "Currency",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "date",
                "label": "Date",
                "fieldtype": "Date",
                "reqd": 1,
                "in_list_view": 1,
                "default": "Today"
            },
            {
                "fieldname": "currency",
                "label": "Currency",
                "fieldtype": "Link",
                "options": "Currency",
                "default": "USD"
            },
            {
                "fieldname": "source",
                "label": "Source",
                "fieldtype": "Data",
                "description": "Where this price was obtained"
            },
            {
                "fieldname": "section_break_1",
                "fieldtype": "Section Break",
                "label": "Additional Details"
            },
            {
                "fieldname": "notes",
                "label": "Notes",
                "fieldtype": "Text"
            }
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            },
            {
                "role": "Sales User",
                "read": 1,
                "write": 1,
                "create": 1
            }
        ]
    })
    
    doctype.insert(ignore_permissions=True)
    frappe.db.commit()
    print("  ✅ Competitor Price created")


def add_custom_fields():
    """Add custom fields to existing DocTypes"""
    print("Adding custom fields to existing DocTypes...")
    
    custom_fields = {
        "Ocean Shipment Item": [
            {
                "fieldname": "ai_pricing_section",
                "label": "AI Pricing Intelligence",
                "fieldtype": "Section Break",
                "insert_after": "unit_landed_cost",
                "collapsible": 1
            },
            {
                "fieldname": "ai_suggested_margin",
                "label": "AI Suggested Margin %",
                "fieldtype": "Percent",
                "insert_after": "ai_pricing_section",
                "read_only": 1
            },
            {
                "fieldname": "ai_target_price",
                "label": "AI Target Price",
                "fieldtype": "Currency",
                "insert_after": "ai_suggested_margin",
                "read_only": 1
            },
            {
                "fieldname": "column_break_ai",
                "fieldtype": "Column Break",
                "insert_after": "ai_target_price"
            },
            {
                "fieldname": "ai_min_margin",
                "label": "AI Min Margin %",
                "fieldtype": "Percent",
                "insert_after": "column_break_ai",
                "read_only": 1
            },
            {
                "fieldname": "ai_reasoning",
                "label": "AI Reasoning",
                "fieldtype": "Small Text",
                "insert_after": "ai_min_margin",
                "read_only": 1
            }
        ],
        "Sales Invoice Item": [
            {
                "fieldname": "ai_price_check",
                "label": "AI Price Check",
                "fieldtype": "Section Break",
                "insert_after": "discount_amount",
                "collapsible": 1
            },
            {
                "fieldname": "ai_historical_avg",
                "label": "Historical Avg Price",
                "fieldtype": "Currency",
                "insert_after": "ai_price_check",
                "read_only": 1
            },
            {
                "fieldname": "ai_price_variance",
                "label": "Price Variance %",
                "fieldtype": "Percent",
                "insert_after": "ai_historical_avg",
                "read_only": 1
            },
            {
                "fieldname": "ai_recommendation",
                "label": "AI Recommendation",
                "fieldtype": "Select",
                "options": "\nAccept\nReview\nAdjust",
                "insert_after": "ai_price_variance",
                "read_only": 1
            }
        ]
    }
    
    create_custom_fields(custom_fields, update=True)
    print("  ✅ Custom fields added")


def create_ai_pricing_dashboard():
    """Create AI Pricing Dashboard"""
    print("Creating AI Pricing Dashboard...")
    
    # This would create a dashboard workspace
    # For now, we'll just print a message
    print("  ℹ️  Dashboard can be created manually in Workspace")
    print("  ℹ️  Add charts for:")
    print("      - AI Suggestions by Type")
    print("      - FX Risk Alerts")
    print("      - Pricing Accuracy")
    print("      - Cost Savings from AI Recommendations")


if __name__ == "__main__":
    install_ai_pricing_engine()
