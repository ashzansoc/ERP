# Compliance & Regulatory Dashboard - System Architecture

## System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COMPLIANCE HEALTH SCORE DASHBOARD                 │
│                         (100 Point Scoring System)                   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │   api/compliance.py           │
                    │   - get_compliance_health_score()
                    │   - get_compliance_alerts()   │
                    │   - get_compliance_metrics()  │
                    └───────────────┬───────────────┘
                                    │
        ┌───────────┬───────────┬───┴────┬──────────┬──────────┐
        │           │           │        │          │          │
        ▼           ▼           ▼        ▼          ▼          ▼
    ┌──────┐   ┌──────┐   ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
    │ IEC  │   │ GST  │   │ LUT  │  │Export│  │Duty  │  │DGFT  │
    │ 20pt │   │ 15pt │   │ 15pt │  │ 15pt │  │ 15pt │  │ 20pt │
    └──────┘   └──────┘   └──────┘  └──────┘  └──────┘  └──────┘
```

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Dashboard   │  │   DocType    │  │   Reports    │             │
│  │   Widgets    │  │    Forms     │  │   & Charts   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                         API / BUSINESS LOGIC LAYER                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  api/compliance.py                                            │  │
│  │  - Score Calculation Functions                                │  │
│  │  - Alert Generation Logic                                     │  │
│  │  - Metrics Aggregation                                        │  │
│  │  - Trend Analysis                                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA PERSISTENCE LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   DocTypes   │  │  Child Tables│  │ Custom Fields│             │
│  │  (5 new)     │  │              │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  MariaDB / PostgreSQL Database                                │  │
│  │  - tabGST Export Refund                                       │  │
│  │  - tabLUT Bond Tracking                                       │  │
│  │  - tabExport Incentive Scheme                                 │  │
│  │  - tabDuty Drawback Claim                                     │  │
│  │  - tabDGFT Scheme Tracking                                    │  │
│  │  - tabIEC Registration (existing)                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXPORT TRANSACTION                           │
│                                                                      │
│  Sales Order → Delivery Note → Sales Invoice → Shipment            │
│                                      │                               │
│                                      ├─→ Shipping Bill               │
│                                      │                               │
└──────────────────────────────────────┼───────────────────────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
        ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
        │ GST Export     │  │ Export         │  │ Duty Drawback  │
        │ Refund         │  │ Incentive      │  │ Claim          │
        │                │  │ Scheme         │  │                │
        │ - Shipping Bill│  │ - Shipping Bill│  │ - Shipping Bill│
        │ - Invoice Link │  │ - Invoice Link │  │ - Invoice Link │
        │ - IGST Amount  │  │ - FOB Value    │  │ - FOB Value    │
        │ - ARN Number   │  │ - Incentive %  │  │ - Drawback Rate│
        └────────────────┘  └────────────────┘  └────────────────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────┐
                        │  COMPLIANCE HEALTH       │
                        │  SCORE DASHBOARD         │
                        │                          │
                        │  Overall Score: 85/100   │
                        │  Status: Good ✓          │
                        │  Alerts: 3 warnings      │
                        └──────────────────────────┘
```

## Scoring Algorithm Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  get_compliance_health_score(company)                                │
└─────────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │  Initialize score_data        │
                │  - overall_score = 0          │
                │  - score_breakdown = {}       │
                │  - alerts = []                │
                │  - metrics = {}               │
                └───────────────┬───────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐        ┌──────────────┐      ┌──────────────┐
│calculate_iec │        │calculate_gst │      │calculate_lut │
│_score()      │        │_refund_score │      │_bond_score() │
│              │        │()            │      │              │
│Returns: 0-20 │        │Returns: 0-15 │      │Returns: 0-15 │
└──────────────┘        └──────────────┘      └──────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐        ┌──────────────┐      ┌──────────────┐
│calculate_    │        │calculate_    │      │calculate_    │
│incentive_    │        │duty_drawback │      │dgft_scheme   │
│scheme_score()│        │_score()      │      │_score()      │
│              │        │              │      │              │
│Returns: 0-15 │        │Returns: 0-15 │      │Returns: 0-20 │
└──────────────┘        └──────────────┘      └──────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │  Sum all scores               │
                │  overall_score = sum(scores)  │
                └───────────────┬───────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
        ┌──────────────┐              ┌──────────────┐
        │get_compliance│              │get_compliance│
        │_alerts()     │              │_metrics()    │
        └──────────────┘              └──────────────┘
                │                               │
                └───────────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │  Return complete score_data   │
                │  - overall_score              │
                │  - score_breakdown            │
                │  - alerts                     │
                │  - metrics                    │
                └───────────────────────────────┘
```

## Alert Generation Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  get_compliance_alerts(company)                                      │
└─────────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │  Initialize alerts = []       │
                └───────────────┬───────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐        ┌──────────────┐      ┌──────────────┐
│ Check IEC    │        │ Check LUT/   │      │ Check DGFT   │
│ Expiry       │        │ Bond Expiry  │      │ Obligations  │
│              │        │              │      │              │
│ Query: IEC   │        │ Query: LUT   │      │ Query: DGFT  │
│ valid_till   │        │ valid_till   │      │ deadline     │
│ <= today+90  │        │ <= today+60  │      │ <= today+90  │
└──────────────┘        └──────────────┘      └──────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐        ┌──────────────┐      ┌──────────────┐
│ For each IEC │        │ For each LUT │      │ For each DGFT│
│ Calculate    │        │ Calculate    │      │ Calculate    │
│ days_left    │        │ days_left    │      │ days_left    │
└──────────────┘        └──────────────┘      └──────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐        ┌──────────────┐      ┌──────────────┐
│ Create Alert │        │ Create Alert │      │ Create Alert │
│ - type       │        │ - type       │      │ - type       │
│ - category   │        │ - category   │      │ - category   │
│ - message    │        │ - message    │      │ - message    │
│ - action     │        │ - action     │      │ - action     │
│ - reference  │        │ - reference  │      │ - reference  │
└──────────────┘        └──────────────┘      └──────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │ Check Pending Applications    │
                │ - GST Refunds > 5             │
                │ - Duty Drawback > 10          │
                └───────────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │ Return alerts array           │
                │ Sorted by priority            │
                │ (Critical → Warning → Info)   │
                └───────────────────────────────┘
```

## Database Schema

```
┌─────────────────────────────────────────────────────────────────────┐
│  tabGST Export Refund                                                │
├─────────────────────────────────────────────────────────────────────┤
│  PK: name (GST-REF-####)                                            │
│  FK: company → tabCompany                                           │
│  FK: iec_number → tabIEC Registration                               │
│  FK: invoice_number → tabSales Invoice                              │
│  Fields: shipping_bill_number, igst_amount, cess_amount,            │
│          total_refund_claimed, refund_sanctioned, arn_number,       │
│          status, processing_time_days, utr_number                   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  tabLUT Bond Tracking                                                │
├─────────────────────────────────────────────────────────────────────┤
│  PK: name (LUT-####)                                                │
│  FK: company → tabCompany                                           │
│  FK: iec_number → tabIEC Registration                               │
│  FK: previous_lut_number → tabLUT Bond Tracking                     │
│  FK: renewed_lut_number → tabLUT Bond Tracking                      │
│  Fields: lut_bond_number, document_type, valid_from, valid_till,    │
│          days_to_expiry, bond_amount, bg_number, status             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  tabExport Incentive Scheme                                          │
├─────────────────────────────────────────────────────────────────────┤
│  PK: name (EIS-####)                                                │
│  FK: company → tabCompany                                           │
│  FK: iec_number → tabIEC Registration                               │
│  FK: invoice_number → tabSales Invoice                              │
│  FK: hs_code → tabCustoms Tariff Number                             │
│  Fields: scheme_type, application_number, shipping_bill_number,     │
│          fob_value, incentive_rate, incentive_amount,               │
│          scrip_number, scrip_value, scrip_utilized_amount, status   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  tabDuty Drawback Claim                                              │
├─────────────────────────────────────────────────────────────────────┤
│  PK: name (DDB-####)                                                │
│  FK: company → tabCompany                                           │
│  FK: iec_number → tabIEC Registration                               │
│  FK: invoice_number → tabSales Invoice                              │
│  FK: hs_code → tabCustoms Tariff Number                             │
│  Fields: drawback_type, shipping_bill_number, fob_value,            │
│          drawback_rate, drawback_percentage, calculated_drawback,   │
│          claimed_amount, sanctioned_amount, utr_number, status      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  tabDGFT Scheme Tracking                                             │
├─────────────────────────────────────────────────────────────────────┤
│  PK: name (DGFT-####)                                               │
│  FK: company → tabCompany                                           │
│  FK: iec_number → tabIEC Registration                               │
│  FK: hs_code_import → tabCustoms Tariff Number                      │
│  FK: hs_code_export → tabCustoms Tariff Number                      │
│  Fields: scheme_name, authorization_number, import_value_allowed,   │
│          import_value_utilized, import_value_balance,               │
│          export_obligation_value, export_obligation_fulfilled,      │
│          export_obligation_pending, export_obligation_percentage,   │
│          duty_saved, compliance_status, penalty_amount, status      │
└─────────────────────────────────────────────────────────────────────┘
```

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EXISTING EXPORT/IMPORT SYSTEM                     │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Sales Order  │  │ Sales Invoice│  │  Shipment    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Bill of      │  │ Certificate  │  │ Letter of    │             │
│  │ Lading       │  │ of Origin    │  │ Credit       │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ IEC          │  │ Customs House│  │ Shipment     │             │
│  │ Registration │  │ Agent        │  │ Bundle       │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ Document Links
                                │ Data References
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                    COMPLIANCE & REGULATORY SYSTEM                    │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ GST Export   │  │ LUT Bond     │  │ Export       │             │
│  │ Refund       │  │ Tracking     │  │ Incentive    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Duty         │  │ DGFT Scheme  │  │ Compliance   │             │
│  │ Drawback     │  │ Tracking     │  │ Dashboard    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ API Calls
                                │ Data Aggregation
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SYSTEMS (Future)                         │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ GST Portal   │  │ ICEGATE      │  │ DGFT Portal  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Banking      │  │ Email        │  │ SMS          │             │
│  │ Integration  │  │ Notifications│  │ Alerts       │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DOCKER ENVIRONMENT                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Backend Container (ERPNext)                                │    │
│  │  ┌──────────────────────────────────────────────────────┐  │    │
│  │  │  Frappe Framework                                     │  │    │
│  │  │  - DocType Engine                                     │  │    │
│  │  │  - API Layer                                          │  │    │
│  │  │  - Business Logic                                     │  │    │
│  │  │  - api/compliance.py ← NEW                            │  │    │
│  │  └──────────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Database Container (MariaDB/PostgreSQL)                   │    │
│  │  ┌──────────────────────────────────────────────────────┐  │    │
│  │  │  Compliance Tables ← NEW                              │  │    │
│  │  │  - tabGST Export Refund                               │  │    │
│  │  │  - tabLUT Bond Tracking                               │  │    │
│  │  │  - tabExport Incentive Scheme                         │  │    │
│  │  │  - tabDuty Drawback Claim                             │  │    │
│  │  │  - tabDGFT Scheme Tracking                            │  │    │
│  │  └──────────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Redis Container (Cache & Queue)                           │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Nginx Container (Web Server)                              │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SECURITY LAYERS                              │
└─────────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐        ┌──────────────┐      ┌──────────────┐
│ Authentication│       │ Authorization│      │ Data         │
│               │       │              │      │ Encryption   │
│ - User Login  │       │ - Role-Based │      │              │
│ - Session Mgmt│       │   Access     │      │ - SSL/TLS    │
│ - 2FA Support │       │ - Permission │      │ - Field Level│
│               │       │   Rules      │      │ - Audit Log  │
└──────────────┘        └──────────────┘      └──────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │  Compliance Data Access       │
                │  - Read/Write/Create/Delete   │
                │  - Field-Level Permissions    │
                │  - Document-Level Permissions │
                └───────────────────────────────┘
```

---

## Performance Optimization

### Caching Strategy
```
┌─────────────────────────────────────────────────────────────────────┐
│  Request → Check Redis Cache → Cache Hit? → Return Cached Data      │
│                                     │                                │
│                                Cache Miss                            │
│                                     │                                │
│                                     ▼                                │
│                          Query Database                              │
│                                     │                                │
│                                     ▼                                │
│                          Calculate Score                             │
│                                     │                                │
│                                     ▼                                │
│                          Store in Cache (TTL: 5 min)                 │
│                                     │                                │
│                                     ▼                                │
│                          Return Data                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### Database Indexing
```
Indexed Fields:
- company (all tables)
- status (all tables)
- valid_till (IEC, LUT, DGFT)
- shipping_bill_number (GST, Incentive, Drawback)
- authorization_number (DGFT)
- iec_number (all tables)
```

---

**Document Version:** 1.0  
**Last Updated:** February 20, 2026  
**Status:** Complete ✅
