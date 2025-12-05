"""
Django Signals for EmployeeHub
Auto-setup and user management
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .user_models import CustomUser
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def setup_new_user(sender, instance, created, **kwargs):
    """
    Auto-setup for new users:
    1. First user becomes Super Admin
    2. All other users become HR Managers by default
    """
    if created:
        # Check if this is the first user
        user_count = CustomUser.objects.count()

        if user_count == 1:
            # First user = Super Admin (for initial setup)
            instance.role = CustomUser.UserRole.SUPER_ADMIN
            instance.is_staff = True
            instance.is_superuser = True
            instance.save(update_fields=['role', 'is_staff', 'is_superuser'])
            logger.info(f"🎉 First user created: {instance.username} - Auto-promoted to SUPER_ADMIN")

        elif not instance.role or instance.role == CustomUser.UserRole.EMPLOYEE:
            # All new signups = HR Manager (this is an HR management tool)
            instance.role = getattr(
                settings,
                'DEFAULT_USER_ROLE',
                CustomUser.UserRole.HR_MANAGER
            )
            instance.save(update_fields=['role'])
            logger.info(f"✅ New HR user created: {instance.username} - Role: {instance.role}")


@receiver(post_save, sender=CustomUser)
def log_user_creation(sender, instance, created, **kwargs):
    """Log user creation for audit purposes"""
    if created:
        from .user_models import UserActivity
        try:
            UserActivity.objects.create(
                user=instance,
                action="User Account Created",
                description=f"New user {instance.username} registered with role {instance.get_role_display()}"
            )
        except Exception as e:
            logger.error(f"Failed to log user creation: {e}")
