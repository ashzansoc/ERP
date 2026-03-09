# White-Label Branding - Quick Start

## 🚀 One-Command Deployment

```bash
chmod +x deploy_whitelabel.sh && ./deploy_whitelabel.sh
```

That's it! The interactive script will guide you through:
1. Choosing your brand (TradeFlow or GlobalEdge)
2. Selecting deployment type (local/docker/gcp)
3. Applying all branding automatically

## 📋 What You Get

### TradeFlow ERP
- **Focus**: Global Trade Management
- **Colors**: Blue, Green, Orange
- **Best For**: Import/Export, Logistics

### GlobalEdge ERP
- **Focus**: Enterprise Solutions
- **Colors**: Deep Blue, Emerald, Red
- **Best For**: Large Enterprises

## ✅ What Changes

- ❌ "ERPNext" → ✅ Your Brand Name
- ❌ "Frappe" → ✅ Your Company Name
- ❌ Generic modules → ✅ Industry terms
- ❌ Default login → ✅ Custom branded login
- ❌ Default theme → ✅ Custom colors/design

## 🎯 Quick Commands

### Deploy TradeFlow (Local)
```bash
./apply_tradeflow_branding.sh local
```

### Deploy TradeFlow (Docker)
```bash
./apply_tradeflow_branding.sh docker
```

### Deploy GlobalEdge
```bash
python3 globaledge_branding.py
bench --site all execute tradeflow_app_config.apply_all_configurations
bench build && bench clear-cache && bench restart
```

### Verify Branding
```bash
# Check system settings
bench --site [site] execute "print(frappe.db.get_single_value('System Settings', 'app_name'))"

# Should output: TradeFlow ERP or GlobalEdge ERP
```

## 🔧 Customize

Edit `tradeflow_branding.py` or `globaledge_branding.py`:

```python
BRAND_CONFIG = {
    "app_name": "YourBrand ERP",
    "company_name": "YourCompany",
    "primary_color": "#YourColor",
    # ...
}
```

Then re-run deployment.

## 📱 Add Logo

```bash
# Create folder
mkdir -p sites/assets/tradeflow/images/

# Copy logo
cp your-logo.png sites/assets/tradeflow/images/logo.png
```

## 🐛 Fix Issues

```bash
# Clear cache
bench clear-cache && bench clear-website-cache

# Rebuild
bench build --force

# Restart
bench restart

# Browser: Ctrl+Shift+R
```

## 📚 Full Documentation

- **WHITELABEL_COMPLETE_GUIDE.md** - Complete guide
- **TRADEFLOW_BRANDING_GUIDE.md** - TradeFlow details
- **BRANDING_COMPARISON.md** - Compare options

## ✓ Checklist

After deployment:
- [ ] Login shows your brand
- [ ] No "ERPNext" visible
- [ ] Custom colors applied
- [ ] Modules renamed
- [ ] Mobile PWA works

## 🎉 Done!

Your system is now fully white-labeled with zero ERPNext branding visible.
