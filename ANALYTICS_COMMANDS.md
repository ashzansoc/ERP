# Analytics System - Command Reference Card

## 🚀 Installation Commands

### Quick Install (Recommended)
```bash
cd /path/to/frappe-bench
bench --site site1.local execute quick_analytics_setup.setup_analytics
```

### Alternative Methods
```bash
# Method 2: Bash script
./install_analytics_now.sh site1.local

# Method 3: Full installation
./implement_analytics_complete.sh site1.local
```

---

## ✅ Verification Commands

### Check Reports Exist
```bash
bench --site site1.local console
```
```python
import frappe
reports = frappe.get_all('Report', 
    filters={'report_type': 'Script Report'},
    fields=['name', 'module'])
for r in reports:
    if 'Analysis' in r.name or 'Analytics' in r.name:
        print(f"✓ {r.name}")
```

### Check Custom Fields
```python
import frappe
field = frappe.db.exists('Custom Field', 
    {'dt': 'Sales Invoice', 'fieldname': 'country_of_destination'})
print(f"Country field: {'✓' if field else '✗'}")
```

### Check HS Code Master
```python
import frappe
count = frappe.db.count('HS Code Master')
print(f"HS Code records: {count}")
```

---

## 🎨 API Commands

### Country-wise Sales
```python
import frappe
data = frappe.call('api.analytics.get_country_wise_sales', {
    'from_date': '2024-01-01',
    'to_date': '2024-12-31'
})
print(data['summary'])
```

### HS Code Profitability
```python
data = frappe.call('api.analytics.get_hs_code_profitability', {
    'from_date': '2024-01-01',
    'to_date': '2024-12-31',
    'filters': '{"country": "United States"}'
})
```

### Shipment Delays
```python
data = frappe.call('api.analytics.get_shipment_delay_analytics', {
    'from_date': '2024-01-01',
    'to_date': '2024-12-31',
    'filters': '{"carrier": "Maersk"}'
})
```

### Executive Dashboard
```python
summary = frappe.call('api.analytics.get_executive_dashboard_summary', {
    'from_date': '2024-01-01',
    'to_date': '2024-12-31'
})
print(f"Revenue: ${summary['revenue']['current']:,.2f}")
print(f"Growth: {summary['revenue']['growth']:.1f}%")
```

---

## 🔧 Maintenance Commands

### Clear Cache
```bash
bench --site site1.local clear-cache
bench restart
```

### Recreate Reports
```bash
bench --site site1.local execute quick_analytics_setup.create_reports
```

### Add Sample Data
```bash
bench --site site1.local execute create_sample_analytics_data.create_sample_analytics_data
```

### Rebuild
```bash
bench --site site1.local migrate
bench build
bench restart
```

---

## 🐛 Troubleshooting Commands

### View Logs
```bash
tail -f logs/site1.local/error.log
```

### Check Site Status
```bash
bench --site site1.local list-apps
```

### Test Database Connection
```bash
bench --site site1.local console
```
```python
import frappe
print(frappe.db.get_value('User', 'Administrator', 'email'))
```

### Reinstall
```bash
bench --site site1.local execute quick_analytics_setup.setup_analytics
```

---

## 📊 Data Management Commands

### Create HS Code Master Record
```python
import frappe
frappe.get_doc({
    'doctype': 'HS Code Master',
    'hs_code': '8471.30',
    'country': 'United States',
    'duty_rate': 5.5,
    'additional_duty_rate': 2.0,
    'description': 'Portable computers'
}).insert()
frappe.db.commit()
```

### Update Custom Field
```python
import frappe
frappe.db.set_value('Sales Invoice', 'SINV-00001', 
    'country_of_destination', 'United States')
frappe.db.commit()
```

### Bulk Update HS Codes
```python
import frappe
items = frappe.get_all('Sales Invoice Item', 
    filters={'item_code': 'ITEM-001'})
for item in items:
    frappe.db.set_value('Sales Invoice Item', item.name, 
        'hs_code', '8471.30')
frappe.db.commit()
```

---

## 🔐 Permission Commands

### Add System Manager Role
```python
import frappe
user = frappe.get_doc('User', 'user@example.com')
user.add_roles('System Manager')
frappe.db.commit()
```

### Grant Report Access
```python
import frappe
report = frappe.get_doc('Report', 'Country-wise Sales Analysis')
report.append('roles', {
    'role': 'Sales User'
})
report.save()
frappe.db.commit()
```

---

## 📈 Performance Commands

### Add Database Indexes
```sql
-- Run in database console
ALTER TABLE `tabSales Invoice` 
ADD INDEX idx_country_date (country_of_destination, posting_date);

ALTER TABLE `tabSales Invoice Item` 
ADD INDEX idx_hs_code (hs_code);

ALTER TABLE `tabOcean Shipment` 
ADD INDEX idx_carrier_dates (carrier, actual_arrival_date);
```

### Clear Report Cache
```python
import frappe
frappe.cache().delete_value('analytics_report_*')
```

---

## 🔄 Backup Commands

### Backup Before Installation
```bash
bench --site site1.local backup
```

### Restore if Needed
```bash
bench --site site1.local restore /path/to/backup.sql.gz
```

---

## 📱 Quick Access URLs

```
# Country-wise Sales
http://localhost:8000/app/query-report/Country-wise%20Sales%20Analysis

# HS Code Profitability
http://localhost:8000/app/query-report/HS%20Code%20Profitability

# Shipment Delays
http://localhost:8000/app/query-report/Shipment%20Delay%20Analytics

# Port Performance
http://localhost:8000/app/query-report/Port%20Performance%20Analysis

# Freight Forwarder
http://localhost:8000/app/query-report/Freight%20Forwarder%20Comparison

# Duty Costs
http://localhost:8000/app/query-report/Duty%20Cost%20Trend%20Analysis

# FX Exposure
http://localhost:8000/app/query-report/FX%20Exposure%20Analysis
```

---

## 🎯 One-Liners

```bash
# Install everything
bench --site site1.local execute quick_analytics_setup.setup_analytics

# Check if working
bench --site site1.local console -c "import frappe; print(len(frappe.get_all('Report', filters={'report_type': 'Script Report'})))"

# Add sample data
bench --site site1.local execute create_sample_analytics_data.create_sample_analytics_data

# Clear and restart
bench --site site1.local clear-cache && bench restart

# View error log
tail -20 logs/site1.local/error.log
```

---

## 📋 Checklist Commands

### Pre-Installation Check
```bash
# Check bench
which bench

# Check site
bench --site site1.local list-apps

# Check permissions
bench --site site1.local console -c "import frappe; print(frappe.session.user)"
```

### Post-Installation Check
```bash
# Count reports
bench --site site1.local console -c "import frappe; print(frappe.db.count('Report', {'report_type': 'Script Report'}))"

# Check HS Code Master
bench --site site1.local console -c "import frappe; print(frappe.db.exists('DocType', 'HS Code Master'))"

# Check custom fields
bench --site site1.local console -c "import frappe; print(frappe.db.count('Custom Field', {'dt': 'Sales Invoice'}))"
```

---

## 🚀 Quick Start Sequence

```bash
# 1. Navigate to bench
cd /path/to/frappe-bench

# 2. Copy setup file
cp /path/to/project/quick_analytics_setup.py .

# 3. Install
bench --site site1.local execute quick_analytics_setup.setup_analytics

# 4. Verify
bench --site site1.local console -c "import frappe; reports = frappe.get_all('Report', filters={'report_type': 'Script Report'}); print(f'Found {len(reports)} reports')"

# 5. Access
open http://localhost:8000
```

---

## 💡 Pro Tips

### Run Multiple Commands
```bash
# Install and verify in one go
bench --site site1.local execute quick_analytics_setup.setup_analytics && \
bench --site site1.local console -c "import frappe; print('Reports:', len(frappe.get_all('Report')))"
```

### Create Alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias analytics-install="bench --site site1.local execute quick_analytics_setup.setup_analytics"
alias analytics-verify="bench --site site1.local console -c \"import frappe; print(frappe.get_all('Report', pluck='name'))\""
```

### Watch Logs During Install
```bash
# Terminal 1: Install
bench --site site1.local execute quick_analytics_setup.setup_analytics

# Terminal 2: Watch logs
tail -f logs/site1.local/error.log
```

---

## 📞 Help Commands

### Get Bench Info
```bash
bench version
bench --help
```

### Get Site Info
```bash
bench --site site1.local console -c "import frappe; print(frappe.get_installed_apps())"
```

### Get Report Info
```bash
bench --site site1.local console -c "import frappe; report = frappe.get_doc('Report', 'Country-wise Sales Analysis'); print(report.as_dict())"
```

---

**Save this file for quick reference!** 📌
