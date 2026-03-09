# Google Firebase Authentication Integration

## Overview
Add Google-based authentication to the ERPNext login page using Firebase Authentication, allowing users to sign in with their Google accounts while maintaining the existing design elements.

## User Stories

### 1. As a user, I want to sign in with my Google account
**Acceptance Criteria:**
- 1.1 A "Sign in with Google" button is visible on the login page
- 1.2 Clicking the button opens Google OAuth consent screen
- 1.3 After successful Google authentication, user is logged into ERPNext
- 1.4 User profile is created/updated with Google account information
- 1.5 Existing design elements and layout are preserved

### 2. As a user, I want seamless authentication experience
**Acceptance Criteria:**
- 2.1 Google sign-in works alongside traditional username/password login
- 2.2 No page refresh required during authentication flow
- 2.3 Error messages are displayed clearly if authentication fails
- 2.4 User is redirected to the appropriate page after successful login

### 3. As an administrator, I want to configure Google OAuth settings
**Acceptance Criteria:**
- 3.1 Firebase configuration can be set via environment variables
- 3.2 OAuth credentials are stored securely
- 3.3 Configuration includes Firebase API key, Auth domain, and Project ID
- 3.4 Settings can be updated without code changes

## Technical Requirements

### Firebase Setup
- Firebase project: ashutosh-a2720
- Enable Google Authentication provider
- Configure OAuth consent screen
- Set authorized domains (localhost:8080 for development)

### Frontend Integration
- Add Firebase SDK to login page
- Implement Google sign-in button with ERPNext design system
- Handle authentication state changes
- Display loading states during authentication

### Backend Integration
- Create API endpoint to handle Firebase token verification
- Create/update user accounts based on Google profile
- Map Google user data to ERPNext user fields
- Handle session management

### Security
- Verify Firebase ID tokens on the server side
- Implement CSRF protection
- Secure storage of Firebase configuration
- Rate limiting for authentication attempts

## Non-Functional Requirements

### Performance
- Authentication should complete within 3 seconds
- No impact on existing login page load time
- Minimal JavaScript bundle size increase

### Compatibility
- Works on all modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive design
- Works with existing ERPNext authentication system

### Maintainability
- Code follows ERPNext/Frappe coding standards
- Comprehensive error handling and logging
- Documentation for configuration and troubleshooting

## Out of Scope
- Other OAuth providers (Facebook, GitHub, etc.)
- Two-factor authentication integration
- User account linking/unlinking UI
- Admin dashboard for OAuth management

## Dependencies
- Firebase Admin SDK (Python)
- Firebase JavaScript SDK
- Google Cloud Project with billing enabled
- OAuth 2.0 credentials configured in Google Cloud Console

## Constraints
- Must work within Docker container environment
- Must not break existing authentication methods
- Must comply with Google OAuth policies
- Firebase free tier limitations apply