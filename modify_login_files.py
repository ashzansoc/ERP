import os

# --- Modify login.py ---
login_py_path = "/home/frappe/frappe-bench/apps/frappe/frappe/www/login.py"

with open(login_py_path, "r") as f:
    content = f.read()

# Add role assignment code
if 'user.insert(ignore_permissions=True)' in content and 'user.add_roles("System Manager")' not in content:
    new_content = content.replace(
        'user.insert(ignore_permissions=True)',
        'user.insert(ignore_permissions=True)\n            user.add_roles("System Manager")'
    )
    
    with open(login_py_path, "w") as f:
        f.write(new_content)
    print("Updated login.py to add System Manager role.")
else:
    print("login.py already has role assignment or pattern not found.")

# --- Modify login.html ---
login_html_path = "/home/frappe/frappe-bench/apps/frappe/frappe/www/login.html"

with open(login_html_path, "r") as f:
    lines = f.readlines()

new_lines = []
in_loop = False
for line in lines:
    if '{% for provider in provider_logins %}' in line:
        new_lines.append(line.replace('{% for provider in provider_logins %}', '{% for provider in provider_logins if provider.provider_name != "Google" %}'))
    else:
        new_lines.append(line)

with open(login_html_path, "w") as f:
    f.writelines(new_lines)
print("Updated login.html to skip Google in provider_logins.")