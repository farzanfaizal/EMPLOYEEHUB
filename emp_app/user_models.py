"""
Custom User Model with Role-Based Access Control
Professional implementation for EmployeeHub
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


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
            from .models import Employee
            return Employee.objects.all()
        elif self.is_dept_manager() and self.employee:
            # Department managers can see their department
            return self.employee.dept.employees.all()
        elif self.employee:
            # Regular employees can only see themselves
            from .models import Employee
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
