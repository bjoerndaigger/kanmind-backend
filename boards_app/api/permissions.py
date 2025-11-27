from rest_framework.permissions import BasePermission


class IsOwnerOrMember(BasePermission):
    """
    Grants access to a Board object if the user is the owner or a member.

    - DELETE: only the owner can delete.
    - GET, PUT, PATCH: owner or member can access.
    """
    def has_object_permission(self, request, view, obj):
        is_owner = (request.user == obj.owner)
        user_id = request.user.id
        is_member = obj.members.filter(id=user_id).exists()

        if request.method == 'DELETE':
            return is_owner
        else:
            return is_owner or is_member
