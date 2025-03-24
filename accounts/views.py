from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from .forms import (
    CustomUserCreationForm, 
    CustomUserChangeForm, 
    CustomAuthenticationForm, 
    CustomPasswordResetForm, 
    CustomSetPasswordForm
)
from .models import User


def register(request):
    """View for user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False  # User needs to verify email
            user.save()
            
            # Send verification email
            current_site = get_current_site(request)
            subject = _('Verify Your Email Address')
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            messages.success(request, _('Registration successful. Please check your email to verify your account.'))
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, uidb64, token):
    """View for email verification."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, _('Email verification successful. You can now log in.'))
        return redirect('accounts:login')
    else:
        messages.error(request, _('Verification link is invalid or has expired.'))
        return redirect('accounts:login')


def login_view(request):
    """View for user login."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    messages.success(request, _('You have been successfully logged in.'))
                    return redirect('home')  # Redirect to home page
                else:
                    messages.error(request, _('Please verify your email before logging in.'))
            else:
                messages.error(request, _('Invalid email or password.'))
        else:
            messages.error(request, _('Invalid email or password.'))
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """View for user logout."""
    logout(request)
    messages.success(request, _('You have been successfully logged out.'))
    return redirect('home')  # Redirect to home page


@login_required
def profile_view(request):
    """View for user profile."""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    """View for editing user profile."""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been successfully updated.'))
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def password_change(request):
    """View for changing password."""
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Your password has been successfully updated.'))
            return redirect('accounts:profile')
    else:
        form = CustomSetPasswordForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


def password_reset_request(request):
    """View for password reset request."""
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = _('Password Reset Requested')
                    current_site = get_current_site(request)
                    message = render_to_string('accounts/password_reset_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    try:
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                messages.success(request, _('Password reset instructions have been sent to your email.'))
                return redirect('accounts:password_reset_done')
            else:
                messages.error(request, _('Email not found in our database.'))
    else:
        form = CustomPasswordResetForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    """View for confirming password reset."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _('Your password has been reset. You can now log in with your new password.'))
                return redirect('accounts:login')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, _('Password reset link is invalid or has expired.'))
        return redirect('accounts:password_reset_request')
