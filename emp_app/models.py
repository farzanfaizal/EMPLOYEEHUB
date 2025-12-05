from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Create your models here.

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