# Google Firebase Authentication - Design Document

## Architecture Overview

### System Components

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Browser       │         │   ERPNext        │         │   Firebase      │
│   (Frontend)    │◄───────►│   (Backend)      │◄───────►│   Auth          │
└─────────────────┘         └──────────────────┘         └─────────────────┘
        │                            │                            │
        │  1. Click Google Sign-in   │                            │
        ├───────────────────────────►│                            │
        │                            │                            │
        │  2. Initialize Firebase    │                            │
        ├────────────────────────────┼───────────────────────────►│
        │                            │                            │
        │  3. Google OAuth Flow      │                            │
        │◄───────────────────────────┼────────────────────────────┤
        │                            │                            │
        │  4. Send ID Token          │                            │
        ├───────────────────────────►│                            │
        │                            │  5. Verify Token           │
        │                            ├───────────────────────────►│
        │                            │◄───────────────────────────┤
        │                            │  6. Create/Update User     │
        │                            │                            │
        │  7. Return Session         │                            │
        │◄───────────────────────────┤                            │
```

## Implementation Design

### 1. Firebase Configuration

**Location**: Custom Frappe app or site configuration

**Configuration Structure**:
```python
# sites/frontend/site_config.json (add these)
{
    "firebase_config": {
        "apiKey": "YOUR_API_KEY",
        "authDomain": "ashutosh-a2720.firebaseapp.com",
        "projectId": "ashutosh-a2720"
    }
}
```

**Environment Variables** (Docker):
```bash
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=ashutosh-a2720.firebaseapp.com
FIREBASE_PROJECT_ID=ashutosh-a2720
FIREBASE_SERVICE_ACCOUNT_KEY=/path/to/service-account.json
```

### 2. Frontend Implementation

**File Structure**:
```
frappe-bench/
└── apps/
    └── frappe/
        └── frappe/
            └── public/
                └── js/
                    └── frappe/
                        └── ui/
                            └── login.js (modify)
```

**Login Page Modifications**:

**HTML Template** (`frappe/templates/pages/login.html`):
```html
<!-- Add Firebase SDK -->
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js"></script>

<!-- Google Sign-in Button -->
<div class="google-signin-container" style="margin-top: 20px;">
    <button id="google-signin-btn" class="btn btn-default btn-block" 
            style="display: flex; align-items: center; justify-content: center; gap: 10px;">
        <svg width="18" height="18" viewBox="0 0 18 18">
            <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
            <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/>
            <path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707s.102-1.167.282-1.707V4.961H.957C.347 6.175 0 7.55 0 9s.348 2.825.957 4.039l3.007-2.332z"/>
            <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.961L3.964 7.293C4.672 5.163 6.656 3.58 9 3.58z"/>
        </svg>
        <span>Sign in with Google</span>
    </button>
    <div id="google-signin-error" class="text-danger" style="margin-top: 10px; display: none;"></div>
</div>
```

**JavaScript Implementation** (`frappe/public/js/frappe/ui/login.js`):
```javascript
// Initialize Firebase
function initializeFirebaseAuth() {
    frappe.call({
        method: 'frappe.auth.get_firebase_config',
        callback: function(r) {
            if (r.message) {
                const firebaseConfig = r.message;
                firebase.initializeApp(firebaseConfig);
                setupGoogleSignIn();
            }
        }
    });
}

// Setup Google Sign-in
function setupGoogleSignIn() {
    const googleSignInBtn = document.getElementById('google-signin-btn');
    const errorDiv = document.getElementById('google-signin-error');
    
    googleSignInBtn.addEventListener('click', async function(e) {
        e.preventDefault();
        googleSignInBtn.disabled = true;
        googleSignInBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Signing in...';
        errorDiv.style.display = 'none';
        
        try {
            const provider = new firebase.auth.GoogleAuthProvider();
            provider.addScope('email');
            provider.addScope('profile');
            
            const result = await firebase.auth().signInWithPopup(provider);
            const idToken = await result.user.getIdToken();
            
            // Send token to backend
            await authenticateWithFirebase(idToken);
            
        } catch (error) {
            console.error('Google sign-in error:', error);
            errorDiv.textContent = error.message || 'Failed to sign in with Google';
            errorDiv.style.display = 'block';
            googleSignInBtn.disabled = false;
            googleSignInBtn.innerHTML = '<svg>...</svg><span>Sign in with Google</span>';
        }
    });
}

// Authenticate with backend
async function authenticateWithFirebase(idToken) {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'frappe.auth.firebase_login',
            args: {
                id_token: idToken
            },
            callback: function(r) {
                if (r.message && r.message.success) {
                    window.location.href = r.message.redirect_to || '/app';
                    resolve();
                } else {
                    reject(new Error(r.message.error || 'Authentication failed'));
                }
            },
            error: function(err) {
                reject(err);
            }
        });
    });
}

// Initialize on page load
$(document).ready(function() {
    if (window.location.pathname === '/login') {
        initializeFirebaseAuth();
    }
});
```

### 3. Backend Implementation

**File Structure**:
```
frappe-bench/
└── apps/
    └── frappe/
        └── frappe/
            └── auth.py (create/modify)
```

**Python Backend** (`frappe/auth.py`):
```python
import frappe
import firebase_admin
from firebase_admin import auth, credentials
import json

# Initialize Firebase Admin SDK
def initialize_firebase_admin():
    """Initialize Firebase Admin SDK with service account"""
    if not firebase_admin._apps:
        service_account_path = frappe.conf.get('firebase_service_account_key')
        if service_account_path:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        else:
            # Use environment variables
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": frappe.conf.get('firebase_project_id'),
                "private_key": frappe.conf.get('firebase_private_key'),
                "client_email": frappe.conf.get('firebase_client_email'),
            })
            firebase_admin.initialize_app(cred)

@frappe.whitelist(allow_guest=True)
def get_firebase_config():
    """Return Firebase configuration for frontend"""
    return {
        "apiKey": frappe.conf.get('firebase_api_key'),
        "authDomain": frappe.conf.get('firebase_auth_domain'),
        "projectId": frappe.conf.get('firebase_project_id')
    }

@frappe.whitelist(allow_guest=True)
def firebase_login(id_token):
    """Authenticate user with Firebase ID token"""
    try:
        # Initialize Firebase Admin if not already done
        initialize_firebase_admin()
        
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')
        name = decoded_token.get('name', '')
        picture = decoded_token.get('picture', '')
        
        if not email:
            return {
                "success": False,
                "error": "Email not provided by Google"
            }
        
        # Check if user exists
        user = frappe.db.exists("User", email)
        
        if not user:
            # Create new user
            user_doc = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": name.split()[0] if name else email.split('@')[0],
                "last_name": ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                "user_image": picture,
                "enabled": 1,
                "send_welcome_email": 0,
                "user_type": "System User"
            })
            user_doc.insert(ignore_permissions=True)
            user = email
        else:
            # Update user info
            user_doc = frappe.get_doc("User", email)
            if picture and not user_doc.user_image:
                user_doc.user_image = picture
                user_doc.save(ignore_permissions=True)
        
        # Create session
        frappe.local.login_manager.login_as(user)
        frappe.local.login_manager.user = user
        
        # Set session
        frappe.local.session_obj = frappe.auth.get_session_manager()
        
        return {
            "success": True,
            "redirect_to": "/app"
        }
        
    except auth.InvalidIdTokenError:
        frappe.log_error("Invalid Firebase ID token", "Firebase Auth Error")
        return {
            "success": False,
            "error": "Invalid authentication token"
        }
    except Exception as e:
        frappe.log_error(str(e), "Firebase Auth Error")
        return {
            "success": False,
            "error": "Authentication failed. Please try again."
        }
```

### 4. Docker Configuration

**Update `pwd.yml`** to include Firebase environment variables:
```yaml
services:
  backend:
    environment:
      FIREBASE_API_KEY: ${FIREBASE_API_KEY}
      FIREBASE_AUTH_DOMAIN: ${FIREBASE_AUTH_DOMAIN}
      FIREBASE_PROJECT_ID: ${FIREBASE_PROJECT_ID}
      FIREBASE_SERVICE_ACCOUNT_KEY: ${FIREBASE_SERVICE_ACCOUNT_KEY}
```

**Create `.env` file**:
```bash
FIREBASE_API_KEY=your_api_key_here
FIREBASE_AUTH_DOMAIN=ashutosh-a2720.firebaseapp.com
FIREBASE_PROJECT_ID=ashutosh-a2720
FIREBASE_SERVICE_ACCOUNT_KEY=/home/frappe/frappe-bench/firebase-service-account.json
```

### 5. Firebase Setup Steps

1. **Enable Google Authentication in Firebase Console**
2. **Configure OAuth Consent Screen**
3. **Add Authorized Domains** (localhost:8080)
4. **Download Service Account Key**
5. **Configure Environment Variables**

## Security Considerations

### Token Verification
- Always verify Firebase ID tokens on the server side
- Never trust client-side authentication alone
- Implement token expiration checks

### User Creation
- Validate email domain if needed
- Set appropriate user roles and permissions
- Implement rate limiting for user creation

### Session Management
- Use Frappe's built-in session management
- Implement session timeout
- Clear sessions on logout

## Error Handling

### Frontend Errors
- Network failures
- Popup blocked
- User cancellation
- Invalid credentials

### Backend Errors
- Token verification failures
- User creation failures
- Database errors
- Firebase service unavailable

## Testing Strategy

### Unit Tests
- Token verification logic
- User creation/update logic
- Configuration loading

### Integration Tests
- End-to-end authentication flow
- Session creation
- User profile updates

### Manual Testing
- Different browsers
- Mobile devices
- Network conditions
- Error scenarios

## Rollback Plan

If issues occur:
1. Disable Google sign-in button via feature flag
2. Revert frontend changes
3. Keep backend code for future use
4. Document issues for resolution

## Performance Metrics

- Authentication completion time: < 3 seconds
- Page load impact: < 100ms
- JavaScript bundle size increase: < 50KB
- API response time: < 500ms