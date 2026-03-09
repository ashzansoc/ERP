# Smart Pricing Engine - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Ocean Shipment  │  │  Sales Invoice   │  │ User Settings│ │
│  │                  │  │                  │  │              │ │
│  │  • AI Pricing    │  │  • Price Check   │  │  • LLM Config│ │
│  │  • Country       │  │  • Volume Disc   │  │  • API Keys  │ │
│  │  • FX Risk       │  │  • Validation    │  │  • Features  │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER (JS)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  • ai_signin_setup.js      - User onboarding & config          │
│  • ocean_shipment_ai.js    - Shipment AI features              │
│  • sales_invoice_ai.js     - Invoice AI features               │
│                                                                 │
│  Functions:                                                     │
│  - Event handling                                               │
│  - UI updates                                                   │
│  - API calls                                                    │
│  - Visual feedback                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       API LAYER (Python)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  api/ai_pricing.py                                              │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  API Endpoints:                                         │   │
│  │  • get_margin_suggestion()                              │   │
│  │  • compare_historical_pricing()                         │   │
│  │  • analyze_country_pricing()                            │   │
│  │  • get_volume_discount_recommendations()                │   │
│  │  • analyze_fx_risk()                                    │   │
│  │  • save_user_ai_settings()                              │   │
│  │  • get_user_ai_settings()                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  SmartPricingEngine                                      │  │
│  │                                                          │  │
│  │  • suggest_margin_based_on_landed_cost()                │  │
│  │  • compare_historical_pricing()                         │  │
│  │  • analyze_country_pricing()                            │  │
│  │  • recommend_volume_discounts()                         │  │
│  │  • analyze_fx_risk()                                    │  │
│  │                                                          │  │
│  │  Helper Methods:                                        │  │
│  │  • _get_historical_pricing()                            │  │
│  │  • _get_market_context()                                │  │
│  │  • _get_country_pricing_data()                          │  │
│  │  • _get_cost_structure()                                │  │
│  │  • _get_fx_historical_data()                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        AI/LLM LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AILLMClient                                             │  │
│  │                                                          │  │
│  │  • call_llm() - Universal interface                     │  │
│  │  • _call_openai()                                       │  │
│  │  • _call_anthropic()                                    │  │
│  │  • _call_google()                                       │  │
│  │  • _call_azure_openai()                                 │  │
│  │  • get_user_ai_settings()                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL LLM PROVIDERS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │  OpenAI  │  │Anthropic │  │  Google  │  │ Azure OpenAI │   │
│  │          │  │          │  │          │  │              │   │
│  │  GPT-4   │  │  Claude  │  │  Gemini  │  │   GPT-4      │   │
│  │  GPT-3.5 │  │  Sonnet  │  │   Pro    │  │   Custom     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  DocTypes:                                               │  │
│  │                                                          │  │
│  │  • User AI Settings      - LLM configuration            │  │
│  │  • AI Pricing Log        - Audit trail                  │  │
│  │  • FX Risk Alert         - Currency alerts              │  │
│  │  • Competitor Price      - Market data                  │  │
│  │  • Ocean Shipment        - Enhanced with AI fields      │  │
│  │  • Sales Invoice         - Enhanced with AI fields      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Historical Data Sources:                                │  │
│  │                                                          │  │
│  │  • Sales Invoice Item    - Past pricing                 │  │
│  │  • Ocean Shipment Item   - Landed costs                 │  │
│  │  • Currency Exchange     - FX rates                     │  │
│  │  • HS Code               - Duty rates                   │  │
│  │  • Customer              - Territory data               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### 1. Margin Suggestion Flow

```
User clicks "Get AI Pricing Suggestions"
              ↓
ocean_shipment_ai.js: getAIPricingSuggestions()
              ↓
For each item in shipment:
              ↓
API Call: api.ai_pricing.get_margin_suggestion
              ↓
SmartPricingEngine.suggest_margin_based_on_landed_cost()
              ↓
Gather data:
  • _get_historical_pricing()
  • _get_market_context()
              ↓
Build AI prompt with:
  • Item details
  • Landed cost breakdown
  • Historical data
  • Market context
              ↓
AILLMClient.call_llm()
              ↓
LLM Provider (OpenAI/Anthropic/Google)
              ↓
Parse JSON response:
  • recommended_margin
  • min_margin
  • target_price
  • reasoning
  • risk_factors
              ↓
Log suggestion: _log_ai_suggestion()
              ↓
Return to frontend
              ↓
Update UI:
  • Set AI fields
  • Highlight row
  • Show alert
```

### 2. Price Validation Flow

```
User enters price in Sales Invoice
              ↓
sales_invoice_ai.js: validateItemPrice()
              ↓
Debounce (1 second)
              ↓
API Call: api.ai_pricing.compare_historical_pricing
              ↓
SmartPricingEngine.compare_historical_pricing()
              ↓
_get_historical_pricing() - Last 50 transactions
              ↓
Build AI prompt with:
  • Proposed price
  • Historical data
  • Trends
              ↓
AILLMClient.call_llm()
              ↓
LLM Provider analyzes and returns:
  • comparison
  • trend
  • anomalies
  • recommendation (Accept/Review/Adjust)
  • confidence_score
              ↓
Log suggestion
              ↓
Return to frontend
              ↓
Update UI:
  • Color-code row (green/orange/red)
  • Set AI fields
  • Show tooltip
  • Alert if significant deviation
```

### 3. FX Risk Analysis Flow

```
User clicks "FX Risk Analysis"
              ↓
ocean_shipment_ai.js: analyzeFXRisk()
              ↓
Collect currencies from:
  • Shipment base currency
  • Cost component currencies
              ↓
API Call: api.ai_pricing.analyze_fx_risk
              ↓
SmartPricingEngine.analyze_fx_risk()
              ↓
Gather FX data:
  • _get_fx_historical_data() - 90 days
  • _get_current_fx_rates()
  • Calculate volatility
              ↓
Build AI prompt with:
  • Currency pairs
  • Transaction value
  • Settlement date
  • Historical rates
  • Volatility metrics
              ↓
AILLMClient.call_llm()
              ↓
LLM Provider analyzes and returns:
  • volatility assessment
  • risk_level (Low/Medium/High)
  • exposure amount
  • hedging_strategy
  • alerts
              ↓
If risk_level == "High":
  _create_fx_alert() - Create FX Risk Alert doc
              ↓
Log suggestion
              ↓
Return to frontend
              ↓
Display analysis in dialog
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layer 1: Authentication                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Frappe session authentication                         │  │
│  │  • User-specific settings                                │  │
│  │  • Permission checks                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Layer 2: API Key Protection                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Encrypted storage (Password field type)               │  │
│  │  • Never exposed in API responses                        │  │
│  │  • Masked display (sk-proj-...xyz)                       │  │
│  │  • User-specific, not shared                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Layer 3: Data Privacy                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • No PII sent to LLM                                    │  │
│  │  • Aggregated data only                                  │  │
│  │  • Anonymized references                                 │  │
│  │  • HTTPS for all external calls                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Layer 4: Audit Trail                                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • All AI calls logged                                   │  │
│  │  • User attribution                                      │  │
│  │  • Timestamp tracking                                    │  │
│  │  • Full suggestion data stored                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Layer 5: Access Control                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Role-based permissions                                │  │
│  │  • Owner-only edit rights                                │  │
│  │  • Feature-level toggles                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION DEPLOYMENT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Frappe/ERPNext Server                                   │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  Web Server (Nginx)                                │ │  │
│  │  │  • HTTPS termination                               │ │  │
│  │  │  • Static file serving                             │ │  │
│  │  │  • Load balancing                                  │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  Application Server (Gunicorn)                     │ │  │
│  │  │  • Python/Frappe app                               │ │  │
│  │  │  • AI Pricing Engine                               │ │  │
│  │  │  • API endpoints                                   │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  Background Workers (Redis Queue)                  │ │  │
│  │  │  • Async AI processing                             │ │  │
│  │  │  • Batch operations                                │ │  │
│  │  │  • Scheduled tasks                                 │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  Database (MariaDB/PostgreSQL)                     │ │  │
│  │  │  • User AI Settings                                │ │  │
│  │  │  • AI Pricing Logs                                 │ │  │
│  │  │  • Historical data                                 │ │  │
│  │  │  • Encrypted API keys                              │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│                              ↓                                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  External Services                                       │  │
│  │                                                          │  │
│  │  • OpenAI API (api.openai.com)                          │  │
│  │  • Anthropic API (api.anthropic.com)                    │  │
│  │  • Google AI API (generativelanguage.googleapis.com)    │  │
│  │  • Azure OpenAI (*.openai.azure.com)                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM INTEGRATIONS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Existing ERPNext Modules:                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                          │  │
│  │  Ocean Shipment ←→ AI Pricing Engine                    │  │
│  │    • Landed cost data                                   │  │
│  │    • Item details                                       │  │
│  │    • Cost components                                    │  │
│  │    • AI suggestions                                     │  │
│  │                                                          │  │
│  │  Sales Invoice ←→ AI Pricing Engine                     │  │
│  │    • Item pricing                                       │  │
│  │    • Historical data                                    │  │
│  │    • Price validation                                   │  │
│  │    • Volume discounts                                   │  │
│  │                                                          │  │
│  │  Item Master ←→ AI Pricing Engine                       │  │
│  │    • Item details                                       │  │
│  │    • HS codes                                           │  │
│  │    • Stock levels                                       │  │
│  │                                                          │  │
│  │  Currency Exchange ←→ AI Pricing Engine                 │  │
│  │    • FX rates                                           │  │
│  │    • Historical data                                    │  │
│  │    • Volatility analysis                                │  │
│  │                                                          │  │
│  │  Customer ←→ AI Pricing Engine                          │  │
│  │    • Territory data                                     │  │
│  │    • Country information                                │  │
│  │    • Purchase history                                   │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Performance Considerations

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE OPTIMIZATION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Frontend:                                                      │
│  • Debounced API calls (1 second)                              │
│  • Cached UI state                                              │
│  • Lazy loading of AI features                                 │
│  • Progressive enhancement                                      │
│                                                                 │
│  Backend:                                                       │
│  • Database query optimization                                  │
│  • Indexed fields for fast lookups                             │
│  • Batch processing for multiple items                         │
│  • Connection pooling                                           │
│                                                                 │
│  LLM Calls:                                                     │
│  • Timeout handling (30 seconds)                               │
│  • Error recovery                                               │
│  • Retry logic                                                  │
│  • Model selection based on complexity                         │
│                                                                 │
│  Caching Strategy:                                              │
│  • Historical data cached per session                          │
│  • FX rates cached (1 hour TTL)                                │
│  • User settings cached                                         │
│  • Competitor prices cached                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Monitoring & Observability

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Metrics to Track:                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • API response times                                    │  │
│  │  • LLM call success rate                                 │  │
│  │  • Error rates by feature                                │  │
│  │  • User adoption metrics                                 │  │
│  │  • Cost per suggestion                                   │  │
│  │  • Suggestion acceptance rate                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Logging:                                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • AI Pricing Log (database)                             │  │
│  │  • Error logs (frappe.log_error)                         │  │
│  │  • Access logs (nginx)                                   │  │
│  │  • Application logs (gunicorn)                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Alerts:                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • High error rate                                       │  │
│  │  • Slow response times                                   │  │
│  │  • API key failures                                      │  │
│  │  • High FX risk detected                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**Architecture Version:** 1.0.0  
**Last Updated:** 2024  
**Status:** Production Ready
