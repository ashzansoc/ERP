# TradeFlow ERP - Complete White-Label Branding Guide

## Overview

This guide covers the complete white-label transformation of ERPNext into **TradeFlow ERP** - a professional, industry-specific global trade management platform with zero ERPNext branding visible.

## What's Included

### ✅ Complete Branding Replacement
- All "ERPNext" references replaced with "TradeFlow ERP"
- All "Frappe" references replaced with "TradeFlow Technologies"
- Custom company identity throughout the system
- Professional color scheme and design

### ✅ Custom Login Screen
- Modern, professional login interface
- Branded with TradeFlow identity
- Responsive design for all devices
- Custom color scheme

### ✅ Custom Theme
- Professional blue/green color palette
- Custom CSS for all UI elements
- Branded navigation and sidebar
- Custom buttons and links

### ✅ Module Renaming (Industry Terms)
- **Buying** → **Procurement**
- **Selling** → **Sales & Distribution**
- **Stock** → **Inventory Management**
- **Accounts** → **Financial Management**
- **HR** → **Human Resources**
- **Manufacturing** → **Production**
- **Projects** → **Project Management**
- **CRM** → **Customer Relations**

### ✅ Custom App Namespace
- App name: `tradeflow`
- No "erpnext" references
- Custom module structure
- Industry-specific terminology

### ✅ Mobile PWA Branding
- Custom PWA manifest
- Branded app icons
- Custom splash screen
- Standalone mobile app experience

## Quick Start

### 1. Local Installation

```bash
# Make script executable
chmod +x apply_tradeflow_branding.sh

# Apply branding
./apply_tradeflow_branding.sh local
```

### 2. Docker Installation

```bash
# Apply branding to Docker container
./apply_tradeflow_branding.sh docker
```

### 3. GCP Installation

```bash
# Set environment variables
export GCP_PROJECT_ID="your-project-id"
export GCP_ZONE="us-central1-a"
export GCP_INSTANCE="erpnext-server"

# Apply branding
./apply_tradeflow_branding.sh gcp
```

## Detailed Configuration

### Brand Configuration

Edit `tradeflow_branding.py` to customize:

```python
BRAND_CONFIG = {
    "app_name": "TradeFlow ERP",           # Main app name
    "app_title": "TradeFlow",              # Short title
    "company_name": "TradeFlow Technologies",
    "tagline": "Global Trade Management Platform",
    "website": "https://tradeflow.io",
    "support_email": "support@tradeflow.io",
    
    # Colors
    "primary_color": "#0066CC",      # Professional blue
    "secondary_color": "#00A86B",    # Trade green
    "accent_color": "#FF6B35",       # Action orange
}
```

### Alternative Branding: GlobalEdge ERP

To use "GlobalEdge ERP" instead:

```python
BRAND_CONFIG = {
    "app_name": "GlobalEdge ERP",
    "app_title": "GlobalEdge",
    "company_name": "GlobalEdge Technologies",
    "tagline": "Enterprise Trade Solutions",
    "website": "https://globaledge.io",
    "support_email": "support@globaledge.io",
    
    # Colors
    "primary_color": "#1E3A8A",      # Deep blue
    "secondary_color": "#059669",    # Emerald green
    "accent_color": "#DC2626",       # Red accent
}
```

## What Gets Changed

### 1. Text Replacements

All files are scanned and updated:
- `.html`, `.js`, `.vue`, `.jsx`, `.tsx` files
- `.css`, `.scss` style files
- `.json` configuration files
- `.py` Python files
- `.md` documentation files

### 2. Custom Assets Created

#### Login Screen (`frappe/www/login.html`)
- Modern, professional design
- Branded header with app name
- Custom color scheme
- Responsive layout

#### Custom Theme (`frappe/public/css/tradeflow_theme.css`)
- CSS variables for colors
- Custom button styles
- Branded navigation
- Custom cards and layouts

#### PWA Manifest (`frappe/public/manifest.json`)
- Mobile app configuration
- Custom icons and colors
- App shortcuts
- Standalone mode

### 3. Database Changes

#### System Settings
- App name updated
- Company information
- Branding settings

#### Website Settings
- Logo and brand HTML
- Footer information
- Copyright notice

#### Module Definitions
- Module names translated
- Industry-specific terms
- Custom labels

#### Workspaces
- Renamed to industry terms
- Custom layouts
- Branded navigation

## Module Renaming Details

### Procurement (formerly Buying)
- Purchase Order → Procurement Order
- Purchase Receipt → Goods Receipt
- Purchase Invoice → Vendor Invoice
- Supplier → Vendor
- Supplier Quotation → Vendor Quote

### Sales & Distribution (formerly Selling)
- Sales Order → Customer Order
- Delivery Note → Shipment Note
- Sales Invoice → Customer Invoice
- Quotation → Sales Quote

### Inventory Management (formerly Stock)
- Stock Entry → Inventory Transaction
- Material Request → Stock Request
- Item → Product
- Warehouse → Storage Location
- Stock Reconciliation → Inventory Adjustment

### Financial Management (formerly Accounts)
- Journal Entry → Financial Entry
- Payment Entry → Payment Transaction
- Chart of Accounts → Account Structure

## Custom Roles Created

Industry-specific roles:
- **Trade Manager** - Manages international trade operations
- **Compliance Officer** - Handles trade compliance and regulations
- **Logistics Coordinator** - Coordinates shipments and logistics
- **Procurement Specialist** - Manages vendor relationships
- **Customs Broker** - Handles customs clearance

## Logo and Images

### Required Images

Create these images in `/assets/tradeflow/images/`:

1. **logo.png** (200x50px) - Main logo
2. **logo-white.png** (200x50px) - White version for dark backgrounds
3. **icon-192.png** (192x192px) - PWA icon
4. **icon-512.png** (512x512px) - PWA icon
5. **favicon.ico** (32x32px) - Browser favicon

### Image Guidelines

- Use PNG format with transparency
- Maintain aspect ratio
- Optimize for web (compress)
- Use SVG for scalability when possible

## Testing Checklist

After applying branding, verify:

- [ ] Login screen shows TradeFlow branding
- [ ] No "ERPNext" text visible anywhere
- [ ] No "Frappe" text visible (except technical references)
- [ ] Custom colors applied throughout
- [ ] Module names show industry terms
- [ ] Navigation shows custom labels
- [ ] Footer shows TradeFlow copyright
- [ ] PWA manifest works on mobile
- [ ] All workspaces renamed
- [ ] Custom roles available

## Troubleshooting

### Branding Not Visible

```bash
# Clear all caches
bench clear-cache
bench clear-website-cache

# Rebuild assets
bench build --force

# Restart services
bench restart
```

### Module Names Not Changed

```bash
# Re-run configuration
bench --site all execute tradeflow_app_config.apply_all_configurations

# Clear cache
bench clear-cache
```

### Login Screen Not Updated

```bash
# Check file location
ls -la apps/frappe/frappe/www/login.html

# Rebuild
bench build --force

# Clear browser cache
# Press Ctrl+Shift+R (hard refresh)
```

### Docker Container Issues

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs backend

# Restart container
docker-compose restart backend
```

## Reverting Branding

If you need to revert to ERPNext branding:

```bash
# Use the reverse script
python3 reverse_whitelabel.py

# Or restore from backup
bench --site [site-name] restore [backup-file]
```

## Advanced Customization

### Custom Login Page

Edit `tradeflow_branding.py` function `create_custom_login()`:

```python
def create_custom_login():
    login_html = f'''
    <!-- Add your custom HTML here -->
    <div class="custom-login">
        <!-- Your design -->
    </div>
    '''
    return login_html
```

### Custom Theme Colors

Edit CSS variables in `create_custom_theme()`:

```css
:root {
    --primary-color: #YourColor;
    --secondary-color: #YourColor;
    --accent-color: #YourColor;
}
```

### Additional Module Renames

Add to `MODULE_TRANSLATIONS` in `tradeflow_app_config.py`:

```python
MODULE_TRANSLATIONS = {
    "Your Module": "New Name",
    # Add more...
}
```

## Performance Considerations

### Build Time
- Initial branding: 5-10 minutes
- Asset rebuild: 2-3 minutes
- Cache clear: 1 minute

### File Processing
- Processes 1000+ files
- Safe replacements only
- Backup recommended before applying

## Security Notes

- No security features are modified
- All permissions remain intact
- User data is not affected
- Only UI/branding changes

## Support

For issues or questions:
- Check logs: `bench --site [site] logs`
- Review error messages
- Verify file permissions
- Check Docker container status

## Next Steps

After branding is complete:

1. **Upload Custom Logo**
   - Create logo files
   - Upload to `/assets/tradeflow/images/`
   - Update references

2. **Customize Colors**
   - Edit `BRAND_CONFIG` in branding script
   - Re-run branding application
   - Test on all pages

3. **Configure Modules**
   - Review renamed modules
   - Adjust permissions
   - Train users on new terminology

4. **Test Mobile PWA**
   - Access site on mobile
   - Add to home screen
   - Verify branding

5. **Update Documentation**
   - Create user guides with new terms
   - Update training materials
   - Inform stakeholders

## Maintenance

### Regular Updates

When updating ERPNext/Frappe:

```bash
# Update apps
bench update

# Re-apply branding
./apply_tradeflow_branding.sh [deployment-type]

# Test thoroughly
```

### Backup Strategy

Before major changes:

```bash
# Backup with files
bench --site [site-name] backup --with-files

# Store backup safely
cp sites/[site-name]/private/backups/* /backup/location/
```

## Conclusion

Your ERPNext installation is now completely white-labeled as **TradeFlow ERP** with:
- Professional branding throughout
- Industry-specific terminology
- Custom login and theme
- Mobile PWA support
- Zero ERPNext visibility

The system is production-ready and fully branded for your business.
