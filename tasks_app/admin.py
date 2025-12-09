from django.contrib import admin

from .models import Task, Comments

# Register your models here.
admin.site.register(Task)
admin.site.register(Comments)
