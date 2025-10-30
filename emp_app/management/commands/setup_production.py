"""
Setup production database with sample data
Run this after migrations
"""

from django.core.management.base import BaseCommand
from django.db import connection
from emp_app.models import Department, Role, Employee, DocumentCategory
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Setup production database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Setting up production database...\n'))

        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                self.stdout.write(self.style.SUCCESS(f'✓ Database connected: PostgreSQL'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Database connection failed: {e}'))
            return

        # Create Departments
        self.stdout.write('📁 Creating departments...')
        departments_data = [
            ('Engineering', 'San Francisco'),
            ('Human Resources', 'New York'),
            ('Sales', 'Chicago'),
            ('Marketing', 'Los Angeles'),
            ('Finance', 'Boston'),
            ('Operations', 'Seattle'),
            ('Customer Support', 'Austin'),
            ('IT', 'Denver'),
        ]

        departments = {}
        for name, location in departments_data:
            dept, created = Department.objects.get_or_create(
                name=name,
                defaults={'location': location}
            )
            departments[name] = dept
            if created:
                self.stdout.write(f'  ✓ Created: {name}')
            else:
                self.stdout.write(f'  → Exists: {name}')

        # Create Roles
        self.stdout.write('\n👔 Creating roles...')
        roles_data = [
            'Software Engineer',
            'Senior Software Engineer',
            'Engineering Manager',
            'HR Manager',
            'HR Specialist',
            'Recruiter',
            'Sales Representative',
            'Sales Manager',
            'Account Executive',
            'Marketing Specialist',
            'Marketing Manager',
            'Content Writer',
            'Financial Analyst',
            'Accountant',
            'Finance Manager',
            'Operations Manager',
            'Support Specialist',
            'IT Administrator',
        ]

        roles = {}
        for role_name in roles_data:
            role, created = Role.objects.get_or_create(name=role_name)
            roles[role_name] = role
            if created:
                self.stdout.write(f'  ✓ Created: {role_name}')
            else:
                self.stdout.write(f'  → Exists: {role_name}')

        # Create Document Categories
        self.stdout.write('\n📄 Creating document categories...')
        categories_data = [
            ('Employment Contracts', 'Employment contracts and agreements', 'fa-file-contract'),
            ('Tax Documents', 'Tax forms and documents', 'fa-file-invoice-dollar'),
            ('Certifications', 'Professional certifications and licenses', 'fa-certificate'),
            ('Performance Reviews', 'Performance evaluations and reviews', 'fa-chart-line'),
            ('Training Materials', 'Training and development documents', 'fa-graduation-cap'),
            ('Personal Documents', 'ID copies and personal documents', 'fa-id-card'),
            ('Benefits Documentation', 'Health insurance, 401k, benefits', 'fa-heartbeat'),
            ('Disciplinary Records', 'Warnings and disciplinary actions', 'fa-gavel'),
        ]

        for name, desc, icon in categories_data:
            cat, created = DocumentCategory.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'icon': icon}
            )
            if created:
                self.stdout.write(f'  ✓ Created: {name}')
            else:
                self.stdout.write(f'  → Exists: {name}')

        # Create Sample Employees (if none exist)
        existing_employees = Employee.objects.count()
        if existing_employees == 0:
            self.stdout.write('\n👥 Creating sample employees...')

            employees_data = [
                ('John', 'Doe', 'Engineering', 'Software Engineer', 95000, 5000, 5551234567),
                ('Jane', 'Smith', 'Human Resources', 'HR Manager', 85000, 4000, 5559876543),
                ('Mike', 'Johnson', 'Sales', 'Sales Manager', 90000, 10000, 5555551111),
                ('Sarah', 'Williams', 'Marketing', 'Marketing Manager', 88000, 6000, 5555552222),
                ('David', 'Brown', 'Finance', 'Finance Manager', 92000, 5500, 5555553333),
                ('Emily', 'Davis', 'Engineering', 'Senior Software Engineer', 105000, 7000, 5555554444),
                ('Robert', 'Miller', 'Sales', 'Account Executive', 75000, 8000, 5555555555),
                ('Lisa', 'Wilson', 'IT', 'IT Administrator', 80000, 3000, 5555556666),
                ('Tom', 'Anderson', 'Operations', 'Operations Manager', 87000, 4500, 5555557777),
                ('Maria', 'Garcia', 'Customer Support', 'Support Specialist', 60000, 2000, 5555558888),
            ]

            for first, last, dept_name, role_name, salary, bonus, phone in employees_data:
                try:
                    # Random hire date in the last 2 years
                    days_ago = random.randint(30, 730)
                    hire_date = date.today() - timedelta(days=days_ago)

                    emp = Employee.objects.create(
                        first_name=first,
                        last_name=last,
                        dept=departments[dept_name],
                        role=roles[role_name],
                        salary=salary,
                        bonus=bonus,
                        phone_num=phone,
                        hire_date=hire_date
                    )
                    self.stdout.write(f'  ✓ Created: {first} {last} - {dept_name}')
                except Exception as e:
                    self.stdout.write(f'  ✗ Error creating {first} {last}: {e}')
        else:
            self.stdout.write(f'\n👥 Employees already exist: {existing_employees} records')

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ Production setup complete!'))
        self.stdout.write(self.style.SUCCESS('='*60))

        self.stdout.write(f'\n📊 Database Summary:')
        self.stdout.write(f'  Departments: {Department.objects.count()}')
        self.stdout.write(f'  Roles: {Role.objects.count()}')
        self.stdout.write(f'  Employees: {Employee.objects.count()}')
        self.stdout.write(f'  Document Categories: {DocumentCategory.objects.count()}')

        self.stdout.write(self.style.WARNING('\n📝 Next Steps:'))
        self.stdout.write(self.style.WARNING('  1. Create a superuser: python manage.py createsuperuser'))
        self.stdout.write(self.style.WARNING('  2. Access admin: /admin/'))
        self.stdout.write(self.style.WARNING('  3. Start using the app!'))
        self.stdout.write('')
