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
]
