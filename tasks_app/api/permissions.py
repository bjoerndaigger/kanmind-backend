from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission

from boards_app.models import Board
from tasks_app.models import Task


class IsBoardMember(BasePermission):
    """
    Grants permission for POST requests only if the user is a member
    of the board specified in the request data.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            board_id = request.data.get('board')
            if not board_id:
                # No board specified, allow by default
                # Validation is handled by the TaskSerializer
                return True
            try:
                board = Board.objects.get(pk=board_id)
                return board.members.filter(pk=request.user.pk).exists()
            except Board.DoesNotExist:
                raise NotFound(detail="Board not found.")
        return True


class IsTaskOwnerBoardMember(BasePermission):
    """
    Grants permission if the user is a member of the board associated
    with the task. Used for task-level access control.
    """
    def has_permission(self, request, view):
        task_pk = view.kwargs.get('task_id')
        if task_pk:
            try:
                task = Task.objects.get(pk=task_pk)
                return task.board.members.filter(pk=request.user.pk).exists()
            except Task.DoesNotExist:
                raise NotFound(detail="Task not found.")
        return True

    def has_object_permission(self, request, view, obj):
        # Object-level check: user must be a member of the task's board
        return obj.board.members.filter(pk=request.user.pk).exists()


class IsAuthor(BasePermission):
    """
    Permission class that allows access to an object only if the requesting user
    is the author of that object. This is used to restrict delete operations to 
    the author.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
