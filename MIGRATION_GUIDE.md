# Database Migration Guide for Render

## ⚠️ IMPORTANT: Run Migrations to Activate New Features

The app is now **backwards compatible** and will work without errors, but the new features (Performance Reviews, Tasks, Announcements, Activity Logs) won't be available until you run migrations.

---

## Option 1: Run Migrations via Render Shell (Recommended)

### Step-by-Step Instructions:

1. **Go to Render Dashboard**
   - Navigate to https://dashboard.render.com
   - Select your `employee-hub-05x7` service

2. **Open Shell**
   - Click on the "Shell" tab in the top menu
   - Wait for the shell to connect

3. **Run Migration Commands**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Verify Success**
   - You should see output showing tables being created:
     - `emp_app_performancereview`
     - `emp_app_activitylog`
     - `emp_app_announcement`
     - `emp_app_task`
     - Employee table modifications

5. **Restart the Service**
   - Go back to your service dashboard
   - Click "Manual Deploy" → "Clear build cache & deploy" (optional but recommended)
   - Or just wait for auto-deploy to complete

---

## Option 2: Add to build.sh (For Future Deploys)

If you have a `build.sh` file, add migrations to it:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py makemigrations --no-input
python manage.py migrate --no-input
```

Then in Render:
- Go to Settings
- Under "Build Command" add: `./build.sh`

---

## Option 3: Manual Database Migration (Advanced)

If you have direct database access:

1. **Connect to your PostgreSQL database**
   ```bash
   psql $DATABASE_URL
   ```

2. **Run migrations locally first** (to generate migration files)
   ```bash
   python manage.py makemigrations
   ```

3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

---

## What Gets Created:

### New Tables:
1. **emp_app_performancereview**
   - Tracks employee performance reviews
   - Multi-criteria rating system

2. **emp_app_activitylog**
   - Complete audit trail
   - Tracks all system changes

3. **emp_app_announcement**
   - Company-wide announcements
   - Priority and expiry management

4. **emp_app_task**
   - Task assignment system
   - Status and priority tracking

5. **emp_app_announcement_target_departments** (Junction table)
   - Links announcements to specific departments

### Modified Tables:
- **emp_app_employee** - Adds new fields:
  - `email` (EmailField)
  - `date_of_birth` (DateField)
  - `address` (TextField)
  - `emergency_contact` (CharField)
  - `is_active` (BooleanField)
  - `created_at` (DateTimeField)
  - `updated_at` (DateTimeField)
  - `phone_num` type changed (BigInt → CharField)

### Removed Tables:
- **emp_app_ccmployee** - Unused model removed

---

## Expected Output:

When you run `python manage.py migrate`, you should see:

```
Running migrations:
  Applying emp_app.XXXX_alter_employee_phone_num... OK
  Applying emp_app.XXXX_remove_ccmployee... OK
  Applying emp_app.XXXX_add_employee_fields... OK
  Applying emp_app.XXXX_performancereview... OK
  Applying emp_app.XXXX_activitylog... OK
  Applying emp_app.XXXX_announcement... OK
  Applying emp_app.XXXX_task... OK
```

---

## After Migration:

Once migrations complete successfully:

1. **New Navigation Items Will Work:**
   - Manage → Departments
   - Manage → Roles
   - Manage → Batch Import
   - Performance → Reviews
   - Performance → Tasks
   - News → Announcements

2. **Homepage Will Show:**
   - Active announcements
   - Pending tasks count
   - Overdue tasks count

3. **Admin Panel Will Have:**
   - Performance Review management
   - Activity Log viewer
   - Announcement creator
   - Task manager

---

## Troubleshooting:

### Issue: "ProgrammingError: relation does not exist"
**Solution:** Migrations haven't been applied yet. Follow Option 1 above.

### Issue: "CommandError: Conflicting migrations detected"
**Solution:**
```bash
python manage.py migrate --fake-initial
```

### Issue: "OperationalError: database is locked"
**Solution:**
- On Render, this shouldn't happen as only one dyno runs at a time
- If it does, restart your service and try again

### Issue: Existing employee phone numbers are BigInt
**Solution:** Migration will automatically convert them to CharField

---

## Rollback (If Needed):

If something goes wrong, you can rollback:

```bash
# List migrations
python manage.py showmigrations

# Rollback to specific migration
python manage.py migrate emp_app XXXX_previous_migration

# Or rollback all new migrations
python manage.py migrate emp_app zero
```

---

## Production Checklist:

Before running migrations on production:

- [ ] Backup database (Render does this automatically)
- [ ] Test migrations in development first (if possible)
- [ ] Check that app is running without 500 errors (backwards compatibility)
- [ ] Run migrations during low-traffic period
- [ ] Verify new features work after migration
- [ ] Check admin panel for new models
- [ ] Test creating a sample announcement
- [ ] Test creating a sample task

---

## Need Help?

If migrations fail or you encounter issues:

1. Check Render logs for specific error messages
2. Verify DATABASE_URL is correctly set
3. Ensure PostgreSQL connection is stable
4. Check that you have write permissions on the database

---

## Current Status:

✅ **App is Running:** Backwards compatible, no 500 errors
⏳ **Migrations Pending:** New features inactive until migrations run
🎯 **Next Step:** Run migrations via Render Shell (Option 1)

---

**Last Updated:** 2025-11-19
**Status:** Ready for Migration
