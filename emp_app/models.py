from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone_num = models.IntegerField(default=0)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
   
class ccmployee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('late', 'Late'),
        ('work_from_home', 'Work From Home'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"

class Leave(models.Model):
    LEAVE_TYPES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('annual', 'Annual Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.start_date} to {self.end_date})"

    def total_days(self):
        return (self.end_date - self.start_date).days + 1