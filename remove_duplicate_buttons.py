import os

file_path = '/home/frappe/frappe-bench/apps/frappe/frappe/www/login.html'

with open(file_path, 'r') as f:
    content = f.read()

button_html = """
<div style="margin-bottom: 10px;">
    <button id="firebase-google-login" class="btn btn-default btn-block btn-sm" style="display: flex; align-items: center; justify-content: center; gap: 8px; background-color: #fff; color: #444; border: 1px solid #ddd;">
       <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="18" height="18">
       Login with Google
    </button>
</div>
"""

# Split content by the button HTML
parts = content.split(button_html)

# If we have more than 2 parts (meaning more than 1 button), we need to reconstruct
# We want to keep the button in the login section. 
# Based on previous context, the first occurrence seems to be in the login section.
# Let's keep the first one and remove others.

if len(parts) > 2:
    # Keep the first button (between parts[0] and parts[1])
    # Remove subsequent buttons
    new_content = parts[0] + button_html + "".join(parts[1:])
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    print("Duplicate buttons removed.")
else:
    print("No duplicate buttons found or only one button exists.")