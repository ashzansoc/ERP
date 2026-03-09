"""
Smart Pricing Engine (AI Layer)
AI-powered pricing intelligence and recommendations for import/export operations
"""
import frappe
from frappe import _
from frappe.utils import flt, nowdate, add_days, get_datetime
import json
import requests
from datetime import datetime, timedelta


class AILLMClient:
    """Universal LLM client supporting multiple providers"""
    
    def __init__(self, user_settings=None):
        """Initialize with user's LLM preferences"""
        if user_settings:
            self.provider = user_settings.get("llm_provider")
            self.api_key = user_settings.get("llm_api_key")
            self.model = user_settings.get("llm_model")
        else:
            # Get from current user settings
            user_ai_settings = self.get_user_ai_settings()
            self.provider = user_ai_settings.get("llm_provider")
            self.api_key = user_ai_settings.get("llm_api_key")
            self.model = user_ai_settings.get("llm_model")
        
        if not self.provider or not self.api_key:
            frappe.throw(_("AI features not configured. Please set up your LLM provider in settings."))
    
    @staticmethod
    def get_user_ai_settings(user=None):
        """Get AI settings for user"""
        if not user:
            user = frappe.session.user
        
        settings = frappe.db.get_value(
            "User AI Settings",
            {"user": user},
            ["llm_provider", "llm_api_key", "llm_model", "enabled"],
            as_dict=True
        )
        
        if not settings or not settings.get("enabled"):
            return {}
        
        return settings
    
    def call_llm(self, prompt, system_prompt=None, temperature=0.7, max_tokens=1000):
        """Universal LLM API call"""
        try:
            if self.provider == "OpenAI":
                return self._call_openai(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "Anthropic":
                return self._call_anthropic(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "Google":
                return self._call_google(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "Azure OpenAI":
                return self._call_azure_openai(prompt, system_prompt, temperature, max_tokens)
            else:
                frappe.throw(_("Unsupported LLM provider: {0}").format(self.provider))
        
        except Exception as e:
            frappe.log_error(f"LLM API Error: {str(e)}", "AI Pricing Engine")
            frappe.throw(_("AI service error: {0}").format(str(e)))
    
    def _call_openai(self, prompt, system_prompt, temperature, max_tokens):
        """Call OpenAI API"""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model or "gpt-4",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def _call_anthropic(self, prompt, system_prompt, temperature, max_tokens):
        """Call Anthropic Claude API"""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model or "claude-3-sonnet-20240229",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["content"][0]["text"]
    
    def _call_google(self, prompt, system_prompt, temperature, max_tokens):
        """Call Google Gemini API"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model or 'gemini-pro'}:generateContent?key={self.api_key}"
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        data = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    
    def _call_azure_openai(self, prompt, system_prompt, temperature, max_tokens):
        """Call Azure OpenAI API"""
        # Azure endpoint format: https://{resource-name}.openai.azure.com/openai/deployments/{deployment-id}/chat/completions?api-version=2023-05-15
        # User should provide full endpoint in model field
        url = self.model  # Full Azure endpoint
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


class SmartPricingEngine:
    """AI-powered pricing intelligence engine"""
    
    def __init__(self, shipment_name=None):
        self.shipment_name = shipment_name
        self.shipment = None
        if shipment_name:
            self.shipment = frappe.get_doc("Ocean Shipment", shipment_name)
        
        self.llm_client = AILLMClient()
    
    def suggest_margin_based_on_landed_cost(self, item_code, landed_cost, quantity):
        """
        AI-powered margin suggestion based on:
        - Historical margins for similar items
        - Market conditions
        - Landed cost components
        - Competitive analysis
        """
        # Get historical data
        historical_data = self._get_historical_pricing(item_code)
        
        # Get market context
        market_context = self._get_market_context(item_code)
        
        # Build AI prompt
        system_prompt = """You are an expert pricing analyst for import/export operations. 
Analyze the provided data and suggest optimal pricing margins considering:
1. Historical performance
2. Market conditions
3. Cost structure
4. Competitive positioning
5. Volume considerations

Provide specific margin percentage recommendations with reasoning."""
        
        user_prompt = f"""
Item: {item_code}
Landed Cost per Unit: ${flt(landed_cost / quantity, 2)}
Order Quantity: {quantity}
Total Landed Cost: ${flt(landed_cost, 2)}

Historical Data:
{json.dumps(historical_data, indent=2)}

Market Context:
{json.dumps(market_context, indent=2)}

Please suggest:
1. Recommended margin percentage
2. Minimum acceptable margin
3. Target selling price
4. Reasoning for recommendations
5. Risk factors to consider

Format response as JSON with keys: recommended_margin, min_margin, target_price, reasoning, risk_factors
"""
        
        response = self.llm_client.call_llm(user_prompt, system_prompt, temperature=0.3)
        
        # Parse and validate response
        try:
            suggestion = json.loads(response)
            
            # Log the suggestion
            self._log_ai_suggestion("Margin Suggestion", item_code, suggestion)
            
            return suggestion
        except:
            # Fallback to text response
            return {
                "recommended_margin": None,
                "reasoning": response,
                "raw_response": True
            }
    
    def compare_historical_pricing(self, item_code, proposed_price):
        """
        Compare proposed pricing against historical data
        Provide insights on pricing trends and anomalies
        """
        historical_data = self._get_historical_pricing(item_code, limit=50)
        
        if not historical_data.get("transactions"):
            return {
                "status": "no_data",
                "message": "No historical pricing data available for comparison"
            }
        
        system_prompt = """You are a pricing analyst. Analyze historical pricing patterns and 
compare them with proposed pricing. Identify trends, anomalies, and provide actionable insights."""
        
        user_prompt = f"""
Item: {item_code}
Proposed Price: ${proposed_price}

Historical Pricing Data (last 50 transactions):
{json.dumps(historical_data, indent=2)}

Analyze:
1. How does proposed price compare to historical average?
2. Pricing trend (increasing/decreasing/stable)
3. Any anomalies or outliers
4. Seasonal patterns if any
5. Recommendation (accept/adjust/reject proposed price)

Format as JSON with keys: comparison, trend, anomalies, recommendation, confidence_score
"""
        
        response = self.llm_client.call_llm(user_prompt, system_prompt, temperature=0.3)
        
        try:
            analysis = json.loads(response)
            self._log_ai_suggestion("Historical Comparison", item_code, analysis)
            return analysis
        except:
            return {"analysis": response, "raw_response": True}
    
    def analyze_country_pricing(self, item_code, countries=None):
        """
        Country-wise pricing analytics
        Compare pricing across different destination countries
        """
        if not countries and self.shipment:
            countries = [self.shipment.destination_country]
        
        country_data = self._get_country_pricing_data(item_code, countries)
        
        system_prompt = """You are an international trade pricing expert. Analyze pricing 
variations across countries and provide strategic insights for market-specific pricing."""
        
        user_prompt = f"""
Item: {item_code}
Countries: {', '.join(countries) if countries else 'All'}

Country-wise Pricing Data:
{json.dumps(country_data, indent=2)}

Provide analysis on:
1. Price variations across countries
2. Factors driving differences (duties, logistics, market demand)
3. Optimal pricing strategy per country
4. Market opportunities
5. Risk assessment

Format as JSON with keys: variations, drivers, strategies, opportunities, risks
"""
        
        response = self.llm_client.call_llm(user_prompt, system_prompt, temperature=0.4)
        
        try:
            analysis = json.loads(response)
            self._log_ai_suggestion("Country Pricing Analysis", item_code, analysis)
            return analysis
        except:
            return {"analysis": response, "raw_response": True}
    
    def recommend_volume_discounts(self, item_code, base_price, quantity_tiers=None):
        """
        AI-powered volume discount recommendations
        Based on cost structure, market dynamics, and historical patterns
        """
        if not quantity_tiers:
            quantity_tiers = [100, 500, 1000, 5000, 10000]
        
        # Get cost structure
        cost_data = self._get_cost_structure(item_code)
        
        # Get historical volume pricing
        volume_history = self._get_volume_pricing_history(item_code)
        
        system_prompt = """You are a pricing strategist specializing in volume-based pricing. 
Design optimal discount tiers that maximize revenue while remaining competitive."""
        
        user_prompt = f"""
Item: {item_code}
Base Price (single unit): ${base_price}
Proposed Quantity Tiers: {quantity_tiers}

Cost Structure:
{json.dumps(cost_data, indent=2)}

Historical Volume Pricing:
{json.dumps(volume_history, indent=2)}

Design volume discount structure:
1. Discount percentage for each tier
2. Rationale for each discount level
3. Break-even analysis
4. Competitive positioning
5. Expected impact on sales volume

Format as JSON with keys: discount_tiers (array of {quantity, discount_pct, price, reasoning}), 
overall_strategy, expected_impact
"""
        
        response = self.llm_client.call_llm(user_prompt, system_prompt, temperature=0.4)
        
        try:
            recommendations = json.loads(response)
            self._log_ai_suggestion("Volume Discount Recommendation", item_code, recommendations)
            return recommendations
        except:
            return {"recommendations": response, "raw_response": True}
    
    def analyze_fx_risk(self, currencies, transaction_value, settlement_date):
        """
        FX risk analysis and hedging recommendations
        Alert on currency volatility and suggest mitigation strategies
        """
        # Get FX historical data
        fx_data = self._get_fx_historical_data(currencies)
        
        # Get current rates
        current_rates = self._get_current_fx_rates(currencies)
        
        system_prompt = """You are a foreign exchange risk analyst. Assess currency risk 
and provide practical hedging recommendations for import/export transactions."""
        
        user_prompt = f"""
Currencies Involved: {', '.join(currencies)}
Transaction Value: ${transaction_value}
Expected Settlement Date: {settlement_date}

Current Exchange Rates:
{json.dumps(current_rates, indent=2)}

Historical FX Data (90 days):
{json.dumps(fx_data, indent=2)}

Provide FX risk analysis:
1. Volatility assessment for each currency pair
2. Risk level (Low/Medium/High)
3. Potential exposure amount
4. Hedging recommendations (forward contracts, options, natural hedging)
5. Timing recommendations
6. Alert triggers (rate thresholds to monitor)

Format as JSON with keys: volatility, risk_level, exposure, hedging_strategy, alerts
"""
        
        response = self.llm_client.call_llm(user_prompt, system_prompt, temperature=0.3)
        
        try:
            analysis = json.loads(response)
            
            # Create FX alert if high risk
            if analysis.get("risk_level") == "High":
                self._create_fx_alert(currencies, analysis)
            
            self._log_ai_suggestion("FX Risk Analysis", ", ".join(currencies), analysis)
            return analysis
        except:
            return {"analysis": response, "raw_response": True}
    
    # Helper methods for data gathering
    
    def _get_historical_pricing(self, item_code, limit=20):
        """Get historical pricing data for item"""
        transactions = frappe.db.sql("""
            SELECT 
                si.item_code,
                si.rate as selling_price,
                si.qty as quantity,
                s.posting_date,
                s.customer,
                s.territory,
                si.base_rate,
                si.discount_percentage
            FROM `tabSales Invoice Item` si
            JOIN `tabSales Invoice` s ON si.parent = s.name
            WHERE si.item_code = %s
                AND s.docstatus = 1
            ORDER BY s.posting_date DESC
            LIMIT %s
        """, (item_code, limit), as_dict=True)
        
        if not transactions:
            return {"transactions": [], "average_price": 0, "count": 0}
        
        avg_price = sum(t.selling_price for t in transactions) / len(transactions)
        
        return {
            "transactions": transactions,
            "average_price": flt(avg_price, 2),
            "count": len(transactions),
            "date_range": {
                "from": transactions[-1].posting_date if transactions else None,
                "to": transactions[0].posting_date if transactions else None
            }
        }
    
    def _get_market_context(self, item_code):
        """Get market context for item"""
        # Get item details
        item = frappe.get_doc("Item", item_code)
        
        # Get recent market activity
        recent_activity = frappe.db.count("Sales Invoice Item", {
            "item_code": item_code,
            "creation": [">=", add_days(nowdate(), -30)]
        })
        
        # Get competitor pricing if available
        competitor_prices = frappe.db.get_all(
            "Competitor Price",
            filters={"item_code": item_code},
            fields=["competitor", "price", "date"],
            order_by="date DESC",
            limit=5
        )
        
        return {
            "item_group": item.item_group,
            "recent_sales_count": recent_activity,
            "competitor_prices": competitor_prices,
            "stock_level": frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty") or 0
        }
    
    def _get_country_pricing_data(self, item_code, countries):
        """Get pricing data by country"""
        country_data = {}
        
        for country in countries:
            data = frappe.db.sql("""
                SELECT 
                    AVG(si.rate) as avg_price,
                    COUNT(*) as transaction_count,
                    SUM(si.qty) as total_quantity
                FROM `tabSales Invoice Item` si
                JOIN `tabSales Invoice` s ON si.parent = s.name
                JOIN `tabCustomer` c ON s.customer = c.name
                WHERE si.item_code = %s
                    AND c.territory = %s
                    AND s.docstatus = 1
                    AND s.posting_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            """, (item_code, country), as_dict=True)
            
            if data and data[0].avg_price:
                country_data[country] = data[0]
        
        return country_data
    
    def _get_cost_structure(self, item_code):
        """Get cost structure for item"""
        # Get latest landed cost data
        latest_shipment = frappe.db.sql("""
            SELECT 
                osi.base_cost,
                osi.allocated_freight,
                osi.allocated_insurance,
                osi.customs_duty,
                osi.allocated_cha_fees,
                osi.allocated_port_charges,
                osi.total_landed_cost,
                osi.quantity
            FROM `tabOcean Shipment Item` osi
            JOIN `tabOcean Shipment` os ON osi.parent = os.name
            WHERE osi.item_code = %s
                AND os.docstatus = 1
            ORDER BY os.shipment_date DESC
            LIMIT 1
        """, (item_code,), as_dict=True)
        
        if latest_shipment:
            item = latest_shipment[0]
            return {
                "base_cost": item.base_cost,
                "freight": item.allocated_freight,
                "insurance": item.allocated_insurance,
                "customs_duty": item.customs_duty,
                "cha_fees": item.allocated_cha_fees,
                "port_charges": item.allocated_port_charges,
                "total_landed_cost": item.total_landed_cost,
                "unit_landed_cost": flt(item.total_landed_cost / item.quantity, 2) if item.quantity else 0
            }
        
        return {}
    
    def _get_volume_pricing_history(self, item_code):
        """Get historical volume-based pricing"""
        volume_data = frappe.db.sql("""
            SELECT 
                si.qty as quantity,
                si.rate as price,
                si.discount_percentage,
                s.posting_date
            FROM `tabSales Invoice Item` si
            JOIN `tabSales Invoice` s ON si.parent = s.name
            WHERE si.item_code = %s
                AND s.docstatus = 1
            ORDER BY si.qty DESC
            LIMIT 20
        """, (item_code,), as_dict=True)
        
        return volume_data
    
    def _get_fx_historical_data(self, currencies):
        """Get historical FX data"""
        fx_data = {}
        
        for currency in currencies:
            if currency == "USD":
                continue
            
            rates = frappe.db.sql("""
                SELECT 
                    date,
                    exchange_rate
                FROM `tabCurrency Exchange`
                WHERE from_currency = %s
                    AND to_currency = 'USD'
                    AND date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
                ORDER BY date DESC
            """, (currency,), as_dict=True)
            
            if rates:
                fx_data[currency] = {
                    "rates": rates,
                    "current": rates[0].exchange_rate if rates else None,
                    "avg_90d": sum(r.exchange_rate for r in rates) / len(rates) if rates else None,
                    "volatility": self._calculate_volatility([r.exchange_rate for r in rates])
                }
        
        return fx_data
    
    def _get_current_fx_rates(self, currencies):
        """Get current FX rates"""
        rates = {}
        
        for currency in currencies:
            if currency == "USD":
                rates[currency] = 1.0
                continue
            
            rate = frappe.db.get_value(
                "Currency Exchange",
                {"from_currency": currency, "to_currency": "USD"},
                "exchange_rate",
                order_by="date DESC"
            )
            
            rates[currency] = flt(rate) if rate else None
        
        return rates
    
    def _calculate_volatility(self, values):
        """Calculate simple volatility (standard deviation)"""
        if len(values) < 2:
            return 0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _create_fx_alert(self, currencies, analysis):
        """Create FX risk alert"""
        try:
            alert = frappe.get_doc({
                "doctype": "FX Risk Alert",
                "alert_date": nowdate(),
                "currencies": ", ".join(currencies),
                "risk_level": analysis.get("risk_level"),
                "exposure_amount": analysis.get("exposure"),
                "recommendation": json.dumps(analysis.get("hedging_strategy")),
                "user": frappe.session.user,
                "status": "Open"
            })
            alert.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Failed to create FX alert: {str(e)}")
    
    def _log_ai_suggestion(self, suggestion_type, reference, suggestion_data):
        """Log AI suggestions for audit trail"""
        try:
            log = frappe.get_doc({
                "doctype": "AI Pricing Log",
                "log_date": get_datetime(),
                "suggestion_type": suggestion_type,
                "reference": reference,
                "user": frappe.session.user,
                "llm_provider": self.llm_client.provider,
                "llm_model": self.llm_client.model,
                "suggestion_data": json.dumps(suggestion_data, indent=2),
                "shipment": self.shipment_name
            })
            log.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Failed to log AI suggestion: {str(e)}")


# API Endpoints

@frappe.whitelist()
def get_margin_suggestion(item_code, landed_cost, quantity):
    """API: Get AI-powered margin suggestion"""
    try:
        engine = SmartPricingEngine()
        suggestion = engine.suggest_margin_based_on_landed_cost(
            item_code,
            flt(landed_cost),
            flt(quantity)
        )
        
        return {
            "success": True,
            "suggestion": suggestion
        }
    except Exception as e:
        frappe.log_error(f"Margin Suggestion Error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def compare_historical_pricing(item_code, proposed_price):
    """API: Compare pricing with historical data"""
    try:
        engine = SmartPricingEngine()
        comparison = engine.compare_historical_pricing(item_code, flt(proposed_price))
        
        return {
            "success": True,
            "comparison": comparison
        }
    except Exception as e:
        frappe.log_error(f"Historical Comparison Error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def analyze_country_pricing(item_code, countries=None):
    """API: Country-wise pricing analytics"""
    try:
        if countries and isinstance(countries, str):
            countries = json.loads(countries)
        
        engine = SmartPricingEngine()
        analysis = engine.analyze_country_pricing(item_code, countries)
        
        return {
            "success": True,
            "analysis": analysis
        }
    except Exception as e:
        frappe.log_error(f"Country Pricing Analysis Error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_volume_discount_recommendations(item_code, base_price, quantity_tiers=None):
    """API: Get volume discount recommendations"""
    try:
        if quantity_tiers and isinstance(quantity_tiers, str):
            quantity_tiers = json.loads(quantity_tiers)
        
        engine = SmartPricingEngine()
        recommendations = engine.recommend_volume_discounts(
            item_code,
            flt(base_price),
            quantity_tiers
        )
        
        return {
            "success": True,
            "recommendations": recommendations
        }
    except Exception as e:
        frappe.log_error(f"Volume Discount Recommendation Error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def analyze_fx_risk(currencies, transaction_value, settlement_date):
    """API: FX risk analysis"""
    try:
        if isinstance(currencies, str):
            currencies = json.loads(currencies)
        
        engine = SmartPricingEngine()
        analysis = engine.analyze_fx_risk(
            currencies,
            flt(transaction_value),
            settlement_date
        )
        
        return {
            "success": True,
            "analysis": analysis
        }
    except Exception as e:
        frappe.log_error(f"FX Risk Analysis Error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def save_user_ai_settings(llm_provider, llm_api_key, llm_model, enabled=1):
    """API: Save user's AI/LLM settings"""
    try:
        user = frappe.session.user
        
        # Check if settings exist
        if frappe.db.exists("User AI Settings", {"user": user}):
            doc = frappe.get_doc("User AI Settings", {"user": user})
            doc.llm_provider = llm_provider
            doc.llm_api_key = llm_api_key
            doc.llm_model = llm_model
            doc.enabled = enabled
            doc.save()
        else:
            doc = frappe.get_doc({
                "doctype": "User AI Settings",
                "user": user,
                "llm_provider": llm_provider,
                "llm_api_key": llm_api_key,
                "llm_model": llm_model,
                "enabled": enabled
            })
            doc.insert()
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("AI settings saved successfully")
        }
    except Exception as e:
        frappe.log_error(f"Save AI Settings Error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_user_ai_settings():
    """API: Get user's AI/LLM settings"""
    try:
        settings = AILLMClient.get_user_ai_settings()
        
        # Don't expose full API key
        if settings.get("llm_api_key"):
            key = settings["llm_api_key"]
            settings["llm_api_key_masked"] = f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "***"
            del settings["llm_api_key"]
        
        return {
            "success": True,
            "settings": settings
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
