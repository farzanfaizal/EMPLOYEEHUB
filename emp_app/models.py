from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=True, null=True, help_text="Employee email address")
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=20, default='', help_text="Phone number with country code")
    hire_date = models.DateField()
    date_of_birth = models.DateField(null=True, blank=True, help_text="Employee date of birth")
    address = models.TextField(blank=True, null=True, help_text="Residential address")
    emergency_contact = models.CharField(max_length=20, blank=True, null=True, help_text="Emergency contact number")
    is_active = models.BooleanField(default=True, help_text="Is employee currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-hire_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def total_compensation(self):
        return self.salary + self.bonus

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


# Performance Management Models
class PerformanceReview(models.Model):
    """Track employee performance reviews"""
    RATING_CHOICES = [
        (1, 'Needs Improvement'),
        (2, 'Below Expectations'),
        (3, 'Meets Expectations'),
        (4, 'Exceeds Expectations'),
        (5, 'Outstanding'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.CharField(max_length=100, help_text="Name of the reviewer")
    review_period_start = models.DateField(help_text="Start of review period")
    review_period_end = models.DateField(help_text="End of review period")
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    technical_skills = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    communication = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    teamwork = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    leadership = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    productivity = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    strengths = models.TextField(help_text="Employee strengths")
    areas_for_improvement = models.TextField(help_text="Areas needing improvement")
    goals = models.TextField(help_text="Goals for next period")
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-review_period_end']
        verbose_name = "Performance Review"
        verbose_name_plural = "Performance Reviews"

    def __str__(self):
        return f"{self.employee} - Review ({self.review_period_end})"


class ActivityLog(models.Model):
    """Track all system activities for audit purposes"""
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('view', 'Viewed'),
        ('export', 'Exported'),
        ('import', 'Imported'),
    ]

    user = models.CharField(max_length=100, help_text="User who performed the action")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100, help_text="Model that was affected")
    object_id = models.IntegerField(help_text="ID of the affected object")
    object_repr = models.CharField(max_length=200, help_text="String representation of object")
    changes = models.TextField(blank=True, null=True, help_text="JSON of changes made")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} ({self.timestamp})"


class Announcement(models.Model):
    """Company-wide announcements"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True, help_text="When announcement expires")
    is_active = models.BooleanField(default=True)
    target_departments = models.ManyToManyField(Department, blank=True, help_text="Specific departments (leave empty for all)")

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.title


class Task(models.Model):
    """Task assignment and tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.CharField(max_length=100, help_text="Person who assigned the task")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.title} - {self.assigned_to}"