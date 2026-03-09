# Analytics Reports System - Ready to Deploy

## 🚀 Quick Start (2 Minutes)

### Step 1: Navigate to your bench directory
```bash
cd /path/to/frappe-bench
```

### Step 2: Copy the setup file
```bash
# Copy quick_analytics_setup.py to your bench directory
cp /path/to/project/quick_analytics_setup.py .
```

### Step 3: Run installation
```bash
bench --site site1.local execute quick_analytics_setup.setup_analytics
```

### Step 4: Access reports
1. Login to your ERP
2. Go to **Selling > Reports**
3. Click **Country-wise Sales Analysis**
4. Set date range and click **Run Report**

**Done! You now have 7 professional analytics reports in your ERP.**

---

## 📊 The 7 Reports

| Report | Location | What It Shows |
|--------|----------|---------------|
| **Country-wise Sales Analysis** | Selling > Reports | Revenue, volume, trends by destination country |
| **HS Code Profitability** | Selling > Reports | Profit margins by product classification |
| **Shipment Delay Analytics** | Stock > Reports | Carrier and route performance with delays |
| **Port Performance Analysis** | Stock > Reports | Port efficiency and throughput metrics |
| **Freight Forwarder Comparison** | Stock > Reports | Cost and performance comparison of vendors |
| **Duty Cost Trend Analysis** | Accounts > Reports | Customs duty costs over time |
| **FX Exposure Analysis** | Accounts > Reports | Currency risk and exchange rate volatility |

---

## 📁 Files Overview

### Installation Files
- `quick_analytics_setup.py` - **Main installation script** (use this!)
- `install_analytics_now.sh` - Bash wrapper for installation
- `implement_analytics_complete.sh` - Full installation with all steps
- `install_analytics_reports.sh` - Alternative installation method

### Core System Files
- `api/analytics.py` - All report logic and API endpoints (500+ lines)
- `install_analytics_reports.py` - Report doctype creation
- `create_sample_analytics_data.py` - Demo data generator

### Documentation
- `ANALYTICS_IMPLEMENTATION.md` - **Complete implementation guide**
- `ANALYTICS_REPORTS_GUIDE.md` - Technical documentation
- `ANALYTICS_QUICK_START.md` - User quick start
- `ANALYTICS_SYSTEM_SUMMARY.md` - System overview
- `ANALYTICS_README.md` - This file

---

## 🎯 What Gets Installed

### 1. New DocType
- **HS Code Master** - Store duty rates by country and HS code

### 2. Custom Fields
- Sales Invoice: `country_of_destination`
- Sales Invoice Item: `hs_code`
- Ocean Shipment: `freight_forwarder`, `freight_cost`

### 3. Reports (7 total)
All reports are Script Reports with:
- Date range filters
- Export to Excel/CSV/PDF
- API access
- Real-time calculations

### 4. Sample Data
- 9 HS Code Master records
- Sample countries and duty rates
- Ready to test immediately

### 5. Workspace
- Analytics workspace for easy access
- Links to all reports
- Quick navigation

---

## 💻 Installation Methods

### Method 1: Quick Setup (Recommended)
```bash
cd /path/to/frappe-bench
bench --site site1.local execute quick_analytics_setup.setup_analytics
```
**Time: 2-3 minutes**

### Method 2: Bash Script
```bash
cd /path/to/project
./install_analytics_now.sh site1.local
```
**Time: 2-3 minutes**

### Method 3: Full Installation
```bash
cd /path/to/project
./implement_analytics_complete.sh site1.local
```
**Time: 3-5 minutes**

### Method 4: Manual Console
```bash
bench --site site1.local console
```
```python
exec(open('/path/to/quick_analytics_setup.py').read())
setup_analytics()
```
**Time: 2-3 minutes**

---

## ✅ Verify Installation

### Check Reports Exist
```bash
bench --site site1.local console
```
```python
import frappe
reports = frappe.get_all('Report', 
    filters={'report_type': 'Script Report', 'module': ['in', ['Selling', 'Stock', 'Accounts']]},
    fields=['name', 'module'])

print(f"\nFound {len(reports)} reports:")
for r in reports:
    if 'Analysis' in r.name or 'Analytics' in r.name or 'Comparison' in r.name:
        print(f"  ✓ {r.name} ({r.module})")
```

### Check Custom Fields
```python
import frappe
field = frappe.db.exists('Custom Field', 
    {'dt': 'Sales Invoice', 'fieldname': 'country_of_destination'})
print(f"Country field exists: {bool(field)}")
```

### Check HS Code Master
```python
import frappe
count = frappe.db.count('HS Code Master')
print(f"HS Code Master records: {count}")
```

---

## 🎨 Using the Reports

### Example 1: Country-wise Sales

**From UI:**
1. Go to Selling > Reports > Country-wise Sales Analysis
2. Set From Date: 2024-01-01
3. Set To Date: 2024-12-31
4. Click Run Report
5. Export to Excel

**From API:**
```javascript
frappe.call({
    method: 'api.analytics.get_country_wise_sales',
    args: {
        from_date: '2024-01-01',
        to_date: '2024-12-31'
    },
    callback: (r) => {
        console.log('Summary:', r.message.summary);
        console.log('Detailed:', r.message.detailed);
    }
});
```

### Example 2: HS Code Profitability

**From UI:**
1. Go to Selling > Reports > HS Code Profitability
2. Set date range
3. Optional: Filter by country
4. Click Run Report
5. See profit margins and costs

**From Python:**
```python
import frappe
data = frappe.call('api.analytics.get_hs_code_profitability', {
    'from_date': '2024-01-01',
    'to_date': '2024-12-31',
    'filters': '{"country": "United States"}'
})

for row in data:
    print(f"{row['hs_code']}: Margin {row['profit_margin']}%")
```

### Example 3: Executive Dashboard

**From API:**
```python
import frappe
summary = frappe.call('api.analytics.get_executive_dashboard_summary', {
    'from_date': '2024-01-01',
    'to_date': '2024-12-31'
})

print(f"Revenue: ${summary['revenue']['current']:,.2f}")
print(f"Growth: {summary['revenue']['growth']:.1f}%")
print(f"On-time: {summary['shipments']['on_time_percentage']:.1f}%")
```

---

## 🔧 Customization

### Add Custom Metric

Edit `api/analytics.py`:

```python
@frappe.whitelist()
def get_my_custom_report(from_date, to_date):
    """Your custom report logic"""
    data = frappe.db.sql("""
        SELECT 
            custom_field,
            SUM(amount) as total
        FROM `tabYour DocType`
        WHERE date BETWEEN %s AND %s
        GROUP BY custom_field
    """, [from_date, to_date], as_dict=True)
    
    return data
```

### Create New Report

1. Add function to `api/analytics.py`
2. Create report doctype:
```python
frappe.get_doc({
    'doctype': 'Report',
    'name': 'My Custom Report',
    'ref_doctype': 'Sales Invoice',
    'report_type': 'Script Report',
    'module': 'Selling'
}).insert()
```

### Modify Existing Report

Edit the corresponding function in `api/analytics.py` and restart bench.

---

## 🐛 Troubleshooting

### Reports Not Showing

**Solution 1: Clear cache**
```bash
bench --site site1.local clear-cache
bench restart
```

**Solution 2: Recreate reports**
```bash
bench --site site1.local execute quick_analytics_setup.create_reports
```

### No Data in Reports

**Solution 1: Add sample data**
```bash
bench --site site1.local execute create_sample_analytics_data.create_sample_analytics_data
```

**Solution 2: Check custom fields**
```bash
bench --site site1.local execute quick_analytics_setup.add_custom_fields
```

### Permission Denied

**Solution: Add System Manager role**
```bash
bench --site site1.local console
```
```python
import frappe
user = frappe.get_doc('User', 'your.email@example.com')
user.add_roles('System Manager')
frappe.db.commit()
```

### API Not Found

**Solution: Copy analytics.py**
```bash
cp api/analytics.py /path/to/frappe-bench/apps/erpnext/erpnext/selling/doctype/
bench restart
```

---

## 📈 Performance Tips

### Add Database Indexes
```sql
ALTER TABLE `tabSales Invoice` 
ADD INDEX idx_country_date (country_of_destination, posting_date);

ALTER TABLE `tabSales Invoice Item` 
ADD INDEX idx_hs_code (hs_code);

ALTER TABLE `tabOcean Shipment` 
ADD INDEX idx_carrier_dates (carrier, actual_arrival_date);
```

### Enable Caching
Reports cache results for 1 hour by default. Adjust in `api/analytics.py`.

### Optimize Queries
For large datasets, add date range limits and use proper indexes.

---

## 🎓 Training Users

### For Sales Teams
- Focus on Country-wise Sales and HS Code Profitability
- Show how to export to Excel
- Explain trend analysis

### For Operations
- Focus on Shipment Delay and Port Performance
- Show carrier comparison
- Explain efficiency scores

### For Finance
- Focus on Duty Cost Trends and FX Exposure
- Show margin analysis
- Explain risk metrics

### For Management
- Show Executive Dashboard
- Explain KPIs and growth metrics
- Demonstrate period comparisons

---

## 🚢 Deployment Checklist

- [ ] Installation completed successfully
- [ ] All 7 reports visible in ERP
- [ ] HS Code Master doctype created
- [ ] Custom fields added
- [ ] Sample data created and visible
- [ ] Can run each report without errors
- [ ] Can export reports to Excel
- [ ] API endpoints tested
- [ ] Users trained on report access
- [ ] Documentation shared with team

---

## 📞 Support

### Check Logs
```bash
tail -f /path/to/frappe-bench/logs/site1.local/error.log
```

### Restart Services
```bash
bench restart
```

### Rebuild
```bash
bench --site site1.local migrate
bench build
```

### Reinstall
```bash
bench --site site1.local execute quick_analytics_setup.setup_analytics
```

---

## 🎉 Success!

Once installed, you have:
- ✅ 7 professional analytics reports
- ✅ Real-time data analysis
- ✅ Export capabilities
- ✅ API access
- ✅ Sample data for testing
- ✅ Production-ready system

Your export-import ERP now has the reporting capabilities that make it a sellable product!

---

## 📚 Additional Resources

- **ANALYTICS_IMPLEMENTATION.md** - Detailed implementation guide
- **ANALYTICS_REPORTS_GUIDE.md** - Complete technical documentation
- **ANALYTICS_QUICK_START.md** - User quick start guide
- **ANALYTICS_SYSTEM_SUMMARY.md** - System architecture overview

---

**Ready to see it in action? Run the installation now!**

```bash
cd /path/to/frappe-bench
bench --site site1.local execute quick_analytics_setup.setup_analytics
```
