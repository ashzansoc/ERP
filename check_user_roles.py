import frappe
import os

# Initialize frappe
if not frappe.conf:
    frappe.init(site='frontend')
    frappe.connect()

# Get the latest user created
users = frappe.get_all("User", fields=["name", "email", "creation", "enabled", "user_type"], order_by="creation desc", limit=5)

print("Latest Users:")
for user in users:
    print(f"User: {user.name}, Email: {user.email}, Type: {user.user_type}")
    roles = frappe.get_roles(user.name)
    # print(f"Roles: {roles}") # Commented out to save space
    if "System Manager" in roles:
        print("  -> Is System Manager")
    else:
        print("  -> NOT System Manager")
    print("-" * 20)