from django.urls import path

from .views import TasksCreateView

urlpatterns = [
    path('', TasksCreateView.as_view(), name="tasks_create")
]