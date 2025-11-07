from rest_framework.permissions import BasePermission


class IsOwnerOrMember(BasePermission):
    """
    Permission class to allow access only if the user is either the owner of the object
    or a member of the object's members list.


    This is necessary because models have an `owner` ForeignKey and a `members` ManyToManyField.
    """
    def has_object_permission(self, request, view, obj):
        is_owner = (request.user == obj.owner)
        user_id = request.user.id
        is_member = obj.members.filter(id=user_id).exists()

        return is_owner or is_member
