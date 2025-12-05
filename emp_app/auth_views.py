"""
Authentication views for EmployeeHub
Handles login, logout, registration, and password management
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserLoginForm, UserRegistrationForm
import logging

logger = logging.getLogger(__name__)


def user_login(request):
    """Handle user login"""
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"User {username} logged in successfully")
                messages.success(request, f"Welcome back, {user.first_name or username}!")

                # Redirect to next page if specified
                next_page = request.GET.get('next', '/')
                return redirect(next_page)
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid form submission")
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
def user_logout(request):
    """Handle user logout"""
    username = request.user.username
    logout(request)
    logger.info(f"User {username} logged out")
    messages.success(request, "You have been logged out successfully")
    return redirect('login')


def user_register(request):
    """Handle user registration"""
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            logger.info(f"New user registered: {username}")

            # Automatically log in the user
            login(request, user)
            messages.success(request, f"Welcome to EmployeeHub, {user.first_name}!")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})


@login_required
def change_password(request):
    """Allow users to change their password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            logger.info(f"User {user.username} changed password")
            messages.success(request, "Your password was successfully updated!")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'auth/change_password.html', {'form': form})


@login_required
def profile(request):
    """Display user profile"""
    return render(request, 'auth/profile.html', {'user': request.user})
