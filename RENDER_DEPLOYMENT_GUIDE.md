# Professional Render Deployment Guide - EmployeeHub

## 🚀 Quick Deploy to Render (Free Tier)

This guide will help you deploy your professional EmployeeHub application to Render with Google OAuth.

---

## 📋 PRE-DEPLOYMENT CHECKLIST

- ✅ Code committed to GitHub
- ✅ Google OAuth credentials ready
- ✅ Render account created (free)
- ✅ All environment variables documented

---

## STEP 1: Prepare Google OAuth Credentials

### 1.1 Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 1.2 Create/Select Project
- Click "Select a project" → "New Project"
- Name: "EmployeeHub"
- Click "Create"

### 1.3 Enable Google+ API
- Go to "APIs & Services" → "Library"
- Search for "Google+ API"
- Click "Enable"

### 1.4 Create OAuth Credentials
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "OAuth client ID"
- Application type: "Web application"
- Name: "EmployeeHub Production"

### 1.5 Add Authorized Redirect URIs
```
https://your-app-name.onrender.com/accounts/google/login/callback/
http://localhost:8000/accounts/google/login/callback/
```

**Replace `your-app-name` with your actual Render app name!**

### 1.6 Save Credentials
- Copy **Client ID**
- Copy **Client Secret**
- Keep these safe - you'll need them for Render

---

## STEP 2: Push to GitHub

### 2.1 Initialize Git (if not done)
```bash
cd C:\Users\ASUS\Desktop\P-Projects\EMPLOYEEHUB
git init
git add .
git commit -m "Professional implementation with Google OAuth and role-based access"
```

### 2.2 Add Remote and Push
```bash
git remote add origin https://github.com/farzanfaizal/EMPLOYEEHUB.git
git branch -M master
git push -f origin master
```

**Note:** `-f` force pushes to overwrite existing code

---

## STEP 3: Deploy on Render

### 3.1 Create Render Account
- Go to https://render.com
- Sign up with GitHub
- Authorize Render to access your repositories

### 3.2 Create New Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repo: `farzanfaizal/EMPLOYEEHUB`
- Click "Connect"

### 3.3 Configure Web Service

**Basic Settings:**
```
Name: employeehub (or your preferred name)
Region: Singapore (or closest to you)
Branch: master
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command: chmod +x build.sh && ./build.sh
Start Command: gunicorn office_emp_mgmt_proj.wsgi:application
```

**Instance Type:**
```
Free ($0/month)
```

### 3.4 Add Environment Variables

Click "Advanced" → "Add Environment Variable"

**Required Variables:**

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `SECRET_KEY` | `<generate-new>` | Use Django secret key generator |
| `DEBUG` | `False` | Production mode |
| `USE_SQLITE` | `False` | Use PostgreSQL |
| `GOOGLE_CLIENT_ID` | `<your-client-id>` | From Google Console |
| `GOOGLE_CLIENT_SECRET` | `<your-client-secret>` | From Google Console |

**Database Variables (Auto-filled if using Render PostgreSQL):**
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.5 Create PostgreSQL Database

- Click "New +" → "PostgreSQL"
- Name: `employeehub-db`
- Database: `employeehub`
- User: (auto-generated)
- Region: Same as web service
- Plan: Free

**Link to Web Service:**
- Render will automatically set `DB_*` environment variables

---

## STEP 4: Deploy!

### 4.1 Start Deployment
- Click "Create Web Service"
- Render will:
  1. Clone your repo
  2. Install dependencies
  3. Run build.sh
  4. Collect static files
  5. Run migrations
  6. Start application

### 4.2 Monitor Deployment
- Watch logs in real-time
- Look for "Build completed successfully!"
- Wait for "Your service is live"

### 4.3 Get Your URL
```
https://employeehub.onrender.com
```

---

## STEP 5: Post-Deployment Setup

### 5.1 Update Google OAuth Redirect URI
- Go back to Google Cloud Console
- Add your Render URL:
  ```
  https://employeehub.onrender.com/accounts/google/login/callback/
  ```

### 5.2 Create Superuser
In Render Dashboard → Shell:
```bash
python manage.py createsuperuser
```

### 5.3 Configure Django Sites
In Render Shell:
```bash
python manage.py shell
```

Then run:
```python
from django.contrib.sites.models import Site
site = Site.objects.get(id=1)
site.domain = 'employeehub.onrender.com'
site.name = 'EmployeeHub'
site.save()
exit()
```

### 5.4 Set Up Social App in Admin
1. Visit: `https://employeehub.onrender.com/admin/`
2. Login with superuser
3. Go to "Social applications"
4. Click "Add social application"
5. Fill in:
   - Provider: Google
   - Name: Google OAuth
   - Client ID: (your Google client ID)
   - Secret key: (your Google client secret)
   - Sites: Select your site (employeehub.onrender.com)
6. Save

---

## STEP 6: Test Everything!

### 6.1 Test Regular Login
```
https://employeehub.onrender.com/accounts/login/
```

### 6.2 Test Google OAuth
```
https://employeehub.onrender.com/accounts/google/login/
```

### 6.3 Test Features
- ✅ Dashboard loads
- ✅ Can create employee
- ✅ Role permissions work
- ✅ Profile page works
- ✅ Activity logging works

---

## 🎯 RENDER FREE TIER LIMITS

| Resource | Free Tier | Notes |
|----------|-----------|-------|
| **Web Services** | 750 hours/month | Enough for 1 app 24/7 |
| **RAM** | 512 MB | Adequate for Django |
| **CPU** | Shared | May spin down after 15 min inactivity |
| **Bandwidth** | 100 GB/month | More than enough |
| **Build Time** | 500 minutes/month | ~16 builds |
| **PostgreSQL** | 90 days free trial | Then $7/month or use external DB |

**Important Notes:**
- Free apps spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Use external DB (Neon, ElephantSQL) for permanent free PostgreSQL

---

## 🔧 TROUBLESHOOTING

### Issue: Build Failed
**Check:**
- `build.sh` has execution permissions
- All requirements in requirements.txt
- Python version correct (3.11.0)

**Solution:**
```bash
chmod +x build.sh
```

### Issue: Google OAuth Not Working
**Check:**
- Client ID and Secret in environment variables
- Redirect URI matches exactly (https://your-app.onrender.com/accounts/google/login/callback/)
- Social application configured in admin
- Site domain is correct

### Issue: Static Files Not Loading
**Check:**
- STATIC_ROOT and STATIC_URL in settings
- WhiteNoise middleware installed
- collectstatic ran successfully

**Solution:**
```bash
python manage.py collectstatic --no-input
```

### Issue: Database Errors
**Check:**
- USE_SQLITE=False in production
- Database environment variables set
- Migrations ran successfully

**Solution:**
```bash
python manage.py migrate --no-input
```

### Issue: 502 Bad Gateway
**Cause:** App crashed or failed to start

**Check Logs:**
- Render Dashboard → Logs
- Look for Python errors
- Check SECRET_KEY is set

---

## 📊 MONITORING & MAINTENANCE

### View Logs
```
Render Dashboard → Your Service → Logs
```

### Redeploy
```
Render Dashboard → Manual Deploy → Deploy latest commit
```

### Update Environment Variables
```
Render Dashboard → Environment → Add/Edit variables → Save
```

### Database Backups
- Render PostgreSQL: Automatic daily backups (free trial)
- After trial: Download and backup manually

---

## 🚀 OPTIONAL: Use External Free PostgreSQL

### Option 1: Neon (Recommended)
- Visit: https://neon.tech
- Free tier: 3 GB storage, unlimited queries
- Get connection string
- Add to Render environment variables

### Option 2: ElephantSQL
- Visit: https://www.elephantsql.com
- Free tier: 20 MB storage
- Good for testing

### Configuration:
```
USE_SQLITE=False
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=your_host.neon.tech
DB_PORT=5432
```

---

## ✅ POST-DEPLOYMENT CHECKLIST

- ✅ App is live and accessible
- ✅ Google OAuth working
- ✅ Admin panel accessible
- ✅ Superuser created
- ✅ Social application configured
- ✅ Site domain updated
- ✅ All environment variables set
- ✅ Logs show no errors
- ✅ Database connected
- ✅ Static files loading
- ✅ Role permissions working
- ✅ Activity logging functional

---

## 📱 CUSTOM DOMAIN (Optional)

### Add Custom Domain on Render
1. Render Dashboard → Settings → Custom Domain
2. Add your domain
3. Update DNS records at your registrar

**DNS Configuration:**
```
Type: CNAME
Name: www (or @)
Value: your-app.onrender.com
```

---

## 🎉 SUCCESS!

Your professional EmployeeHub is now live with:
- ✅ Google OAuth authentication
- ✅ Role-based access control
- ✅ Professional UI
- ✅ Secure configuration
- ✅ Activity logging
- ✅ Production database

**Live URL:** `https://employeehub.onrender.com`

---

## 📞 SUPPORT

### Issues?
1. Check logs in Render Dashboard
2. Review environment variables
3. Verify Google OAuth setup
4. Check database connection

### Need Help?
- Render Docs: https://render.com/docs
- Django Allauth: https://django-allauth.readthedocs.io
- Your documentation: COMPLETE_IMPLEMENTATION_GUIDE.md

---

**Deployed with ❤️ by Professional Developers**
**Version:** 2.0.0 Enterprise Edition
