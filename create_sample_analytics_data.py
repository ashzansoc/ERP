#!/usr/bin/env python3
"""
Create sample data for analytics reports demonstration
"""

import frappe
from frappe.utils import today, add_days, add_months, flt
import random

def create_sample_analytics_data():
    """Generate sample data to demonstrate analytics reports"""
    
    print("Creating sample analytics data...")
    
    # Create sample countries
    countries = ['United States', 'United Kingdom', 'Germany', 'Japan', 'Australia', 'Canada']
    
    # Create sample HS codes with duty rates
    hs_codes = [
        {'code': '8471.30', 'desc': 'Portable computers', 'duty': 5.5, 'add_duty': 2.0},
        {'code': '8517.12', 'desc': 'Smartphones', 'duty': 0.0, 'add_duty': 0.0},
        {'code': '8528.72', 'desc': 'LCD monitors', 'duty': 3.9, 'add_duty': 1.5},
        {'code': '9403.60', 'desc': 'Wooden furniture', 'duty': 0.0, 'add_duty': 0.0},
        {'code': '6204.62', 'desc': 'Cotton trousers', 'duty': 16.6, 'add_duty': 4.0}
    ]
    
    # Create HS Code Master records
    for country in countries:
        for hs in hs_codes:
            if not frappe.db.exists('HS Code Master', {'hs_code': hs['code'], 'country': country}):
                frappe.get_doc({
                    'doctype': 'HS Code Master',
                    'hs_code': hs['code'],
                    'country': country,
                    'duty_rate': hs['duty'],
                    'additional_duty_rate': hs['add_duty'],
                    'description': hs['desc']
                }).insert(ignore_permissions=True)
    
    print(f"✓ Created {len(countries) * len(hs_codes)} HS Code Master records")
    
    # Create sample customers
    customers = []
    for i, country in enumerate(countries):
        customer_name = f"Customer {country[:3].upper()}-{i+1}"
        if not frappe.db.exists('Customer', customer_name):
            customer = frappe.get_doc({
                'doctype': 'Customer',
                'customer_name': customer_name,
                'customer_type': 'Company',
                'customer_group': 'Commercial',
                'territory': country
            })
            customer.insert(ignore_permissions=True)
            customers.append(customer.name)
        else:
            customers.append(customer_name)
    
    print(f"✓ Created {len(customers)} sample customers")
    
    # Create sample items
    items = []
    for hs in hs_codes:
        item_code = f"ITEM-{hs['code']}"
        if not frappe.db.exists('Item', item_code):
            item = frappe.get_doc({
                'doctype': 'Item',
                'item_code': item_code,
                'item_name': hs['desc'],
                'item_group': 'Products',
                'stock_uom': 'Nos',
                'is_stock_item': 1,
                'valuation_rate': random.randint(100, 500)
            })
            item.insert(ignore_permissions=True)
            items.append({'code': item_code, 'hs': hs['code'], 'rate': random.randint(150, 800)})
        else:
            items.append({'code': item_code, 'hs': hs['code'], 'rate': random.randint(150, 800)})
    
    print(f"✓ Created {len(items)} sample items")
    
    # Create sample sales invoices (last 12 months)
    invoice_count = 0
    for month_offset in range(-12, 0):
        posting_date = add_months(today(), month_offset)
        
        # Create 5-10 invoices per month
        for _ in range(random.randint(5, 10)):
            customer = random.choice(customers)
            country = frappe.db.get_value('Customer', customer, 'territory')
            
            invoice = frappe.get_doc({
                'doctype': 'Sales Invoice',
                'customer': customer,
                'posting_date': posting_date,
                'country_of_destination': country,
                'currency': random.choice(['USD', 'EUR', 'GBP', 'JPY']),
                'conversion_rate': random.uniform(0.8, 1.5),
                'items': []
            })
            
            # Add 1-3 items per invoice
            for _ in range(random.randint(1, 3)):
                item = random.choice(items)
                qty = random.randint(1, 20)
                invoice.append('items', {
                    'item_code': item['code'],
                    'qty': qty,
                    'rate': item['rate'],
                    'hs_code': item['hs']
                })
            
            try:
                invoice.insert(ignore_permissions=True)
                invoice.submit()
                invoice_count += 1
            except Exception as e:
                print(f"  Warning: Could not create invoice: {str(e)}")
    
    print(f"✓ Created {invoice_count} sample sales invoices")
    
    # Create sample ocean shipments
    carriers = ['Maersk', 'MSC', 'CMA CGM', 'Hapag-Lloyd', 'ONE']
    ports_loading = ['Shanghai', 'Singapore', 'Hong Kong', 'Busan']
    ports_discharge = ['Los Angeles', 'Rotterdam', 'Hamburg', 'Tokyo']
    forwarders = ['DHL Global Forwarding', 'Kuehne + Nagel', 'DB Schenker', 'Expeditors']
    
    shipment_count = 0
    for month_offset in range(-6, 0):
        base_date = add_months(today(), month_offset)
        
        for _ in range(random.randint(3, 8)):
            est_departure = add_days(base_date, random.randint(0, 28))
            act_departure = add_days(est_departure, random.randint(-2, 5))
            est_arrival = add_days(est_departure, random.randint(20, 35))
            act_arrival = add_days(est_arrival, random.randint(-3, 7))
            
            shipment = frappe.get_doc({
                'doctype': 'Ocean Shipment',
                'carrier': random.choice(carriers),
                'freight_forwarder': random.choice(forwarders),
                'port_of_loading': random.choice(ports_loading),
                'port_of_discharge': random.choice(ports_discharge),
                'estimated_departure_date': est_departure,
                'actual_departure_date': act_departure,
                'estimated_arrival_date': est_arrival,
                'actual_arrival_date': act_arrival,
                'status': 'Delivered' if act_arrival <= today() else 'In Transit',
                'freight_cost': random.randint(5000, 25000),
                'total_value': random.randint(50000, 500000)
            })
            
            try:
                shipment.insert(ignore_permissions=True)
                shipment_count += 1
            except Exception as e:
                print(f"  Warning: Could not create shipment: {str(e)}")
    
    print(f"✓ Created {shipment_count} sample ocean shipments")
    
    print("\n" + "="*50)
    print("✓ Sample analytics data created successfully!")
    print("="*50)
    print("\nYou can now run the analytics reports to see data.")

if __name__ == '__main__':
    frappe.init(site='site1.local')
    frappe.connect()
    create_sample_analytics_data()
    frappe.db.commit()
