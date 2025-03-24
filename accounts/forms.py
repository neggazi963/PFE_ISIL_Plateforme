
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email Address')}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Full Name')}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Country')}))
    institution = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Institution')}))
    is_researcher = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_developer = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirm Password')}))

    class Meta:
        model = User
        fields = ('email', 'full_name', 'institution', 'country', 'is_researcher', 'is_developer',  'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    """Form for user profile update."""
    class Meta:
        model = User
        fields = ('email', 'full_name', 'institution', 'is_researcher', 'is_developer')


class CustomAuthenticationForm(AuthenticationForm):
    """Form for user login."""
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email Address')}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}))


class CustomPasswordResetForm(PasswordResetForm):
    """Form for password reset."""
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email Address')}))


class CustomSetPasswordForm(SetPasswordForm):
    """Form for setting a new password."""
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('New Password')}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirm New Password')}))




