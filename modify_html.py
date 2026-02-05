import os

file_path = '/home/frappe/frappe-bench/apps/frappe/frappe/www/login.html'

with open(file_path, 'r') as f:
    content = f.read()

firebase_script = """
<script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
  import { getAuth, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
  import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

  const firebaseConfig = {
    apiKey: "REPLACE_WITH_YOUR_API_KEY",
    authDomain: "ashutosh-a2720.firebaseapp.com",
    projectId: "ashutosh-a2720",
    storageBucket: "ashutosh-a2720.appspot.com",
    messagingSenderId: "REPLACE_WITH_YOUR_SENDER_ID",
    appId: "REPLACE_WITH_YOUR_APP_ID"
  };

  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  const db = getFirestore(app);
  const provider = new GoogleAuthProvider();

  function loginWithGoogle() {
      signInWithPopup(auth, provider)
        .then(async (result) => {
            const user = result.user;
            const idToken = await user.getIdToken();
            
            // Store in Firestore
            try {
                await setDoc(doc(db, "users", user.uid), {
                    email: user.email,
                    displayName: user.displayName,
                    photoURL: user.photoURL,
                    lastLogin: new Date()
                }, { merge: true });
            } catch (e) {
                console.error("Error writing to Firestore", e);
            }

            // Login to ERPNext
            fetch('/api/method/frappe.www.login.login_via_firebase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Frappe-CSRF-Token': frappe.csrf_token
                },
                body: JSON.stringify({ id_token: idToken })
            })
            .then(res => res.json())
            .then(data => {
                if (data.message && data.message.status === 'success') {
                    window.location.href = '/app';
                } else {
                    frappe.msgprint('Login Failed: ' + (data.message ? data.message.message : 'Unknown error'));
                }
            })
            .catch(err => {
                console.error(err);
                frappe.msgprint('Login Error');
            });

        }).catch((error) => {
            console.error(error);
            frappe.msgprint(error.message);
        });
  }

  window.loginWithGoogle = loginWithGoogle;
  
  // Attach to button if it exists (using a slightly delayed check or event delegation)
  document.addEventListener('click', function(e) {
      if(e.target && (e.target.id === 'firebase-google-login' || e.target.closest('#firebase-google-login'))){
          e.preventDefault();
          loginWithGoogle();
      }
  });
</script>
"""

login_button_html = """
<div style="margin-bottom: 10px;">
    <button id="firebase-google-login" class="btn btn-default btn-block btn-sm" style="display: flex; align-items: center; justify-content: center; gap: 8px; background-color: #fff; color: #444; border: 1px solid #ddd;">
       <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="18" height="18">
       Login with Google
    </button>
</div>
"""

# Insert Script before </body> or inside block script
if "</body>" in content:
    content = content.replace("</body>", firebase_script + "</body>")
elif "{% block script %}" in content:
    # Fallback if no body tag (it is a template)
    content = content.replace("{% block script %}", "{% block script %}" + firebase_script)

# Insert Button inside the form or before it
# Looking for password field to insert before it or at the top of the form
if 'name="pwd"' in content:
     # Try to insert before the password field or email field
    pass

# Let's insert it before the email field for visibility
if '<input type="email"' in content:
    content = content.replace('<div class="page-card-body">', '<div class="page-card-body">' + login_button_html)
else:
    # Fallback
    content = content.replace('<form', login_button_html + '<form')

with open(file_path, 'w') as f:
    f.write(content)