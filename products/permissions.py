from rest_framework.permissions import BasePermission

from users.models import Permission as RolePermission, Role


class HasProductPermission(BasePermission):
    message = 'Недостаточно прав для выполнения действия'

    method_action_map = {
        'GET': RolePermission.ACTION_READ,
        'HEAD': RolePermission.ACTION_READ,
        'OPTIONS': RolePermission.ACTION_READ,
        'POST': RolePermission.ACTION_CREATE,
        'PUT': RolePermission.ACTION_UPDATE,
        'PATCH': RolePermission.ACTION_UPDATE,
        'DELETE': RolePermission.ACTION_DELETE,
    }

    def _get_action(self, request):
        return self.method_action_map.get(request.method)

    @staticmethod
    def _has_permission(role, action, scope):
        if role is None:
            return False

        return role.permissions.filter(
            resource=RolePermission.RESOURCE_PRODUCT,
            action=action,
            scope=scope,
        ).exists()

    def has_permission(self, request, view):
        action = self._get_action(request)
        if action is None:
            return False

        if not request.user.is_authenticated:
            if action != RolePermission.ACTION_READ:
                return False
            role = Role.objects.filter(code=Role.GUEST).first()
            return self._has_permission(role, action, RolePermission.SCOPE_ANY)

        role = getattr(request.user, 'role', None)
        return self._has_permission(role, action, RolePermission.SCOPE_ANY) or self._has_permission(
            role,
            action,
            RolePermission.SCOPE_OWN,
        )

    def has_object_permission(self, request, view, obj):
        action = self._get_action(request)
        if action is None:
            return False

        if action == RolePermission.ACTION_READ:
            return True

        if not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)

        if self._has_permission(role, action, RolePermission.SCOPE_ANY):
            return True

        if self._has_permission(role, action, RolePermission.SCOPE_OWN):
            return obj.owner_id == request.user.id

        return False
