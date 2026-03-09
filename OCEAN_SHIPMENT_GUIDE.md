# 🚢 Ocean Shipment & Container Tracking Module

## ✅ Installation Complete!

The Ocean Shipment & Container Tracking module has been successfully installed in your ERP system.

## 📍 Access the Module

### Web Interface
1. Open your browser and go to: **http://localhost:8080**
2. Login with your credentials
3. Navigate to: **Desk → Stock → Ocean Shipment**
4. Click **New** to create your first shipment

### Quick Search
- Press `Ctrl+K` (or `Cmd+K` on Mac)
- Type "Ocean Shipment"
- Select from the results

## 🎯 Features

### Shipment Information
- **Shipment Type**: Import or Export
- **Shipment Date**: Date of shipment creation
- **Customer**: Link to customer record
- **Booking Number**: Reference number from shipping line
- **Auto-naming**: OSHIP-0001, OSHIP-0002, etc.

### Port & Route Details
- **Port of Loading**: Origin port
- **Port of Discharge**: Destination port
- **ETD**: Estimated Time of Departure
- **ETA**: Estimated Time of Arrival
- **Actual Departure Date**: Real departure time (filled when ship departs)
- **Actual Arrival Date**: Real arrival time (filled when ship arrives)

### Shipping Details
- **Shipping Line**: Carrier company (e.g., Maersk, MSC, CMA CGM, Hapag-Lloyd)
- **Vessel Name**: Name of the ship
- **Freight Forwarder**: Logistics partner handling the shipment

### Container Tracking (Multiple Containers per Shipment)
Each shipment can have multiple containers with:
- **Container No**: Unique container identifier (e.g., MSCU1234567)
- **Container Type**: 
  - 20ft Standard
  - 40ft Standard
  - 40ft High Cube
  - 20ft Refrigerated
  - 40ft Refrigerated
- **Seal No**: Security seal number
- **Gross Weight**: Total weight in KG
- **Net Weight**: Cargo weight in KG
- **Container Status**: 
  - Empty
  - Loaded
  - In Transit
  - Discharged
  - Returned

### Status Workflow
Track your shipment through these stages:
1. **Draft** - Initial creation (editable)
2. **Booked** - Confirmed with shipping line
3. **In Transit** - Shipment is moving
4. **Customs** - Undergoing customs clearance
5. **Delivered** - Reached final destination
6. **Cancelled** - Shipment cancelled

### Integration
- **Bill of Lading**: Link to related B/L document
- **Tracking Notes**: Rich text editor for detailed notes and updates

## 📝 Creating Your First Shipment

### Step 1: Basic Details
1. Go to **Stock → Ocean Shipment → New**
2. Select **Shipment Type** (Import or Export)
3. Choose **Customer** from the dropdown
4. Set **Shipment Date** (defaults to today)

### Step 2: Port Information
1. Enter **Port of Loading** (e.g., "Shanghai Port")
2. Enter **Port of Discharge** (e.g., "Los Angeles Port")
3. Set **ETD** (Estimated Time of Departure)
4. Set **ETA** (Estimated Time of Arrival)

### Step 3: Shipping Details
1. Enter **Shipping Line** name
2. Enter **Vessel Name**
3. Add **Freight Forwarder** (optional)
4. Add **Booking Number** (optional)

### Step 4: Add Containers
1. Scroll to **Container Information** section
2. Click **Add Row** in the Containers table
3. Enter **Container No**
4. Select **Container Type**
5. Add **Seal No**
6. Enter **Gross Weight** and **Net Weight**
7. Set **Container Status**
8. Repeat for additional containers

### Step 5: Set Status and Save
1. Set **Status** to "Booked"
2. Click **Save**
3. Click **Submit** when ready to lock the record

## 🔐 Permissions

### System Manager
- Full access: Create, Read, Write, Delete, Submit, Cancel, Amend

### Stock User
- Create, Read, Write, Submit

## 💡 Tips & Best Practices

1. **Naming**: Shipments are auto-named as OSHIP-0001, OSHIP-0002, etc.
2. **Submittable**: Once submitted, shipments are locked. Use "Amend" to make changes.
3. **Tracking**: Update the Status field as the shipment progresses through its journey
4. **Actual Dates**: Fill in actual departure/arrival dates when available for accurate tracking
5. **Multiple Containers**: Add as many containers as needed per shipment
6. **Bill of Lading**: Link related B/L documents for complete documentation
7. **Notes**: Use the Tracking Notes field to record important updates, delays, or issues

## 📊 Reporting & Analytics

You can create custom reports for:
- Shipments by status
- Shipments by customer
- Shipments by port
- Container utilization
- Transit time analysis
- Delayed shipments

## 🔧 Customization

To modify the DocType:
1. Go to **Desk → Customize Form**
2. Select "Ocean Shipment" in the DocType field
3. Add/modify fields as needed
4. Click **Update**

## 🆚 Difference from Standard Shipment

ERPNext has a standard "Shipment" DocType for general logistics. The "Ocean Shipment" module is specifically designed for:
- Import/Export ocean freight
- Container-level tracking
- Port-to-port shipping
- Integration with Bill of Lading
- Customs workflow

## 📱 Mobile Access

The module is fully accessible from mobile devices through the ERPNext mobile interface.

## 🔗 Integration Points

- **Customer**: Links to Customer master
- **Bill of Lading**: Links to B/L documents
- Can be extended to link with:
  - Sales Orders
  - Purchase Orders
  - Delivery Notes
  - Stock Entries

## 🚀 Next Steps

1. ✅ Create a test shipment to familiarize yourself with the fields
2. ✅ Set up custom fields if you need additional information
3. ✅ Create reports for shipment tracking and analytics
4. ✅ Set up email notifications for status changes (optional)
5. ✅ Train your team on using the module
6. ✅ Integrate with your existing workflow

## 📞 Support

For customization or issues:
- Use **Customize Form** to add fields
- Check ERPNext documentation for general Frappe/ERPNext features
- Consult with your system administrator for complex modifications

## 📋 Technical Details

- **Module**: Stock
- **DocType Names**: 
  - Ocean Shipment (Main)
  - Ocean Shipment Container (Child Table)
- **Naming Rule**: OSHIP-{####}
- **Submittable**: Yes
- **Track Changes**: Yes
- **Custom**: Yes
- **Total Fields**: 29

---

**Installation Date**: February 20, 2026  
**Status**: ✅ Ready to Use  
**Access URL**: http://localhost:8080  
**Path**: Desk → Stock → Ocean Shipment
