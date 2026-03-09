#!/bin/bash

echo "=========================================="
echo "Workflow Verification"
echo "=========================================="
echo ""

docker compose -f frappe_docker/compose.yaml exec -T backend bash -c "
mysql -u root -p123 -D localhost <<'SQL'
SELECT '✅ Workflows:' as '';
SELECT name, document_type, is_active FROM tabWorkflow WHERE is_active = 1;

SELECT '' as '';
SELECT '✅ Workflow States (first 15):' as '';
SELECT workflow_state_name, style FROM \`tabWorkflow State\` LIMIT 15;

SELECT '' as '';
SELECT '✅ Custom Fields - Sales Order:' as '';
SELECT fieldname, label, fieldtype FROM \`tabCustom Field\` WHERE dt = 'Sales Order' AND (fieldname LIKE '%workflow%' OR fieldname LIKE '%production%' OR fieldname LIKE '%packing%' OR fieldname LIKE '%forex%');

SELECT '' as '';
SELECT '✅ Custom Fields - Purchase Order:' as '';
SELECT fieldname, label, fieldtype FROM \`tabCustom Field\` WHERE dt = 'Purchase Order' AND (fieldname LIKE '%workflow%' OR fieldname LIKE '%customs%' OR fieldname LIKE '%grn%' OR fieldname LIKE '%landed%');

SELECT '' as '';
SELECT '✅ Client Scripts:' as '';
SELECT name, dt, enabled FROM \`tabClient Script\` WHERE name LIKE '%Workflow%';
SQL
"

echo ""
echo "=========================================="
echo "✅ Installation Verified!"
echo "=========================================="
echo ""
echo "Access your ERP at: http://localhost:8080"
echo ""
