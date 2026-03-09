#!/bin/bash

echo "=========================================="
echo "Compliance & Regulatory Dashboard Setup"
echo "=========================================="
echo ""

# Make scripts executable
chmod +x create_compliance_dashboard.sh
chmod +x create_compliance_schemes.sh
chmod +x create_dgft_tracking.sh

echo "Phase 1: Creating GST Refund and LUT/Bond Tracking..."
./create_compliance_dashboard.sh
if [ $? -ne 0 ]; then
    echo "Error in Phase 1"
    exit 1
fi
echo "✓ Phase 1 Complete"
echo ""

echo "Phase 2: Creating Export Incentive Scheme and Duty Drawback..."
./create_compliance_schemes.sh
if [ $? -ne 0 ]; then
    echo "Error in Phase 2"
    exit 1
fi
echo "✓ Phase 2 Complete"
echo ""

echo "Phase 3: Creating DGFT Scheme Tracking..."
./create_dgft_tracking.sh
if [ $? -ne 0 ]; then
    echo "Error in Phase 3"
    exit 1
fi
echo "✓ Phase 3 Complete"
echo ""

echo "=========================================="
echo "✓ Compliance Dashboard Installation Complete!"
echo "=========================================="
echo ""
echo "Created DocTypes:"
echo "  1. GST Export Refund"
echo "  2. LUT Bond Tracking"
echo "  3. Export Incentive Scheme (MEIS/RoDTEP)"
echo "  4. Duty Drawback Claim"
echo "  5. DGFT Scheme Tracking"
echo ""
echo "API Endpoints:"
echo "  - /api/method/api.compliance.get_compliance_health_score"
echo "  - /api/method/api.compliance.get_compliance_trend"
echo "  - /api/method/api.compliance.export_compliance_report"
echo ""
echo "Access the dashboard:"
echo "  Search for 'Compliance Health Score' in ERPNext"
echo ""
echo "Next Steps:"
echo "  1. Configure IEC Registration (if not done)"
echo "  2. Add LUT/Bond details"
echo "  3. Start tracking GST refunds"
echo "  4. Record export incentive schemes"
echo "  5. Track DGFT authorizations"
echo ""
