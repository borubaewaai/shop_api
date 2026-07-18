from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuth(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated)


class IsModerator(BasePermission):


    def has_permission(self, request, view):

        if request.method == 'POST':
            user = request.user
            is_moderator = bool(user and user.is_authenticated and user.is_staff)
            return not is_moderator
        return True

    def has_object_permission(self, request, view, obj):
        from rest_framework.permissions import SAFE_METHODS
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff)