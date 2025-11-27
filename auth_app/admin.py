from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    """
    Custom admin for User model.

    - Displays first name as 'Full Name' in the list view.
    - Uses default fieldsets with minimal customization.
    """

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
        # Display first name as Full Name in the admin list view
        return obj.first_name
    get_fullname.short_description = 'Full Name'


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
