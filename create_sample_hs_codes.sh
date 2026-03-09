#!/bin/bash
# Create sample HS codes

cd frappe_docker

echo "📝 Creating sample HS codes..."

docker-compose exec -T backend bench --site localhost console <<'PYTHON'
import frappe

samples = [
    {"hs_code": "8517.62", "description": "Telecom equipment - reception, conversion and transmission"},
    {"hs_code": "8471.30", "description": "Portable computers, weighing not more than 10 kg"},
    {"hs_code": "8528.72", "description": "Reception apparatus for television, color"},
    {"hs_code": "6203.42", "description": "Men's or boys' trousers, breeches and shorts, of cotton"},
    {"hs_code": "6204.62", "description": "Women's or girls' trousers, breeches and shorts, of cotton"},
]

for s in samples:
    if not frappe.db.exists("HS Code", s["hs_code"]):
        print(f"Creating HS Code: {s['hs_code']}")
        hs = frappe.get_doc({
            "doctype": "HS Code",
            "hs_code": s["hs_code"],
            "description": s["description"],
            "duty_rates": [
                {
                    "country_of_origin": "China",
                    "destination_country": "United States",
                    "duty_rate": 10.0,
                    "valid_from": "2024-01-01",
                },
                {
                    "country_of_origin": "India",
                    "destination_country": "United States",
                    "duty_rate": 8.0,
                    "valid_from": "2024-01-01",
                }
            ]
        })
        hs.insert(ignore_permissions=True)
    else:
        print(f"HS Code {s['hs_code']} already exists")

frappe.db.commit()
print(f"\\n✅ Created {len(samples)} sample HS codes")

PYTHON

echo ""
echo "✅ Done!"
