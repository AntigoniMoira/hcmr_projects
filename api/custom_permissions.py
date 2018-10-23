from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    message='No from UserPermission'
    def has_permission(self, request, view):
        if request.user.is_active:
            return True
        else:
            return False