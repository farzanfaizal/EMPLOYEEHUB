# Render Environment Variables Setup Guide

## Required Environment Variables for Render Deployment

Set these environment variables in your Render Web Service dashboard under **Environment**.

---

## 🔐 Security & Django Core

### `SECRET_KEY`
**Required**: Yes
**Value**: Generate a new secret key
**How to Generate**:
```python
# Run this in Python shell:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
**Example**: `django-insecure-xyz123abc456...`
**Note**: Never use the development key in production!

### `DEBUG`
**Required**: Yes
**Value**: `False`
**Note**: Must be False in production for security

---

## 🗄️ Database Configuration (PostgreSQL)

Render automatically provides a PostgreSQL database. Set these variables:

### `USE_SQLITE`
**Required**: Yes
**Value**: `False`
**Note**: Must be False to use PostgreSQL in production

### `DB_NAME`
**Required**: Yes
**Value**: Get from Render PostgreSQL dashboard
**Example**: `employeehub_db`

### `DB_USER`
**Required**: Yes
**Value**: Get from Render PostgreSQL dashboard
**Example**: `employeehub_user`

### `DB_PASSWORD`
**Required**: Yes
**Value**: Get from Render PostgreSQL dashboard
**Example**: Auto-generated secure password

### `DB_HOST`
**Required**: Yes
**Value**: Get from Render PostgreSQL dashboard
**Example**: `dpg-abc123xyz-a.oregon-postgres.render.com`

### `DB_PORT`
**Required**: No (defaults to 5432)
**Value**: `5432`

---

## 🔑 Google OAuth 2.0 Configuration

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth 2.0 Client ID**
5. Select **Web application**
6. Add **Authorized JavaScript origins**:
   - `https://employee-hub-05x7.onrender.com`
   - `http://localhost:8000` (for local testing)
7. Add **Authorized redirect URIs**:
   - `https://employee-hub-05x7.onrender.com/accounts/google/login/callback/`
   - `http://localhost:8000/accounts/google/login/callback/`
8. Click **Create** and copy your credentials

### `GOOGLE_CLIENT_ID`
**Required**: Yes (for Google Sign-In)
**Value**: From Google Cloud Console
**Example**: `123456789-abc123xyz.apps.googleusercontent.com`

### `GOOGLE_CLIENT_SECRET`
**Required**: Yes (for Google Sign-In)
**Value**: From Google Cloud Console
**Example**: `GOCSPX-abc123xyz456`

---

## 🌐 Render Specific

### `RENDER_EXTERNAL_URL`
**Required**: No (auto-provided by Render)
**Value**: Automatically set by Render
**Example**: `https://employee-hub-05x7.onrender.com`
**Note**: Used for ALLOWED_HOSTS and Site configuration

---

## 📋 Complete Environment Variables Checklist

Copy and paste this into Render Environment section, replacing values with your actual credentials:

```
# Security
SECRET_KEY=your-generated-secret-key-here
DEBUG=False

# Database
USE_SQLITE=False
DB_NAME=your-render-postgres-db-name
DB_USER=your-render-postgres-username
DB_PASSWORD=your-render-postgres-password
DB_HOST=your-render-postgres-host
DB_PORT=5432

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-google-secret
```

---

## 🚀 First-Time Deployment Steps

### 1. Set Up PostgreSQL Database
- In Render Dashboard, create a new **PostgreSQL** database
- Copy all database credentials (name, user, password, host)
- Add them to your Web Service environment variables

### 2. Set Up Environment Variables
- Go to your Web Service > **Environment**
- Add all variables from the checklist above
- Click **Save Changes**

### 3. Initial Deployment
When the service deploys for the first time:
- The build script will run migrations automatically
- A Django Site will be configured automatically
- **No superuser creation needed!** 🎉

### 4. Create First Admin User
Since Render free tier has no shell access, we use automatic setup:

**Option A: Sign Up via Web Interface** (RECOMMENDED)
1. Go to your deployed site: `https://employee-hub-05x7.onrender.com/accounts/signup/`
2. Create an account (first user)
3. **You'll automatically become Super Admin!** ✅
4. All subsequent signups will become HR Managers

**Option B: Use Google Sign-In**
1. Go to: `https://employee-hub-05x7.onrender.com/accounts/google/login/`
2. Sign in with Google (first user)
3. **You'll automatically become Super Admin!** ✅

---

## 🔧 How First User Becomes Admin

Our application uses Django signals to automatically:
1. Detect when the first user is created
2. Auto-promote them to **Super Admin** with full permissions
3. Set `is_staff=True` and `is_superuser=True`
4. All subsequent users default to **HR Manager** role

**Code Location**: `emp_app/signals.py:14-31`

---

## 🎯 User Roles Explained

### Super Admin (First User Only)
- Full system access
- Can manage all users, employees, departments
- Access to Django admin panel
- Auto-assigned to first signup

### HR Manager (Default for New Users)
- Can manage employees
- Can create/edit/delete employee records
- Cannot access admin panel
- Perfect for HR staff

### Department Manager
- Can view and manage employees in their department
- Limited access
- Must be manually promoted by Super Admin

### Employee
- Read-only access
- Can view their own profile
- Not used in this HR tool (employees don't need app access)

---

## 🧪 Testing Your Deployment

### 1. Check Homepage
Visit: `https://employee-hub-05x7.onrender.com/`
Should see: Professional landing page

### 2. Test Google Sign-In
Visit: `https://employee-hub-05x7.onrender.com/accounts/google/login/`
Should: Redirect to Google OAuth page

### 3. Test Regular Signup
Visit: `https://employee-hub-05x7.onrender.com/accounts/signup/`
Should: Show signup form

### 4. Verify First User Admin
After first signup:
1. Go to: `https://employee-hub-05x7.onrender.com/admin/`
2. Login with your credentials
3. Should have full admin access

---

## 🐛 Common Issues & Solutions

### Issue 1: Google Sign-In Shows Error
**Solution**: Verify redirect URIs in Google Cloud Console match exactly:
```
https://employee-hub-05x7.onrender.com/accounts/google/login/callback/
```

### Issue 2: Database Connection Error
**Solution**:
- Verify all DB_* environment variables are set correctly
- Check PostgreSQL database is running in Render
- Ensure `USE_SQLITE=False`

### Issue 3: Static Files Not Loading
**Solution**:
- Check `build.sh` ran successfully
- Verify `collectstatic` completed
- WhiteNoise should serve files automatically

### Issue 4: First User Not Admin
**Solution**:
- Check logs for signal execution
- Verify `emp_app/signals.py` is being imported
- Check `emp_app/apps.py` has `ready()` method

---

## 📝 Local Development

For local testing, create `.env` file:

```
# Local Development Settings
DEBUG=True
USE_SQLITE=True
SECRET_KEY=django-insecure-dev-key-only

# Google OAuth (use same credentials)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
```

---

## 🔒 Security Checklist

- ✅ DEBUG=False in production
- ✅ SECRET_KEY is unique and secure
- ✅ Database uses SSL (configured automatically)
- ✅ ALLOWED_HOSTS restricted to your domain
- ✅ HTTPS enforced in production
- ✅ Session cookies secure
- ✅ CSRF protection enabled
- ✅ Google OAuth redirect URIs restricted

---

## 📞 Support

If you encounter issues:
1. Check Render logs: Dashboard > Logs
2. Verify all environment variables are set
3. Ensure PostgreSQL database is connected
4. Check Google OAuth credentials are valid

**Build Script Location**: `build.sh`
**Settings Location**: `office_emp_mgmt_proj/settings.py`
**Signals Location**: `emp_app/signals.py`
