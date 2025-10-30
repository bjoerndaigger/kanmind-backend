from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    """
    Custom Django admin configuration for the User model.

    This class customizes the User admin interface by:
        - Organizing fields into meaningful sections (fieldsets)
        - Displaying the user's full name and email in the user list
        - Providing a custom method to display the full name
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
        """
        Custom method to display the user's full name in the admin list view.

        Args:
            obj (User): User instance

        Returns:
            str: First name of the user
        """
        return obj.first_name
    # Provide a readable label for the admin column
    get_fullname.short_description = 'Full Name'


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
