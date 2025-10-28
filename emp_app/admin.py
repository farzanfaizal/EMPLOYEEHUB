from django.contrib import admin
from emp_app.models import (
    Role, Department, Employee, Attendance, Leave,
    FingerprintData, BiometricAttendance, DocumentCategory, EmployeeDocument
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
    list_display = ['emp_id', 'first_name', 'last_name', 'dept', 'role', 'hire_date']
    list_filter = ['dept', 'role', 'hire_date']
    search_fields = ['first_name', 'last_name', 'phone_num']
    date_hierarchy = 'hire_date'

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