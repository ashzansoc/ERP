# Smart Pricing Engine (AI Layer) 🤖

## Overview

The Smart Pricing Engine adds AI-powered pricing intelligence to your white-labeled ERP system, differentiating it from stock ERPNext with advanced features that help optimize pricing decisions, manage currency risks, and maximize profitability.

## Key Features

### 1. 🎯 Landed Cost Based Margin Suggestion
AI analyzes your landed costs and suggests optimal pricing margins based on:
- Historical performance data
- Market conditions
- Cost structure breakdown
- Competitive positioning
- Volume considerations

### 2. 📊 Historical Pricing Comparison
Compare proposed prices against historical data with:
- Trend analysis (increasing/decreasing/stable)
- Anomaly detection
- Seasonal pattern recognition
- Confidence scoring
- Accept/Review/Adjust recommendations

### 3. 🌍 Country-wise Pricing Analytics
Analyze pricing variations across destination countries:
- Price variation analysis
- Market-specific factors (duties, logistics, demand)
- Optimal pricing strategy per country
- Market opportunity identification
- Risk assessment by region

### 4. 📦 Volume-based Discount Recommendations
AI-powered volume discount tier suggestions:
- Optimal discount percentages per quantity tier
- Break-even analysis
- Competitive positioning
- Expected impact on sales volume
- Revenue maximization strategy

### 5. 💱 FX Risk Alert System
Proactive currency risk management:
- Real-time volatility assessment
- Risk level classification (Low/Medium/High)
- Exposure amount calculation
- Hedging strategy recommendations
- Alert triggers for rate thresholds

## Installation

### Prerequisites
- Frappe/ERPNext installation
- Ocean Shipment module installed
- Python 3.8+
- Internet connectivity for LLM API calls

### Installation Steps

```bash
# Navigate to your bench directory
cd /path/to/frappe-bench

# Copy the installation files
cp install_ai_pricing_engine.py apps/erpnext/
cp api/ai_pricing.py apps/erpnext/erpnext/api/

# Run installation
./install_ai_pricing.sh your-site-name
```

## Configuration

### User LLM Setup (Required for Each User)

During sign-in or in User Settings, each user must configure their AI preferences:

1. **Navigate to User Settings**
   - Click on user profile
   - Go to "AI Settings" or "User AI Settings"

2. **Select LLM Provider**
   Choose from:
   - **OpenAI** (GPT-4, GPT-3.5)
   - **Anthropic** (Claude 3 Sonnet, Claude 3 Opus)
   - **Google** (Gemini Pro)
   - **Azure OpenAI** (Enterprise deployments)

3. **Enter API Key**
   - Obtain API key from your chosen provider
   - Enter securely (stored encrypted)

4. **Choose Model**
   - OpenAI: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
   - Anthropic: `claude-3-sonnet-20240229`, `claude-3-opus-20240229`
   - Google: `gemini-pro`, `gemini-pro-vision`
   - Azure: Full endpoint URL

5. **Enable Features**
   - Toggle individual AI features on/off
   - Control which features use AI

### Obtaining API Keys

#### OpenAI
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create new secret key
5. Copy and save securely

#### Anthropic
1. Visit https://console.anthropic.com/
2. Sign up for Claude API access
3. Generate API key
4. Copy and save securely

#### Google (Gemini)
1. Visit https://makersuite.google.com/
2. Get API key from Google AI Studio
3. Copy and save securely

#### Azure OpenAI
1. Set up Azure OpenAI resource
2. Get endpoint URL and API key
3. Use full endpoint as "model" field

## Usage

### 1. Margin Suggestions in Ocean Shipment

```python
# Automatic suggestion when landed cost is calculated
# Or manually trigger:

# In Ocean Shipment form
1. Calculate landed cost
2. Click "Get AI Pricing Suggestions"
3. Review AI-suggested margins for each item
4. Apply or adjust as needed
```

**API Usage:**
```python
import frappe

result = frappe.call(
    "api.ai_pricing.get_margin_suggestion",
    item_code="ITEM-001",
    landed_cost=5000.00,
    quantity=100
)

# Response:
{
    "success": True,
    "suggestion": {
        "recommended_margin": 35.5,
        "min_margin": 25.0,
        "target_price": 67.75,
        "reasoning": "Based on historical data...",
        "risk_factors": ["Market volatility", "Seasonal demand"]
    }
}
```

### 2. Historical Price Comparison

```python
# In Sales Invoice
# AI automatically compares when price is entered

# Manual API call:
result = frappe.call(
    "api.ai_pricing.compare_historical_pricing",
    item_code="ITEM-001",
    proposed_price=75.00
)

# Response:
{
    "success": True,
    "comparison": {
        "comparison": "15% above historical average",
        "trend": "Increasing",
        "anomalies": [],
        "recommendation": "Accept",
        "confidence_score": 0.85
    }
}
```

### 3. Country Pricing Analytics

```python
# Analyze pricing across countries
result = frappe.call(
    "api.ai_pricing.analyze_country_pricing",
    item_code="ITEM-001",
    countries=["USA", "UK", "Germany", "Japan"]
)

# Response:
{
    "success": True,
    "analysis": {
        "variations": {
            "USA": {"avg_price": 75, "variance": "+5%"},
            "UK": {"avg_price": 82, "variance": "+15%"},
            ...
        },
        "drivers": ["Import duties", "Logistics costs", "Market demand"],
        "strategies": {...},
        "opportunities": ["Expand in UK market"],
        "risks": ["Currency volatility in Japan"]
    }
}
```

### 4. Volume Discount Recommendations

```python
# Get AI-powered volume discount tiers
result = frappe.call(
    "api.ai_pricing.get_volume_discount_recommendations",
    item_code="ITEM-001",
    base_price=75.00,
    quantity_tiers=[100, 500, 1000, 5000]
)

# Response:
{
    "success": True,
    "recommendations": {
        "discount_tiers": [
            {
                "quantity": 100,
                "discount_pct": 5,
                "price": 71.25,
                "reasoning": "Entry tier to encourage bulk orders"
            },
            {
                "quantity": 500,
                "discount_pct": 12,
                "price": 66.00,
                "reasoning": "Sweet spot for volume economics"
            },
            ...
        ],
        "overall_strategy": "Aggressive volume pricing to gain market share",
        "expected_impact": "30% increase in large orders"
    }
}
```

### 5. FX Risk Analysis

```python
# Monitor currency risk
result = frappe.call(
    "api.ai_pricing.analyze_fx_risk",
    currencies=["EUR", "GBP", "JPY"],
    transaction_value=100000,
    settlement_date="2024-06-30"
)

# Response:
{
    "success": True,
    "analysis": {
        "volatility": {
            "EUR": "Medium",
            "GBP": "High",
            "JPY": "Low"
        },
        "risk_level": "High",
        "exposure": 8500,
        "hedging_strategy": {
            "recommendation": "Forward contract for GBP",
            "timing": "Within 7 days",
            "coverage": "80% of exposure"
        },
        "alerts": [
            {
                "currency": "GBP",
                "threshold": 1.25,
                "action": "Review hedging"
            }
        ]
    }
}
```

## Integration Points

### Ocean Shipment
- AI margin suggestions appear after landed cost calculation
- Custom fields added to Ocean Shipment Item child table
- Button: "Get AI Pricing Suggestions"

### Sales Invoice
- Automatic price comparison on item selection
- Visual indicators for price variance
- AI recommendation badges (Accept/Review/Adjust)

### Dashboard
- AI Pricing Dashboard workspace
- Charts for AI usage and accuracy
- FX Risk Alert summary
- Cost savings from AI recommendations

## Data Privacy & Security

### API Key Storage
- API keys stored encrypted in database
- Never exposed in API responses (masked)
- User-specific, not shared across users

### Data Transmission
- All LLM API calls use HTTPS
- No sensitive customer data sent to LLM
- Only aggregated, anonymized data used for analysis

### Audit Trail
- All AI suggestions logged in "AI Pricing Log"
- User, timestamp, and suggestion details recorded
- Full traceability for compliance

## Cost Management

### API Usage Tracking
- Track API calls per user
- Monitor costs by feature
- Set usage limits (optional)

### Cost Optimization Tips
1. Use appropriate model for task (GPT-3.5 vs GPT-4)
2. Cache frequent queries
3. Batch similar requests
4. Set temperature lower for deterministic results
5. Use shorter prompts when possible

### Estimated Costs (as of 2024)
- **OpenAI GPT-4**: ~$0.03-0.06 per suggestion
- **Anthropic Claude**: ~$0.015-0.075 per suggestion
- **Google Gemini**: ~$0.001-0.005 per suggestion

## Troubleshooting

### "AI features not configured"
**Solution:** User needs to set up LLM provider in User AI Settings

### "AI service error: 401 Unauthorized"
**Solution:** Check API key validity, regenerate if needed

### "No historical data available"
**Solution:** System needs transaction history to build. Use manual pricing initially.

### Slow AI responses
**Solution:** 
- Check internet connectivity
- Try different LLM provider
- Use faster model (e.g., GPT-3.5 instead of GPT-4)

### Unexpected AI suggestions
**Solution:**
- Review prompt engineering in code
- Adjust temperature parameter
- Provide more context in historical data

## API Reference

### Save User AI Settings
```python
POST /api/method/api.ai_pricing.save_user_ai_settings

Parameters:
- llm_provider: "OpenAI" | "Anthropic" | "Google" | "Azure OpenAI"
- llm_api_key: string
- llm_model: string
- enabled: 0 | 1

Response:
{
    "success": true,
    "message": "AI settings saved successfully"
}
```

### Get User AI Settings
```python
GET /api/method/api.ai_pricing.get_user_ai_settings

Response:
{
    "success": true,
    "settings": {
        "llm_provider": "OpenAI",
        "llm_api_key_masked": "sk-proj-...xyz",
        "llm_model": "gpt-4",
        "enabled": 1
    }
}
```

## Best Practices

### 1. Start with Conservative Settings
- Begin with lower-cost models
- Enable one feature at a time
- Monitor accuracy and adjust

### 2. Validate AI Suggestions
- Don't blindly accept AI recommendations
- Use as decision support, not replacement
- Combine with human expertise

### 3. Build Historical Data
- More data = better suggestions
- Consistently record transactions
- Include competitor pricing data

### 4. Regular Review
- Weekly review of AI accuracy
- Monthly cost analysis
- Quarterly strategy adjustment

### 5. User Training
- Train users on AI features
- Explain limitations
- Encourage feedback

## Roadmap

### Planned Features
- [ ] Multi-currency optimization
- [ ] Seasonal pricing patterns
- [ ] Competitor price tracking automation
- [ ] Real-time market data integration
- [ ] Custom AI model fine-tuning
- [ ] Predictive demand forecasting
- [ ] Dynamic pricing automation

## Support

### Documentation
- This guide
- API documentation in code
- Video tutorials (coming soon)

### Community
- GitHub Issues
- Frappe Forum
- Discord channel

### Enterprise Support
- Dedicated support available
- Custom AI model training
- Integration assistance
- SLA guarantees

## License

This module is part of the white-labeled ERP system and follows the same license terms.

## Credits

Built with:
- Frappe Framework
- ERPNext
- OpenAI / Anthropic / Google AI APIs
- Python 3.8+

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Maintainer:** Your Organization
