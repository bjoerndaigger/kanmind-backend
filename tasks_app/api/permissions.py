from rest_framework.permissions import BasePermission

from boards_app.models import Board


class IsBoardMember(BasePermission):
    """
    Custom permission to allow access only to members of a specific board.

    This permission checks whether the authenticated user is a member
    of the board specified in the request data.

    Usage:
    - Include 'board' field in request.data when making POST requests.
    - Returns True if the user is a member of the board, False otherwise.
    """

    def has_permission(self, request, view):
        """
        Determine if the request should be granted permission.

        Steps:
        1. Retrieve 'board' ID from request data.
        2. Return False if no board ID is provided.
        3. Attempt to fetch the board from the database.
        4. Return False if the board does not exist.
        5. Check if the requesting user is among the board's members.
        6. Return True if the user is a member, otherwise False.
        """
        board_id = request.data.get('board')

        if not board_id:
            return False

        try:
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return False

        return board.members.filter(pk=request.user.pk).exists()
