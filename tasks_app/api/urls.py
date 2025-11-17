from django.urls import path

from .views import TasksCreateView, AssignedTasksListView, ReviewingTasksListView

urlpatterns = [
    path('', TasksCreateView.as_view(), name="tasks_create"),
    path('assigned-to-me/', AssignedTasksListView.as_view(), name="tasks-assigned"),
    path('reviewing/', ReviewingTasksListView.as_view(), name="tasks-reviewing")
]
