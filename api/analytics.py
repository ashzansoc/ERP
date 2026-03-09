"""
Analytics and Reporting API for Export-Import System
Provides industry-standard reports for business intelligence
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days, get_first_day, get_last_day
from datetime import datetime, timedelta
import json

@frappe.whitelist()
def get_country_wise_sales(from_date=None, to_date=None, filters=None):
    """
    Country-wise sales analysis with revenue, volume, and trends
    """
    if not from_date:
        from_date = add_days(getdate(), -365)
    if not to_date:
        to_date = getdate()
    
    filters_dict = json.loads(filters) if filters else {}
    
    query = """
        SELECT 
            si.country_of_destination as country,
            COUNT(DISTINCT si.name) as shipment_count,
            SUM(si.grand_total) as total_revenue,
            SUM(si.total_qty) as total_quantity,
            AVG(si.grand_total) as avg_order_value,
            MONTH(si.posting_date) as month,
            YEAR(si.posting_date) as year
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        AND si.country_of_destination IS NOT NULL
    """
    
    params = [from_date, to_date]
    
    if filters_dict.get('customer'):
        query += " AND si.customer = %s"
        params.append(filters_dict['customer'])
    
    query += " GROUP BY si.country_of_destination, YEAR(si.posting_date), MONTH(si.posting_date)"
    query += " ORDER BY total_revenue DESC"
    
    data = frappe.db.sql(query, params, as_dict=True)
    
    # Calculate growth trends
    country_summary = {}
    for row in data:
        country = row['country']
        if country not in country_summary:
            country_summary[country] = {
                'country': country,
                'total_revenue': 0,
                'total_quantity': 0,
                'shipment_count': 0,
                'monthly_data': []
            }
        
        country_summary[country]['total_revenue'] += flt(row['total_revenue'])
        country_summary[country]['total_quantity'] += flt(row['total_quantity'])
        country_summary[country]['shipment_count'] += row['shipment_count']
        country_summary[country]['monthly_data'].append({
            'month': row['month'],
            'year': row['year'],
            'revenue': flt(row['total_revenue'])
        })
    
    return {
        'summary': list(country_summary.values()),
        'detailed': data
    }

@frappe.whitelist()
def get_hs_code_profitability(from_date=None, to_date=None, filters=None):
    """
    HS Code profitability analysis with margins and cost breakdown
    """
    if not from_date:
        from_date = add_days(getdate(), -365)
    if not to_date:
        to_date = getdate()
    
    filters_dict = json.loads(filters) if filters else {}
    
    query = """
        SELECT 
            sii.hs_code,
            sii.item_name,
            COUNT(DISTINCT si.name) as invoice_count,
            SUM(sii.qty) as total_quantity,
            SUM(sii.amount) as total_revenue,
            AVG(sii.rate) as avg_selling_price,
            SUM(sii.qty * COALESCE(item.valuation_rate, 0)) as total_cost,
            (SUM(sii.amount) - SUM(sii.qty * COALESCE(item.valuation_rate, 0))) as gross_profit,
            ((SUM(sii.amount) - SUM(sii.qty * COALESCE(item.valuation_rate, 0))) / NULLIF(SUM(sii.amount), 0) * 100) as profit_margin
        FROM `tabSales Invoice Item` sii
        INNER JOIN `tabSales Invoice` si ON sii.parent = si.name
        LEFT JOIN `tabItem` item ON sii.item_code = item.name
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        AND sii.hs_code IS NOT NULL
    """
    
    params = [from_date, to_date]
    
    if filters_dict.get('country'):
        query += " AND si.country_of_destination = %s"
        params.append(filters_dict['country'])
    
    query += " GROUP BY sii.hs_code, sii.item_name"
    query += " ORDER BY gross_profit DESC"
    
    data = frappe.db.sql(query, params, as_dict=True)
    
    # Add duty costs if available
    for row in data:
        duty_query = """
            SELECT SUM(lci.duty_amount) as total_duty
            FROM `tabLanded Cost Item` lci
            INNER JOIN `tabLanded Cost Voucher` lcv ON lci.parent = lcv.name
            WHERE lcv.docstatus = 1
            AND lci.item_code IN (
                SELECT item_code FROM `tabSales Invoice Item` 
                WHERE hs_code = %s AND parent IN (
                    SELECT name FROM `tabSales Invoice` 
                    WHERE posting_date BETWEEN %s AND %s
                )
            )
        """
        duty_result = frappe.db.sql(duty_query, [row['hs_code'], from_date, to_date], as_dict=True)
        row['total_duty'] = flt(duty_result[0]['total_duty']) if duty_result else 0
        row['net_profit'] = flt(row['gross_profit']) - flt(row['total_duty'])
    
    return data

@frappe.whitelist()
def get_shipment_delay_analytics(from_date=None, to_date=None, filters=None):
    """
    Shipment delay analysis with carrier and route performance
    """
    if not from_date:
        from_date = add_days(getdate(), -180)
    if not to_date:
        to_date = getdate()
    
    filters_dict = json.loads(filters) if filters else {}
    
    query = """
        SELECT 
            os.name as shipment_id,
            os.carrier,
            os.port_of_loading,
            os.port_of_discharge,
            os.estimated_departure_date,
            os.actual_departure_date,
            os.estimated_arrival_date,
            os.actual_arrival_date,
            DATEDIFF(os.actual_departure_date, os.estimated_departure_date) as departure_delay_days,
            DATEDIFF(os.actual_arrival_date, os.estimated_arrival_date) as arrival_delay_days,
            os.status,
            os.total_value
        FROM `tabOcean Shipment` os
        WHERE os.creation BETWEEN %s AND %s
        AND os.estimated_departure_date IS NOT NULL
    """
    
    params = [from_date, to_date]
    
    if filters_dict.get('carrier'):
        query += " AND os.carrier = %s"
        params.append(filters_dict['carrier'])
    
    if filters_dict.get('port_of_loading'):
        query += " AND os.port_of_loading = %s"
        params.append(filters_dict['port_of_loading'])
    
    data = frappe.db.sql(query, params, as_dict=True)
    
    # Calculate statistics
    carrier_stats = {}
    route_stats = {}
    
    for row in data:
        carrier = row['carrier'] or 'Unknown'
        route = f"{row['port_of_loading']} → {row['port_of_discharge']}"
        
        if carrier not in carrier_stats:
            carrier_stats[carrier] = {
                'carrier': carrier,
                'total_shipments': 0,
                'delayed_shipments': 0,
                'avg_delay_days': 0,
                'total_delay_days': 0
            }
        
        if route not in route_stats:
            route_stats[route] = {
                'route': route,
                'total_shipments': 0,
                'delayed_shipments': 0,
                'avg_delay_days': 0,
                'total_delay_days': 0
            }
        
        carrier_stats[carrier]['total_shipments'] += 1
        route_stats[route]['total_shipments'] += 1
        
        delay = flt(row.get('arrival_delay_days', 0))
        if delay > 0:
            carrier_stats[carrier]['delayed_shipments'] += 1
            carrier_stats[carrier]['total_delay_days'] += delay
            route_stats[route]['delayed_shipments'] += 1
            route_stats[route]['total_delay_days'] += delay
    
    # Calculate averages
    for stats in carrier_stats.values():
        if stats['total_shipments'] > 0:
            stats['avg_delay_days'] = stats['total_delay_days'] / stats['total_shipments']
            stats['on_time_percentage'] = ((stats['total_shipments'] - stats['delayed_shipments']) / stats['total_shipments']) * 100
    
    for stats in route_stats.values():
        if stats['total_shipments'] > 0:
            stats['avg_delay_days'] = stats['total_delay_days'] / stats['total_shipments']
            stats['on_time_percentage'] = ((stats['total_shipments'] - stats['delayed_shipments']) / stats['total_shipments']) * 100
    
    return {
        'shipments': data,
        'carrier_performance': list(carrier_stats.values()),
        'route_performance': list(route_stats.values())
    }

@frappe.whitelist()
def get_port_performance_analysis(from_date=None, to_date=None):
    """
    Port performance analysis with throughput and efficiency metrics
    """
    if not from_date:
        from_date = add_days(getdate(), -365)
    if not to_date:
        to_date = getdate()
    
    query = """
        SELECT 
            os.port_of_loading,
            os.port_of_discharge,
            COUNT(*) as shipment_count,
            AVG(DATEDIFF(os.actual_arrival_date, os.actual_departure_date)) as avg_transit_days,
            SUM(os.total_value) as total_cargo_value,
            AVG(os.total_value) as avg_cargo_value,
            SUM(CASE WHEN DATEDIFF(os.actual_arrival_date, os.estimated_arrival_date) <= 0 THEN 1 ELSE 0 END) as on_time_arrivals
        FROM `tabOcean Shipment` os
        WHERE os.creation BETWEEN %s AND %s
        AND os.actual_departure_date IS NOT NULL
        AND os.actual_arrival_date IS NOT NULL
        GROUP BY os.port_of_loading, os.port_of_discharge
        ORDER BY shipment_count DESC
    """
    
    data = frappe.db.sql(query, [from_date, to_date], as_dict=True)
    
    # Calculate performance scores
    for row in data:
        row['on_time_percentage'] = (flt(row['on_time_arrivals']) / flt(row['shipment_count'])) * 100 if row['shipment_count'] > 0 else 0
        row['efficiency_score'] = min(100, (row['on_time_percentage'] * 0.7) + ((30 / max(1, row['avg_transit_days'])) * 30))
    
    return data

@frappe.whitelist()
def get_freight_forwarder_comparison(from_date=None, to_date=None):
    """
    Freight forwarder comparison with cost, performance, and reliability metrics
    """
    if not from_date:
        from_date = add_days(getdate(), -365)
    if not to_date:
        to_date = getdate()
    
    query = """
        SELECT 
            os.freight_forwarder,
            os.carrier,
            COUNT(*) as total_shipments,
            AVG(os.freight_cost) as avg_freight_cost,
            SUM(os.freight_cost) as total_freight_cost,
            AVG(DATEDIFF(os.actual_arrival_date, os.estimated_arrival_date)) as avg_delay_days,
            SUM(CASE WHEN os.actual_arrival_date <= os.estimated_arrival_date THEN 1 ELSE 0 END) as on_time_deliveries,
            AVG(os.total_value) as avg_shipment_value
        FROM `tabOcean Shipment` os
        WHERE os.creation BETWEEN %s AND %s
        AND os.freight_forwarder IS NOT NULL
        AND os.actual_arrival_date IS NOT NULL
        GROUP BY os.freight_forwarder, os.carrier
        ORDER BY total_shipments DESC
    """
    
    data = frappe.db.sql(query, [from_date, to_date], as_dict=True)
    
    # Calculate performance metrics
    for row in data:
        row['on_time_percentage'] = (flt(row['on_time_deliveries']) / flt(row['total_shipments'])) * 100 if row['total_shipments'] > 0 else 0
        row['cost_per_value'] = (flt(row['avg_freight_cost']) / flt(row['avg_shipment_value'])) * 100 if row['avg_shipment_value'] > 0 else 0
        row['reliability_score'] = min(100, row['on_time_percentage'] * 0.8 + (20 if row['avg_delay_days'] <= 1 else 0))
    
    return data

@frappe.whitelist()
def get_duty_cost_trend_report(from_date=None, to_date=None, filters=None):
    """
    Duty cost trend analysis with country and HS code breakdown
    """
    if not from_date:
        from_date = add_days(getdate(), -365)
    if not to_date:
        to_date = getdate()
    
    filters_dict = json.loads(filters) if filters else {}
    
    query = """
        SELECT 
            si.country_of_destination as country,
            sii.hs_code,
            MONTH(si.posting_date) as month,
            YEAR(si.posting_date) as year,
            SUM(sii.amount) as invoice_value,
            COUNT(DISTINCT si.name) as invoice_count
        FROM `tabSales Invoice Item` sii
        INNER JOIN `tabSales Invoice` si ON sii.parent = si.name
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        AND sii.hs_code IS NOT NULL
    """
    
    params = [from_date, to_date]
    
    if filters_dict.get('country'):
        query += " AND si.country_of_destination = %s"
        params.append(filters_dict['country'])
    
    query += " GROUP BY si.country_of_destination, sii.hs_code, YEAR(si.posting_date), MONTH(si.posting_date)"
    query += " ORDER BY year DESC, month DESC"
    
    data = frappe.db.sql(query, params, as_dict=True)
    
    # Get duty rates from compliance system
    for row in data:
        duty_rate_query = """
            SELECT duty_rate, additional_duty_rate
            FROM `tabHS Code Master`
            WHERE hs_code = %s AND country = %s
            LIMIT 1
        """
        duty_rate = frappe.db.sql(duty_rate_query, [row['hs_code'], row['country']], as_dict=True)
        
        if duty_rate:
            row['duty_rate'] = flt(duty_rate[0].get('duty_rate', 0))
            row['additional_duty_rate'] = flt(duty_rate[0].get('additional_duty_rate', 0))
            row['estimated_duty'] = flt(row['invoice_value']) * (flt(row['duty_rate']) / 100)
            row['total_duty_cost'] = row['estimated_duty'] * (1 + flt(row['additional_duty_rate']) / 100)
        else:
            row['duty_rate'] = 0
            row['estimated_duty'] = 0
            row['total_duty_cost'] = 0
    
    return data

@frappe.whitelist()
def get_fx_exposure_report(from_date=None, to_date=None, base_currency=None):
    """
    Foreign exchange exposure analysis with currency-wise breakdown
    """
    if not from_date:
        from_date = add_days(getdate(), -180)
    if not to_date:
        to_date = getdate()
    
    if not base_currency:
        base_currency = frappe.defaults.get_global_default('currency') or 'USD'
    
    query = """
        SELECT 
            si.currency,
            si.country_of_destination as country,
            COUNT(*) as transaction_count,
            SUM(si.grand_total) as total_amount_foreign,
            SUM(si.base_grand_total) as total_amount_base,
            AVG(si.conversion_rate) as avg_exchange_rate,
            MIN(si.conversion_rate) as min_exchange_rate,
            MAX(si.conversion_rate) as max_exchange_rate,
            MONTH(si.posting_date) as month,
            YEAR(si.posting_date) as year
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        AND si.currency != %s
        GROUP BY si.currency, si.country_of_destination, YEAR(si.posting_date), MONTH(si.posting_date)
        ORDER BY total_amount_base DESC
    """
    
    data = frappe.db.sql(query, [from_date, to_date, base_currency], as_dict=True)
    
    # Calculate FX exposure metrics
    currency_summary = {}
    for row in data:
        currency = row['currency']
        if currency not in currency_summary:
            currency_summary[currency] = {
                'currency': currency,
                'total_exposure': 0,
                'transaction_count': 0,
                'volatility': 0,
                'countries': []
            }
        
        currency_summary[currency]['total_exposure'] += flt(row['total_amount_base'])
        currency_summary[currency]['transaction_count'] += row['transaction_count']
        
        if row['country'] not in currency_summary[currency]['countries']:
            currency_summary[currency]['countries'].append(row['country'])
        
        # Calculate volatility
        rate_range = flt(row['max_exchange_rate']) - flt(row['min_exchange_rate'])
        volatility = (rate_range / flt(row['avg_exchange_rate'])) * 100 if row['avg_exchange_rate'] > 0 else 0
        currency_summary[currency]['volatility'] = max(currency_summary[currency]['volatility'], volatility)
    
    return {
        'detailed': data,
        'summary': list(currency_summary.values()),
        'base_currency': base_currency
    }

@frappe.whitelist()
def get_executive_dashboard_summary(from_date=None, to_date=None):
    """
    Executive dashboard with key metrics and KPIs
    """
    if not from_date:
        from_date = add_days(getdate(), -30)
    if not to_date:
        to_date = getdate()
    
    # Get previous period for comparison
    period_days = (getdate(to_date) - getdate(from_date)).days
    prev_from_date = add_days(from_date, -period_days)
    prev_to_date = from_date
    
    summary = {}
    
    # Total revenue
    revenue_query = """
        SELECT 
            SUM(grand_total) as total_revenue,
            COUNT(*) as invoice_count,
            AVG(grand_total) as avg_invoice_value
        FROM `tabSales Invoice`
        WHERE docstatus = 1 AND posting_date BETWEEN %s AND %s
    """
    current_revenue = frappe.db.sql(revenue_query, [from_date, to_date], as_dict=True)[0]
    prev_revenue = frappe.db.sql(revenue_query, [prev_from_date, prev_to_date], as_dict=True)[0]
    
    summary['revenue'] = {
        'current': flt(current_revenue['total_revenue']),
        'previous': flt(prev_revenue['total_revenue']),
        'growth': ((flt(current_revenue['total_revenue']) - flt(prev_revenue['total_revenue'])) / flt(prev_revenue['total_revenue']) * 100) if prev_revenue['total_revenue'] > 0 else 0,
        'invoice_count': current_revenue['invoice_count'],
        'avg_value': flt(current_revenue['avg_invoice_value'])
    }
    
    # Shipment metrics
    shipment_query = """
        SELECT 
            COUNT(*) as total_shipments,
            SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) as delivered,
            SUM(CASE WHEN actual_arrival_date <= estimated_arrival_date THEN 1 ELSE 0 END) as on_time
        FROM `tabOcean Shipment`
        WHERE creation BETWEEN %s AND %s
    """
    shipments = frappe.db.sql(shipment_query, [from_date, to_date], as_dict=True)[0]
    
    summary['shipments'] = {
        'total': shipments['total_shipments'],
        'delivered': shipments['delivered'],
        'on_time_percentage': (flt(shipments['on_time']) / flt(shipments['total_shipments']) * 100) if shipments['total_shipments'] > 0 else 0
    }
    
    # Top countries
    top_countries = frappe.db.sql("""
        SELECT country_of_destination, SUM(grand_total) as revenue
        FROM `tabSales Invoice`
        WHERE docstatus = 1 AND posting_date BETWEEN %s AND %s
        GROUP BY country_of_destination
        ORDER BY revenue DESC
        LIMIT 5
    """, [from_date, to_date], as_dict=True)
    
    summary['top_countries'] = top_countries
    
    # Compliance status
    compliance_query = """
        SELECT 
            COUNT(*) as total_schemes,
            SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_schemes,
            SUM(CASE WHEN expiry_date < CURDATE() THEN 1 ELSE 0 END) as expired_schemes
        FROM `tabCompliance Scheme`
    """
    compliance = frappe.db.sql(compliance_query, as_dict=True)[0]
    
    summary['compliance'] = compliance
    
    return summary
