# 🔥 Firebase Google Authentication - Setup Instructions

## ✅ What's Been Implemented

I've successfully implemented the backend and frontend code for Firebase Google Authentication. Here's what's ready:

### Backend (Python)
- ✅ Firebase Admin SDK installed
- ✅ Authentication module created (`auth_firebase.py`)
- ✅ API endpoints for config and login
- ✅ User creation and session management

### Frontend (JavaScript)
- ✅ Firebase SDK integration
- ✅ Google Sign-in button with ERPNext styling
- ✅ OAuth flow implementation
- ✅ Error handling and loading states

### Docker Configuration
- ✅ Environment variables configured
- ✅ Volume mount for service account key
- ✅ Updated pwd.yml

## 🚀 Next Steps - Firebase Console Setup

You need to complete these steps in the Firebase Console to activate the authentication:

### Step 1: Access Firebase Console

1. Go to https://console.firebase.google.com/
2. Select your project: **ashutosh-a2720**

### Step 2: Enable Google Authentication

1. In the left sidebar, click **Authentication**
2. Click on the **Sign-in method** tab
3. Find **Google** in the list of providers
4. Click on **Google**
5. Toggle the **Enable** switch to ON
6. Enter your support email (your email address)
7. Click **Save**

### Step 3: Get Web App Configuration

1. Click the **gear icon** (⚙️) next to "Project Overview"
2. Select **Project settings**
3. Scroll down to **Your apps** section
4. If you don't have a web app:
   - Click the **</>** (Web) icon
   - Register app name: "ERPNext Auth"
   - Don't check "Firebase Hosting"
   - Click **Register app**
5. You'll see a `firebaseConfig` object like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "ashutosh-a2720.firebaseapp.com",
  projectId: "ashutosh-a2720",
  // ... other fields
};
```

6. **Copy the `apiKey` value** - you'll need this!

### Step 4: Generate Service Account Key

1. Still in **Project settings**, click the **Service accounts** tab
2. Click **Generate new private key**
3. Click **Generate key** in the confirmation dialog
4. A JSON file will download - this is your service account key
5. **Save this file securely** - you'll need it next

### Step 5: Configure Your Local Environment

1. **Rename the downloaded service account key**:
   ```bash
   mv ~/Downloads/ashutosh-a2720-*.json frappe_docker/firebase-service-account.json
   ```

2. **Create/Update your .env file**:
   ```bash
   cd frappe_docker
   
   # Add Firebase configuration to .env
   cat >> .env << EOF

# Firebase Configuration
FIREBASE_API_KEY=YOUR_API_KEY_FROM_STEP_3
FIREBASE_AUTH_DOMAIN=ashutosh-a2720.firebaseapp.com
FIREBASE_PROJECT_ID=ashutosh-a2720
FIREBASE_SERVICE_ACCOUNT_KEY=/home/frappe/frappe-bench/firebase-service-account.json
EOF
   ```

3. **Replace `YOUR_API_KEY_FROM_STEP_3`** with the actual API key you copied

### Step 6: Restart Docker Containers

```bash
cd frappe_docker

# Restart all services to load new environment variables
docker compose -f pwd.yml down
docker compose -f pwd.yml up -d

# Wait for services to start (about 30 seconds)
sleep 30

# Check if services are running
docker compose -f pwd.yml ps
```

### Step 7: Test the Authentication

1. Open your browser and go to: **http://localhost:8080/login**
2. You should see:
   - The standard ERPNext login form
   - An "OR" divider
   - A **"Sign in with Google"** button with the Google logo

3. Click the **"Sign in with Google"** button
4. A Google OAuth popup should appear
5. Select your Google account
6. Grant permissions
7. You should be redirected to the ERPNext dashboard!

## 🔍 Troubleshooting

### Issue: "Sign in with Google" button not appearing

**Check 1: Firebase SDK loaded**
- Open browser console (F12)
- Look for any JavaScript errors
- Check if Firebase is defined: type `firebase` in console

**Check 2: Backend configuration**
```bash
# Check if environment variables are set
docker compose -f pwd.yml exec backend env | grep FIREBASE
```

**Check 3: Service account key exists**
```bash
# Check if file exists in container
docker compose -f pwd.yml exec backend ls -la /home/frappe/frappe-bench/firebase-service-account.json
```

### Issue: "Invalid authentication token"

**Solution**: Verify service account key is correctly mounted
```bash
# Check the file content (first few lines)
docker compose -f pwd.yml exec backend head -5 /home/frappe/frappe-bench/firebase-service-account.json
```

### Issue: "Popup blocked"

**Solution**: Allow popups for localhost:8080 in your browser settings

### Issue: "Email not provided by Google"

**Solution**: Ensure your Google account has an email address associated with it

## 📝 Configuration Files Created

1. `/home/frappe/frappe-bench/apps/frappe/frappe/auth_firebase.py` - Backend authentication module
2. `/home/frappe/frappe-bench/apps/frappe/frappe/public/js/firebase_auth.js` - Frontend JavaScript
3. `frappe_docker/pwd.yml` - Updated with Firebase environment variables
4. `frappe_docker/.env.firebase.template` - Environment variable template

## 🎨 Customization Options

### Change Button Text
Edit `/home/frappe/frappe-bench/apps/frappe/frappe/public/js/firebase_auth.js`:
```javascript
// Find this line:
<span>Sign in with Google</span>

// Change to:
<span>Login with Google</span>
```

### Change Button Style
Modify the `googleButton.style.cssText` in the same file to customize colors, padding, etc.

### Add More OAuth Providers
You can extend this implementation to support:
- Facebook Login
- GitHub Login
- Microsoft Login
- Apple Login

Just follow the same pattern in `auth_firebase.py` and `firebase_auth.js`.

## 🔒 Security Checklist

- [ ] Service account key is NOT committed to git
- [ ] `.env` file is in `.gitignore`
- [ ] Firebase Console has authorized domains configured
- [ ] OAuth consent screen is properly configured
- [ ] Only necessary scopes are requested (email, profile)

## 📊 What Happens When a User Signs In

1. User clicks "Sign in with Google"
2. Firebase opens Google OAuth popup
3. User selects Google account and grants permissions
4. Firebase returns an ID token
5. Frontend sends ID token to backend API
6. Backend verifies token with Firebase Admin SDK
7. Backend creates/updates user in ERPNext
8. Backend creates ERPNext session
9. User is redirected to `/app` dashboard

## 🎉 Success!

Once you complete these steps, your ERPNext installation will have Google Sign-in enabled!

Users can now:
- Sign in with their Google accounts
- Have accounts automatically created
- Access ERPNext without remembering passwords

## 📞 Need Help?

If you encounter any issues:

1. Check the backend logs:
   ```bash
   docker compose -f pwd.yml logs -f backend
   ```

2. Check browser console for frontend errors (F12)

3. Verify Firebase Console settings

4. Ensure all environment variables are set correctly

---

**Project ID**: ashutosh-a2720  
**Access URL**: http://localhost:8080  
**Implementation Status**: ✅ Code Complete - Awaiting Firebase Console Configuration