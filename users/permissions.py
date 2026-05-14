from rest_framework.permissions import BasePermission

from users.models import Role


class IsOwner(BasePermission):
    message = 'Вы можете взаимодействовать только со своими объектами'

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class HasUserAccessPermission(BasePermission):
    message = 'Недостаточно прав для взаимодействия с пользователями'

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        role = getattr(user, 'role', None)
        if role is None:
            return False

        if role.code == Role.ADMIN:
            return True

        if role.code == Role.MANAGER:
            return request.method in ('GET', 'HEAD', 'OPTIONS')

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        role = getattr(user, 'role', None)
        if role is None:
            return False

        if role.code == Role.ADMIN:
            return True

        if role.code == Role.MANAGER:
            return request.method in ('GET', 'HEAD', 'OPTIONS')

        return obj.id == user.id
