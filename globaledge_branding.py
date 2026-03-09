#!/usr/bin/env python3
"""
GlobalEdge ERP - Complete White-Label Branding System
Alternative branding configuration for enterprise trade solutions
"""

import os
import json
import re
from pathlib import Path

# ============================================================================
# BRANDING CONFIGURATION - GLOBALEDGE
# ============================================================================

BRAND_CONFIG = {
    "app_name": "GlobalEdge ERP",
    "app_title": "GlobalEdge",
    "company_name": "GlobalEdge Technologies",
    "tagline": "Enterprise Trade Solutions",
    "copyright": "© 2024 GlobalEdge Technologies. All rights reserved.",
    "website": "https://globaledge.io",
    "support_email": "support@globaledge.io",
    
    # Color scheme - Professional corporate
    "primary_color": "#1E3A8A",      # Deep blue
    "secondary_color": "#059669",    # Emerald green
    "accent_color": "#DC2626",       # Red accent
    "text_color": "#1F2937",         # Dark gray
    "background_color": "#F9FAFB",   # Light background
    
    # Module renaming
    "module_names": {
        "Buying": "Global Procurement",
        "Selling": "Sales Operations",
        "Stock": "Supply Chain",
        "Accounts": "Finance & Accounting",
        "HR": "Workforce Management",
        "Manufacturing": "Operations",
        "Projects": "Enterprise Projects",
        "CRM": "Client Management",
        "Support": "Service Desk",
        "Assets": "Asset Tracking",
        "Quality Management": "Quality Control",
        "Maintenance": "Facility Management"
    }
}

# Text replacements
REPLACEMENTS = {
    "ERPNext": BRAND_CONFIG["app_name"],
    "ERP Next": BRAND_CONFIG["app_name"],
    "erpnext": "globaledge",
    "Frappe ERP": BRAND_CONFIG["app_name"],
    "frappe ERP": BRAND_CONFIG["app_name"],
    "Frappe Technologies": BRAND_CONFIG["company_name"],
    "Frappe Technologies Pvt. Ltd.": BRAND_CONFIG["company_name"],
    "Powered by Frappe": f"Powered by {BRAND_CONFIG['app_name']}",
    "Built on Frappe": f"Built on {BRAND_CONFIG['app_name']}",
    "https://erpnext.com": BRAND_CONFIG["website"],
    "https://erpnext.org": BRAND_CONFIG["website"],
    "https://frappe.io": BRAND_CONFIG["website"],
    "erpnext.com": "globaledge.io",
    "frappe.io": "globaledge.io",
    "support@erpnext.com": BRAND_CONFIG["support_email"],
    "support@frappe.io": BRAND_CONFIG["support_email"],
}

EXTENSIONS = ('.html', '.js', '.vue', '.jsx', '.tsx', '.css', '.scss', '.json', '.py', '.md', '.txt')
SKIP_DIRS = {'node_modules', 'dist', 'build', '__pycache__', '.git', '.github', 'venv', 'env'}

# ============================================================================
# CUSTOM LOGIN SCREEN - GLOBALEDGE
# ============================================================================

def create_custom_login():
    """Create GlobalEdge custom login screen"""
    login_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{BRAND_CONFIG["app_name"]} - Enterprise Login</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, {BRAND_CONFIG["primary_color"]} 0%, #0F172A 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }}
        
        body::before {{
            content: '';
            position: absolute;
            width: 500px;
            height: 500px;
            background: {BRAND_CONFIG["secondary_color"]};
            border-radius: 50%;
            top: -250px;
            right: -250px;
            opacity: 0.1;
        }}
        
        body::after {{
            content: '';
            position: absolute;
            width: 400px;
            height: 400px;
            background: {BRAND_CONFIG["accent_color"]};
            border-radius: 50%;
            bottom: -200px;
            left: -200px;
            opacity: 0.1;
        }}
        
        .login-container {{
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
            max-width: 480px;
            width: 100%;
            overflow: hidden;
            position: relative;
            z-index: 1;
        }}
        
        .login-header {{
            background: linear-gradient(135deg, {BRAND_CONFIG["primary_color"]} 0%, {BRAND_CONFIG["secondary_color"]} 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
            position: relative;
        }}
        
        .login-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M 20 0 L 0 0 0 20" fill="none" stroke="white" stroke-width="0.5" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }}
        
        .login-header h1 {{
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 10px;
            position: relative;
            letter-spacing: -0.5px;
        }}
        
        .login-header p {{
            font-size: 17px;
            opacity: 0.95;
            position: relative;
            font-weight: 500;
        }}
        
        .login-body {{
            padding: 45px 40px;
        }}
        
        .form-group {{
            margin-bottom: 28px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 10px;
            color: {BRAND_CONFIG["text_color"]};
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .form-group input {{
            width: 100%;
            padding: 14px 18px;
            border: 2px solid #E5E7EB;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
            background: #F9FAFB;
        }}
        
        .form-group input:focus {{
            outline: none;
            border-color: {BRAND_CONFIG["primary_color"]};
            background: white;
            box-shadow: 0 0 0 4px rgba(30, 58, 138, 0.1);
        }}
        
        .login-button {{
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, {BRAND_CONFIG["primary_color"]} 0%, {BRAND_CONFIG["secondary_color"]} 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 17px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .login-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(30, 58, 138, 0.4);
        }}
        
        .login-button:active {{
            transform: translateY(-1px);
        }}
        
        .login-footer {{
            text-align: center;
            padding: 25px 40px;
            background: #F9FAFB;
            color: #6B7280;
            font-size: 13px;
            border-top: 1px solid #E5E7EB;
        }}
        
        .forgot-password {{
            text-align: center;
            margin-top: 20px;
        }}
        
        .forgot-password a {{
            color: {BRAND_CONFIG["primary_color"]};
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
        }}
        
        .forgot-password a:hover {{
            text-decoration: underline;
        }}
        
        .enterprise-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 10px;
            letter-spacing: 1px;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>{BRAND_CONFIG["app_name"]}</h1>
            <p>{BRAND_CONFIG["tagline"]}</p>
            <span class="enterprise-badge">ENTERPRISE EDITION</span>
        </div>
        
        <div class="login-body">
            <form id="login-form" method="post">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="usr" required autocomplete="username" placeholder="Enter your username">
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="pwd" required autocomplete="current-password" placeholder="Enter your password">
                </div>
                
                <button type="submit" class="login-button">Sign In</button>
                
                <div class="forgot-password">
                    <a href="/forgot-password">Forgot Password?</a>
                </div>
            </form>
        </div>
        
        <div class="login-footer">
            {BRAND_CONFIG["copyright"]}<br>
            Secure Enterprise Access
        </div>
    </div>
</body>
</html>
'''
    return login_html

# ============================================================================
# CUSTOM THEME - GLOBALEDGE
# ============================================================================

def create_custom_theme():
    """Create GlobalEdge custom theme"""
    theme_css = f'''/* {BRAND_CONFIG["app_name"]} Enterprise Theme */

:root {{
    --primary-color: {BRAND_CONFIG["primary_color"]};
    --secondary-color: {BRAND_CONFIG["secondary_color"]};
    --accent-color: {BRAND_CONFIG["accent_color"]};
    --text-color: {BRAND_CONFIG["text_color"]};
    --background-color: {BRAND_CONFIG["background_color"]};
}}

/* Navbar branding */
.navbar-brand {{
    font-weight: 800;
    color: var(--primary-color) !important;
    font-size: 20px;
    letter-spacing: -0.5px;
}}

.navbar-brand::before {{
    content: "{BRAND_CONFIG["app_title"]}";
}}

.navbar-brand img,
.navbar-brand svg {{
    display: none !important;
}}

/* Enterprise button styles */
.btn-primary {{
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
    border: none !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(30, 58, 138, 0.3);
}}

/* Sidebar */
.desk-sidebar {{
    background: linear-gradient(180deg, var(--primary-color) 0%, #0F172A 100%);
}}

/* Page header */
.page-head {{
    background: var(--background-color);
    border-bottom: 3px solid var(--primary-color);
}}

/* Cards */
.card {{
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid #E5E7EB;
}}

/* Links */
a {{
    color: var(--primary-color);
    font-weight: 500;
}}

a:hover {{
    color: var(--secondary-color);
}}

/* Footer */
.footer {{
    background: var(--text-color);
    color: white;
}}

.footer::after {{
    content: "{BRAND_CONFIG["copyright"]}";
    display: block;
    text-align: center;
    padding: 12px;
    font-weight: 600;
}}

/* Enterprise badges */
.enterprise-badge {{
    background: var(--primary-color);
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
'''
    return theme_css

# ============================================================================
# PWA MANIFEST - GLOBALEDGE
# ============================================================================

def create_pwa_manifest():
    """Create GlobalEdge PWA manifest"""
    manifest = {
        "name": BRAND_CONFIG["app_name"],
        "short_name": BRAND_CONFIG["app_title"],
        "description": BRAND_CONFIG["tagline"],
        "start_url": "/",
        "display": "standalone",
        "background_color": BRAND_CONFIG["background_color"],
        "theme_color": BRAND_CONFIG["primary_color"],
        "orientation": "portrait-primary",
        "icons": [
            {
                "src": "/assets/globaledge/images/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/assets/globaledge/images/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "categories": ["business", "productivity", "enterprise"],
        "shortcuts": [
            {
                "name": "Dashboard",
                "url": "/app/home",
                "description": "Enterprise dashboard"
            },
            {
                "name": "Procurement",
                "url": "/app/global-procurement",
                "description": "Global procurement"
            }
        ]
    }
    return json.dumps(manifest, indent=2)

# ============================================================================
# FILE PROCESSING (Same as TradeFlow)
# ============================================================================

def process_file(filepath):
    """Process a single file for branding replacements"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        for old, new in REPLACEMENTS.items():
            if old in content:
                content = content.replace(old, new)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Modified: {filepath}")
            return True
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False
    
    return False

def apply_branding(base_path="/home/frappe/frappe-bench/apps"):
    """Apply GlobalEdge branding"""
    
    print(f"\n{'='*70}")
    print(f"  {BRAND_CONFIG['app_name']} - White-Label Branding System")
    print(f"{'='*70}\n")
    
    if not os.path.exists(base_path):
        print(f"⚠ Path {base_path} not found. Using current directory.")
        base_path = os.getcwd()
    
    print(f"📁 Base path: {base_path}\n")
    
    files_processed = 0
    files_modified = 0
    
    print("🔄 Processing files...")
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            if file.endswith(EXTENSIONS):
                filepath = os.path.join(root, file)
                files_processed += 1
                if process_file(filepath):
                    files_modified += 1
    
    print("\n🎨 Creating custom assets...")
    
    login_path = os.path.join(base_path, "frappe/www/login.html")
    if os.path.exists(os.path.dirname(login_path)):
        with open(login_path, 'w') as f:
            f.write(create_custom_login())
        print(f"✓ Created custom login: {login_path}")
    
    theme_path = os.path.join(base_path, "frappe/public/css/globaledge_theme.css")
    if os.path.exists(os.path.dirname(theme_path)):
        with open(theme_path, 'w') as f:
            f.write(create_custom_theme())
        print(f"✓ Created custom theme: {theme_path}")
    
    manifest_path = os.path.join(base_path, "frappe/public/manifest.json")
    if os.path.exists(os.path.dirname(manifest_path)):
        with open(manifest_path, 'w') as f:
            f.write(create_pwa_manifest())
        print(f"✓ Created PWA manifest: {manifest_path}")
    
    print(f"\n{'='*70}")
    print(f"  Branding Complete!")
    print(f"{'='*70}")
    print(f"  Files processed: {files_processed}")
    print(f"  Files modified: {files_modified}")
    print(f"  Brand: {BRAND_CONFIG['app_name']}")
    print(f"{'='*70}\n")
    
    print("🧹 Clearing cache...")
    if os.system("which bench > /dev/null 2>&1") == 0:
        os.system("bench clear-cache")
        os.system("bench build")
        print("✓ Cache cleared and assets rebuilt")
    
    print(f"\n✅ {BRAND_CONFIG['app_name']} branding complete!\n")

if __name__ == "__main__":
    apply_branding()
