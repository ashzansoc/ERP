# Portal White-Label Configuration Guide 🎨

## Overview
Configure your vendor and freight forwarder portals with custom branding, domains, and workflows to match your company identity.

## Branding Configuration

### 1. Logo and Colors
```python
# Set custom logo
frappe.db.set_value('Website Settings', None, 'brand_html', 
    '<img src="/files/your-logo.png" alt="Company Logo" style="height: 40px;">')

# Set custom colors
frappe.db.set_value('Website Settings', None, 'primary_color', '#1a73e8')
frappe.db.set_value('Website Settings', None, 'text_color', '#333333')
```

### 2. Custom Domain
```nginx
# nginx configuration for custom domain
server {
    listen 443 ssl;
    server_name vendor.yourcompany.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
```

### 3. Email Templates
Customize email templates for:
- Document upload notifications
- Quote submissions
- Invoice approvals
- Milestone updates

```python
# Create custom email template
template = frappe.get_doc({
    "doctype": "Email Template",
    "name": "Vendor Document Upload",
    "subject": "Document Uploaded - {{ doc.reference_name }}",
    "response": """
        <p>Dear Team,</p>
        <p>{{ doc.vendor }} has uploaded a new document:</p>
        <ul>
            <li>Type: {{ doc.document_type }}</li>
            <li>Reference: {{ doc.reference_name }}</li>
            <li>Date: {{ doc.upload_date }}</li>
        </ul>
        <p>Please review in the portal.</p>
    """
})
template.insert()
```

## Portal Customization

### 1. Vendor Portal Features
Enable/disable features per vendor:
```python
# Configure vendor portal access
vendor_config = {
    "document_upload": True,
    "invoice_submission": True,
    "po_visibility": True,
    "payment_tracking": True,
    "chat_support": False
}

frappe.db.set_value('Supplier', vendor_name, 'portal_config', 
    json.dumps(vendor_config))
```

### 2. Freight Portal Features
```python
# Configure freight forwarder portal
freight_config = {
    "quote_submission": True,
    "milestone_updates": True,
    "document_upload": True,
    "container_tracking": True,
    "rate_management": True
}

frappe.db.set_value('Supplier', forwarder_name, 'portal_config', 
    json.dumps(freight_config))
```

## Workflow Customization

### 1. Invoice Approval Levels
```python
# Set approval hierarchy
approval_levels = [
    {"level": 1, "role": "Purchase Manager", "amount_limit": 10000},
    {"level": 2, "role": "Finance Manager", "amount_limit": 50000},
    {"level": 3, "role": "Director", "amount_limit": None}
]
```

### 2. Document Requirements
```python
# Define required documents per transaction type
document_requirements = {
    "Purchase Order": ["Invoice", "Packing List"],
    "Shipment": ["Bill of Lading", "Certificate of Origin", "Packing List"],
    "Import": ["Commercial Invoice", "Customs Declaration", "Insurance Certificate"]
}
```

## Multi-Language Support

### 1. Enable Languages
```python
# Enable multiple languages
frappe.db.set_value('System Settings', None, 'language', 'en')

# Add translations
translations = {
    "en": "Upload Document",
    "es": "Subir Documento",
    "fr": "Télécharger le Document",
    "de": "Dokument Hochladen"
}
```

### 2. Language Selector
Add language selector to portal header:
```javascript
// portal_header.js
frappe.ui.toolbar.add_dropdown_button('Language', [
    {label: 'English', action: () => setLanguage('en')},
    {label: 'Español', action: () => setLanguage('es')},
    {label: 'Français', action: () => setLanguage('fr')}
]);
```

## Security Configuration

### 1. Access Control
```python
# Set IP restrictions
frappe.db.set_value('Supplier', vendor_name, 'allowed_ips', 
    '192.168.1.0/24,10.0.0.0/8')

# Set session timeout
frappe.db.set_value('System Settings', None, 'session_expiry', '02:00:00')
```

### 2. Two-Factor Authentication
```python
# Enable 2FA for portal users
frappe.db.set_value('User', portal_user, 'two_factor_auth', 1)
```

## Notification Configuration

### 1. Email Notifications
```python
notification_config = {
    "document_upload": {
        "enabled": True,
        "recipients": ["purchase@company.com"],
        "template": "Vendor Document Upload"
    },
    "quote_received": {
        "enabled": True,
        "recipients": ["logistics@company.com"],
        "template": "New Freight Quote"
    },
    "milestone_update": {
        "enabled": True,
        "recipients": ["customer@company.com"],
        "template": "Shipment Update"
    }
}
```

### 2. SMS Notifications
```python
# Configure SMS for critical updates
sms_config = {
    "provider": "twilio",
    "critical_milestones": ["Departed Origin", "Arrived at Port", "Delivered"],
    "recipients": ["+1234567890"]
}
```

## Dashboard Widgets

### 1. Vendor Dashboard
```python
vendor_widgets = [
    {"type": "number_card", "label": "Open POs", "source": "open_pos"},
    {"type": "number_card", "label": "Pending Invoices", "source": "pending_invoices"},
    {"type": "chart", "label": "Payment History", "chart_type": "line"},
    {"type": "list", "label": "Recent Activities", "limit": 10}
]
```

### 2. Freight Dashboard
```python
freight_widgets = [
    {"type": "number_card", "label": "Active Shipments", "source": "active_shipments"},
    {"type": "number_card", "label": "Pending Quotes", "source": "pending_quotes"},
    {"type": "map", "label": "Shipment Tracking", "source": "shipment_locations"},
    {"type": "chart", "label": "On-Time Performance", "chart_type": "bar"}
]
```

## API Configuration

### 1. API Keys
```python
# Generate API key for vendor
api_key = frappe.generate_hash(length=32)
api_secret = frappe.generate_hash(length=32)

frappe.get_doc({
    "doctype": "API Key",
    "user": vendor_user,
    "api_key": api_key,
    "api_secret": api_secret
}).insert()
```

### 2. Webhook Configuration
```python
# Set up webhooks for external integrations
webhook = frappe.get_doc({
    "doctype": "Webhook",
    "webhook_doctype": "Shipment Milestone",
    "webhook_docevent": "after_insert",
    "request_url": "https://external-system.com/webhook",
    "request_method": "POST"
})
webhook.insert()
```

## Testing Configuration

### 1. Test Accounts
```bash
# Create test vendor account
bench --site mysite execute frappe.get_doc({
    "doctype": "User",
    "email": "test.vendor@example.com",
    "first_name": "Test",
    "last_name": "Vendor",
    "roles": [{"role": "Vendor"}]
}).insert()
```

### 2. Sample Data
```python
# Create sample data for testing
create_sample_purchase_orders(vendor="Test Vendor", count=5)
create_sample_shipments(forwarder="Test Forwarder", count=3)
create_sample_quotes(forwarder="Test Forwarder", count=10)
```

## Performance Optimization

### 1. Caching
```python
# Enable portal caching
frappe.cache().set_value('portal_cache_enabled', True)
frappe.cache().set_value('portal_cache_ttl', 300)  # 5 minutes
```

### 2. Database Indexing
```sql
-- Add indexes for better performance
CREATE INDEX idx_vendor_docs ON `tabVendor Document Log`(vendor, upload_date);
CREATE INDEX idx_freight_quotes ON `tabFreight Quote`(freight_forwarder, quote_date);
CREATE INDEX idx_shipment_milestones ON `tabShipment Milestone`(shipment, milestone_date);
```

## Backup and Recovery

### 1. Automated Backups
```bash
# Set up daily backups
bench --site mysite backup --with-files
```

### 2. Data Export
```python
# Export portal data
frappe.get_doc({
    "doctype": "Data Export",
    "reference_doctype": "Vendor Document Log",
    "file_type": "CSV"
}).insert()
```
