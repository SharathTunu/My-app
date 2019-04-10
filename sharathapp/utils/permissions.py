from rest_framework import permissions
from rest_framework.compat import is_authenticated


class GenerateOfferPermission(permissions.BasePermission):
    """
    Handles the permissions to the offers generator
    """

    def has_permission(self, request, view):
        if not is_authenticated(request.user):
            return False

        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only authenticated user can read proposals and edit own proposals.
    """

    def has_permission(self, request, view):
        return is_authenticated(request.user)

    def has_object_permission(self, request, view, obj):
        return (
            (
                request.method in permissions.SAFE_METHODS or
                request.user.id== obj.user_id)  and
            is_authenticated(request.user)
        )


class BasicPermission(permissions.BasePermission):
    """
    Only authenticated user can read proposals and edit own proposals.
    """

    def has_permission(self, request, view):
        return is_authenticated(request.user)