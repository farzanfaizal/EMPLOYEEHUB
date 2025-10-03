from django.contrib import admin
from emp_app.models import Role, Department, Employee, Attendance, Leave

# Register your models here.

admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Leave)