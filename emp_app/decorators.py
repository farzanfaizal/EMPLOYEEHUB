"""
Custom decorators for role-based access control
Professional implementation for EmployeeHub
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


def role_required(*roles):
    """
    Decorator to check if user has one of the required roles
    Usage: @role_required('HR_MANAGER', 'SUPER_ADMIN')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                logger.warning(
                    f"User {request.user.username} attempted to access {view_func.__name__} "
                    f"without required role. User role: {request.user.role}, Required: {roles}"
                )
                messages.error(request, "You don't have permission to access this page.")
                raise PermissionDenied
        return _wrapped_view
    return decorator


def hr_required(view_func):
    """
    Decorator to require HR Manager or Super Admin role
    Usage: @hr_required
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_hr_manager():
            return view_func(request, *args, **kwargs)
        else:
            logger.warning(
                f"User {request.user.username} attempted to access HR-only function {view_func.__name__}"
            )
            messages.error(request, "This action requires HR Manager privileges.")
            raise PermissionDenied
    return _wrapped_view


def manager_required(view_func):
    """
    Decorator to require Department Manager, HR Manager, or Super Admin role
    Usage: @manager_required
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_dept_manager():
            return view_func(request, *args, **kwargs)
        else:
            logger.warning(
                f"User {request.user.username} attempted to access manager-only function {view_func.__name__}"
            )
            messages.error(request, "This action requires Manager privileges.")
            raise PermissionDenied
    return _wrapped_view


def super_admin_required(view_func):
    """
    Decorator to require Super Admin role
    Usage: @super_admin_required
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_super_admin():
            return view_func(request, *args, **kwargs)
        else:
            logger.warning(
                f"User {request.user.username} attempted to access admin-only function {view_func.__name__}"
            )
            messages.error(request, "This action requires Super Admin privileges.")
            raise PermissionDenied
    return _wrapped_view


def log_activity(action_name):
    """
    Decorator to log user activity
    Usage: @log_activity("Viewed Employee List")
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Execute the view
            response = view_func(request, *args, **kwargs)

            # Log the activity
            if request.user.is_authenticated:
                from .models import UserActivity
                try:
                    UserActivity.objects.create(
                        user=request.user,
                        action=action_name,
                        description=f"Accessed {view_func.__name__}",
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
                    )
                except Exception as e:
                    logger.error(f"Failed to log activity: {e}")

            return response
        return _wrapped_view
    return decorator


def get_client_ip(request):
    """Helper function to get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ajax_required(view_func):
    """
    Decorator to ensure the request is AJAX
    Usage: @ajax_required
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "This action can only be performed via AJAX")
            return redirect('index')
    return _wrapped_view
