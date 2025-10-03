from django.shortcuts import render, HttpResponse, redirect
from emp_app.models import Employee, Department, Role, Attendance, Leave
from django.contrib import messages
import json
from django.db.models import Q
from datetime import date, datetime, timedelta
from django.db.models import Count

# Create your views here.

def index(request):
    return render(request, 'index.html')

def allEmp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    return render(request, 'all_emp.html', context)

def addEmp(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        emp_dept = request.POST.get('department')
        emp_role = request.POST.get('role')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone_number')
        hire_date = request.POST.get('hire_date')
        if emp_dept == "department" or emp_role == "role":
            messages.warning(request, "Select Department and Role")
        else:
            dept = Department.objects.get(id=emp_dept)
            role = Role.objects.get(id=emp_role)
            emp = Employee(first_name=firstname, last_name=lastname, dept=dept, salary=salary, bonus=bonus, role=role, phone_num=phone, hire_date=hire_date)
            emp.save()
            messages.success(request, "Successfully added an employee")
            return redirect("/")
        return redirect("/add-emp")

    all_depts = Department.objects.all()
    all_roles = Role.objects.all()
    context = {
        'dept': all_depts,
        'role': all_roles
    }
    return render(request, 'add_emp.html', context)

def removeEmp(request, empID=None):
    if request.method == 'POST':
        if empID:
            emp = Employee.objects.get(emp_id=empID)
            emp.delete()
            messages.success(request, "Employee removed")
            return redirect("/")
        else:
            emp_id = int(request.POST.get('emp_id'))
            try:
                emp = Employee.objects.get(emp_id=emp_id)
                if emp:
                    response = json.dumps({'status':'success', 'empID':emp.emp_id, 'firstname':emp.first_name, 'lastname':emp.last_name, 'dept':emp.dept.name, 'location':emp.dept.location, 'salary':emp.salary, 'bonus':emp.bonus, 'role':emp.role.name, 'phone':emp.phone_num, 'hire_date':str(emp.hire_date)})
                    return HttpResponse(response)
            except:
                return HttpResponse('{"status":"not found"}')
    
    return render(request, 'remove_emp.html')


def filterEmp(request):
    if request.method == "POST":
        name = request.POST.get('name')
        dept = request.POST.get('department')
        role = request.POST.get('role')

        emp = Employee.objects.all()
        if name:
            emp = emp.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            dept = int(dept)
            emp = emp.filter(dept__id=dept)
        if role:
            role = int(role)
            emp = emp.filter(role__id=role)
            
        return render(request, 'all_emp.html', {'emps': emp}) 
            
    all_depts = Department.objects.all()
    all_roles = Role.objects.all()
    context = {
        'dept': all_depts,
        'role': all_roles
    }
    return render(request, 'filter_emp.html', context)

def listEmployees(request):
    # Fetch all employees
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'list_employees.html', context)
 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee, Department, Role
 
def updateEmp(request, emp_id):
    # Get the employee object or return 404 if not found
    emp = get_object_or_404(Employee, emp_id=emp_id)
   
    if request.method == 'POST':
        # Fetch form data
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        emp_dept = request.POST.get('department')
        emp_role = request.POST.get('role')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone_number')
        hire_date = request.POST.get('hire_date')
       
        # Get department and role objects
        dept = get_object_or_404(Department, id=emp_dept)
        role = get_object_or_404(Role, id=emp_role)
       
        # Update the employee details
        emp.first_name = firstname
        emp.last_name = lastname
        emp.dept = dept
        emp.role = role
        emp.salary = salary
        emp.bonus = bonus
        emp.phone_num = phone
        emp.hire_date = hire_date
        emp.save()
 
        messages.success(request, "Successfully updated the employee details")
        return redirect('list_employees')  # Go back to employee list after updating
 
    # Fetch all departments and roles to populate the form
    all_depts = Department.objects.all()
    all_roles = Role.objects.all()
 
    context = {
        'emp': emp,
        'depts': all_depts,
        'roles': all_roles
    }
    return render(request, 'update_emp.html', context)

# Attendance Views
def markAttendance(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        attendance_date = request.POST.get('date')
        status = request.POST.get('status')
        check_in = request.POST.get('check_in_time')
        check_out = request.POST.get('check_out_time')
        notes = request.POST.get('notes', '')

        try:
            emp = Employee.objects.get(emp_id=employee_id)
            attendance, created = Attendance.objects.update_or_create(
                employee=emp,
                date=attendance_date,
                defaults={
                    'status': status,
                    'check_in_time': check_in if check_in else None,
                    'check_out_time': check_out if check_out else None,
                    'notes': notes
                }
            )
            if created:
                messages.success(request, f"Attendance marked for {emp.first_name} {emp.last_name}")
            else:
                messages.success(request, f"Attendance updated for {emp.first_name} {emp.last_name}")
            return redirect('/attendance/mark')
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found")
            return redirect('/attendance/mark')

    employees = Employee.objects.all()
    today = date.today()
    context = {
        'employees': employees,
        'today': today
    }
    return render(request, 'attendance/mark_attendance.html', context)

def viewAttendance(request):
    today = date.today()
    selected_date = request.GET.get('date', today)

    if isinstance(selected_date, str):
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    attendances = Attendance.objects.filter(date=selected_date).select_related('employee')

    context = {
        'attendances': attendances,
        'selected_date': selected_date,
        'today': today
    }
    return render(request, 'attendance/view_attendance.html', context)

def attendanceReport(request):
    # Get date range
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()

    # Get attendance stats
    attendances = Attendance.objects.filter(date__range=[start_date, end_date])

    stats = attendances.values('status').annotate(count=Count('status'))

    employees = Employee.objects.all()
    employee_stats = []

    for emp in employees:
        emp_attendances = attendances.filter(employee=emp)
        present = emp_attendances.filter(status='present').count()
        absent = emp_attendances.filter(status='absent').count()
        half_day = emp_attendances.filter(status='half_day').count()
        late = emp_attendances.filter(status='late').count()
        wfh = emp_attendances.filter(status='work_from_home').count()

        employee_stats.append({
            'employee': emp,
            'present': present,
            'absent': absent,
            'half_day': half_day,
            'late': late,
            'wfh': wfh,
            'total': emp_attendances.count()
        })

    context = {
        'stats': stats,
        'employee_stats': employee_stats,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'attendance/attendance_report.html', context)

# Leave Management Views
def applyLeave(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        try:
            emp = Employee.objects.get(emp_id=employee_id)
            leave = Leave.objects.create(
                employee=emp,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )
            messages.success(request, f"Leave application submitted for {emp.first_name} {emp.last_name}")
            return redirect('/attendance/leaves')
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found")
            return redirect('/attendance/apply-leave')

    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'attendance/apply_leave.html', context)

def viewLeaves(request):
    leaves = Leave.objects.all().select_related('employee')

    status_filter = request.GET.get('status')
    if status_filter:
        leaves = leaves.filter(status=status_filter)

    context = {'leaves': leaves}
    return render(request, 'attendance/view_leaves.html', context)

def approveLeave(request, leave_id):
    if request.method == 'POST':
        try:
            leave = Leave.objects.get(id=leave_id)
            action = request.POST.get('action')

            if action == 'approve':
                leave.status = 'approved'
                leave.approved_by = 'Admin'  # You can customize this
                messages.success(request, "Leave approved successfully")
            elif action == 'reject':
                leave.status = 'rejected'
                messages.success(request, "Leave rejected")

            leave.save()
        except Leave.DoesNotExist:
            messages.error(request, "Leave not found")

    return redirect('/attendance/leaves')
