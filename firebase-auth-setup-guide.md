# Firebase Google Authentication - Quick Setup Guide

## Prerequisites
- Firebase project: ashutosh-a2720
- ERPNext running on Docker (localhost:8080)
- Access to Google Cloud Console

## Step 1: Firebase Console Setup

### 1.1 Enable Google Authentication
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `ashutosh-a2720`
3. Navigate to **Authentication** → **Sign-in method**
4. Click on **Google** provider
5. Toggle **Enable**
6. Set support email
7. Click **Save**

### 1.2 Configure Authorized Domains
1. In Authentication settings, go to **Settings** tab
2. Scroll to **Authorized domains**
3. Add: `localhost` (for development)
4. Add your production domain when ready

### 1.3 Get Firebase Configuration
1. Go to **Project Settings** (gear icon)
2. Scroll to **Your apps** section
3. Click **Web app** icon (</>) to create a web app
4. Register app with name: "ERPNext Auth"
5. Copy the Firebase configuration object:
```javascript
{
  apiKey: "YOUR_API_KEY",
  authDomain: "ashutosh-a2720.firebaseapp.com",
  projectId: "ashutosh-a2720"
}
```

### 1.4 Generate Service Account Key
1. Go to **Project Settings** → **Service accounts**
2. Click **Generate new private key**
3. Download the JSON file
4. Rename it to `firebase-service-account.json`

## Step 2: Configure ERPNext

### 2.1 Copy Service Account Key
```bash
# Copy the service account key to your project
cp ~/Downloads/firebase-service-account.json frappe_docker/firebase-service-account.json
```

### 2.2 Create Environment File
```bash
cd frappe_docker

# Create or update .env file
cat >> .env << EOF

# Firebase Configuration
FIREBASE_API_KEY=your_api_key_here
FIREBASE_AUTH_DOMAIN=ashutosh-a2720.firebaseapp.com
FIREBASE_PROJECT_ID=ashutosh-a2720
FIREBASE_SERVICE_ACCOUNT_KEY=/home/frappe/frappe-bench/firebase-service-account.json
EOF
```

### 2.3 Update Docker Compose
Add Firebase environment variables to `pwd.yml`:

```yaml
services:
  backend:
    environment:
      # ... existing environment variables ...
      FIREBASE_API_KEY: ${FIREBASE_API_KEY}
      FIREBASE_AUTH_DOMAIN: ${FIREBASE_AUTH_DOMAIN}
      FIREBASE_PROJECT_ID: ${FIREBASE_PROJECT_ID}
    volumes:
      # ... existing volumes ...
      - ./firebase-service-account.json:/home/frappe/frappe-bench/firebase-service-account.json:ro
```

## Step 3: Install Dependencies

### 3.1 Add Firebase Admin SDK
```bash
# Enter the backend container
docker compose -f pwd.yml exec backend bash

# Install firebase-admin
pip install firebase-admin

# Exit container
exit
```

## Step 4: Implement Backend Code

### 4.1 Create Authentication Module
```bash
# Create the auth module
docker compose -f pwd.yml exec backend bash -c "cat > /home/frappe/frappe-bench/apps/frappe/frappe/auth_firebase.py << 'EOF'
import frappe
import firebase_admin
from firebase_admin import auth, credentials
import os

def initialize_firebase_admin():
    if not firebase_admin._apps:
        service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)

@frappe.whitelist(allow_guest=True)
def get_firebase_config():
    return {
        'apiKey': os.getenv('FIREBASE_API_KEY'),
        'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
        'projectId': os.getenv('FIREBASE_PROJECT_ID')
    }

@frappe.whitelist(allow_guest=True)
def firebase_login(id_token):
    try:
        initialize_firebase_admin()
        decoded_token = auth.verify_id_token(id_token)
        email = decoded_token.get('email')
        name = decoded_token.get('name', '')
        
        if not email:
            return {'success': False, 'error': 'Email not provided'}
        
        # Create or get user
        if not frappe.db.exists('User', email):
            user_doc = frappe.get_doc({
                'doctype': 'User',
                'email': email,
                'first_name': name.split()[0] if name else email.split('@')[0],
                'enabled': 1,
                'user_type': 'System User'
            })
            user_doc.insert(ignore_permissions=True)
        
        # Login
        frappe.local.login_manager.login_as(email)
        return {'success': True, 'redirect_to': '/app'}
        
    except Exception as e:
        frappe.log_error(str(e), 'Firebase Auth Error')
        return {'success': False, 'error': str(e)}
EOF"
```

## Step 5: Implement Frontend Code

### 5.1 Modify Login Page
```bash
# This will be done in the next steps with proper file modifications
# For now, we'll create a custom app to override the login page
```

## Step 6: Restart Services

```bash
# Restart all services to apply changes
docker compose -f pwd.yml restart

# Check logs
docker compose -f pwd.yml logs -f backend
```

## Step 7: Test Authentication

1. Open http://localhost:8080/login
2. You should see the "Sign in with Google" button
3. Click the button
4. Complete Google OAuth flow
5. You should be logged into ERPNext

## Troubleshooting

### Issue: "Sign in with Google" button not appearing
- Check browser console for JavaScript errors
- Verify Firebase SDK is loaded
- Check network tab for failed requests

### Issue: "Invalid authentication token"
- Verify service account key is correctly mounted
- Check Firebase Admin SDK initialization
- Verify token is being sent to backend

### Issue: "Email not provided by Google"
- Ensure email scope is requested in OAuth
- Check Google account has email address
- Verify OAuth consent screen configuration

### Issue: User creation fails
- Check ERPNext user permissions
- Verify database connectivity
- Check backend logs for detailed errors

## Next Steps

1. **Customize button design** to match your branding
2. **Add user role mapping** based on email domain
3. **Implement user profile sync** to update user data
4. **Add analytics** to track authentication usage
5. **Set up production OAuth** with your domain

## Security Checklist

- [ ] Service account key is not committed to git
- [ ] Environment variables are properly secured
- [ ] OAuth consent screen is configured
- [ ] Authorized domains are restricted
- [ ] Token verification is implemented server-side
- [ ] Rate limiting is configured
- [ ] Error messages don't leak sensitive information
- [ ] Logs are properly sanitized

## Support

For issues or questions:
1. Check ERPNext logs: `docker compose -f pwd.yml logs backend`
2. Check Firebase Console for authentication logs
3. Review Google Cloud Console for OAuth errors
4. Check browser console for frontend errors