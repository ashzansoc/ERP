# Analytics Reports System - Complete Guide

## Overview

This analytics system provides 7 industry-standard reports that transform your export-import system into a sellable product with actionable business intelligence.

## Installation

```bash
./install_analytics_reports.sh site1.local
```

## Reports Overview

### 1. Country-wise Sales Analysis

**Purpose**: Track revenue, volume, and trends by destination country

**Key Metrics**:
- Total revenue per country
- Shipment count and volume
- Average order value
- Month-over-month growth trends
- Market share analysis

**API Endpoint**:
```python
frappe.call('api.analytics.get_country_wise_sales', {
    from_date: '2024-01-01',
    to_date: '2024-12-31',
    filters: JSON.stringify({customer: 'ABC Corp'})
})
```

**Use Cases**:
- Identify top-performing markets
- Track market penetration
- Plan regional expansion
- Forecast country-specific demand

---

### 2. HS Code Profitability Analysis

**Purpose**: Analyze profit margins and costs by product classification

**Key Metrics**:
- Revenue per HS code
- Gross profit and margins
- Cost breakdown (COGS + duties)
- Net profitability after duties
- Volume trends

**API Endpoint**:
```python
frappe.call('api.analytics.get_hs_code_profitability', {
    from_date: '2024-01-01',
    to_date: '2024-12-31',
    filters: JSON.stringify({country: 'USA'})
})
```

**Use Cases**:
- Identify most profitable products
- Optimize product mix
- Price optimization
- Duty impact analysis

---

### 3. Shipment Delay Analytics

**Purpose**: Monitor carrier and route performance with delay tracking

**Key Metrics**:
- Departure and arrival delays
- On-time delivery percentage
- Carrier performance comparison
- Route-specific delays
- Delay cost impact

**API Endpoint**:
```python
frappe.call('api.analytics.get_shipment_delay_analytics', {
    from_date: '2024-01-01',
    to_date: '2024-12-31',
    filters: JSON.stringify({carrier: 'Maersk'})
})
```

**Use Cases**:
- Carrier selection and negotiation
- Route optimization
- Customer expectation management
- SLA monitoring

---

### 4. Port Performance Analysis

**Purpose**: Evaluate port efficiency and throughput

**Key Metrics**:
- Average transit time per port pair
- Cargo value throughput
- On-time arrival rates
- Efficiency scores
- Port congestion indicators

**API Endpoint**:
```python
frappe.call('api.analytics.get_port_performance_analysis', {
    from_date: '2024-01-01',
    to_date: '2024-12-31'
})
```

**Use Cases**:
- Port selection optimization
- Route planning
- Capacity planning
- Bottleneck identification

---

### 5. Freight Forwarder Comparison

**Purpose**: Compare freight forwarders on cost, performance, and reliability

**Key Metrics**:
- Average freight cost
- Total freight spend
- On-time delivery percentage
- Average delay days
- Cost per shipment value
- Reliability score

**API Endpoint**:
```python
frappe.call('api.analytics.get_freight_forwarder_comparison', {
    from_date: '2024-01-01',
    to_date: '2024-12-31'
})
```

**Use Cases**:
- Vendor selection and negotiation
- Cost optimization
- Performance benchmarking
- Contract renewal decisions

---

### 6. Duty Cost Trend Report

**Purpose**: Track customs duty costs and trends over time

**Key Metrics**:
- Duty costs by country and HS code
- Duty rate changes over time
- Total duty burden
- Duty as % of invoice value
- Month-over-month trends

**API Endpoint**:
```python
frappe.call('api.analytics.get_duty_cost_trend_report', {
    from_date: '2024-01-01',
    to_date: '2024-12-31',
    filters: JSON.stringify({country: 'India'})
})
```

**Use Cases**:
- Duty optimization strategies
- Trade agreement utilization
- Pricing adjustments
- Compliance planning

---

### 7. FX Exposure Report

**Purpose**: Analyze foreign exchange risk and exposure

**Key Metrics**:
- Currency-wise exposure
- Exchange rate volatility
- Transaction volume by currency
- Rate trends and ranges
- Hedging recommendations

**API Endpoint**:
```python
frappe.call('api.analytics.get_fx_exposure_report', {
    from_date: '2024-01-01',
    to_date: '2024-12-31',
    base_currency: 'USD'
})
```

**Use Cases**:
- FX risk management
- Hedging strategy
- Currency diversification
- Pricing in multiple currencies

---

## Executive Dashboard

**Purpose**: High-level KPIs for management decision-making

**Key Metrics**:
- Total revenue with growth %
- Shipment volume and on-time %
- Top 5 countries by revenue
- Compliance status overview
- Period-over-period comparisons

**API Endpoint**:
```python
frappe.call('api.analytics.get_executive_dashboard_summary', {
    from_date: '2024-01-01',
    to_date: '2024-12-31'
})
```

---

## Integration Examples

### JavaScript (Frontend)

```javascript
// Get country sales data
frappe.call({
    method: 'api.analytics.get_country_wise_sales',
    args: {
        from_date: '2024-01-01',
        to_date: '2024-12-31'
    },
    callback: function(r) {
        if (r.message) {
            console.log('Country Sales:', r.message.summary);
            // Render charts/tables
        }
    }
});
```

### Python (Backend)

```python
import frappe
from api.analytics import get_hs_code_profitability

# Get profitability data
data = get_hs_code_profitability(
    from_date='2024-01-01',
    to_date='2024-12-31',
    filters='{"country": "USA"}'
)

# Process data
for row in data:
    print(f"HS Code: {row['hs_code']}, Profit: {row['gross_profit']}")
```

---

## Data Requirements

### Required Custom Fields

The installation script creates these fields automatically:

**Sales Invoice**:
- `country_of_destination` (Link to Country)

**Sales Invoice Item**:
- `hs_code` (Data)

**Ocean Shipment**:
- `freight_forwarder` (Link to Supplier)
- `freight_cost` (Currency)

### Required Doctypes

- Sales Invoice (standard)
- Ocean Shipment (custom)
- HS Code Master (created by script)
- Landed Cost Voucher (standard)

---

## Report Scheduling

Set up automated report generation:

```python
# Create scheduled job for daily executive summary
frappe.get_doc({
    'doctype': 'Scheduled Job Type',
    'method': 'api.analytics.send_executive_summary_email',
    'frequency': 'Daily',
    'cron_format': '0 8 * * *'  # 8 AM daily
}).insert()
```

---

## Export Options

All reports support multiple export formats:

- **Excel**: Full data with formatting
- **CSV**: Raw data for analysis
- **PDF**: Formatted reports for sharing
- **JSON**: API integration

---

## Performance Optimization

### Indexing

Add these indexes for faster queries:

```sql
ALTER TABLE `tabSales Invoice` ADD INDEX idx_country_date (country_of_destination, posting_date);
ALTER TABLE `tabSales Invoice Item` ADD INDEX idx_hs_code (hs_code);
ALTER TABLE `tabOcean Shipment` ADD INDEX idx_carrier_dates (carrier, actual_arrival_date);
```

### Caching

Reports cache results for 1 hour by default. Clear cache:

```python
frappe.cache().delete_value('analytics_report_*')
```

---

## Customization

### Adding Custom Metrics

Edit `api/analytics.py` to add custom calculations:

```python
@frappe.whitelist()
def get_custom_metric(from_date, to_date):
    # Your custom query
    data = frappe.db.sql("""
        SELECT custom_field, SUM(amount)
        FROM `tabYour DocType`
        WHERE date BETWEEN %s AND %s
        GROUP BY custom_field
    """, [from_date, to_date], as_dict=True)
    
    return data
```

### Creating Custom Reports

1. Copy an existing report function
2. Modify the SQL query
3. Add to `install_analytics_reports.py`
4. Run installation script

---

## Troubleshooting

### Report Returns No Data

- Check date ranges
- Verify doctype permissions
- Ensure custom fields exist
- Check data availability

### Slow Performance

- Add database indexes
- Reduce date range
- Enable query caching
- Optimize SQL queries

### Missing Fields

```bash
# Reinstall custom fields
bench --site site1.local execute install_analytics_reports.create_analytics_custom_fields
```

---

## Business Value

These reports provide:

1. **Data-Driven Decisions**: Replace gut feelings with facts
2. **Cost Optimization**: Identify savings opportunities
3. **Risk Management**: Monitor FX and compliance exposure
4. **Performance Tracking**: Measure KPIs consistently
5. **Competitive Advantage**: Industry-standard analytics
6. **Scalability**: Reports grow with your business
7. **Sellability**: Professional reporting increases product value

---

## Next Steps

1. Install the analytics system
2. Populate historical data
3. Schedule automated reports
4. Train users on report interpretation
5. Customize for your specific needs
6. Integrate with BI tools (Power BI, Tableau)

---

## Support

For issues or customization requests, refer to the main system documentation or contact your implementation team.
