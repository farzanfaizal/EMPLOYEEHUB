from django.contrib import admin
from emp_app.models import (
    Role, Department, Employee, Attendance, Leave,
    FingerprintData, BiometricAttendance, DocumentCategory, EmployeeDocument,
    PerformanceReview, ActivityLog, Announcement, Task
)

# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    search_fields = ['name', 'location']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_id', 'first_name', 'last_name', 'email', 'dept', 'role', 'hire_date', 'is_active']
    list_filter = ['dept', 'role', 'is_active', 'hire_date']
    search_fields = ['first_name', 'last_name', 'email', 'phone_num']
    date_hierarchy = 'hire_date'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'phone_num', 'emergency_contact', 'address')
        }),
        ('Work Information', {
            'fields': ('dept', 'role', 'hire_date', 'is_active')
        }),
        ('Compensation', {
            'fields': ('salary', 'bonus')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

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

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'reviewer', 'review_period_end', 'overall_rating', 'created_at']
    list_filter = ['overall_rating', 'review_period_end']
    search_fields = ['employee__first_name', 'employee__last_name', 'reviewer']
    date_hierarchy = 'review_period_end'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee', 'reviewer', 'review_period_start', 'review_period_end')
        }),
        ('Ratings', {
            'fields': ('overall_rating', 'technical_skills', 'communication', 'teamwork', 'leadership', 'productivity')
        }),
        ('Feedback', {
            'fields': ('strengths', 'areas_for_improvement', 'goals', 'comments')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_repr', 'timestamp', 'ip_address']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user', 'object_repr', 'model_name']
    date_hierarchy = 'timestamp'
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address', 'timestamp']

    def has_add_permission(self, request):
        return False  # Logs should only be created automatically

    def has_change_permission(self, request, obj=None):
        return False  # Logs should not be editable

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'author', 'published_date', 'expiry_date', 'is_active']
    list_filter = ['priority', 'is_active', 'published_date']
    search_fields = ['title', 'content', 'author']
    date_hierarchy = 'published_date'
    filter_horizontal = ['target_departments']
    readonly_fields = ['published_date']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'assigned_by', 'status', 'priority', 'due_date', 'completed_date']
    list_filter = ['status', 'priority', 'due_date']
    search_fields = ['title', 'description', 'assigned_to__first_name', 'assigned_to__last_name', 'assigned_by']
    date_hierarchy = 'due_date'
    readonly_fields = ['created_at', 'updated_at', 'completed_date']
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'assigned_by', 'due_date')
        }),
        ('Status', {
            'fields': ('status', 'priority', 'completed_date')
        }),
        ('Additional Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )