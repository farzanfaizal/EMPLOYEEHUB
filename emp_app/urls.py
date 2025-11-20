from django.urls import path
from emp_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-emp', views.allEmp, name='all-emp'),
    path('add-emp', views.addEmp, name='add-emp'),
    path('remove-emp', views.removeEmp, name='remove-emp'),
    path('remove-emp/<int:empID>', views.removeEmp, name='remove-emp'),
    path('filter-emp', views.filterEmp, name='filter-emp'),
    path('employees/', views.listEmployees, name='list_employees'),
    path('update-emp/<int:emp_id>/', views.updateEmp, name='update_emp'),

    # Attendance URLs
    path('attendance/mark', views.markAttendance, name='mark-attendance'),
    path('attendance/view', views.viewAttendance, name='view-attendance'),
    path('attendance/report', views.attendanceReport, name='attendance-report'),

    # Leave URLs
    path('attendance/apply-leave', views.applyLeave, name='apply-leave'),
    path('attendance/leaves', views.viewLeaves, name='view-leaves'),
    path('attendance/leave/<int:leave_id>/approve', views.approveLeave, name='approve-leave'),

    # Biometric Fingerprint URLs
    path('biometric/fingerprint', views.fingerprintManagement, name='fingerprint-management'),
    path('biometric/enroll', views.enrollFingerprint, name='enroll-fingerprint'),
    path('biometric/update/<int:fingerprint_id>', views.updateFingerprint, name='update-fingerprint'),
    path('biometric/delete/<int:fingerprint_id>', views.deleteFingerprint, name='delete-fingerprint'),
    path('biometric/logs', views.biometricAttendanceLogs, name='biometric-logs'),
    path('biometric/simulate-scan', views.simulateBiometricScan, name='simulate-scan'),

    # Document Management URLs
    path('documents/dashboard', views.documentDashboard, name='document-dashboard'),
    path('documents/employee/<int:emp_id>', views.employeeDocuments, name='employee-documents'),
    path('documents/upload', views.uploadDocument, name='upload-document'),
    path('documents/download/<int:doc_id>', views.downloadDocument, name='download-document'),
    path('documents/delete/<int:doc_id>', views.deleteDocument, name='delete-document'),
    path('documents/categories', views.manageCategories, name='manage-categories'),

    # Analytics URLs
    path('analytics/dashboard', views.analyticsDashboard, name='analytics-dashboard'),

    # HR Tools URLs
    path('hr-tools/dashboard', views.hrToolsDashboard, name='hr-tools-dashboard'),
    path('hr-tools/export-directory', views.employeeDirectoryExport, name='export-directory'),
    path('hr-tools/birthday-reminders', views.birthdayReminders, name='birthday-reminders'),
    path('hr-tools/salary-calculator', views.salaryCalculator, name='salary-calculator'),

    # About Page
    path('about', views.about, name='about'),

    # Contact Page
    path('contact', views.contact, name='contact'),

    # Department & Role Management
    path('manage/departments', views.manageDepartments, name='manage-departments'),
    path('manage/roles', views.manageRoles, name='manage-roles'),

    # Performance Reviews
    path('performance/reviews', views.performanceReviews, name='performance-reviews'),
    path('performance/add-review', views.addPerformanceReview, name='add-performance-review'),

    # Task Management
    path('tasks/dashboard', views.tasksDashboard, name='tasks-dashboard'),
    path('tasks/add', views.addTask, name='add-task'),
    path('tasks/<int:task_id>/update-status', views.updateTaskStatus, name='update-task-status'),

    # Announcements
    path('announcements/dashboard', views.announcementsDashboard, name='announcements-dashboard'),
    path('announcements/create', views.createAnnouncement, name='create-announcement'),

    # Activity Logs
    path('admin/activity-logs', views.activityLogs, name='activity-logs'),

    # Batch Operations
    path('batch/import', views.batchImportEmployees, name='batch-import'),

    # Coming Soon routes (placeholders)
    path('attendance/view', views.coming_soon, name='attendance_view'),
    path('attendance/mark', views.coming_soon, name='attendance_mark'),
    path('attendance/leaves', views.coming_soon, name='attendance_leaves'),
    path('attendance/apply-leave', views.coming_soon, name='attendance_apply_leave'),
    path('documents/upload', views.coming_soon, name='documents_upload'),
    path('documents/dashboard', views.coming_soon, name='documents_dashboard'),
    path('analytics/dashboard', views.coming_soon, name='analytics_dashboard'),
    path('hr-tools/dashboard', views.coming_soon, name='hr_tools_dashboard'),
    path('biometric/fingerprint', views.coming_soon, name='biometric_fingerprint'),
]
