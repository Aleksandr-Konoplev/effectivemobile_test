from rest_framework.permissions import BasePermission


class IsProductOwnerOrReadOnly(BasePermission):
    message = 'Вы можете изменять только свои продукты'

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS', ):
            return True

        return obj.owner == request.user
