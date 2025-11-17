from django.urls import path

from .views import TasksCreateView, AssignedToMeTaskListView

urlpatterns = [
    path('', TasksCreateView.as_view(), name="tasks_create"),
    path('assigned-to-me/', AssignedToMeTaskListView.as_view(), name="assigned_to_me" )
]