from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not view.action == 'list':
            if not request.user.user_type == 1:
                return False
        return True


class IsAlbumAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            if not request.user == obj.created_by:
                return False
        return True
