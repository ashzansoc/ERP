# Analytics Reports - Quick Start Guide

## Installation (5 minutes)

```bash
# Run the installation script
./install_analytics_reports.sh site1.local

# Verify installation
bench --site site1.local console
>>> frappe.get_list('Report', filters={'name': ['like', '%Analysis%']})
```

## The 7 Reports That Make It Sellable

### 1. Country-wise Sales 🌍
**What it shows**: Which countries are buying from you and how much
**Why it matters**: Focus on profitable markets, plan expansion

### 2. HS Code Profitability 💰
**What it shows**: Which products make the most money after all costs
**Why it matters**: Optimize product mix, adjust pricing

### 3. Shipment Delay Analytics ⏱️
**What it shows**: Which carriers and routes are reliable
**Why it matters**: Choose better partners, set realistic expectations

### 4. Port Performance 🚢
**What it shows**: Which ports are efficient vs. congested
**Why it matters**: Route optimization, avoid bottlenecks

### 5. Freight Forwarder Comparison 📊
**What it shows**: Cost and performance of each freight partner
**Why it matters**: Negotiate better rates, switch underperformers

### 6. Duty Cost Trends 📈
**What it shows**: How customs duties are impacting your margins
**Why it matters**: Plan for duty changes, optimize trade agreements

### 7. FX Exposure 💱
**What it shows**: Your currency risk across all transactions
**Why it matters**: Hedge properly, avoid FX losses

## Quick Access

### From UI
1. Go to **Selling > Reports** or **Stock > Reports**
2. Find report by name
3. Set date range and filters
4. Click "Run Report"
5. Export to Excel/PDF

### From API
```javascript
// Example: Get country sales
frappe.call({
    method: 'api.analytics.get_country_wise_sales',
    args: {
        from_date: '2024-01-01',
        to_date: '2024-12-31'
    },
    callback: (r) => console.log(r.message)
});
```

## Sample Data Setup

```python
# Add sample HS codes with duty rates
bench --site site1.local console

>>> frappe.get_doc({
    'doctype': 'HS Code Master',
    'hs_code': '8471.30',
    'country': 'United States',
    'duty_rate': 5.5,
    'additional_duty_rate': 2.0,
    'description': 'Portable computers'
}).insert()
```

## Executive Dashboard

Access the summary dashboard:
```python
frappe.call('api.analytics.get_executive_dashboard_summary', {
    from_date: '2024-01-01',
    to_date: '2024-12-31'
})
```

Returns:
- Revenue with growth %
- Shipment metrics
- Top 5 countries
- Compliance status

## Common Use Cases

### Monthly Business Review
1. Run Executive Dashboard
2. Check Country-wise Sales for market trends
3. Review Shipment Delays for operational issues
4. Analyze FX Exposure for risk

### Vendor Negotiations
1. Run Freight Forwarder Comparison
2. Show performance vs. cost data
3. Negotiate based on facts

### Product Strategy
1. Run HS Code Profitability
2. Identify high-margin products
3. Phase out low-margin items

### Compliance Planning
1. Run Duty Cost Trends
2. Forecast duty impact
3. Plan for trade agreement changes

## Troubleshooting

**No data showing?**
- Check date range (use last 12 months)
- Verify Sales Invoices exist with country_of_destination
- Ensure Ocean Shipments have dates filled

**Slow performance?**
- Reduce date range to 3-6 months
- Add database indexes (see full guide)

**Missing fields?**
```bash
bench --site site1.local execute install_analytics_reports.create_analytics_custom_fields
```

## What Makes This Sellable

✅ **Professional**: Industry-standard metrics
✅ **Actionable**: Clear insights for decisions
✅ **Comprehensive**: Covers all aspects of export-import
✅ **Automated**: No manual Excel work
✅ **Scalable**: Works with growing data
✅ **Exportable**: Share with stakeholders
✅ **API-ready**: Integrate with other systems

## Next Steps

1. ✅ Install reports
2. ✅ Populate historical data
3. ✅ Run each report once to verify
4. ✅ Schedule automated daily/weekly reports
5. ✅ Train team on interpretation
6. ✅ Customize for your industry

See **ANALYTICS_REPORTS_GUIDE.md** for complete documentation.
