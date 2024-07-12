from rest_framework.permissions import BasePermission


class TodoPermesion(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id