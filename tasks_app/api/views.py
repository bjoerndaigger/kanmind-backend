from django.db.models import Q
from rest_framework import generics, mixins

from tasks_app.models import Task, Comments
from .permissions import IsBoardMember, IsAuthor, IsTaskOwnerBoardMember
from .serializers import TaskSerializer, TaskReadSerializer, CommentSerializer


class TasksCreateView(generics.CreateAPIView):
    """
    Create a new task.

    - Only users who are members of the associated board can create tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]


class AssignedTasksListView(generics.ListAPIView):
    """
    List all tasks assigned to the requesting user.
    """
    serializer_class = TaskReadSerializer

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(assignee=user)


class ReviewingTasksListView(generics.ListAPIView):
    """
    List all tasks where the requesting user is assigned as reviewer.
    """
    serializer_class = TaskReadSerializer

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(reviewer=user)


class TaskUpdateDeleteView(generics.UpdateAPIView, mixins.DestroyModelMixin):
    """
    Update or delete a task.

    - Only users who are members of the task's board can update or delete.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTaskOwnerBoardMember]

    def delete(self, request, *args, **kwargs):
        # Use mixin to handle DELETE request
        return self.destroy(request, *args, **kwargs)


class CommentsListCreateView(generics.ListCreateAPIView):
    """
    List and create comments for a specific task.

    - Only board members of the task can create or view comments.
    - New comments are automatically assigned to the requesting user and task.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsTaskOwnerBoardMember]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return Comments.objects.filter(task_id=task_id).order_by('created_at')

    def perform_create(self, serializer):
        # Assign author and task when creating a comment
        serializer.save(author=self.request.user,task_id=self.kwargs.get('task_id'))


class CommentsDeleteView(generics.DestroyAPIView):
    """
    Delete a comment.

    - Only the author of the comment can delete it.
    """
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]
