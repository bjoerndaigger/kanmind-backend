from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

from boards_app.models import Board
from tasks_app.models import Task


class IsBoardMember(BasePermission):
    """
    Custom permission to allow access only to members of a board.

    Behavior:
    - POST requests: checks if the user is a member of the board specified in request.data['board']. If no 
        'board' is provided, attempts to extract 'task_id' from the URL and checks whether the user is a 
        member of the board associated with that task.
    - PATCH/DELETE/GET requests: checks if the user is a member of the board associated with the task object.

    Usage:
    - Include 'board' field in request.data when creating a new Task (POST).
    - If the API route structure passes a task_id during creation, membership is
      validated through the task’s board as fallback.
    - For updating or deleting a Task, the permission checks the board linked to the Task instance.
    - Returns True if the user is a member of the board, False otherwise.
    - Raises NotFound (404) if the board or task does not exist.
    """

    def has_permission(self, request, view):
        """
        Determines if the request should be granted permission.

        Steps for POST:
        1. Try to retrieve 'board' from request.data.
           - If provided: validate user membership in that board.
        2. If not provided:
           - Attempt to retrieve 'task_id' from the URL.
           - Validate membership via the task's associated board.
        3. If neither is found or validation fails: deny access.

        For other methods, returns True to defer to has_object_permission.
        """
        if request.method == 'POST':
            board_id = request.data.get('board')
            if board_id:
                try:
                    board = Board.objects.get(pk=board_id)
                    return board.members.filter(pk=request.user.pk).exists()
                except Board.DoesNotExist:
                    raise NotFound(detail="Board not found.")

            task_pk = view.kwargs.get('task_id')
            if task_pk:
                try:
                    task = Task.objects.get(pk=task_pk)
                    return task.board.members.filter(pk=request.user.pk).exists()
                except Task.DoesNotExist:
                    raise NotFound(detail="Task not found.")

            return False
        return True

    def has_object_permission(self, request, view, obj):
        """
        Checks object-level permission.

        Returns True if the requesting user is a member of the board
        associated with the Task object, otherwise False.
        """
        return obj.board.members.filter(pk=request.user.pk).exists()


class IsAuthor(BasePermission):
    """
    Permission class that allows access to an object only if the requesting user
    is the author of that object. This is used to restrict delete operations to 
    the author.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
