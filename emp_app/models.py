from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Create your models here.

# ==================== USER MODELS ====================

class CustomUser(AbstractUser):
    """
    Extended user model with role-based access control
    Roles: Super Admin, HR Manager, Department Manager, Employee
    """

    class UserRole(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Administrator'
        HR_MANAGER = 'HR_MANAGER', 'HR Manager'
        DEPT_MANAGER = 'DEPT_MANAGER', 'Department Manager'
        EMPLOYEE = 'EMPLOYEE', 'Employee'

    # Extended fields
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE,
        help_text="User's role in the system"
    )
    employee = models.OneToOneField(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account',
        help_text="Linked employee record"
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_regex],
        blank=True,
        help_text="Contact phone number"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text="User profile picture"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Date of birth"
    )
    address = models.TextField(
        blank=True,
        help_text="Home address"
    )
    emergency_contact = models.CharField(
        max_length=100,
        blank=True,
        help_text="Emergency contact name"
    )
    emergency_phone = models.CharField(
        max_length=15,
        validators=[phone_regex],
        blank=True,
        help_text="Emergency contact phone"
    )

    # OAuth fields
    google_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="Google OAuth ID"
    )

    # Preferences
    email_notifications = models.BooleanField(
        default=True,
        help_text="Receive email notifications"
    )
    theme_preference = models.CharField(
        max_length=10,
        choices=[('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')],
        default='light',
        help_text="UI theme preference"
    )

    # Metadata
    is_verified = models.BooleanField(
        default=False,
        help_text="Email verified"
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Last login IP address"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['email']),
            models.Index(fields=['google_id']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    # Permission helper methods
    def is_super_admin(self):
        """Check if user is super admin"""
        return self.role == self.UserRole.SUPER_ADMIN or self.is_superuser

    def is_hr_manager(self):
        """Check if user is HR manager"""
        return self.role == self.UserRole.HR_MANAGER or self.is_super_admin()

    def is_dept_manager(self):
        """Check if user is department manager"""
        return self.role == self.UserRole.DEPT_MANAGER or self.is_hr_manager()

    def can_manage_employees(self):
        """Check if user can manage employees"""
        return self.is_hr_manager()

    def can_view_salary(self):
        """Check if user can view salary information"""
        return self.is_hr_manager()

    def can_approve_leaves(self):
        """Check if user can approve leave requests"""
        return self.is_dept_manager()

    def can_manage_documents(self):
        """Check if user can manage documents"""
        return self.is_dept_manager()

    def get_accessible_employees(self):
        """Get employees this user can access"""
        if self.is_super_admin() or self.is_hr_manager():
            return Employee.objects.all()
        elif self.is_dept_manager() and self.employee:
            # Department managers can see their department
            return self.employee.dept.employees.all()
        elif self.employee:
            # Regular employees can only see themselves
            return Employee.objects.filter(pk=self.employee.pk)
        return Employee.objects.none()


class UserActivity(models.Model):
    """
    Track user activity for audit purposes
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    action = models.CharField(
        max_length=100,
        help_text="Action performed"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        blank=True,
        help_text="Browser user agent"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"


class LoginAttempt(models.Model):
    """
    Track failed login attempts for security
    """
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Login Attempt'
        verbose_name_plural = 'Login Attempts'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['username', '-timestamp']),
            models.Index(fields=['ip_address', '-timestamp']),
        ]

    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.username} - {status} - {self.timestamp}"


# ==================== EMPLOYEE MODELS ====================

class Role(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        unique=True,
        help_text="Role name (e.g., Manager, Developer, HR)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        unique=True,
        help_text="Department name"
    )
    location = models.CharField(
        max_length=100,
        help_text="Department location/office"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.name


class Employee(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(
        max_length=50,
        null=False,
        help_text="Employee's first name"
    )
    last_name = models.CharField(
        max_length=50,
        help_text="Employee's last name"
    )
    dept = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,  # Changed from CASCADE to PROTECT
        related_name='employees',
        help_text="Employee's department"
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Monthly salary"
    )
    bonus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Annual bonus"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,  # Changed from CASCADE to PROTECT
        related_name='employees',
        help_text="Employee's role"
    )
    phone_num = models.CharField(
        max_length=15,
        validators=[phone_regex],
        blank=True,
        help_text="Contact phone number"
    )
    hire_date = models.DateField(help_text="Date of hire")
    is_active = models.BooleanField(default=True, help_text="Is employee currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-hire_date', 'first_name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['dept', 'role']),
            models.Index(fields=['hire_date']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Return the employee's full name."""
        return f"{self.first_name} {self.last_name}"

    def get_total_compensation(self):
        """Calculate total annual compensation."""
        return (self.salary * 12) + self.bonus


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('late', 'Late'),
        ('work_from_home', 'Work From Home'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"

class Leave(models.Model):
    LEAVE_TYPES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('annual', 'Annual Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.start_date} to {self.end_date})"

    def total_days(self):
        return (self.end_date - self.start_date).days + 1


# Biometric Fingerprint Models
class FingerprintData(models.Model):
    """Store fingerprint biometric data for employees"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='fingerprint')
    fingerprint_template = models.TextField(help_text="Encoded fingerprint template data")
    fingerprint_image = models.ImageField(upload_to='fingerprints/', null=True, blank=True, help_text="Optional fingerprint image")
    enrolled_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    device_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID of the fingerprint device used")
    is_active = models.BooleanField(default=True)
    quality_score = models.IntegerField(default=0, help_text="Quality score of fingerprint (0-100)")

    class Meta:
        verbose_name = "Fingerprint Data"
        verbose_name_plural = "Fingerprint Data"

    def __str__(self):
        return f"Fingerprint - {self.employee.first_name} {self.employee.last_name}"


class BiometricAttendance(models.Model):
    """Log attendance records from biometric fingerprint scans"""
    STATUS_CHOICES = [
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
        ('break_start', 'Break Start'),
        ('break_end', 'Break End'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='biometric_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    device_id = models.CharField(max_length=100, help_text="ID of the fingerprint device")
    location = models.CharField(max_length=200, blank=True, null=True)
    confidence_score = models.IntegerField(default=100, help_text="Confidence score of fingerprint match (0-100)")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Biometric Attendance Log"
        verbose_name_plural = "Biometric Attendance Logs"

    def __str__(self):
        return f"{self.employee} - {self.status} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


# Document Management Models
class DocumentCategory(models.Model):
    """Categories for employee documents"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-file', help_text="FontAwesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Document Category"
        verbose_name_plural = "Document Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class EmployeeDocument(models.Model):
    """Store employee-related documents"""
    DOCUMENT_STATUS = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('archived', 'Archived'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, related_name='documents')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='employee_documents/%Y/%m/')
    file_size = models.IntegerField(default=0, help_text="File size in bytes")
    file_type = models.CharField(max_length=50, blank=True)
    uploaded_by = models.CharField(max_length=100, help_text="User who uploaded the document")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateField(null=True, blank=True, help_text="For documents that expire (e.g., contracts, certifications)")
    status = models.CharField(max_length=20, choices=DOCUMENT_STATUS, default='active')
    is_confidential = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Employee Document"
        verbose_name_plural = "Employee Documents"

    def __str__(self):
        return f"{self.employee} - {self.title}"

    def is_expired(self):
        if self.expiry_date:
            from datetime import date
            return date.today() > self.expiry_date
        return False

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)