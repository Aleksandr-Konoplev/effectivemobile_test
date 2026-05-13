from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = 'Вы можете взаимодействовать только со своими объектами'

    def has_object_permission(self, request, view, obj):
        return obj == request.user