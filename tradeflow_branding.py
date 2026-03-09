#!/usr/bin/env python3
"""
TradeFlow ERP - Complete White-Label Branding System
Replaces all ERPNext branding with TradeFlow ERP identity
"""

import os
import json
import re
from pathlib import Path

# ============================================================================
# BRANDING CONFIGURATION
# ============================================================================

BRAND_CONFIG = {
    "app_name": "TradeFlow ERP",
    "app_title": "TradeFlow",
    "company_name": "TradeFlow Technologies",
    "tagline": "Global Trade Management Platform",
    "copyright": "© 2024 TradeFlow Technologies. All rights reserved.",
    "website": "https://tradeflow.io",
    "support_email": "support@tradeflow.io",
    
    # Color scheme
    "primary_color": "#0066CC",      # Professional blue
    "secondary_color": "#00A86B",    # Trade green
    "accent_color": "#FF6B35",       # Action orange
    "text_color": "#2C3E50",         # Dark slate
    "background_color": "#F8F9FA",   # Light gray
    
    # Module renaming (ERPNext → Industry Terms)
    "module_names": {
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
        "Maintenance": "Equipment Maintenance"
    }
}

# Text replacements
REPLACEMENTS = {
    # Primary branding
    "ERPNext": BRAND_CONFIG["app_name"],
    "ERP Next": BRAND_CONFIG["app_name"],
    "erpnext": "tradeflow",
    "Frappe ERP": BRAND_CONFIG["app_name"],
    "frappe ERP": BRAND_CONFIG["app_name"],
    
    # Company references
    "Frappe Technologies": BRAND_CONFIG["company_name"],
    "Frappe Technologies Pvt. Ltd.": BRAND_CONFIG["company_name"],
    "Powered by Frappe": f"Powered by {BRAND_CONFIG['app_name']}",
    "Built on Frappe": f"Built on {BRAND_CONFIG['app_name']}",
    
    # URLs and links
    "https://erpnext.com": BRAND_CONFIG["website"],
    "https://erpnext.org": BRAND_CONFIG["website"],
    "https://frappe.io": BRAND_CONFIG["website"],
    "erpnext.com": "tradeflow.io",
    "frappe.io": "tradeflow.io",
    
    # Support references
    "support@erpnext.com": BRAND_CONFIG["support_email"],
    "support@frappe.io": BRAND_CONFIG["support_email"],
}

# File extensions to process
EXTENSIONS = ('.html', '.js', '.vue', '.jsx', '.tsx', '.css', '.scss', '.json', '.py', '.md', '.txt')

# Directories to skip
SKIP_DIRS = {
    'node_modules', 'dist', 'build', '__pycache__', '.git', 
    '.github', 'venv', 'env', '.pytest_cache', '.mypy_cache'
}

# ============================================================================
# FILE PROCESSING
# ============================================================================

def process_file(filepath):
    """Process a single file for branding replacements"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # Perform text replacements
        for old, new in REPLACEMENTS.items():
            if old in content:
                content = content.replace(old, new)
                modified = True
        
        # Special handling for JSON files
        if filepath.endswith('.json'):
            content = process_json_branding(content, filepath)
            if content != original_content:
                modified = True
        
        # Special handling for Python files
        if filepath.endswith('.py'):
            content = process_python_branding(content)
            if content != original_content:
                modified = True
        
        # Write back if modified
        if modified and content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Modified: {filepath}")
            return True
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False
    
    return False

def process_json_branding(content, filepath):
    """Special handling for JSON configuration files"""
    try:
        data = json.loads(content)
        
        # Update app metadata
        if 'app_name' in data:
            data['app_name'] = 'tradeflow'
        if 'app_title' in data:
            data['app_title'] = BRAND_CONFIG['app_name']
        if 'app_description' in data:
            data['app_description'] = BRAND_CONFIG['tagline']
        if 'app_publisher' in data:
            data['app_publisher'] = BRAND_CONFIG['company_name']
        if 'app_email' in data:
            data['app_email'] = BRAND_CONFIG['support_email']
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    except:
        return content

def process_python_branding(content):
    """Special handling for Python files"""
    # Update module docstrings
    content = re.sub(
        r'""".*?ERPNext.*?"""',
        f'"""{BRAND_CONFIG["app_name"]} - {BRAND_CONFIG["tagline"]}"""',
        content,
        flags=re.DOTALL
    )
    return content

# ============================================================================
# CUSTOM LOGIN SCREEN
# ============================================================================

def create_custom_login():
    """Create custom login screen HTML"""
    login_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{BRAND_CONFIG["app_name"]} - Login</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, {BRAND_CONFIG["primary_color"]} 0%, {BRAND_CONFIG["secondary_color"]} 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        
        .login-container {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 440px;
            width: 100%;
            overflow: hidden;
        }}
        
        .login-header {{
            background: {BRAND_CONFIG["primary_color"]};
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        .login-header h1 {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .login-header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .login-body {{
            padding: 40px 30px;
        }}
        
        .form-group {{
            margin-bottom: 24px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 8px;
            color: {BRAND_CONFIG["text_color"]};
            font-weight: 500;
            font-size: 14px;
        }}
        
        .form-group input {{
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            font-size: 15px;
            transition: all 0.3s;
        }}
        
        .form-group input:focus {{
            outline: none;
            border-color: {BRAND_CONFIG["primary_color"]};
            box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
        }}
        
        .login-button {{
            width: 100%;
            padding: 14px;
            background: {BRAND_CONFIG["primary_color"]};
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .login-button:hover {{
            background: {BRAND_CONFIG["secondary_color"]};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
        }}
        
        .login-footer {{
            text-align: center;
            padding: 20px 30px;
            background: {BRAND_CONFIG["background_color"]};
            color: #666;
            font-size: 13px;
        }}
        
        .forgot-password {{
            text-align: right;
            margin-top: 12px;
        }}
        
        .forgot-password a {{
            color: {BRAND_CONFIG["primary_color"]};
            text-decoration: none;
            font-size: 14px;
        }}
        
        .forgot-password a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>{BRAND_CONFIG["app_name"]}</h1>
            <p>{BRAND_CONFIG["tagline"]}</p>
        </div>
        
        <div class="login-body">
            <form id="login-form" method="post">
                <div class="form-group">
                    <label for="username">Email or Username</label>
                    <input type="text" id="username" name="usr" required autocomplete="username">
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="pwd" required autocomplete="current-password">
                </div>
                
                <button type="submit" class="login-button">Sign In</button>
                
                <div class="forgot-password">
                    <a href="/forgot-password">Forgot Password?</a>
                </div>
            </form>
        </div>
        
        <div class="login-footer">
            {BRAND_CONFIG["copyright"]}
        </div>
    </div>
</body>
</html>
'''
    return login_html

# ============================================================================
# CUSTOM THEME
# ============================================================================

def create_custom_theme():
    """Create custom CSS theme"""
    theme_css = f'''/* {BRAND_CONFIG["app_name"]} Custom Theme */

:root {{
    --primary-color: {BRAND_CONFIG["primary_color"]};
    --secondary-color: {BRAND_CONFIG["secondary_color"]};
    --accent-color: {BRAND_CONFIG["accent_color"]};
    --text-color: {BRAND_CONFIG["text_color"]};
    --background-color: {BRAND_CONFIG["background_color"]};
}}

/* Override default branding */
.navbar-brand {{
    font-weight: 700;
    color: var(--primary-color) !important;
}}

.navbar-brand::before {{
    content: "{BRAND_CONFIG["app_title"]}";
}}

/* Hide original ERPNext branding */
.navbar-brand img,
.navbar-brand svg {{
    display: none !important;
}}

/* Custom button styles */
.btn-primary {{
    background-color: var(--primary-color) !important;
    border-color: var(--primary-color) !important;
}}

.btn-primary:hover {{
    background-color: var(--secondary-color) !important;
    border-color: var(--secondary-color) !important;
}}

/* Custom sidebar */
.desk-sidebar {{
    background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
}}

/* Custom page header */
.page-head {{
    background-color: var(--background-color);
    border-bottom: 2px solid var(--primary-color);
}}

/* Custom cards */
.card {{
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}}

/* Custom links */
a {{
    color: var(--primary-color);
}}

a:hover {{
    color: var(--secondary-color);
}}

/* Footer branding */
.footer {{
    background-color: var(--text-color);
    color: white;
}}

.footer::after {{
    content: "{BRAND_CONFIG["copyright"]}";
    display: block;
    text-align: center;
    padding: 10px;
}}
'''
    return theme_css

# ============================================================================
# PWA CONFIGURATION
# ============================================================================

def create_pwa_manifest():
    """Create PWA manifest for mobile branding"""
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
                "src": "/assets/tradeflow/images/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/assets/tradeflow/images/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "categories": ["business", "productivity", "finance"],
        "shortcuts": [
            {
                "name": "Dashboard",
                "url": "/app/home",
                "description": "Open dashboard"
            },
            {
                "name": "New Order",
                "url": "/app/sales-order/new",
                "description": "Create new sales order"
            }
        ]
    }
    return json.dumps(manifest, indent=2)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def apply_branding(base_path="/home/frappe/frappe-bench/apps"):
    """Apply complete branding transformation"""
    
    print(f"\n{'='*70}")
    print(f"  {BRAND_CONFIG['app_name']} - White-Label Branding System")
    print(f"{'='*70}\n")
    
    if not os.path.exists(base_path):
        print(f"⚠ Path {base_path} not found. Using current directory.")
        base_path = os.getcwd()
    
    print(f"📁 Base path: {base_path}\n")
    
    # Statistics
    files_processed = 0
    files_modified = 0
    
    # Process all files
    print("🔄 Processing files...")
    for root, dirs, files in os.walk(base_path):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            if file.endswith(EXTENSIONS):
                filepath = os.path.join(root, file)
                files_processed += 1
                if process_file(filepath):
                    files_modified += 1
    
    # Create custom assets
    print("\n🎨 Creating custom assets...")
    
    # Create custom login
    login_path = os.path.join(base_path, "frappe/www/login.html")
    if os.path.exists(os.path.dirname(login_path)):
        with open(login_path, 'w') as f:
            f.write(create_custom_login())
        print(f"✓ Created custom login: {login_path}")
    
    # Create custom theme
    theme_path = os.path.join(base_path, "frappe/public/css/tradeflow_theme.css")
    if os.path.exists(os.path.dirname(theme_path)):
        with open(theme_path, 'w') as f:
            f.write(create_custom_theme())
        print(f"✓ Created custom theme: {theme_path}")
    
    # Create PWA manifest
    manifest_path = os.path.join(base_path, "frappe/public/manifest.json")
    if os.path.exists(os.path.dirname(manifest_path)):
        with open(manifest_path, 'w') as f:
            f.write(create_pwa_manifest())
        print(f"✓ Created PWA manifest: {manifest_path}")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"  Branding Complete!")
    print(f"{'='*70}")
    print(f"  Files processed: {files_processed}")
    print(f"  Files modified: {files_modified}")
    print(f"  Brand: {BRAND_CONFIG['app_name']}")
    print(f"  Company: {BRAND_CONFIG['company_name']}")
    print(f"{'='*70}\n")
    
    # Clear cache
    print("🧹 Clearing cache...")
    if os.system("which bench > /dev/null 2>&1") == 0:
        os.system("bench clear-cache")
        os.system("bench build")
        print("✓ Cache cleared and assets rebuilt")
    else:
        print("⚠ Bench not found. Please clear cache manually:")
        print("  bench clear-cache")
        print("  bench build")
    
    print("\n✅ Branding transformation complete!")
    print(f"🌐 Your system is now branded as: {BRAND_CONFIG['app_name']}\n")

if __name__ == "__main__":
    apply_branding()
