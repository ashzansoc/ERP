# White-Label Branding - Deployment Checklist

## Pre-Deployment

### 1. Preparation
- [ ] Review both branding options (TradeFlow vs GlobalEdge)
- [ ] Choose your brand identity
- [ ] Prepare logo files (if available)
- [ ] Review color scheme
- [ ] Plan deployment window
- [ ] Notify stakeholders

### 2. Backup
- [ ] Create full database backup
  ```bash
  bench --site [site-name] backup --with-files
  ```
- [ ] Store backup in safe location
- [ ] Verify backup integrity
- [ ] Document backup location
- [ ] Test restore procedure (optional)

### 3. Environment Check
- [ ] Verify ERPNext version
- [ ] Check disk space (need ~500MB free)
- [ ] Verify bench access
- [ ] Check Docker status (if using Docker)
- [ ] Verify GCP access (if using GCP)
- [ ] Test internet connectivity

### 4. File Verification
- [ ] Confirm `tradeflow_branding.py` exists
- [ ] Confirm `globaledge_branding.py` exists
- [ ] Confirm `tradeflow_app_config.py` exists
- [ ] Confirm deployment scripts exist
- [ ] Make scripts executable
  ```bash
  chmod +x *.sh
  ```

## Deployment

### 5. Choose Deployment Method

#### Option A: Interactive (Recommended)
- [ ] Run interactive script
  ```bash
  ./deploy_whitelabel.sh
  ```
- [ ] Select brand (TradeFlow or GlobalEdge)
- [ ] Select deployment type (local/docker/gcp)
- [ ] Confirm settings
- [ ] Wait for completion

#### Option B: Direct Deployment
- [ ] Choose brand script
- [ ] Run branding script
  ```bash
  python3 tradeflow_branding.py
  # or
  python3 globaledge_branding.py
  ```
- [ ] Apply configuration
  ```bash
  bench --site all execute tradeflow_app_config.apply_all_configurations
  ```
- [ ] Build assets
  ```bash
  bench build
  ```
- [ ] Clear cache
  ```bash
  bench clear-cache
  bench clear-website-cache
  ```
- [ ] Restart services
  ```bash
  bench restart
  ```

### 6. Monitor Deployment
- [ ] Watch for errors in output
- [ ] Check file modification count
- [ ] Verify build completion
- [ ] Confirm cache cleared
- [ ] Verify services restarted

## Post-Deployment Verification

### 7. Visual Verification
- [ ] Open site in incognito/private window
- [ ] Verify login screen shows brand name
- [ ] Check custom colors applied
- [ ] Confirm no "ERPNext" text visible
- [ ] Confirm no "Frappe" text visible (except technical)
- [ ] Verify custom footer

### 8. Login Test
- [ ] Login with admin account
- [ ] Verify dashboard loads
- [ ] Check navigation bar
- [ ] Verify brand name in header
- [ ] Check footer copyright

### 9. Module Verification
- [ ] Open each module
- [ ] Verify renamed module names:
  - [ ] Procurement (was Buying)
  - [ ] Sales & Distribution (was Selling)
  - [ ] Inventory Management (was Stock)
  - [ ] Financial Management (was Accounts)
  - [ ] Human Resources (was HR)
  - [ ] Production (was Manufacturing)
  - [ ] Project Management (was Projects)
  - [ ] Customer Relations (was CRM)
- [ ] Check module functionality
- [ ] Verify no broken links

### 10. Workspace Verification
- [ ] Open each workspace
- [ ] Verify workspace names updated
- [ ] Check workspace layouts
- [ ] Verify shortcuts work
- [ ] Check charts and widgets

### 11. Database Verification
- [ ] Check system settings
  ```bash
  bench --site [site] execute "print(frappe.db.get_single_value('System Settings', 'app_name'))"
  ```
- [ ] Verify website settings
- [ ] Check module definitions
- [ ] Verify custom roles created

### 12. Mobile Verification
- [ ] Open site on mobile device
- [ ] Verify responsive login
- [ ] Add to home screen
- [ ] Open as PWA
- [ ] Verify custom icon
- [ ] Check app name
- [ ] Test navigation

### 13. Browser Compatibility
- [ ] Test in Chrome
- [ ] Test in Firefox
- [ ] Test in Safari
- [ ] Test in Edge
- [ ] Verify all show branding

### 14. User Access Test
- [ ] Login as different user roles
- [ ] Verify branding for all roles
- [ ] Check permissions intact
- [ ] Test user workflows

## Logo Upload (Optional)

### 15. Prepare Logo Files
- [ ] Create logo.png (200x50px)
- [ ] Create logo-white.png (200x50px)
- [ ] Create icon-192.png (192x192px)
- [ ] Create icon-512.png (512x512px)
- [ ] Create favicon.ico (32x32px)

### 16. Upload Logos
- [ ] Create assets directory
  ```bash
  mkdir -p sites/assets/tradeflow/images/
  # or
  mkdir -p sites/assets/globaledge/images/
  ```
- [ ] Upload logo files
  ```bash
  cp logo.png sites/assets/tradeflow/images/
  cp logo-white.png sites/assets/tradeflow/images/
  cp icon-192.png sites/assets/tradeflow/images/
  cp icon-512.png sites/assets/tradeflow/images/
  cp favicon.ico sites/assets/tradeflow/images/
  ```
- [ ] Update website settings to use logos
- [ ] Clear cache
- [ ] Verify logos display

## Documentation

### 17. Update Documentation
- [ ] Update user guides with new terminology
- [ ] Update training materials
- [ ] Update API documentation
- [ ] Update integration docs
- [ ] Create change log

### 18. User Communication
- [ ] Notify users of branding change
- [ ] Provide terminology mapping
- [ ] Schedule training sessions
- [ ] Create FAQ document
- [ ] Set up support channel

## Training

### 19. User Training
- [ ] Create training materials
- [ ] Schedule training sessions
- [ ] Demonstrate new interface
- [ ] Explain module name changes
- [ ] Answer user questions
- [ ] Provide quick reference guide

### 20. Admin Training
- [ ] Train admins on maintenance
- [ ] Explain update procedure
- [ ] Document troubleshooting
- [ ] Create admin guide
- [ ] Set up monitoring

## Monitoring

### 21. Post-Deployment Monitoring
- [ ] Monitor error logs
  ```bash
  bench --site [site] logs
  ```
- [ ] Check user feedback
- [ ] Monitor performance
- [ ] Watch for issues
- [ ] Track user adoption

### 22. Performance Check
- [ ] Measure page load times
- [ ] Check database performance
- [ ] Monitor server resources
- [ ] Verify cache effectiveness
- [ ] Test under load

## Troubleshooting

### 23. Common Issues
- [ ] If branding not visible:
  ```bash
  bench clear-cache
  bench clear-website-cache
  bench build --force
  bench restart
  ```
- [ ] If modules not renamed:
  ```bash
  bench --site all execute tradeflow_app_config.apply_all_configurations
  bench clear-cache
  ```
- [ ] If login screen not updated:
  ```bash
  ls -la apps/frappe/frappe/www/login.html
  bench build --force
  ```
- [ ] Browser cache issues:
  - Press Ctrl+Shift+R (hard refresh)
  - Clear browser cache
  - Try incognito mode

## Maintenance

### 24. Regular Maintenance
- [ ] Schedule regular backups
- [ ] Plan for ERPNext updates
- [ ] Monitor for branding issues
- [ ] Keep documentation updated
- [ ] Review user feedback

### 25. Update Procedure
- [ ] Document update process
- [ ] Test updates on staging
- [ ] Re-apply branding after updates
- [ ] Verify branding after updates
- [ ] Update documentation

## Sign-Off

### 26. Deployment Sign-Off
- [ ] All verification tests passed
- [ ] No critical issues found
- [ ] Users notified
- [ ] Documentation updated
- [ ] Training completed
- [ ] Monitoring in place

### 27. Stakeholder Approval
- [ ] Demo to stakeholders
- [ ] Get approval
- [ ] Document approval
- [ ] Close deployment ticket
- [ ] Celebrate success! 🎉

## Quick Reference

### Essential Commands

```bash
# Deploy (Interactive)
./deploy_whitelabel.sh

# Deploy TradeFlow (Direct)
./apply_tradeflow_branding.sh local

# Deploy GlobalEdge (Direct)
python3 globaledge_branding.py
bench --site all execute tradeflow_app_config.apply_all_configurations
bench build && bench clear-cache && bench restart

# Verify
bench --site [site] execute "print(frappe.db.get_single_value('System Settings', 'app_name'))"

# Troubleshoot
bench clear-cache && bench build --force && bench restart

# Backup
bench --site [site] backup --with-files

# Restore
bench --site [site] restore [backup-file]
```

### Support Resources

- **Complete Guide**: WHITELABEL_COMPLETE_GUIDE.md
- **TradeFlow Guide**: TRADEFLOW_BRANDING_GUIDE.md
- **Comparison**: BRANDING_COMPARISON.md
- **Quick Start**: QUICK_START.md
- **Results**: BRANDING_RESULTS.md

## Notes

### Deployment Date
- Date: _______________
- Time: _______________
- Deployed by: _______________

### Environment
- ERPNext Version: _______________
- Deployment Type: _______________
- Brand Selected: _______________

### Issues Encountered
- Issue 1: _______________
- Resolution: _______________
- Issue 2: _______________
- Resolution: _______________

### Success Metrics
- Files Modified: _______________
- Deployment Time: _______________
- Downtime: _______________
- User Feedback: _______________

---

**Deployment Status**: [ ] Not Started [ ] In Progress [ ] Complete [ ] Verified

**Sign-Off**: _______________  Date: _______________
