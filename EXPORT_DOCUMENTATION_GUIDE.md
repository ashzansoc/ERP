# Export Documentation System - User Guide

## Overview
Your ERPNext system now includes a comprehensive export documentation management system with the following features:

## Available Documents

### 1. Bill of Lading (B/L) Tracking
**Access:** Search for "Bill of Lading" in ERPNext

**Features:**
- B/L Number and Date tracking
- Status tracking (Draft → Delivered)
- Shipper & Consignee details
- Port information
- Vessel & Carrier details
- Container tracking (multiple containers)
- Cargo details with weight and volume
- Freight terms and payment
- Real-time tracking with URL
- Estimated vs Actual arrival dates

**Linking Fields:**
- Sales Order
- Purchase Order
- Shipment
- Delivery Note

---

### 2. Certificate of Origin
**Access:** Search for "Certificate of Origin" in ERPNext

**Features:**
- Certificate Number and Type (GSP, FTA, Form A/B/E/D)
- Status workflow (Draft → Issued)
- Exporter & Consignee details with IEC
- Shipment and transport details
- Item-wise origin declaration with HS Codes
- Origin criteria per item
- Issuing authority and signatory
- Validity tracking

**Linking Fields:**
- Sales Order ✓
- Purchase Order ✓
- Shipment ✓
- Bill of Lading ✓
- Invoice Number

---

### 3. Letter of Credit (LC) Tracking
**Access:** Search for "Letter of Credit" in ERPNext

**Features:**
- LC Number and comprehensive LC types
- Status tracking (Draft → Completed)
- Issuing & Advising bank details with SWIFT
- Applicant (Buyer) & Beneficiary (Seller) details
- LC Amount with tolerance and utilization tracking
- Validity and shipment dates
- Required documents checklist with status
- Payment terms (Sight/Usance)
- Amendment tracking
- Special conditions and instructions

**Linking Fields:**
- Sales Order ✓
- Purchase Order ✓
- Shipment ✓
- Bill of Lading ✓

---

### 4. IEC Registration
**Access:** Search for "IEC Registration" in ERPNext

**Features:**
- IEC Number storage
- Registration type (Importer/Exporter/Both)
- Status tracking (Active/Suspended/Cancelled)
- Validity period tracking
- Company information with PAN, GSTIN, CIN
- Contact details
- Bank details with SWIFT and AD Code
- Nature of business and products

---

### 5. Customs House Agent (CHA) Tracking
**Access:** Search for "Customs House Agent" in ERPNext

**Features:**
- CHA License Number
- License validity tracking
- Contact and company information
- Tax registration (PAN, GSTIN, Customs Code)
- Bank details
- Services offered and specialization
- Shipment tracking table
- Performance metrics (auto-calculated)
  - Total shipments handled
  - Average clearance time
  - Total value handled
- Rating system

**Shipment Tracking:**
Each CHA can track multiple shipments with:
- Import/Export type
- B/L or AWB numbers
- Status (Pending → Cleared)
- Clearance dates
- CHA charges

---

### 6. Shipment Document Bundle
**Access:** Search for "Shipment Document Bundle" in ERPNext

**Features:**
- Auto-generate ZIP bundles of all shipment documents
- Link all related documents:
  - Sales Order
  - Purchase Order
  - Commercial Invoice
  - Delivery Note
  - Packing Slip
  - Shipment
  - Bill of Lading
  - Certificate of Origin
  - Letter of Credit
- Include/exclude attachments
- Include/exclude print formats (PDFs)
- Organized folder structure in ZIP
- Manifest file with document list
- Download tracking

**How to Use:**
1. Create a new "Shipment Document Bundle"
2. Select the Shipment
3. Link all related documents
4. Check options (Include Attachments, Include Print Formats)
5. Save the bundle
6. Use the "Generate Bundle" button to create ZIP file
7. Download the generated ZIP file

**Folder Structure in ZIP:**
```
01_Orders/
02_Invoices/
03_Delivery/
04_Packing/
05_Shipment/
06_Transport_Documents/
07_Certificates/
08_Financial_Documents/
attachments/
MANIFEST.txt
```

---

## Workflow Example

### Export Shipment Process:

1. **Create Sales Order**
   - Enter customer and items

2. **Create IEC Registration** (if not exists)
   - Store your company's IEC details

3. **Create Letter of Credit** (if applicable)
   - Link to Sales Order
   - Track LC status and documents

4. **Create Delivery Note**
   - From Sales Order

5. **Create Commercial Invoice**
   - From Delivery Note

6. **Create Packing Slip**
   - From Delivery Note

7. **Create Shipment**
   - Link Delivery Note

8. **Select Customs House Agent**
   - Choose CHA from master
   - Add shipment to CHA's tracking

9. **Create Bill of Lading**
   - Link to Shipment, Sales Order
   - Add container details
   - Track status

10. **Create Certificate of Origin**
    - Link to Sales Order, Shipment, B/L
    - Add items with HS Codes
    - Get authority signature

11. **Create Document Bundle**
    - Link all above documents
    - Generate ZIP bundle
    - Download for submission

---

## API Functions

### Generate Bundle Programmatically

```python
import frappe

# Generate bundle from existing bundle document
result = frappe.call(
    'frappe.custom.shipment_bundle_generator.generate_shipment_bundle',
    bundle_name='SDB-0001'
)

# Auto-create bundle from shipment
bundle_name = frappe.call(
    'frappe.custom.shipment_bundle_generator.create_bundle_from_shipment',
    shipment_name='MAT-SHP-2024-00001'
)
```

---

## Reports & Analytics

### Available Views:
- Bill of Lading List (filter by status, port, shipping line)
- Certificate of Origin List (filter by country, type, status)
- Letter of Credit List (filter by status, bank, amount)
- CHA Performance Dashboard (shipments, clearance time)
- IEC Registration List (filter by status, type)

### Custom Reports:
You can create custom reports for:
- Shipments by destination
- LC utilization tracking
- CHA performance comparison
- Document completion status
- Export value by country

---

## Tips & Best Practices

1. **Always link documents** - Use the linking fields to connect related documents for easy tracking

2. **Update statuses regularly** - Keep document statuses current for accurate reporting

3. **Use Document Bundles** - Generate bundles before submitting to banks or customs

4. **Track CHA performance** - Monitor clearance times and costs across different CHAs

5. **Maintain IEC records** - Keep IEC registration details updated with validity dates

6. **LC Amendment tracking** - Record all LC amendments for audit trail

7. **Attach supporting documents** - Upload scanned copies of physical documents

8. **Use remarks fields** - Add notes for special conditions or issues

---

## Access Control

Documents are accessible based on roles:
- **Stock User/Manager**: Bill of Lading, CHA, Shipment Bundles
- **Sales User/Manager**: Certificate of Origin, IEC Registration
- **Accounts User/Manager**: Letter of Credit, IEC Registration
- **Purchase User/Manager**: CHA tracking

---

## Support & Customization

For additional customization needs:
- Custom print formats for documents
- Additional fields specific to your business
- Integration with shipping line APIs
- Automated email notifications
- Custom workflows and approvals

Contact your system administrator for assistance.
