from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from emp_app.models import (
    Employee, Department, Role, Attendance, Leave,
    FingerprintData, BiometricAttendance, DocumentCategory, EmployeeDocument
)
from django.contrib import messages
import json
from django.db.models import Q
from datetime import date, datetime, timedelta
from django.db.models import Count
from django.http import JsonResponse, FileResponse
from django.core.files.storage import default_storage
import os

# Create your views here.

def index(request):
    # Get statistics for the dashboard
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    total_roles = Role.objects.count()

    # Calculate growth rate based on employees hired in last 30 days
    from datetime import date, timedelta
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_hires = Employee.objects.filter(hire_date__gte=thirty_days_ago).count()
    growth_rate = round((recent_hires / total_employees * 100) if total_employees > 0 else 0, 1)

    # Get recent employees (last 5 added)
    recent_employees = Employee.objects.order_by('-emp_id')[:5]

    # Get today's attendance stats
    today = date.today()
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='present').count()
    absent_today = today_attendance.filter(status='absent').count()

    # Get pending leave requests
    pending_leaves = Leave.objects.filter(status='pending').count()

    # Get recent documents (last 5 uploaded)
    recent_documents = EmployeeDocument.objects.order_by('-uploaded_at')[:5]

    # Calculate average salary
    from django.db.models import Avg
    avg_salary = Employee.objects.aggregate(Avg('salary'))['salary__avg']
    avg_salary = round(avg_salary) if avg_salary else 0

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_roles': total_roles,
        'growth_rate': growth_rate,
        'recent_employees': recent_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'pending_leaves': pending_leaves,
        'recent_documents': recent_documents,
        'avg_salary': avg_salary,
    }
    return render(request, 'index.html', context)

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


# ==========================================
# FINGERPRINT BIOMETRIC MANAGEMENT VIEWS
# ==========================================

def fingerprintManagement(request):
    """Main fingerprint management dashboard"""
    employees = Employee.objects.all()
    enrolled_count = FingerprintData.objects.filter(is_active=True).count()
    not_enrolled = employees.count() - enrolled_count

    fingerprints = FingerprintData.objects.select_related('employee').all()

    context = {
        'employees': employees,
        'fingerprints': fingerprints,
        'enrolled_count': enrolled_count,
        'not_enrolled': not_enrolled,
        'total_employees': employees.count()
    }
    return render(request, 'biometric/fingerprint_management.html', context)


def enrollFingerprint(request):
    """Enroll a new fingerprint for an employee"""
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        fingerprint_template = request.POST.get('fingerprint_template')
        device_id = request.POST.get('device_id', '')
        quality_score = request.POST.get('quality_score', 0)
        fingerprint_image = request.FILES.get('fingerprint_image')

        try:
            emp = Employee.objects.get(emp_id=employee_id)

            # Check if fingerprint already exists
            if FingerprintData.objects.filter(employee=emp).exists():
                messages.warning(request, f"Fingerprint already enrolled for {emp.first_name} {emp.last_name}")
                return redirect('/biometric/fingerprint')

            # Create new fingerprint record
            fingerprint = FingerprintData.objects.create(
                employee=emp,
                fingerprint_template=fingerprint_template,
                device_id=device_id,
                quality_score=quality_score,
                fingerprint_image=fingerprint_image
            )

            messages.success(request, f"Fingerprint enrolled successfully for {emp.first_name} {emp.last_name}")
            return redirect('/biometric/fingerprint')

        except Employee.DoesNotExist:
            messages.error(request, "Employee not found")
            return redirect('/biometric/enroll')

    # Get employees without fingerprints
    enrolled_emp_ids = FingerprintData.objects.values_list('employee_id', flat=True)
    available_employees = Employee.objects.exclude(emp_id__in=enrolled_emp_ids)

    context = {'employees': available_employees}
    return render(request, 'biometric/enroll_fingerprint.html', context)


def updateFingerprint(request, fingerprint_id):
    """Update existing fingerprint data"""
    fingerprint = get_object_or_404(FingerprintData, id=fingerprint_id)

    if request.method == 'POST':
        fingerprint_template = request.POST.get('fingerprint_template')
        device_id = request.POST.get('device_id')
        quality_score = request.POST.get('quality_score', 0)
        fingerprint_image = request.FILES.get('fingerprint_image')
        is_active = request.POST.get('is_active') == 'on'

        fingerprint.fingerprint_template = fingerprint_template
        fingerprint.device_id = device_id
        fingerprint.quality_score = quality_score
        fingerprint.is_active = is_active

        if fingerprint_image:
            fingerprint.fingerprint_image = fingerprint_image

        fingerprint.save()
        messages.success(request, f"Fingerprint updated for {fingerprint.employee.first_name} {fingerprint.employee.last_name}")
        return redirect('/biometric/fingerprint')

    context = {'fingerprint': fingerprint}
    return render(request, 'biometric/update_fingerprint.html', context)


def deleteFingerprint(request, fingerprint_id):
    """Delete fingerprint data"""
    if request.method == 'POST':
        try:
            fingerprint = FingerprintData.objects.get(id=fingerprint_id)
            emp_name = f"{fingerprint.employee.first_name} {fingerprint.employee.last_name}"
            fingerprint.delete()
            messages.success(request, f"Fingerprint removed for {emp_name}")
        except FingerprintData.DoesNotExist:
            messages.error(request, "Fingerprint data not found")

    return redirect('/biometric/fingerprint')


def biometricAttendanceLogs(request):
    """View biometric attendance logs"""
    logs = BiometricAttendance.objects.select_related('employee').all()

    # Filter by date
    filter_date = request.GET.get('date')
    if filter_date:
        logs = logs.filter(timestamp__date=filter_date)

    # Filter by employee
    employee_id = request.GET.get('employee')
    if employee_id:
        logs = logs.filter(employee_id=employee_id)

    employees = Employee.objects.all()

    context = {
        'logs': logs[:100],  # Limit to 100 recent logs
        'employees': employees,
        'filter_date': filter_date or date.today().strftime('%Y-%m-%d')
    }
    return render(request, 'biometric/attendance_logs.html', context)


def simulateBiometricScan(request):
    """Simulate a fingerprint scan for testing (API endpoint)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        status = data.get('status', 'check_in')
        device_id = data.get('device_id', 'DEVICE_001')

        try:
            emp = Employee.objects.get(emp_id=employee_id)

            # Check if fingerprint exists
            if not FingerprintData.objects.filter(employee=emp, is_active=True).exists():
                return JsonResponse({'status': 'error', 'message': 'No active fingerprint found'}, status=400)

            # Create biometric log
            log = BiometricAttendance.objects.create(
                employee=emp,
                status=status,
                device_id=device_id,
                confidence_score=95
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Attendance logged for {emp.first_name} {emp.last_name}',
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'action': status
            })

        except Employee.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Employee not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# ==========================================
# DOCUMENT MANAGEMENT VIEWS
# ==========================================

def documentDashboard(request):
    """Main document management dashboard"""
    documents = EmployeeDocument.objects.select_related('employee', 'category').all()
    categories = DocumentCategory.objects.all()

    # Get statistics
    total_docs = documents.count()
    active_docs = documents.filter(status='active').count()
    expired_docs = documents.filter(status='expired').count()

    # Check for expiring documents (within 30 days)
    thirty_days_later = date.today() + timedelta(days=30)
    expiring_soon = documents.filter(
        expiry_date__lte=thirty_days_later,
        expiry_date__gte=date.today(),
        status='active'
    ).count()

    context = {
        'documents': documents[:50],  # Show recent 50 documents
        'categories': categories,
        'total_docs': total_docs,
        'active_docs': active_docs,
        'expired_docs': expired_docs,
        'expiring_soon': expiring_soon
    }
    return render(request, 'documents/dashboard.html', context)


def employeeDocuments(request, emp_id):
    """View all documents for a specific employee"""
    employee = get_object_or_404(Employee, emp_id=emp_id)
    documents = EmployeeDocument.objects.filter(employee=employee).select_related('category')
    categories = DocumentCategory.objects.all()

    context = {
        'employee': employee,
        'documents': documents,
        'categories': categories
    }
    return render(request, 'documents/employee_documents.html', context)


def uploadDocument(request):
    """Upload a new document with validation"""
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        category_id = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        file = request.FILES.get('file')
        expiry_date = request.POST.get('expiry_date') or None
        is_confidential = request.POST.get('is_confidential') == 'on'
        uploaded_by = request.POST.get('uploaded_by', 'Public User')

        # Validate file upload
        if not file:
            messages.error(request, "Please select a file to upload")
            return redirect('/documents/upload')

        # Check file size (5MB limit)
        from django.conf import settings
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5 * 1024 * 1024)
        if file.size > max_size:
            messages.error(request, f"File size exceeds {max_size / (1024*1024):.0f}MB limit. Your file: {file.size / (1024*1024):.2f}MB")
            return redirect('/documents/upload')

        # Check file type
        file_ext = file.name.split('.')[-1].lower()
        allowed_types = getattr(settings, 'ALLOWED_DOCUMENT_TYPES', ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'])
        if file_ext not in allowed_types:
            messages.error(request, f"File type '.{file_ext}' not allowed. Allowed types: {', '.join(allowed_types)}")
            return redirect('/documents/upload')

        # Sanitize title and description
        title = title.strip()[:200]  # Limit title length
        description = description.strip()[:1000]  # Limit description length

        if not title:
            messages.error(request, "Please provide a document title")
            return redirect('/documents/upload')

        try:
            emp = Employee.objects.get(emp_id=employee_id)
            category = DocumentCategory.objects.get(id=category_id) if category_id else None

            # Check total documents per employee (limit to 50)
            doc_count = EmployeeDocument.objects.filter(employee=emp).count()
            if doc_count >= 50:
                messages.error(request, f"Maximum 50 documents per employee reached for {emp.first_name} {emp.last_name}")
                return redirect('/documents/upload')

            document = EmployeeDocument.objects.create(
                employee=emp,
                category=category,
                title=title,
                description=description,
                file=file,
                expiry_date=expiry_date,
                is_confidential=is_confidential,
                uploaded_by=uploaded_by
            )

            messages.success(request, f"Document '{title}' uploaded successfully ({file.size / 1024:.0f}KB)")
            return redirect(f'/documents/employee/{employee_id}')

        except Employee.DoesNotExist:
            messages.error(request, "Employee not found")
        except DocumentCategory.DoesNotExist:
            messages.error(request, "Category not found")
        except Exception as e:
            messages.error(request, f"Upload failed: {str(e)}")
            return redirect('/documents/upload')

    employees = Employee.objects.all()
    categories = DocumentCategory.objects.all()

    context = {
        'employees': employees,
        'categories': categories
    }
    return render(request, 'documents/upload_document.html', context)


def downloadDocument(request, doc_id):
    """Download a document"""
    document = get_object_or_404(EmployeeDocument, id=doc_id)

    if document.file:
        response = FileResponse(document.file.open('rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(document.file.name)}"'
        return response

    messages.error(request, "File not found")
    return redirect('/documents/dashboard')


def deleteDocument(request, doc_id):
    """Delete a document"""
    if request.method == 'POST':
        try:
            document = EmployeeDocument.objects.get(id=doc_id)
            emp_id = document.employee.emp_id

            # Delete the file from storage
            if document.file:
                document.file.delete()

            document.delete()
            messages.success(request, "Document deleted successfully")
            return redirect(f'/documents/employee/{emp_id}')
        except EmployeeDocument.DoesNotExist:
            messages.error(request, "Document not found")

    return redirect('/documents/dashboard')


def manageCategories(request):
    """Manage document categories"""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            icon = request.POST.get('icon', 'fa-file')

            DocumentCategory.objects.create(
                name=name,
                description=description,
                icon=icon
            )
            messages.success(request, f"Category '{name}' created successfully")

        elif action == 'delete':
            category_id = request.POST.get('category_id')
            try:
                category = DocumentCategory.objects.get(id=category_id)
                category.delete()
                messages.success(request, "Category deleted successfully")
            except DocumentCategory.DoesNotExist:
                messages.error(request, "Category not found")

    categories = DocumentCategory.objects.all()
    context = {'categories': categories}
    return render(request, 'documents/manage_categories.html', context)


# ==========================================
# ANALYTICS AND REPORTING VIEWS
# ==========================================

def analyticsDashboard(request):
    """Advanced analytics dashboard with charts and insights"""
    from django.db.models import Avg, Sum, Max, Min

    # Employee statistics
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    total_roles = Role.objects.count()

    # Department-wise employee distribution
    dept_distribution = Department.objects.annotate(
        emp_count=Count('employee')
    ).values('name', 'emp_count')

    # Role-wise employee distribution
    role_distribution = Role.objects.annotate(
        emp_count=Count('employee')
    ).values('name', 'emp_count')

    # Salary statistics
    salary_stats = Employee.objects.aggregate(
        avg_salary=Avg('salary'),
        total_salary=Sum('salary'),
        max_salary=Max('salary'),
        min_salary=Min('salary')
    )

    # Attendance statistics (last 30 days)
    thirty_days_ago = date.today() - timedelta(days=30)
    attendance_stats = Attendance.objects.filter(date__gte=thirty_days_ago).values('status').annotate(
        count=Count('status')
    )

    # Leave statistics
    leave_stats = Leave.objects.values('status').annotate(count=Count('status'))
    leave_type_stats = Leave.objects.values('leave_type').annotate(count=Count('leave_type'))

    # Hiring trends (last 12 months)
    one_year_ago = date.today() - timedelta(days=365)
    twelve_months_ago = date.today() - timedelta(days=365)
    hiring_by_month = []
    for i in range(12):
        month_start = twelve_months_ago + timedelta(days=30*i)
        month_end = twelve_months_ago + timedelta(days=30*(i+1))
        count = Employee.objects.filter(hire_date__gte=month_start, hire_date__lt=month_end).count()
        hiring_by_month.append({'month': month_start.strftime('%b %Y'), 'count': count})

    # Document statistics
    doc_stats = {
        'total': EmployeeDocument.objects.count(),
        'active': EmployeeDocument.objects.filter(status='active').count(),
        'expired': EmployeeDocument.objects.filter(status='expired').count(),
        'confidential': EmployeeDocument.objects.filter(is_confidential=True).count()
    }

    # Biometric enrollment status
    biometric_stats = {
        'enrolled': FingerprintData.objects.filter(is_active=True).count(),
        'not_enrolled': total_employees - FingerprintData.objects.filter(is_active=True).count()
    }

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_roles': total_roles,
        'dept_distribution': list(dept_distribution),
        'role_distribution': list(role_distribution),
        'salary_stats': salary_stats,
        'attendance_stats': list(attendance_stats),
        'leave_stats': list(leave_stats),
        'leave_type_stats': list(leave_type_stats),
        'hiring_trend': hiring_by_month,
        'doc_stats': doc_stats,
        'biometric_stats': biometric_stats
    }

    return render(request, 'analytics/dashboard.html', context)


# ==========================================
# HR TOOLS AND UTILITIES
# ==========================================

def hrToolsDashboard(request):
    """Creative HR tools and utilities"""
    context = {}
    return render(request, 'hr_tools/dashboard.html', context)


def employeeDirectoryExport(request):
    """Export employee directory to CSV"""
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="employee_directory_{date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'First Name', 'Last Name', 'Department', 'Role', 'Salary', 'Bonus', 'Phone', 'Hire Date'])

    employees = Employee.objects.select_related('dept', 'role').all()
    for emp in employees:
        writer.writerow([
            emp.emp_id,
            emp.first_name,
            emp.last_name,
            emp.dept.name,
            emp.role.name,
            emp.salary,
            emp.bonus,
            emp.phone_num,
            emp.hire_date
        ])

    return response


def birthdayReminders(request):
    """View upcoming employee birthdays (requires birthdate field)"""
    # Note: This requires adding a birthdate field to Employee model
    # For now, we'll show a placeholder
    context = {
        'message': 'Birthday tracking feature coming soon! Add a birthdate field to Employee model to enable this.'
    }
    return render(request, 'hr_tools/birthday_reminders.html', context)


def salaryCalculator(request):
    """Salary calculator and comparison tool"""
    if request.method == 'POST':
        base_salary = float(request.POST.get('base_salary', 0))
        bonus = float(request.POST.get('bonus', 0))
        deductions = float(request.POST.get('deductions', 0))
        tax_rate = float(request.POST.get('tax_rate', 0)) / 100

        gross_salary = base_salary + bonus
        tax_amount = gross_salary * tax_rate
        net_salary = gross_salary - tax_amount - deductions

        context = {
            'calculated': True,
            'base_salary': base_salary,
            'bonus': bonus,
            'gross_salary': gross_salary,
            'tax_rate': tax_rate * 100,
            'tax_amount': tax_amount,
            'deductions': deductions,
            'net_salary': net_salary
        }
        return render(request, 'hr_tools/salary_calculator.html', context)

    return render(request, 'hr_tools/salary_calculator.html', {})


# About Page View
def about(request):
    """Display developer information and portfolio"""
    return render(request, 'about.html')


# Contact Page View
def contact(request):
    """Display contact information and form"""
    return render(request, 'contact.html')
