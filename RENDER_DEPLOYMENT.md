# Render Deployment Guide - EmployeeHub

## 🚀 Complete Deployment Instructions

---

## Part 1: Environment Variables for Render

### Go to Render Dashboard → Your Service → Environment

Add these **EXACT** environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.9` |
| `DEBUG` | `False` |
| `SECRET_KEY` | `django-insecure-mnhn4zrmjxxzfiicy_4m%=bxn78o*va2h+3+in4d^1)$yjz$io` |
| `DB_NAME` | `neondb` |
| `DB_USER` | `neondb_owner` |
| `DB_PASSWORD` | `npg_M7RXbu5jdZAG` |
| `DB_HOST` | `ep-old-silence-a1skq2st-pooler.ap-southeast-1.aws.neon.tech` |
| `DB_PORT` | `5432` |

### Copy-Paste Format for Render:
```
PYTHON_VERSION=3.11.9
DEBUG=False
SECRET_KEY=django-insecure-mnhn4zrmjxxzfiicy_4m%=bxn78o*va2h+3+in4d^1)$yjz$io
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=npg_M7RXbu5jdZAG
DB_HOST=ep-old-silence-a1skq2st-pooler.ap-southeast-1.aws.neon.tech
DB_PORT=5432
```

---

## Part 2: Migrate Data from SQLite to PostgreSQL

### Step 1: Export Data from SQLite (Local)

```bash
# Make sure you're using SQLite
export USE_SQLITE=True

# Run the migration script
python migrate_to_postgres.py
```

This will create `data_backup.json` with all your data.

### Step 2: Import Data to PostgreSQL (Local Test)

```bash
# Switch to PostgreSQL
unset USE_SQLITE
# Or set DB_PASSWORD if not in environment
export DB_PASSWORD=npg_M7RXbu5jdZAG

# Run migrations on PostgreSQL
python manage.py migrate

# Import the data (the script will do this)
python migrate_to_postgres.py
```

### Step 3: Verify Data

```bash
# Check data in PostgreSQL
python manage.py shell

# In the shell:
from emp_app.models import Employee, Department, Role
print(f"Employees: {Employee.objects.count()}")
print(f"Departments: {Department.objects.count()}")
print(f"Roles: {Role.objects.count()}")
```

---

## Part 3: Deploy to Render

### Option A: Automatic Deployment (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Fix requirements.txt and add PostgreSQL support"
   git push origin master
   ```

2. **Render will automatically**:
   - Detect the push
   - Start building
   - Install dependencies
   - Run migrations
   - Collect static files
   - Deploy

3. **After deployment**, run migrations on Render:
   - Go to Render Dashboard → Your Service → Shell
   - Run: `python manage.py migrate`

4. **Create Superuser on Render**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Import Data to Production**:
   - Upload `data_backup.json` to your repository
   - In Render Shell:
   ```bash
   python manage.py loaddata data_backup.json
   ```

### Option B: Manual Migration

1. **Connect to Neon PostgreSQL directly**:
   ```bash
   psql 'postgresql://neondb_owner:npg_M7RXbu5jdZAG@ep-old-silence-a1skq2st-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
   ```

2. **Export from SQLite and Import to Neon** (using the migration script)

---

## Part 4: Post-Deployment Steps

### 1. Create Superuser (if not done)
```bash
# In Render Shell
python manage.py createsuperuser
```

### 2. Verify Deployment
Visit these URLs:
- `https://your-app.onrender.com/` - Homepage
- `https://your-app.onrender.com/admin/` - Admin panel
- `https://your-app.onrender.com/all-emp` - Employee list

### 3. Setup Document Categories
Via Admin panel or Django shell:
```python
from emp_app.models import DocumentCategory

categories = [
    ('Employment Contracts', 'fa-file-contract'),
    ('Tax Documents', 'fa-file-invoice-dollar'),
    ('Certifications', 'fa-certificate'),
    ('Performance Reviews', 'fa-chart-line'),
    ('Training Materials', 'fa-graduation-cap'),
    ('Personal Documents', 'fa-id-card'),
]

for name, icon in categories:
    DocumentCategory.objects.get_or_create(
        name=name,
        defaults={'icon': icon}
    )
```

### 4. Test All Features
- ✅ Homepage statistics
- ✅ Employee CRUD operations
- ✅ Attendance tracking
- ✅ Leave management
- ✅ Fingerprint management (UI)
- ✅ Document uploads
- ✅ Analytics dashboard
- ✅ HR tools

---

## Part 5: Troubleshooting

### Error: "requirements.txt encoding issue"
✅ **FIXED** - Recreated requirements.txt with proper UTF-8 encoding

### Error: "No module named psycopg2"
- Make sure `psycopg2-binary==2.9.9` is in requirements.txt
- Render will install it automatically

### Error: "Database connection failed"
- Check environment variables are set correctly
- Verify DB_PASSWORD is correct
- Check Neon.tech database is active

### Error: "Static files not found"
- Run: `python manage.py collectstatic --noinput`
- Should be in build command automatically

### Error: "Migration failed"
- Run migrations manually in Render Shell:
  ```bash
  python manage.py migrate
  ```

### Database is Empty After Deployment
- Upload `data_backup.json` to repository
- Run in Render Shell:
  ```bash
  python manage.py loaddata data_backup.json
  ```

---

## Part 6: Build Command for Render

Your build command should be:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Note**: Migrations should be run manually or via a release command, not in build.

---

## Part 7: Database Migration Commands Summary

### Local: Export from SQLite
```bash
export USE_SQLITE=True
python migrate_to_postgres.py
# Creates: data_backup.json
```

### Local: Test with PostgreSQL
```bash
unset USE_SQLITE
export DB_PASSWORD=npg_M7RXbu5jdZAG
python manage.py migrate
python manage.py loaddata data_backup.json
```

### Production: Import to Render
```bash
# In Render Shell
python manage.py migrate
python manage.py loaddata data_backup.json
python manage.py createsuperuser
```

---

## Part 8: Environment Variables - Detailed Explanation

### Required Variables

**PYTHON_VERSION**
- Value: `3.11.9`
- Why: Ensures compatibility with your dependencies

**DEBUG**
- Value: `False`
- Why: Security - disables debug mode in production

**SECRET_KEY**
- Value: `django-insecure-mnhn4zrmjxxzfiicy_4m%=bxn78o*va2h+3+in4d^1)$yjz$io`
- Why: Django security - used for cryptographic signing
- ⚠️ Generate a new one for production using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

**DB_NAME**
- Value: `neondb`
- Why: Your PostgreSQL database name on Neon.tech

**DB_USER**
- Value: `neondb_owner`
- Why: PostgreSQL username

**DB_PASSWORD**
- Value: `npg_M7RXbu5jdZAG`
- Why: PostgreSQL password
- ⚠️ Keep this secret!

**DB_HOST**
- Value: `ep-old-silence-a1skq2st-pooler.ap-southeast-1.aws.neon.tech`
- Why: Your Neon.tech database host URL

**DB_PORT**
- Value: `5432`
- Why: Standard PostgreSQL port

---

## Part 9: Checklist

### Before Deployment
- [x] Fix requirements.txt encoding
- [x] Update settings.py for environment variables
- [x] Create migration script
- [ ] Export data from SQLite
- [ ] Test locally with PostgreSQL
- [ ] Commit and push to GitHub

### During Deployment
- [ ] Add environment variables to Render
- [ ] Trigger deployment
- [ ] Monitor build logs
- [ ] Check for errors

### After Deployment
- [ ] Run migrations in Render Shell
- [ ] Create superuser
- [ ] Import data backup
- [ ] Test all features
- [ ] Setup document categories
- [ ] Verify database connection

---

## Part 10: Quick Commands Reference

### Git Commands
```bash
git add .
git commit -m "Deploy to Render with PostgreSQL"
git push origin master
```

### Django Commands (Render Shell)
```bash
# Migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load data
python manage.py loaddata data_backup.json

# Django shell
python manage.py shell

# Check database
python manage.py dbshell
```

### Database Commands
```bash
# Connect to Neon PostgreSQL
psql 'postgresql://neondb_owner:npg_M7RXbu5jdZAG@ep-old-silence-a1skq2st-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'

# List tables
\dt

# Count records
SELECT COUNT(*) FROM emp_app_employee;

# Exit
\q
```

---

## Support

If you encounter issues:
1. Check Render logs: Dashboard → Service → Logs
2. Check environment variables: Dashboard → Service → Environment
3. Verify Neon.tech database is active
4. Test database connection locally first

---

## Success Criteria

✅ Build succeeds without errors
✅ Application is accessible at your Render URL
✅ Admin panel works
✅ Database shows all migrated data
✅ All features functional

---

**Last Updated**: October 28, 2025
**Deployment Status**: Ready for Production
