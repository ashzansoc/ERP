# Smart Pricing Engine - Quick Start Guide 🚀

## 5-Minute Setup

### Step 1: Install (2 minutes)
```bash
cd /path/to/frappe-bench
./install_ai_pricing.sh your-site-name
```

### Step 2: Configure LLM (2 minutes)

**Option A: OpenAI (Recommended for beginners)**
1. Get API key: https://platform.openai.com/api-keys
2. Go to User Settings → AI Settings
3. Select "OpenAI"
4. Enter API key
5. Model: `gpt-4` or `gpt-3.5-turbo`
6. Click Save

**Option B: Anthropic Claude**
1. Get API key: https://console.anthropic.com/
2. Select "Anthropic"
3. Enter API key
4. Model: `claude-3-sonnet-20240229`

**Option C: Google Gemini (Most economical)**
1. Get API key: https://makersuite.google.com/app/apikey
2. Select "Google"
3. Enter API key
4. Model: `gemini-pro`

### Step 3: Use AI Features (1 minute)

**In Ocean Shipment:**
1. Calculate landed cost
2. Click "AI Features" → "Get AI Pricing Suggestions"
3. Review AI-suggested margins

**In Sales Invoice:**
- AI automatically validates prices as you enter them
- Green = Good price
- Orange = Review recommended
- Red = Adjust suggested

## Cost Estimates

| Provider | Model | Cost per Suggestion | Best For |
|----------|-------|---------------------|----------|
| Google | Gemini Pro | ~$0.001 | High volume, budget-conscious |
| OpenAI | GPT-3.5 | ~$0.01 | Balanced performance |
| OpenAI | GPT-4 | ~$0.05 | Complex analysis |
| Anthropic | Claude Sonnet | ~$0.03 | Detailed reasoning |

## 5 Key Features

### 1. 🎯 Margin Suggestions
**Where:** Ocean Shipment → AI Features  
**What:** AI suggests optimal margin % based on landed cost  
**When:** After calculating landed cost

### 2. 📊 Price Validation
**Where:** Sales Invoice (automatic)  
**What:** Compares price to historical data  
**When:** As you enter item prices

### 3. 🌍 Country Analytics
**Where:** Ocean Shipment → AI Features  
**What:** Compare pricing across countries  
**When:** Planning international sales

### 4. 📦 Volume Discounts
**Where:** Sales Invoice → AI Features  
**What:** AI-recommended discount tiers  
**When:** Large quantity orders

### 5. 💱 FX Risk Alerts
**Where:** Ocean Shipment → AI Features  
**What:** Currency risk analysis  
**When:** Multi-currency transactions

## Troubleshooting

### "AI features not configured"
→ Go to User Settings → AI Settings and configure

### "Invalid API key"
→ Check key is correct, regenerate if needed

### "No historical data"
→ Normal for new items, AI learns over time

### Slow responses
→ Try faster model (GPT-3.5 or Gemini)

## Best Practices

✅ **DO:**
- Start with one feature at a time
- Review AI suggestions before applying
- Build historical data consistently
- Use appropriate model for task

❌ **DON'T:**
- Blindly accept all AI suggestions
- Use expensive models for simple tasks
- Share API keys between users
- Ignore pricing anomalies

## Support

- 📚 Full Guide: `AI_PRICING_ENGINE_GUIDE.md`
- 🐛 Issues: GitHub Issues
- 💬 Community: Frappe Forum
- 📧 Enterprise: support@yourcompany.com

## Quick Commands

```bash
# Check installation
bench --site your-site console
>>> frappe.db.exists("DocType", "User AI Settings")

# View AI logs
bench --site your-site mariadb
> SELECT * FROM `tabAI Pricing Log` ORDER BY log_date DESC LIMIT 10;

# Reset user settings
bench --site your-site console
>>> frappe.delete_doc("User AI Settings", "user@example.com")
```

## Next Steps

1. ✅ Complete setup above
2. 📊 Add competitor pricing data
3. 🎯 Test on sample shipment
4. 📈 Monitor AI accuracy
5. 🚀 Roll out to team

---

**Ready to go?** Start with Ocean Shipment and click "Get AI Pricing Suggestions"! 🎉
