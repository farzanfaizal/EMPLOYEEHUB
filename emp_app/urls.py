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
]
