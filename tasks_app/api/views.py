from django.db.models import Q
from rest_framework import generics, mixins

from tasks_app.models import Task, Comments
from .permissions import IsBoardMember
from .serializers import TaskSerializer, TaskReadSerializer, CommentSerializer


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


class CommentsListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsBoardMember]

    def get_queryset(self):
        task_id = self.kwargs.get('pk')
        return Comments.objects.filter(task_id=task_id).order_by('created_at')

    def perform_create(self, serializer):
        user = self.request.user
        task_id = self.kwargs.get('pk')
        serializer.save(author=user, task_id=task_id)
