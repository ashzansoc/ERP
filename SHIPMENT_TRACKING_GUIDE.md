# 🚢 Shipment & Container Tracking Module

## Overview
The Shipment & Container Tracking module has been successfully installed in your ERP system. This module allows you to track shipments from booking through delivery with comprehensive container management.

## Installation Status
✅ **Shipment DocType** - Installed
✅ **Shipment Container DocType** - Installed  
✅ **Cache Cleared** - Complete
✅ **Global Search Rebuilt** - Complete

## Accessing the Module

### Via Web Interface
1. Open your ERP at: `http://localhost:8080` (or your configured port)
2. Login with your credentials
3. Navigate to: **Desk → Stock → Shipment**
4. Click **New** to create your first shipment

### Via Search
- Press `Ctrl+K` (or `Cmd+K` on Mac)
- Type "Shipment"
- Select "Shipment" from the results

## Features

### Shipment Information
- **Shipment Type**: Import or Export
- **Shipment Date**: Date of shipment creation
- **Customer**: Link to customer record
- **Booking Number**: Reference number from shipping line

### Port & Route Details
- **Port of Loading**: Origin port
- **Port of Discharge**: Destination port
- **ETD**: Estimated Time of Departure
- **ETA**: Estimated Time of Arrival
- **Actual Departure Date**: Real departure time
- **Actual Arrival Date**: Real arrival time

### Shipping Details
- **Shipping Line**: Carrier company (e.g., Maersk, MSC, CMA CGM)
- **Vessel Name**: Name of the ship
- **Freight Forwarder**: Logistics partner handling the shipment

### Container Tracking
Each shipment can have multiple containers with:
- **Container No**: Unique container identifier
- **Container Type**: 
  - 20ft Standard
  - 40ft Standard
  - 40ft High Cube
  - 20ft Refrigerated
  - 40ft Refrigerated
- **Seal No**: Security seal number
- **Gross Weight**: Total weight in KG
- **Net Weight**: Cargo weight in KG
- **Container Status**: Empty, Loaded, In Transit, Discharged, Returned

### Status Workflow
Track your shipment through these stages:
1. **Draft** - Initial creation
2. **Booked** - Confirmed with shipping line
3. **In Transit** - Shipment is moving
4. **Customs** - Undergoing customs clearance
5. **Delivered** - Reached final destination
6. **Cancelled** - Shipment cancelled

### Integration
- **Bill of Lading**: Link to related B/L document
- **Tracking Notes**: Rich text editor for detailed notes

## Creating Your First Shipment

1. Go to **Stock → Shipment → New**
2. Fill in basic details:
   - Select Shipment Type (Import/Export)
   - Choose Customer
   - Set Shipment Date
3. Add Port Information:
   - Enter Port of Loading
   - Enter Port of Discharge
   - Set ETD and ETA
4. Enter Shipping Details:
   - Shipping Line name
   - Vessel Name
   - Freight Forwarder (optional)
   - Booking Number (optional)
5. Add Containers:
   - Click "Add Row" in the Containers table
   - Enter Container No
   - Select Container Type
   - Add Seal No
   - Enter weights
   - Set Container Status
6. Set Status to "Booked"
7. Click **Save**
8. Click **Submit** when ready to lock the record

## Permissions

### System Manager
- Full access: Create, Read, Write, Delete, Submit, Cancel, Amend

### Stock User
- Create, Read, Write, Submit

## Tips

1. **Naming**: Shipments are auto-named as SHIP-0001, SHIP-0002, etc.
2. **Submittable**: Once submitted, shipments are locked. Use "Amend" to make changes.
3. **Tracking**: Update the Status field as the shipment progresses
4. **Actual Dates**: Fill in actual departure/arrival dates when available
5. **Multiple Containers**: Add as many containers as needed per shipment
6. **Bill of Lading**: Link related B/L documents for complete documentation

## Next Steps

1. Create a test shipment to familiarize yourself with the fields
2. Set up custom fields if you need additional information
3. Create reports for shipment tracking and analytics
4. Set up email notifications for status changes (optional)
5. Integrate with your existing workflow

## Support

If you need to modify the DocType:
1. Go to **Desk → Customize Form**
2. Select "Shipment" in the DocType field
3. Add/modify fields as needed
4. Click **Update**

## Technical Details

- **Module**: Stock
- **DocType Names**: 
  - Shipment (Main)
  - Shipment Container (Child Table)
- **Naming Rule**: SHIP-{####}
- **Submittable**: Yes
- **Track Changes**: Yes

---

**Installation Date**: February 20, 2026
**Status**: ✅ Ready to Use
