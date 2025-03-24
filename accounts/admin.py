from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """Custom admin for the User model."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'full_name', 'institution', 'is_researcher', 'is_developer', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_researcher', 'is_developer', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'institution', 'biography', 'research_interests')}),
        (_('User type'), {'fields': ('is_researcher', 'is_developer')}),
        (_('Permissions'), {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_researcher', 'is_developer', 'is_verified', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'full_name', 'institution')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)

# Register your models here.
