import os

file_path = '/home/frappe/frappe-bench/apps/frappe/frappe/www/login.html'

with open(file_path, 'r') as f:
    content = f.read()

# Replacements
replacements = {
    'apiKey: "REPLACE_WITH_YOUR_API_KEY"': 'apiKey: "AIzaSyBVTHBeu7QUIua4HmWAm8rFjssDK-YkJf4"',
    'messagingSenderId: "REPLACE_WITH_YOUR_SENDER_ID"': 'messagingSenderId: "302526843375"',
    'appId: "REPLACE_WITH_YOUR_APP_ID"': 'appId: "1:302526843375:web:e39ec25b7d217336e50e1a"',
    'storageBucket: "ashutosh-a2720.appspot.com"': 'storageBucket: "ashutosh-a2720.firebasestorage.app"'
}

new_content = content
for old, new in replacements.items():
    new_content = new_content.replace(old, new)

with open(file_path, 'w') as f:
    f.write(new_content)

print("Firebase configuration updated successfully.")