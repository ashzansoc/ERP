# Analytics Implementation - See It In Your ERP

## Quick Implementation (Choose One Method)

### Method 1: One-Command Setup (Recommended)

```bash
# From your project directory
bench --site site1.local execute quick_analytics_setup.setup_analytics
```

This will:
- ✓ Create HS Code Master DocType
- ✓ Add custom fields to Sales Invoice and Ocean Shipment
- ✓ Create all 7 analytics reports
- ✓ Create Analytics workspace
- ✓ Add sample data for testing

**Time: 2-3 minutes**

---

### Method 2: Full Installation Script

```bash
# From your project directory
./implement_analytics_complete.sh site1.local
```

This does everything Method 1 does, plus:
- Copies API files to ERPNext
- Creates comprehensive workspace
- More detailed logging

**Time: 3-5 minutes**

---

### Method 3: Manual Step-by-Step

If you prefer to see each step:

#### Step 1: Copy API File
```bash
# Find your bench directory
cd /path/to/frappe-bench

# Copy analytics API
cp /path/to/project/api/analytics.py apps/erpnext/erpnext/selling/doctype/
```

#### Step 2: Run Setup
```bash
bench --site site1.local console
```

Then in the console:
```python
exec(open('/path/to/project/quick_analytics_setup.py').read())
setup_analytics()
```

---

## Verify Installation

After running any method above, verify it worked:

```bash
bench --site site1.local console
```

```python
# Check if reports exist
import frappe
reports = frappe.get_all('Report', filters={'name': ['like', '%Analysis%']}, fields=['name'])
print(f"Found {len(reports)} analytics reports:")
for r in reports:
    print(f"  ✓ {r.name}")
```

You should see:
- Country-wise Sales Analysis
- HS Code Profitability
- Shipment Delay Analytics
- Port Performance Analysis
- Freight Forwarder Comparison
- Duty Cost Trend Analysis
- FX Exposure Analysis

---

## Access Reports in ERP

### Option 1: From Modules
1. Login to your ERP
2. Go to **Selling** module
3. Click **Reports** section
4. Find:
   - Country-wise Sales Analysis
   - HS Code Profitability

5. Go to **Stock** module
6. Click **Reports** section
7. Find:
   - Shipment Delay Analytics
   - Port Performance Analysis
   - Freight Forwarder Comparison

8. Go to **Accounts** module
9. Click **Reports** section
10. Find:
    - Duty Cost Trend Analysis
    - FX Exposure Analysis

### Option 2: Search Bar
1. Click the search bar (or press Ctrl+K / Cmd+K)
2. Type "Analytics"
3. See all reports listed

### Option 3: Report Builder
1. Go to **Home > Report Builder**
2. Filter by "Script Report"
3. Find all analytics reports

---

## View Sample Data

The setup creates sample data automatically. To see it:

### Check HS Code Master
```
Home > HS Code Master > List
```

You should see entries like:
- HS-8471.30-United States (Portable computers, 5.5% duty)
- HS-8517.12-United Kingdom (Smartphones, 0% duty)
- HS-8528.72-Germany (LCD monitors, 3.9% duty)

### Check Sales Invoices
```
Selling > Sales Invoice > List
```

Filter by last 12 months to see sample invoices with:
- Country of Destination filled
- HS Codes on items

### Check Ocean Shipments (if installed)
```
Stock > Ocean Shipment > List
```

See sample shipments with:
- Freight forwarders
- Freight costs
- Departure/arrival dates

---

## Run Your First Report

### Example: Country-wise Sales Analysis

1. Go to **Selling > Reports > Country-wise Sales Analysis**

2. Set filters:
   - From Date: 1 year ago
   - To Date: Today
   - Customer: (leave blank for all)

3. Click **Run Report**

4. You'll see:
   - Revenue by country
   - Shipment counts
   - Average order values
   - Quantity totals

5. Export options:
   - Excel
   - CSV
   - PDF
   - Print

### Example: HS Code Profitability

1. Go to **Selling > Reports > HS Code Profitability**

2. Set filters:
   - From Date: 1 year ago
   - To Date: Today
   - Country: (optional filter)

3. Click **Run Report**

4. You'll see:
   - Revenue per HS code
   - Costs and margins
   - Profit calculations
   - Duty impacts

---

## Using the API

### From JavaScript (Frontend)

```javascript
// Get country sales data
frappe.call({
    method: 'api.analytics.get_country_wise_sales',
    args: {
        from_date: '2024-01-01',
        to_date: '2024-12-31'
    },
    callback: function(r) {
        console.log('Country Sales:', r.message);
        // r.message.summary = aggregated data
        // r.message.detailed = monthly breakdown
    }
});
```

### From Python (Backend)

```python
import frappe

# Get HS code profitability
data = frappe.call('api.analytics.get_hs_code_profitability', {
    'from_date': '2024-01-01',
    'to_date': '2024-12-31',
    'filters': '{"country": "United States"}'
})

for row in data:
    print(f"{row['hs_code']}: ${row['gross_profit']}")
```

### From REST API

```bash
# Get executive dashboard
curl -X POST https://your-site.com/api/method/api.analytics.get_executive_dashboard_summary \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "from_date": "2024-01-01",
    "to_date": "2024-12-31"
  }'
```

---

## Troubleshooting

### Reports Not Showing?

**Check if reports were created:**
```bash
bench --site site1.local console
```
```python
import frappe
print(frappe.get_all('Report', filters={'report_type': 'Script Report'}, pluck='name'))
```

**Recreate reports:**
```bash
bench --site site1.local execute quick_analytics_setup.create_reports
```

### No Data in Reports?

**Check if custom fields exist:**
```bash
bench --site site1.local console
```
```python
import frappe
fields = frappe.get_all('Custom Field', 
    filters={'dt': 'Sales Invoice', 'fieldname': 'country_of_destination'})
print(f"Found {len(fields)} custom fields")
```

**Add sample data:**
```bash
bench --site site1.local execute create_sample_analytics_data.create_sample_analytics_data
```

### Permission Errors?

**Grant permissions:**
```bash
bench --site site1.local console
```
```python
import frappe
# Add your user to System Manager role
user = frappe.get_doc('User', 'your.email@example.com')
user.add_roles('System Manager')
frappe.db.commit()
```

### API Not Found?

**Check if analytics.py is in the right place:**
```bash
# Find where it should be
find /path/to/frappe-bench/apps -name "analytics.py"

# Copy it manually
cp api/analytics.py /path/to/frappe-bench/apps/erpnext/erpnext/selling/doctype/
```

**Restart bench:**
```bash
bench restart
```

---

## Next Steps

### 1. Add Real Data

Replace sample data with your actual:
- Sales invoices with countries
- Items with HS codes
- Ocean shipments with dates
- Freight costs

### 2. Customize Reports

Edit `api/analytics.py` to:
- Add custom metrics
- Modify calculations
- Add new filters
- Change groupings

### 3. Schedule Reports

Set up automated report generation:
```python
# Create scheduled job
frappe.get_doc({
    'doctype': 'Scheduled Job Type',
    'method': 'api.analytics.send_executive_summary_email',
    'frequency': 'Daily',
    'cron_format': '0 8 * * *'
}).insert()
```

### 4. Create Dashboards

Build visual dashboards using:
- Chart widgets
- Number cards
- Report links
- Custom HTML

### 5. Export to BI Tools

Connect to:
- Power BI
- Tableau
- Google Data Studio
- Metabase

---

## Support

If you encounter issues:

1. Check the logs:
   ```bash
   tail -f /path/to/frappe-bench/logs/site1.local/error.log
   ```

2. Clear cache:
   ```bash
   bench --site site1.local clear-cache
   ```

3. Rebuild:
   ```bash
   bench --site site1.local migrate
   bench build
   ```

4. Restart:
   ```bash
   bench restart
   ```

---

## Success Checklist

- [ ] Ran setup script successfully
- [ ] Can see reports in Selling/Stock/Accounts modules
- [ ] Can search "Analytics" and find reports
- [ ] HS Code Master doctype exists
- [ ] Custom fields added to Sales Invoice
- [ ] Sample data visible in reports
- [ ] Can run Country-wise Sales Analysis
- [ ] Can run HS Code Profitability
- [ ] Can export reports to Excel
- [ ] API calls work from console

Once all checked, your analytics system is live! 🎉
