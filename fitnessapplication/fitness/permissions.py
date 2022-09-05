from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "You do not have permission to preform this action"
    
    def has_object_permission(self, request, view, obj):
        return obj.trainee.user == request.user
    


class IsProfileOwner(BasePermission):
    message = "You do not have permission to preform this action"
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user