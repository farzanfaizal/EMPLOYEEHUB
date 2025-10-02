# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**EmployeeHub** is a Django-based employee management system deployed on Render. The application manages employees, departments, and roles with CRUD operations and filtering capabilities.

## Architecture

### Project Structure
- **Main Project**: `office_emp_mgmt_proj/` - Django project configuration
- **App**: `emp_app/` - Core employee management application
  - Models: Employee, Department, Role (and unused ccmployee model)
  - Views: Function-based views for all operations
  - Templates: Located in `emp_app/templates/`
  - Static files: Located in `emp_app/static/emp_app/`

### Data Models (emp_app/models.py)
- **Employee**: Primary model with fields for personal info, salary, bonus, phone, hire_date
  - Foreign keys to Department and Role
  - Auto-incrementing `emp_id` as primary key
- **Department**: Has name and location
- **Role**: Has name only
- **ccmployee**: Incomplete/unused model (only has emp_id, first_name, last_name)

### URL Routing
Project uses two-level URL configuration:
1. `office_emp_mgmt_proj/urls.py` - Root URLs, includes emp_app URLs at root path
2. `emp_app/urls.py` - All employee-related endpoints

### Key Views (emp_app/views.py)
- `index`: Homepage
- `allEmp`: Display all employees
- `addEmp`: Add new employee (GET shows form, POST processes)
- `removeEmp`: Remove employee by ID (supports both URL param and POST request, returns JSON for AJAX)
- `filterEmp`: Filter employees by name, department, or role using Q objects
- `listEmployees`: List view for employees
- `updateEmp`: Update employee details by emp_id

### Static Files
Static files collected from `emp_app/static/` to `staticfiles/` for Render deployment. Images include branding (ehub.png) and favicons.

## Development Commands

### Setup and Installation
```bash
pip install -r requirements.txt
```

### Database Operations
```bash
# Run migrations
python manage.py migrate

# Create migrations after model changes
python manage.py makemigrations

# Create superuser for admin access
python manage.py createsuperuser
```

### Running the Application
```bash
# Development server
python manage.py runserver

# Production (Render uses this via Procfile)
gunicorn office_emp_mgmt_proj.wsgi --log-file -
```

### Static Files
```bash
# Collect static files for deployment
python manage.py collectstatic
```

### Admin Panel
Access Django admin at `/admin/` with superuser credentials. Employee, Department, and Role models are registered.

## Deployment

Configured for Render deployment:
- Procfile uses Gunicorn with `office_emp_mgmt_proj.wsgi`
- ALLOWED_HOSTS includes `employee-hub-05x7.onrender.com`
- Static files served from `staticfiles/` directory
- Uses SQLite database (db.sqlite3)

## Important Notes

- The `ccmployee` model exists but is unused and incomplete
- DEBUG is set to True (should be False in production)
- SECRET_KEY is exposed in settings.py (should use environment variable)
- removeEmp view has dual functionality: form-based removal and AJAX endpoint returning employee JSON
- Messages framework used for user feedback throughout views
