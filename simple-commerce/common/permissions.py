from rest_framework.permissions import BasePermission


class IsSelfOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.pk == request.user.pk


class IsUsersOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        owner = getattr(obj, "user", None)
        return owner == request.user
