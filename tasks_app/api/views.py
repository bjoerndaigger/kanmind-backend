from django.db.models import Q
from rest_framework import generics

from tasks_app.models import Task
from .permissions import IsBoardMember
from .serializers import TaskSerializer, AssignedTaskSerializer


class TasksCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]


class AssignedToMeTaskListView(generics.ListAPIView):
    serializer_class = AssignedTaskSerializer

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(Q(assignee=user) | Q(reviewer=user)).distinct()