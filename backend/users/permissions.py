from rest_framework import permissions


class IsCurrentUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user == obj.author


class IsCurrentUserOrSAFEMETHODS(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
