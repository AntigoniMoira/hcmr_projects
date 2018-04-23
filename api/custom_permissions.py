from rest_framework import permissions

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return False