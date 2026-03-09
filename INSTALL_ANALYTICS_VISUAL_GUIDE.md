# 📊 Analytics Installation - Visual Step-by-Step Guide

## 🎯 Goal
Install 7 professional analytics reports in your ERP in under 3 minutes.

---

## 📋 Prerequisites

✅ Frappe/ERPNext installed and running  
✅ Access to terminal/command line  
✅ Site name (usually `site1.local`)  
✅ System Manager permissions  

---

## 🚀 Installation Steps

### Step 1: Open Terminal
```
┌─────────────────────────────────────┐
│ $ cd /path/to/frappe-bench          │
│                                     │
│ You should see:                     │
│ ├── apps/                           │
│ ├── sites/                          │
│ ├── config/                         │
│ └── ...                             │
└─────────────────────────────────────┘
```

### Step 2: Copy Setup File
```bash
# Option A: If project is in parent directory
cp ../ERP2/quick_analytics_setup.py .

# Option B: If project is elsewhere
cp /full/path/to/ERP2/quick_analytics_setup.py .
```

```
✓ File copied to bench directory
```

### Step 3: Run Installation
```bash
bench --site site1.local execute quick_analytics_setup.setup_analytics
```

```
You'll see:
============================================================
ANALYTICS SYSTEM SETUP
============================================================

→ Creating HS Code Master DocType...
  ✓ HS Code Master created
→ Adding custom fields...
  ✓ Custom fields added
→ Creating analytics reports...
  ✓ Country-wise Sales Analysis
  ✓ HS Code Profitability
  ✓ Shipment Delay Analytics
  ✓ Port Performance Analysis
  ✓ Freight Forwarder Comparison
  ✓ Duty Cost Trend Analysis
  ✓ FX Exposure Analysis
→ Creating Analytics workspace...
  ✓ Analytics workspace created
→ Creating sample data...
  ✓ Created 9 HS Code Master records
  ✓ Sample data ready

============================================================
✓ ANALYTICS SYSTEM READY!
============================================================
```

### Step 4: Verify in Browser

**Open your ERP:**
```
http://localhost:8000
```

**Login and navigate:**
```
┌─────────────────────────────────────────────────┐
│  ERPNext                            [Search] 🔍  │
├─────────────────────────────────────────────────┤
│                                                 │
│  Home > Selling > Reports                       │
│                                                 │
│  📊 Reports                                      │
│  ├─ Country-wise Sales Analysis      ← NEW!    │
│  ├─ HS Code Profitability            ← NEW!    │
│  └─ ...                                         │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Accessing Reports

### Method 1: From Modules

```
┌──────────────────────────────────────┐
│ 1. Click "Selling" module            │
│    ↓                                 │
│ 2. Scroll to "Reports" section       │
│    ↓                                 │
│ 3. Click report name                 │
│    ↓                                 │
│ 4. Set date range                    │
│    ↓                                 │
│ 5. Click "Run Report"                │
└──────────────────────────────────────┘
```

### Method 2: Search Bar

```
┌──────────────────────────────────────┐
│ 1. Press Ctrl+K (or Cmd+K on Mac)   │
│    ↓                                 │
│ 2. Type "Country"                    │
│    ↓                                 │
│ 3. See: Country-wise Sales Analysis  │
│    ↓                                 │
│ 4. Press Enter                       │
└──────────────────────────────────────┘
```

### Method 3: Direct URL

```
http://localhost:8000/app/query-report/Country-wise%20Sales%20Analysis
```

---

## 📊 Report Locations Map

```
ERPNext
│
├─ 📁 Selling Module
│  └─ 📊 Reports
│     ├─ Country-wise Sales Analysis
│     └─ HS Code Profitability
│
├─ 📁 Stock Module
│  └─ 📊 Reports
│     ├─ Shipment Delay Analytics
│     ├─ Port Performance Analysis
│     └─ Freight Forwarder Comparison
│
└─ 📁 Accounts Module
   └─ 📊 Reports
      ├─ Duty Cost Trend Analysis
      └─ FX Exposure Analysis
```

---

## 🎯 Running Your First Report

### Example: Country-wise Sales Analysis

```
Step 1: Navigate
┌─────────────────────────────────────┐
│ Selling > Reports >                 │
│ Country-wise Sales Analysis         │
└─────────────────────────────────────┘

Step 2: Set Filters
┌─────────────────────────────────────┐
│ From Date: [2024-01-01]             │
│ To Date:   [2024-12-31]             │
│ Customer:  [Leave blank]            │
└─────────────────────────────────────┘

Step 3: Run
┌─────────────────────────────────────┐
│         [Run Report] 🚀              │
└─────────────────────────────────────┘

Step 4: View Results
┌─────────────────────────────────────────────────────────┐
│ Country        │ Shipments │ Revenue    │ Avg Order    │
├────────────────┼───────────┼────────────┼──────────────┤
│ United States  │    45     │ $450,000   │ $10,000      │
│ United Kingdom │    32     │ $320,000   │ $10,000      │
│ Germany        │    28     │ $280,000   │ $10,000      │
└─────────────────────────────────────────────────────────┘

Step 5: Export
┌─────────────────────────────────────┐
│ [Excel] [CSV] [PDF] [Print]         │
└─────────────────────────────────────┘
```

---

## 🔍 What Each Report Shows

### 1. Country-wise Sales Analysis 🌍
```
Shows:
├─ Revenue by country
├─ Shipment counts
├─ Average order values
├─ Quantity totals
└─ Monthly trends

Use for:
├─ Market analysis
├─ Expansion planning
└─ Sales forecasting
```

### 2. HS Code Profitability 💰
```
Shows:
├─ Revenue per HS code
├─ Cost breakdown
├─ Profit margins
├─ Duty impacts
└─ Net profitability

Use for:
├─ Product mix optimization
├─ Pricing strategy
└─ Margin analysis
```

### 3. Shipment Delay Analytics ⏱️
```
Shows:
├─ Carrier performance
├─ Route delays
├─ On-time percentages
├─ Delay patterns
└─ Cost impacts

Use for:
├─ Carrier selection
├─ Route optimization
└─ SLA monitoring
```

### 4. Port Performance Analysis 🚢
```
Shows:
├─ Port efficiency scores
├─ Transit times
├─ Throughput metrics
├─ Congestion levels
└─ On-time rates

Use for:
├─ Port selection
├─ Route planning
└─ Capacity planning
```

### 5. Freight Forwarder Comparison 📦
```
Shows:
├─ Cost comparison
├─ Performance scores
├─ Reliability metrics
├─ On-time delivery
└─ Cost efficiency

Use for:
├─ Vendor selection
├─ Contract negotiation
└─ Cost optimization
```

### 6. Duty Cost Trend Analysis 📈
```
Shows:
├─ Duty costs over time
├─ Rates by country/HS code
├─ Duty burden %
├─ Trend analysis
└─ Forecasts

Use for:
├─ Compliance planning
├─ Cost forecasting
└─ Trade agreement analysis
```

### 7. FX Exposure Analysis 💱
```
Shows:
├─ Currency exposure
├─ Exchange rate volatility
├─ Transaction volumes
├─ Risk metrics
└─ Hedging needs

Use for:
├─ FX risk management
├─ Hedging strategy
└─ Currency planning
```

---

## ✅ Success Checklist

After installation, verify:

```
□ Can access Selling > Reports
□ See "Country-wise Sales Analysis" in list
□ See "HS Code Profitability" in list
□ Can access Stock > Reports
□ See shipment-related reports
□ Can access Accounts > Reports
□ See financial reports
□ Can search "Analytics" in search bar
□ Can run a report successfully
□ Can see sample data in reports
□ Can export report to Excel
□ HS Code Master doctype exists
□ Custom fields added to Sales Invoice
```

**All checked? You're ready to go! 🎉**

---

## 🆘 Quick Troubleshooting

### Problem: Reports not showing
```bash
# Solution 1: Clear cache
bench --site site1.local clear-cache
bench restart

# Solution 2: Recreate reports
bench --site site1.local execute quick_analytics_setup.create_reports
```

### Problem: No data in reports
```bash
# Solution: Add sample data
bench --site site1.local execute create_sample_analytics_data.create_sample_analytics_data
```

### Problem: Permission denied
```bash
# Solution: Add System Manager role
bench --site site1.local console
```
```python
import frappe
user = frappe.get_doc('User', 'Administrator')
# Or your email: frappe.get_doc('User', 'your@email.com')
```

### Problem: Installation failed
```bash
# Solution: Check logs
tail -f logs/site1.local/error.log

# Then retry
bench --site site1.local execute quick_analytics_setup.setup_analytics
```

---

## 🎓 Next Steps

### 1. Explore Each Report
```
□ Run Country-wise Sales Analysis
□ Run HS Code Profitability
□ Run Shipment Delay Analytics
□ Run Port Performance Analysis
□ Run Freight Forwarder Comparison
□ Run Duty Cost Trend Analysis
□ Run FX Exposure Analysis
```

### 2. Add Real Data
```
□ Add countries to Sales Invoices
□ Add HS codes to items
□ Create Ocean Shipments with dates
□ Add freight costs
□ Add duty rates to HS Code Master
```

### 3. Customize
```
□ Modify report filters
□ Add custom metrics
□ Create dashboards
□ Schedule automated reports
```

### 4. Train Team
```
□ Show sales team country reports
□ Show operations team shipment reports
□ Show finance team duty/FX reports
□ Show management executive dashboard
```

---

## 📚 Documentation

For more details, see:

- **ANALYTICS_README.md** - Complete overview
- **ANALYTICS_IMPLEMENTATION.md** - Technical guide
- **ANALYTICS_REPORTS_GUIDE.md** - Full documentation
- **ANALYTICS_QUICK_START.md** - User guide

---

## 🎉 You're Done!

```
╔═══════════════════════════════════════════════╗
║                                               ║
║   ✓ Analytics System Installed                ║
║   ✓ 7 Reports Available                       ║
║   ✓ Sample Data Created                       ║
║   ✓ Ready to Use                              ║
║                                               ║
║   Your ERP now has professional               ║
║   business intelligence capabilities!         ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

**Start exploring your reports now!** 🚀
