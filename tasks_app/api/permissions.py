from rest_framework.permissions import BasePermission

from boards_app.models import Board


class IsBoardMember(BasePermission):
    """
    Custom permission to allow access only to members of a board.

    Behavior:
    - POST requests: checks if the user is a member of the board specified in request.data['board'].
    - PATCH/DELETE/GET requests: checks if the user is a member of the board associated with the task object.
    
    Usage:
    - Include 'board' field in request.data when creating a new Task (POST).
    - For updating or deleting a Task, the permission checks the board linked to the Task instance.
    - Returns True if the user is a member of the board, False otherwise.
    """

    def has_permission(self, request, view):
        """
        Determines if the request should be granted permission.

        Steps for POST:
        1. Retrieve 'board' ID from request data.
        2. Return False if no board ID is provided.
        3. Attempt to fetch the board from the database.
        4. Return False if the board does not exist.
        5. Return True if the requesting user is a member of the board, otherwise False.

        For other methods, returns True to defer to has_object_permission.
        """
        if request.method == 'POST':
            board_id = request.data.get('board')

            if not board_id:
                return False

            try:
                board = Board.objects.get(pk=board_id)
            except Board.DoesNotExist:
                return False

            return board.members.filter(pk=request.user.pk).exists()
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Checks object-level permission.

        Returns True if the requesting user is a member of the board
        associated with the Task object, otherwise False.
        """
        return obj.board.members.filter(pk=request.user.pk).exists()
