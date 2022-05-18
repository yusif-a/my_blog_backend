from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuserCreatorOrReadOnly(BasePermission):
    """
    Custom permission to only allow superusers to create, and edit their own created objects.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsCreatorOrReadOnly(BasePermission):
    """
    Anyone can create, but only the authenticated creator can modify.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.method == 'POST' or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user
