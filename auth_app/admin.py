from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class CustomUserChangeForm(UserChangeForm):
    """
    User change form for admin.

    Renames the first_name label to "Full name" in the admin form.
    """

    first_name = forms.CharField(label='Full name', required=False)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    """
    Custom admin for User model.

    - Displays first_name as "Full name" in the list view.
    - Renames the first_name field label to "Full name" in the edit form.
    """

    # Use custom change form to relabel first_name in admin form.
    form = CustomUserChangeForm

    # Fieldsets define sections in the user edit page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define columns to display in the user list page
    list_display = ('get_fullname', 'email', 'is_staff')

    def get_fullname(self, obj):
        # Show first_name under a clearer column label in the list view.
        return obj.first_name
    get_fullname.short_description = 'Full name'


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
