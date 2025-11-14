from rest_framework import generics

from tasks_app.models import Task
from .permissions import IsBoardMember
from .serializers import TaskSerializer


class TasksCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]
