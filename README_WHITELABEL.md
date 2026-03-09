# Complete White-Label Branding System for ERPNext

## 🎯 What This Is

A **production-ready, complete white-label branding system** that transforms ERPNext into a fully-branded ERP solution with **ZERO ERPNext visibility**.

Choose between:
- **TradeFlow ERP** - Global Trade Management Platform
- **GlobalEdge ERP** - Enterprise Trade Solutions

## ✨ What You Get

### Complete Branding Transformation
✅ All "ERPNext" → Your brand name  
✅ All "Frappe" → Your company name  
✅ Custom professional login screen  
✅ Custom theme with your colors  
✅ Industry-specific module names  
✅ Custom app namespace  
✅ Mobile PWA branding  
✅ Custom navigation & footer  

### Zero ERPNext Visibility
❌ No "ERPNext" text anywhere  
❌ No "Frappe" branding visible  
❌ No generic module names  
❌ No default login screen  
❌ No default theme  

## 🚀 Quick Start

### One Command Deployment

```bash
chmod +x deploy_whitelabel.sh && ./deploy_whitelabel.sh
```

That's it! The interactive script handles everything.

### Manual Deployment

#### TradeFlow ERP
```bash
./apply_tradeflow_branding.sh local
```

#### GlobalEdge ERP
```bash
python3 globaledge_branding.py
bench --site all execute tradeflow_app_config.apply_all_configurations
bench build && bench clear-cache && bench restart
```

## 📦 Files Included

### Core Scripts
1. **tradeflow_branding.py** - TradeFlow branding engine
2. **globaledge_branding.py** - GlobalEdge branding engine
3. **tradeflow_app_config.py** - Configuration & module setup

### Deployment Scripts
4. **deploy_whitelabel.sh** - Interactive deployment (recommended)
5. **apply_tradeflow_branding.sh** - TradeFlow deployment

### Documentation
6. **QUICK_START.md** - Get started in 5 minutes
7. **WHITELABEL_COMPLETE_GUIDE.md** - Complete implementation guide
8. **TRADEFLOW_BRANDING_GUIDE.md** - TradeFlow detailed guide
9. **BRANDING_COMPARISON.md** - Compare both options
10. **BRANDING_RESULTS.md** - See what you get
11. **DEPLOYMENT_CHECKLIST.md** - Step-by-step checklist
12. **README_WHITELABEL.md** - This file

## 🎨 Brand Options

### TradeFlow ERP
**Identity**: Global Trade Management Platform  
**Colors**: Professional Blue, Trade Green, Action Orange  
**Style**: Modern, clean, trade-focused  
**Best For**: Import/Export, Logistics, Freight Forwarders  

**Module Names**:
- Procurement
- Sales & Distribution
- Inventory Management
- Financial Management

### GlobalEdge ERP
**Identity**: Enterprise Trade Solutions  
**Colors**: Deep Blue, Emerald Green, Red Accent  
**Style**: Corporate, professional, enterprise  
**Best For**: Large Enterprises, Corporations, ERP Partners  

**Module Names**:
- Global Procurement
- Sales Operations
- Supply Chain
- Finance & Accounting

## 📋 What Changes

### Text Replacements
- ERPNext → TradeFlow ERP / GlobalEdge ERP
- Frappe → TradeFlow Technologies / GlobalEdge Technologies
- All URLs and support emails updated

### Visual Changes
- Custom login screen (modern, professional)
- Custom theme (your colors throughout)
- Branded navigation bar
- Custom footer with your copyright

### Module Renaming
- Buying → Procurement / Global Procurement
- Selling → Sales & Distribution / Sales Operations
- Stock → Inventory Management / Supply Chain
- Accounts → Financial Management / Finance & Accounting
- All other modules renamed appropriately

### Database Updates
- System settings
- Website settings
- Module definitions
- Workspace names
- Custom roles created

## 🔧 Customization

### Change Brand Name
Edit the branding script:
```python
BRAND_CONFIG = {
    "app_name": "YourBrand ERP",
    "company_name": "YourCompany",
    "tagline": "Your Tagline",
}
```

### Change Colors
```python
BRAND_CONFIG = {
    "primary_color": "#YourColor",
    "secondary_color": "#YourColor",
    "accent_color": "#YourColor",
}
```

### Add Your Logo
```bash
mkdir -p sites/assets/tradeflow/images/
cp your-logo.png sites/assets/tradeflow/images/logo.png
```

## ✓ Verification

After deployment, verify:
- [ ] Login shows your brand name
- [ ] No "ERPNext" text visible
- [ ] Custom colors applied
- [ ] Modules renamed
- [ ] Navigation customized
- [ ] Footer shows your copyright
- [ ] Mobile PWA works

## 🐛 Troubleshooting

### Branding Not Visible
```bash
bench clear-cache
bench clear-website-cache
bench build --force
bench restart
# Browser: Ctrl+Shift+R
```

### Module Names Not Changed
```bash
bench --site all execute tradeflow_app_config.apply_all_configurations
bench clear-cache
```

### Docker Issues
```bash
docker-compose restart backend
docker exec -u frappe container_id python3 /home/frappe/tradeflow_branding.py
```

## 📚 Documentation

### Quick Reference
- **QUICK_START.md** - 5-minute setup guide
- **DEPLOYMENT_CHECKLIST.md** - Step-by-step checklist

### Detailed Guides
- **WHITELABEL_COMPLETE_GUIDE.md** - Complete guide
- **TRADEFLOW_BRANDING_GUIDE.md** - TradeFlow details
- **BRANDING_COMPARISON.md** - Compare options

### Results & Reference
- **BRANDING_RESULTS.md** - See what you get
- **PORTAL_WHITELABEL_CONFIG.md** - Portal customization

## 🎯 Deployment Types

### Local (Bench)
```bash
./apply_tradeflow_branding.sh local
```

### Docker
```bash
./apply_tradeflow_branding.sh docker
```

### GCP
```bash
export GCP_PROJECT_ID="your-project"
./apply_tradeflow_branding.sh gcp
```

## 💾 Backup & Restore

### Backup Before Branding
```bash
bench --site [site-name] backup --with-files
```

### Restore if Needed
```bash
bench --site [site-name] restore [backup-file]
```

## 🔐 Security

- ✅ No security features modified
- ✅ All permissions intact
- ✅ User data unchanged
- ✅ Safe for production

## 📊 Performance

- **Processing Time**: 5-10 minutes
- **Files Modified**: 1000+ files
- **Runtime Impact**: None
- **Storage Impact**: ~5MB

## 🎓 Training

### Key Changes for Users
1. New brand name (not "ERPNext")
2. Module names changed (industry terms)
3. Same functionality (only names changed)

### Documentation Updates
- Update user guides
- Update training materials
- Create terminology mapping
- Provide quick reference

## 🌐 Multi-Site Support

```bash
# Apply to specific site
bench --site site1.example.com execute tradeflow_app_config.apply_all_configurations

# Apply to all sites
bench --site all execute tradeflow_app_config.apply_all_configurations
```

## 🔄 Updates

### After ERPNext Updates
```bash
bench update
./deploy_whitelabel.sh
# Test thoroughly
```

## 📞 Support

### Common Issues
1. **Cache Issues** → Clear cache and rebuild
2. **Module Names** → Re-run configuration
3. **Login Screen** → Check file location
4. **Docker** → Restart container

### Getting Help
- Check logs: `bench --site [site] logs`
- Review documentation
- Verify file permissions
- Check container status

## 🏆 Success Criteria

Your deployment is successful when:
- ✅ Zero ERPNext branding visible
- ✅ Professional custom login
- ✅ Consistent brand colors
- ✅ Industry-specific terminology
- ✅ Mobile PWA working
- ✅ All tests passing

## 📈 Next Steps

After deployment:
1. Upload custom logo files
2. Customize colors (if needed)
3. Train users on new terminology
4. Update documentation
5. Announce new branding

## 🎉 Result

A professional, fully-branded ERP system that looks like a custom-built solution, not a modified ERPNext installation.

**Zero ERPNext visibility. Complete professional branding. Production ready.**

---

## Quick Commands Reference

```bash
# Deploy (Interactive)
./deploy_whitelabel.sh

# Deploy TradeFlow
./apply_tradeflow_branding.sh local

# Deploy GlobalEdge
python3 globaledge_branding.py
bench --site all execute tradeflow_app_config.apply_all_configurations
bench build && bench clear-cache && bench restart

# Verify
bench --site [site] execute "print(frappe.db.get_single_value('System Settings', 'app_name'))"

# Troubleshoot
bench clear-cache && bench build --force && bench restart

# Backup
bench --site [site] backup --with-files
```

---

**Ready to deploy?** Start with `QUICK_START.md` or run `./deploy_whitelabel.sh`

**Need details?** Read `WHITELABEL_COMPLETE_GUIDE.md`

**Want to compare?** Check `BRANDING_COMPARISON.md`
