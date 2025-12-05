"""
Account management views - Professional Implementation
User profile, settings, password change, activity logs
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import log_activity
import logging

logger = logging.getLogger(__name__)


@login_required
@log_activity("Viewed Profile")
def profile(request):
    """User profile page with recent activity"""
    try:
        recent_activities = request.user.activities.all()[:10]
    except:
        recent_activities = []

    context = {
        'user': request.user,
        'recent_activities': recent_activities
    }
    return render(request, 'account/profile.html', context)


@login_required
@log_activity("Updated Profile")
def update_profile(request):
    """Update user profile information"""
    if request.method == 'POST':
        user = request.user

        # Update fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.address = request.POST.get('address', '')
        user.emergency_contact = request.POST.get('emergency_contact', '')
        user.emergency_phone = request.POST.get('emergency_phone', '')

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        try:
            user.save()
            messages.success(request, "Profile updated successfully!")
            logger.info(f"User {user.username} updated their profile")
        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
            logger.error(f"Profile update failed for {user.username}: {e}")

        return redirect('profile')

    return redirect('profile')


@login_required
@log_activity("Changed Password")
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password was successfully updated!")
            logger.info(f"User {user.username} changed password")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/change_password.html', {'form': form})


@login_required
@log_activity("Updated Settings")
def settings(request):
    """User settings page"""
    if request.method == 'POST':
        user = request.user
        user.email_notifications = request.POST.get('email_notifications') == 'on'
        user.theme_preference = request.POST.get('theme_preference', 'light')

        try:
            user.save()
            messages.success(request, "Settings updated successfully!")
            logger.info(f"User {user.username} updated settings")
        except Exception as e:
            messages.error(request, f"Error updating settings: {str(e)}")
            logger.error(f"Settings update failed for {user.username}: {e}")

        return redirect('settings')

    return render(request, 'account/settings.html', {'user': request.user})


@login_required
def activity_log(request):
    """View user activity log"""
    try:
        activities = request.user.activities.all()[:50]
    except:
        activities = []

    return render(request, 'account/activity_log.html', {'activities': activities})
