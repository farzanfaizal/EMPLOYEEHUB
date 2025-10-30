#!/usr/bin/env python
"""
Migration script to move data from SQLite to PostgreSQL (Neon.tech)

Usage:
    python migrate_to_postgres.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'office_emp_mgmt_proj.settings')
django.setup()

from django.core import serializers
from django.db import connections
from django.apps import apps

def export_data_from_sqlite():
    """Export all data from SQLite database"""
    print("📦 Exporting data from SQLite...")

    # Use SQLite database
    os.environ['USE_SQLITE'] = 'True'

    # Get all models
    models_to_export = []

    # Core models
    from emp_app.models import (
        Role, Department, Employee, Attendance, Leave,
        FingerprintData, BiometricAttendance, DocumentCategory, EmployeeDocument
    )

    models_to_export = [
        Role, Department, Employee, Attendance, Leave,
        DocumentCategory, FingerprintData, BiometricAttendance, EmployeeDocument
    ]

    # Export data from each model
    all_data = []
    for model in models_to_export:
        objects = model.objects.all()
        count = objects.count()
        if count > 0:
            print(f"  ✓ {model.__name__}: {count} records")
            all_data.extend(objects)
        else:
            print(f"  - {model.__name__}: 0 records (skipped)")

    # Serialize data
    print("\n🔄 Serializing data...")
    serialized_data = serializers.serialize('json', all_data, indent=2)

    # Save to file
    with open('data_backup.json', 'w', encoding='utf-8') as f:
        f.write(serialized_data)

    print(f"✅ Data exported to data_backup.json\n")
    return len(all_data)

def import_data_to_postgres():
    """Import data to PostgreSQL database"""
    print("📥 Importing data to PostgreSQL...")

    # Use PostgreSQL
    if 'USE_SQLITE' in os.environ:
        del os.environ['USE_SQLITE']

    # Reload Django with PostgreSQL settings
    from django.core.management import call_command

    try:
        # Load the fixture
        call_command('loaddata', 'data_backup.json')
        print("✅ Data imported successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Error importing data: {e}\n")
        return False

def verify_migration():
    """Verify the migration was successful"""
    print("🔍 Verifying migration...")

    from emp_app.models import (
        Role, Department, Employee, Attendance, Leave,
        FingerprintData, BiometricAttendance, DocumentCategory, EmployeeDocument
    )

    models = [
        ('Roles', Role),
        ('Departments', Department),
        ('Employees', Employee),
        ('Attendance Records', Attendance),
        ('Leave Records', Leave),
        ('Document Categories', DocumentCategory),
        ('Fingerprint Data', FingerprintData),
        ('Biometric Logs', BiometricAttendance),
        ('Employee Documents', EmployeeDocument)
    ]

    print("\nPostgreSQL Database Contents:")
    print("-" * 50)
    for name, model in models:
        count = model.objects.count()
        print(f"  {name}: {count} records")
    print("-" * 50)
    print()

def main():
    """Main migration process"""
    print("=" * 60)
    print("  SQLite → PostgreSQL Migration Tool")
    print("=" * 60)
    print()

    # Check if data backup exists
    if os.path.exists('data_backup.json'):
        response = input("⚠️  data_backup.json exists. Use existing backup? (y/n): ")
        if response.lower() != 'y':
            # Export new data
            count = export_data_from_sqlite()
            if count == 0:
                print("⚠️  No data to migrate!")
                return
    else:
        # Export data
        count = export_data_from_sqlite()
        if count == 0:
            print("⚠️  No data to migrate!")
            return

    # Confirm before importing
    print("⚠️  WARNING: This will import data into PostgreSQL.")
    print("   Make sure your PostgreSQL database is empty or you may get duplicate key errors.")
    response = input("\nContinue with import? (y/n): ")

    if response.lower() != 'y':
        print("❌ Migration cancelled.")
        return

    # Import data
    success = import_data_to_postgres()

    if success:
        # Verify
        verify_migration()
        print("✅ Migration completed successfully!")
        print()
        print("📝 Next steps:")
        print("   1. Test your application with PostgreSQL")
        print("   2. Update environment variables on Render")
        print("   3. Deploy to production")
        print()
    else:
        print("❌ Migration failed. Please check the errors above.")

if __name__ == '__main__':
    main()
