from django.urls import path

from .views import TasksCreateView, AssignedTasksListView, ReviewingTasksListView, TaskUpdateDeleteView, CommentsListCreateView

urlpatterns = [
    path('', TasksCreateView.as_view(), name="tasks_create"),
    path('assigned-to-me/', AssignedTasksListView.as_view(), name="tasks_assigned"),
    path('reviewing/', ReviewingTasksListView.as_view(), name="tasks_reviewing"),
    path('<int:pk>/', TaskUpdateDeleteView.as_view(), name="tasks_update_delete"),
    path('<int:pk>/comments/', CommentsListCreateView.as_view(), name="comments")
]
