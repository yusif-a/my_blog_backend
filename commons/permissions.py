from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsSuperuser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


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


class IsCreatorOrAnyoneCanCreateOrReadOnly(BasePermission):
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


class IsCreatorOrReadOnly(BasePermission):
    """
    Only the authenticated creator can modify.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user
