"""
Landed Cost Automation API
Provides calculation engine and API endpoints for automated landed cost calculation
"""
import frappe
from frappe import _
from frappe.utils import flt, nowdate, get_datetime
import json

class LandedCostCalculator:
    """Main calculation engine for landed cost automation"""
    
    def __init__(self, shipment):
        self.shipment = shipment
        self.items = shipment.items or []
        self.cost_components = shipment.cost_components or []
        self.base_currency = shipment.base_currency or "USD"
        self.previous_total = shipment.total_landed_cost or 0
        
    def calculate_all(self):
        """Main calculation orchestrator"""
        try:
            # Step 1: Validate data
            self.validate_data()
            
            # Step 2: Convert all costs to base currency
            self.convert_currencies()
            
            # Step 3: Calculate customs duties
            self.calculate_customs_duties()
            
            # Step 4: Allocate freight costs
            self.allocate_freight()
            
            # Step 5: Allocate insurance costs
            self.allocate_insurance()
            
            # Step 6: Allocate CHA fees
            self.allocate_cha_fees()
            
            # Step 7: Allocate port charges
            self.allocate_port_charges()
            
            # Step 8: Calculate total landed cost per item
            self.calculate_total_landed_cost()
            
            # Step 9: Update shipment totals
            self.update_shipment_totals()
            
            # Step 10: Log the calculation
            self.log_calculation("Manual")
            
            return True, "Landed cost calculated successfully"
            
        except Exception as e:
            frappe.log_error(f"Landed Cost Calculation Error: {str(e)}")
            return False, str(e)
    
    def validate_data(self):
        """Validate data before calculation"""
        if not self.items:
            frappe.throw(_("No items found in shipment"))
        
        for item in self.items:
            if not item.quantity or item.quantity <= 0:
                frappe.throw(_("Item {0} has invalid quantity").format(item.item_code))
            
            if not item.base_cost or item.base_cost < 0:
                frappe.throw(_("Item {0} has invalid base cost").format(item.item_code))
        
        for cost in self.cost_components:
            if not cost.amount or cost.amount < 0:
                frappe.throw(_("Cost component {0} has invalid amount").format(cost.description))
    
    def convert_currencies(self):
        """Convert all cost components to base currency"""
        for cost in self.cost_components:
            if cost.currency != self.base_currency:
                exchange_rate = get_exchange_rate(
                    cost.currency,
                    self.base_currency,
                    self.shipment.shipment_date or nowdate()
                )
                
                if not exchange_rate:
                    frappe.msgprint(
                        _("Exchange rate not found for {0} to {1}. Using rate 1.0").format(
                            cost.currency, self.base_currency
                        ),
                        indicator="orange"
                    )
                    exchange_rate = 1.0
                
                cost.exchange_rate = exchange_rate
                cost.amount_in_base_currency = flt(cost.amount * exchange_rate, 2)
            else:
                cost.exchange_rate = 1.0
                cost.amount_in_base_currency = cost.amount
    
    def calculate_customs_duties(self):
        """Calculate customs duty for each item based on HS code"""
        for item in self.items:
            # Calculate total weight and volume
            item.total_weight = flt(item.weight_per_unit * item.quantity, 3)
            item.total_volume = flt(item.volume_per_unit * item.quantity, 3)
            
            if item.hs_code:
                duty_rate = get_duty_rate(
                    item.hs_code,
                    self.shipment.get("country_of_origin"),
                    self.shipment.get("destination_country"),
                    self.shipment.shipment_date or nowdate()
                )
                
                if duty_rate is not None:
                    item.duty_rate = duty_rate
                    customs_value = item.customs_value or item.base_cost
                    item.customs_duty = flt(customs_value * (duty_rate / 100), 2)
                else:
                    item.duty_rate = 0
                    item.customs_duty = 0
                    frappe.msgprint(
                        _("Duty rate not found for HS Code {0}. Please set manually.").format(item.hs_code),
                        indicator="orange"
                    )
            else:
                item.duty_rate = 0
                item.customs_duty = 0
    
    def allocate_freight(self):
        """Allocate freight costs based on configured method"""
        freight_costs = sum(
            flt(c.amount_in_base_currency) 
            for c in self.cost_components 
            if c.cost_type == "Freight"
        )
        
        if freight_costs > 0:
            method = self.shipment.freight_allocation_method or "Weight"
            
            if method == "Weight":
                self.allocate_by_weight(freight_costs, "allocated_freight")
            elif method == "Volume":
                self.allocate_by_volume(freight_costs, "allocated_freight")
            elif method == "Value":
                self.allocate_by_value(freight_costs, "allocated_freight")
    
    def allocate_insurance(self):
        """Allocate insurance costs based on declared value"""
        insurance_costs = sum(
            flt(c.amount_in_base_currency) 
            for c in self.cost_components 
            if c.cost_type == "Insurance"
        )
        
        if insurance_costs > 0:
            self.allocate_by_value(insurance_costs, "allocated_insurance", use_declared_value=True)
    
    def allocate_cha_fees(self):
        """Allocate CHA fees based on configured method"""
        cha_costs = sum(
            flt(c.amount_in_base_currency) 
            for c in self.cost_components 
            if c.cost_type == "CHA Fees"
        )
        
        if cha_costs > 0:
            method = self.shipment.cha_allocation_method or "Customs Value"
            
            if method == "Customs Value":
                self.allocate_by_value(cha_costs, "allocated_cha_fees", use_customs_value=True)
            elif method == "Equal":
                self.allocate_equally(cha_costs, "allocated_cha_fees")
    
    def allocate_port_charges(self):
        """Allocate port charges based on configured method"""
        port_costs = sum(
            flt(c.amount_in_base_currency) 
            for c in self.cost_components 
            if c.cost_type == "Port Charges"
        )
        
        if port_costs > 0:
            method = self.shipment.port_allocation_method or "Weight"
            
            if method == "Weight":
                self.allocate_by_weight(port_costs, "allocated_port_charges")
            elif method == "Volume":
                self.allocate_by_volume(port_costs, "allocated_port_charges")
    
    def allocate_by_weight(self, total_cost, target_field):
        """Allocate cost proportionally based on item weight"""
        total_weight = sum(flt(item.total_weight) for item in self.items)
        
        if total_weight > 0:
            allocated_sum = 0
            for i, item in enumerate(self.items):
                if i == len(self.items) - 1:
                    # Last item gets the remainder to avoid rounding issues
                    setattr(item, target_field, flt(total_cost - allocated_sum, 2))
                else:
                    weight_ratio = flt(item.total_weight) / total_weight
                    allocated = flt(total_cost * weight_ratio, 2)
                    setattr(item, target_field, allocated)
                    allocated_sum += allocated
        else:
            frappe.msgprint(
                _("Total weight is zero. Cannot allocate {0} by weight.").format(target_field),
                indicator="orange"
            )
            for item in self.items:
                setattr(item, target_field, 0)
    
    def allocate_by_volume(self, total_cost, target_field):
        """Allocate cost proportionally based on item volume"""
        total_volume = sum(flt(item.total_volume) for item in self.items)
        
        if total_volume > 0:
            allocated_sum = 0
            for i, item in enumerate(self.items):
                if i == len(self.items) - 1:
                    setattr(item, target_field, flt(total_cost - allocated_sum, 2))
                else:
                    volume_ratio = flt(item.total_volume) / total_volume
                    allocated = flt(total_cost * volume_ratio, 2)
                    setattr(item, target_field, allocated)
                    allocated_sum += allocated
        else:
            frappe.msgprint(
                _("Total volume is zero. Cannot allocate {0} by volume.").format(target_field),
                indicator="orange"
            )
            for item in self.items:
                setattr(item, target_field, 0)
    
    def allocate_by_value(self, total_cost, target_field, use_customs_value=False, use_declared_value=False):
        """Allocate cost proportionally based on item value"""
        total_value = 0
        
        for item in self.items:
            if use_declared_value:
                value = flt(item.declared_value) or flt(item.base_cost)
            elif use_customs_value:
                value = flt(item.customs_value) or flt(item.base_cost)
            else:
                value = flt(item.base_cost)
            total_value += value
        
        if total_value > 0:
            allocated_sum = 0
            for i, item in enumerate(self.items):
                if use_declared_value:
                    value = flt(item.declared_value) or flt(item.base_cost)
                elif use_customs_value:
                    value = flt(item.customs_value) or flt(item.base_cost)
                else:
                    value = flt(item.base_cost)
                
                if i == len(self.items) - 1:
                    setattr(item, target_field, flt(total_cost - allocated_sum, 2))
                else:
                    value_ratio = value / total_value
                    allocated = flt(total_cost * value_ratio, 2)
                    setattr(item, target_field, allocated)
                    allocated_sum += allocated
        else:
            for item in self.items:
                setattr(item, target_field, 0)
    
    def allocate_equally(self, total_cost, target_field):
        """Distribute cost equally across all items"""
        item_count = len(self.items)
        
        if item_count > 0:
            cost_per_item = flt(total_cost / item_count, 2)
            allocated_sum = 0
            
            for i, item in enumerate(self.items):
                if i == len(self.items) - 1:
                    # Last item gets the remainder
                    setattr(item, target_field, flt(total_cost - allocated_sum, 2))
                else:
                    setattr(item, target_field, cost_per_item)
                    allocated_sum += cost_per_item
    
    def calculate_total_landed_cost(self):
        """Calculate total landed cost for each item"""
        for item in self.items:
            item.total_landed_cost = flt(
                flt(item.base_cost) +
                flt(item.allocated_freight) +
                flt(item.allocated_insurance) +
                flt(item.customs_duty) +
                flt(item.allocated_cha_fees) +
                flt(item.allocated_port_charges),
                2
            )
            
            if item.quantity > 0:
                item.unit_landed_cost = flt(item.total_landed_cost / item.quantity, 2)
            else:
                item.unit_landed_cost = 0
    
    def update_shipment_totals(self):
        """Update shipment-level totals"""
        self.shipment.total_freight = sum(
            flt(c.amount_in_base_currency) 
            for c in self.cost_components 
            if c.cost_type == "Freight"
        )
        
        self.shipment.total_insurance = sum(
            flt(c.amount_in_base_currency) 
            for c in self.cost_components 
            if c.cost_type == "Insurance"
        )
        
        self.shipment.total_customs_duty = sum(flt(item.customs_duty) for item in self.items)
        
        self.shipment.total_cha_fees = sum(
            flt(c.amount_in_base_currency) 
            for c in self.cost_components 
            if c.cost_type == "CHA Fees"
        )
        
        self.shipment.total_port_charges = sum(
            flt(c.amount_in_base_currency) 
            for c in self.cost_components 
            if c.cost_type == "Port Charges"
        )
        
        self.shipment.total_landed_cost = sum(flt(item.total_landed_cost) for item in self.items)
    
    def log_calculation(self, trigger_reason):
        """Log the calculation for audit trail"""
        try:
            calculation_details = {
                "items_count": len(self.items),
                "cost_components_count": len(self.cost_components),
                "allocation_methods": {
                    "freight": self.shipment.freight_allocation_method,
                    "cha": self.shipment.cha_allocation_method,
                    "port": self.shipment.port_allocation_method,
                },
                "totals": {
                    "freight": self.shipment.total_freight,
                    "insurance": self.shipment.total_insurance,
                    "customs_duty": self.shipment.total_customs_duty,
                    "cha_fees": self.shipment.total_cha_fees,
                    "port_charges": self.shipment.total_port_charges,
                    "total_landed_cost": self.shipment.total_landed_cost,
                }
            }
            
            log = frappe.get_doc({
                "doctype": "Landed Cost Calculation Log",
                "shipment": self.shipment.name,
                "calculation_date": get_datetime(),
                "triggered_by": frappe.session.user,
                "trigger_reason": trigger_reason,
                "calculation_details": json.dumps(calculation_details, indent=2),
                "previous_total": self.previous_total,
                "new_total": self.shipment.total_landed_cost,
            })
            log.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Failed to log calculation: {str(e)}")


# Utility Functions

def get_exchange_rate(from_currency, to_currency, date):
    """Get exchange rate from ERPNext"""
    if from_currency == to_currency:
        return 1.0
    
    try:
        from erpnext.setup.utils import get_exchange_rate as erpnext_get_exchange_rate
        return erpnext_get_exchange_rate(from_currency, to_currency, date)
    except:
        # Fallback: query Currency Exchange table
        rate = frappe.db.get_value(
            "Currency Exchange",
            {"from_currency": from_currency, "to_currency": to_currency},
            "exchange_rate"
        )
        return flt(rate) if rate else None


def get_duty_rate(hs_code, origin_country, dest_country, date):
    """Get duty rate for HS code"""
    if not hs_code:
        return None
    
    # Get HS Code document
    if not frappe.db.exists("HS Code", hs_code):
        return None
    
    hs_doc = frappe.get_doc("HS Code", hs_code)
    
    # Find applicable duty rate
    for rate in hs_doc.duty_rates:
        # Check country match
        if origin_country and rate.country_of_origin != origin_country:
            continue
        if dest_country and rate.destination_country != dest_country:
            continue
        
        # Check date validity
        if rate.valid_from and date < rate.valid_from:
            continue
        if rate.valid_to and date > rate.valid_to:
            continue
        
        return flt(rate.duty_rate) + flt(rate.additional_duty or 0)
    
    return None


# API Endpoints

@frappe.whitelist()
def calculate_landed_cost(shipment_name):
    """
    API endpoint to calculate landed cost for a shipment
    """
    try:
        shipment = frappe.get_doc("Ocean Shipment", shipment_name)
        
        # Check permissions
        if not shipment.has_permission("write"):
            frappe.throw(_("No permission to modify this shipment"))
        
        calculator = LandedCostCalculator(shipment)
        success, message = calculator.calculate_all()
        
        if success:
            shipment.save()
            frappe.db.commit()
            return {
                "success": True,
                "message": message,
                "total_landed_cost": shipment.total_landed_cost
            }
        else:
            return {
                "success": False,
                "message": message
            }
    
    except Exception as e:
        frappe.log_error(f"Calculate Landed Cost API Error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_duty_rate_api(hs_code, origin_country=None, dest_country=None, date=None):
    """
    API endpoint to get duty rate for HS code
    """
    if not date:
        date = nowdate()
    
    duty_rate = get_duty_rate(hs_code, origin_country, dest_country, date)
    
    return {
        "hs_code": hs_code,
        "duty_rate": duty_rate,
        "origin_country": origin_country,
        "dest_country": dest_country,
        "date": date
    }


@frappe.whitelist()
def create_landed_cost_voucher_from_shipment(shipment_name):
    """
    Create Landed Cost Voucher from Ocean Shipment
    """
    try:
        shipment = frappe.get_doc("Ocean Shipment", shipment_name)
        
        # Check permissions
        if not shipment.has_permission("write"):
            frappe.throw(_("No permission to modify this shipment"))
        
        # Validate shipment has items and costs
        if not shipment.items:
            frappe.throw(_("Shipment has no items"))
        
        if not shipment.cost_components:
            frappe.throw(_("Shipment has no cost components"))
        
        # Check if voucher already exists
        if shipment.landed_cost_voucher:
            voucher = frappe.get_doc("Landed Cost Voucher", shipment.landed_cost_voucher)
            frappe.msgprint(_("Updating existing Landed Cost Voucher: {0}").format(voucher.name))
        else:
            voucher = frappe.new_doc("Landed Cost Voucher")
            voucher.company = shipment.get("company") or frappe.defaults.get_defaults().get("company")
            voucher.posting_date = shipment.shipment_date or nowdate()
        
        # Clear existing items and taxes
        voucher.items = []
        voucher.taxes = []
        
        # Add shipment items to voucher
        # Note: This requires linking to Purchase Receipt or Stock Entry
        # For now, we'll create a placeholder structure
        for item in shipment.items:
            voucher.append("items", {
                "item_code": item.item_code,
                "quantity": item.quantity,
                "rate": item.base_cost,
                "amount": item.base_cost * item.quantity,
                # "receipt_document_type": "Purchase Receipt",
                # "receipt_document": item.purchase_receipt,
            })
        
        # Add cost components as taxes
        for cost in shipment.cost_components:
            voucher.append("taxes", {
                "description": f"{cost.cost_type} - {cost.description or ''}",
                "amount": cost.amount_in_base_currency,
                # "account_head": get_expense_account(cost.cost_type),
            })
        
        voucher.save()
        
        # Link back to shipment
        shipment.landed_cost_voucher = voucher.name
        shipment.save()
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Landed Cost Voucher created successfully"),
            "voucher_name": voucher.name
        }
    
    except Exception as e:
        frappe.log_error(f"Create Landed Cost Voucher Error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
