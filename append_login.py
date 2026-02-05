import requests

@frappe.whitelist(allow_guest=True, methods=["POST"])
def login_via_firebase(id_token):
    try:
        # Verify the token with Google
        response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}")
        if response.status_code != 200:
            frappe.throw("Invalid Token")
        
        token_info = response.json()
        email = token_info.get("email")
        if not email:
             frappe.throw("Email not found in token")
             
        # Check if user exists
        if not frappe.db.exists("User", email):
            # Create User
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": token_info.get("given_name", ""),
                "last_name": token_info.get("family_name", ""),
                "enabled": 1,
                "user_type": "System User", 
                "send_welcome_email": 0
            })
            user.insert(ignore_permissions=True)
            
        # Login
        frappe.local.login_manager.login_as(email)
        
        return {"status": "success"}
        
    except Exception as e:
        frappe.log_error(f"Firebase Login Error: {str(e)}")
        return {"status": "error", "message": str(e)}