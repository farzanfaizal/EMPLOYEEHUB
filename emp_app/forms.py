"""
Django Forms for EmployeeHub Application
Provides validation and clean data handling for all user inputs
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from .models import (
    Employee, Department, Role, Attendance, Leave,
    FingerprintData, BiometricAttendance, DocumentCategory, EmployeeDocument
)


class EmployeeForm(forms.ModelForm):
    """Form for creating and updating employees with validation"""

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'dept', 'role', 'salary', 'bonus', 'phone_num', 'hire_date', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter last name',
                'required': True
            }),
            'dept': forms.Select(attrs={
                'class': 'form-select-modern',
                'required': True
            }),
            'role': forms.Select(attrs={
                'class': 'form-select-modern',
                'required': True
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control-modern',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'bonus': forms.NumberInput(attrs={
                'class': 'form-control-modern',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'phone_num': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': '+1234567890',
                'pattern': r'^\+?1?\d{9,15}$'
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control-modern',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_hire_date(self):
        """Validate hire date is not in the future"""
        hire_date = self.cleaned_data.get('hire_date')
        if hire_date and hire_date > date.today():
            raise ValidationError("Hire date cannot be in the future")
        return hire_date

    def clean_salary(self):
        """Validate salary is reasonable"""
        salary = self.cleaned_data.get('salary')
        if salary and salary < 0:
            raise ValidationError("Salary must be positive")
        if salary and salary > 1000000:
            raise ValidationError("Salary seems unreasonably high. Please verify.")
        return salary


class AttendanceForm(forms.ModelForm):
    """Form for marking attendance"""

    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'check_in_time', 'check_out_time', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select-modern'}),
            'date': forms.DateInput(attrs={'class': 'form-control-modern', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select-modern'}),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control-modern', 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control-modern', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control-modern', 'rows': 3}),
        }

    def clean(self):
        """Validate check-out is after check-in"""
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_time')
        check_out = cleaned_data.get('check_out_time')

        if check_in and check_out and check_out <= check_in:
            raise ValidationError("Check-out time must be after check-in time")

        return cleaned_data


class LeaveForm(forms.ModelForm):
    """Form for leave applications"""

    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select-modern'}),
            'leave_type': forms.Select(attrs={'class': 'form-select-modern'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control-modern', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control-modern', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control-modern', 'rows': 4, 'placeholder': 'Please provide reason for leave'}),
        }

    def clean(self):
        """Validate leave dates"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError("End date must be after start date")

            # Check if dates are too far in past
            if start_date < date.today():
                raise ValidationError("Cannot apply for leave in the past")

            # Check if leave duration is reasonable (max 90 days)
            duration = (end_date - start_date).days + 1
            if duration > 90:
                raise ValidationError("Leave duration cannot exceed 90 days")

        return cleaned_data


class DocumentUploadForm(forms.ModelForm):
    """Form for document uploads with security validation"""

    class Meta:
        model = EmployeeDocument
        fields = ['employee', 'category', 'title', 'description', 'file', 'expiry_date', 'is_confidential']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select-modern'}),
            'category': forms.Select(attrs={'class': 'form-select-modern'}),
            'title': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': 'Document title'}),
            'description': forms.Textarea(attrs={'class': 'form-control-modern', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control-modern'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control-modern', 'type': 'date'}),
            'is_confidential': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_file(self):
        """Validate file upload"""
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (5MB limit)
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("File size cannot exceed 5MB")

            # Check file extension
            allowed_extensions = ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'xls', 'xlsx', 'csv', 'zip']
            ext = file.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(f"File type '.{ext}' not allowed. Allowed types: {', '.join(allowed_extensions)}")

        return file

    def clean_title(self):
        """Sanitize title"""
        title = self.cleaned_data.get('title')
        if title:
            # Remove any potentially dangerous characters
            title = title.strip()[:200]
        return title


class FingerprintEnrollmentForm(forms.ModelForm):
    """Form for fingerprint enrollment"""

    class Meta:
        model = FingerprintData
        fields = ['employee', 'fingerprint_template', 'device_id', 'quality_score', 'fingerprint_image']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select-modern'}),
            'fingerprint_template': forms.Textarea(attrs={'class': 'form-control-modern', 'rows': 4}),
            'device_id': forms.TextInput(attrs={'class': 'form-control-modern'}),
            'quality_score': forms.NumberInput(attrs={'class': 'form-control-modern', 'min': 0, 'max': 100}),
            'fingerprint_image': forms.FileInput(attrs={'class': 'form-control-modern'}),
        }


class DocumentCategoryForm(forms.ModelForm):
    """Form for creating document categories"""

    class Meta:
        model = DocumentCategory
        fields = ['name', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': 'Category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control-modern', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': 'fa-file'}),
        }


class EmployeeFilterForm(forms.Form):
    """Form for filtering employees"""

    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Search by name...'
        })
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="All Departments",
        widget=forms.Select(attrs={'class': 'form-select-modern'})
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=False,
        empty_label="All Roles",
        widget=forms.Select(attrs={'class': 'form-select-modern'})
    )
    is_active = forms.ChoiceField(
        choices=[('', 'All'), ('true', 'Active'), ('false', 'Inactive')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select-modern'})
    )


# Authentication Forms

class UserLoginForm(AuthenticationForm):
    """Custom login form with styling"""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Password'
        })
    )


class UserRegistrationForm(UserCreationForm):
    """User registration form with email"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Last name'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control-modern', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control-modern', 'placeholder': 'Confirm password'}),
        }

    def clean_email(self):
        """Ensure email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email
