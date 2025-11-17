from django.db.models import Q
from rest_framework import generics, mixins

from tasks_app.models import Task
from .permissions import IsBoardMember
from .serializers import TaskSerializer, TaskReadSerializer


class TasksCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]


class AssignedTasksListView(generics.ListAPIView):
    serializer_class = TaskReadSerializer

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(assignee=user)


class ReviewingTasksListView(generics.ListAPIView):
    serializer_class = TaskReadSerializer

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(reviewer=user)


class TaskUpdateDeleteView(generics.UpdateAPIView, mixins.DestroyModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
