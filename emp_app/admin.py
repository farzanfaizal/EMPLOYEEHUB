from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from emp_app.user_models import CustomUser, UserActivity, LoginAttempt
from emp_app.models import (
    Role, Department, Employee, Attendance, Leave,
    FingerprintData, BiometricAttendance, DocumentCategory, EmployeeDocument
)

# ==================== USER MANAGEMENT ====================

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'is_verified', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Role & Access', {
            'fields': ('role', 'employee', 'is_verified')
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'date_of_birth', 'address', 'profile_picture')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('OAuth & Social', {
            'fields': ('google_id',)
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'theme_preference')
        }),
        ('Security', {
            'fields': ('last_login_ip',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'email', 'first_name', 'last_name')
        }),
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'action', 'description', 'ip_address']
    readonly_fields = ['user', 'action', 'description', 'ip_address', 'user_agent', 'timestamp']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False  # Activities are auto-created

    def has_change_permission(self, request, obj=None):
        return False  # Read-only


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['username', 'success', 'timestamp', 'ip_address']
    list_filter = ['success', 'timestamp']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['username', 'ip_address', 'user_agent', 'success', 'timestamp']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# ==================== CORE MODELS ====================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'created_at', 'updated_at']
    search_fields = ['name', 'location']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_id', 'first_name', 'last_name', 'dept', 'role', 'hire_date', 'is_active']
    list_filter = ['dept', 'role', 'hire_date', 'is_active']
    search_fields = ['first_name', 'last_name', 'phone_num']
    date_hierarchy = 'hire_date'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'check_in_time', 'check_out_time']
    list_filter = ['status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name']
    date_hierarchy = 'date'

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_date']
    list_filter = ['status', 'leave_type', 'start_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'reason']
    date_hierarchy = 'applied_date'

@admin.register(FingerprintData)
class FingerprintDataAdmin(admin.ModelAdmin):
    list_display = ['employee', 'enrolled_date', 'last_updated', 'is_active', 'quality_score', 'device_id']
    list_filter = ['is_active', 'enrolled_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'device_id']
    readonly_fields = ['enrolled_date', 'last_updated']

@admin.register(BiometricAttendance)
class BiometricAttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'timestamp', 'status', 'device_id', 'confidence_score']
    list_filter = ['status', 'timestamp', 'device_id']
    search_fields = ['employee__first_name', 'employee__last_name', 'device_id']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name', 'description']

@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'title', 'category', 'uploaded_by', 'uploaded_at', 'status', 'is_confidential']
    list_filter = ['status', 'category', 'is_confidential', 'uploaded_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'title', 'description']
    date_hierarchy = 'uploaded_at'
    readonly_fields = ['uploaded_at', 'updated_at', 'file_size', 'file_type']