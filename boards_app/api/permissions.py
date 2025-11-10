from rest_framework.permissions import BasePermission


class IsOwnerOrMember(BasePermission):
    """
    Permission class to allow access to a Board object only if the user has the appropriate role:

    - For DELETE requests: only the owner of the board is allowed to delete it.
    - For other requests (GET, PUT, PATCH): the user is allowed if they are either the owner or a member of the board.

    This is necessary because models have an `owner` ForeignKey and a `members` ManyToManyField.
    """

    def has_object_permission(self, request, view, obj):
        is_owner = (request.user == obj.owner)
        user_id = request.user.id
        is_member = obj.members.filter(id=user_id).exists()

        if request.method == 'DELETE':
            return is_owner
        else:
            return is_owner or is_member
