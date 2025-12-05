# Generated manually for CustomUser model migration

from django.conf import settings
from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('emp_app', '0005_alter_employee_phone_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('SUPER_ADMIN', 'Super Administrator'), ('HR_MANAGER', 'HR Manager'), ('DEPT_MANAGER', 'Department Manager'), ('EMPLOYEE', 'Employee')], default='EMPLOYEE', help_text="User's role in the system", max_length=20)),
                ('phone_number', models.CharField(blank=True, help_text='Contact phone number', max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('profile_picture', models.ImageField(blank=True, help_text='User profile picture', null=True, upload_to='profile_pictures/')),
                ('date_of_birth', models.DateField(blank=True, help_text='Date of birth', null=True)),
                ('address', models.TextField(blank=True, help_text='Home address')),
                ('emergency_contact', models.CharField(blank=True, help_text='Emergency contact name', max_length=100)),
                ('emergency_phone', models.CharField(blank=True, help_text='Emergency contact phone', max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('google_id', models.CharField(blank=True, help_text='Google OAuth ID', max_length=255, null=True, unique=True)),
                ('email_notifications', models.BooleanField(default=True, help_text='Receive email notifications')),
                ('theme_preference', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')], default='light', help_text='UI theme preference', max_length=10)),
                ('is_verified', models.BooleanField(default=False, help_text='Email verified')),
                ('last_login_ip', models.GenericIPAddressField(blank=True, help_text='Last login IP address', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.OneToOneField(blank=True, help_text='Linked employee record', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_account', to='emp_app.employee')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['-date_joined'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('success', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Login Attempt',
                'verbose_name_plural': 'Login Attempts',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(help_text='Action performed', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Detailed description')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, help_text='Browser user agent')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Activity',
                'verbose_name_plural': 'User Activities',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['role'], name='emp_app_cus_role_1b2c3d_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['email'], name='emp_app_cus_email_4e5f6a_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['google_id'], name='emp_app_cus_google__7b8c9d_idx'),
        ),
        migrations.AddIndex(
            model_name='loginattempt',
            index=models.Index(fields=['username', '-timestamp'], name='emp_app_log_usernam_0a1b2c_idx'),
        ),
        migrations.AddIndex(
            model_name='loginattempt',
            index=models.Index(fields=['ip_address', '-timestamp'], name='emp_app_log_ip_addr_3d4e5f_idx'),
        ),
        migrations.AddIndex(
            model_name='useractivity',
            index=models.Index(fields=['user', '-timestamp'], name='emp_app_use_user_id_6g7h8i_idx'),
        ),
        migrations.AddIndex(
            model_name='useractivity',
            index=models.Index(fields=['action'], name='emp_app_use_action_9j0k1l_idx'),
        ),
    ]
