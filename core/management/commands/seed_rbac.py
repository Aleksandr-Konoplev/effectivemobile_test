from django.core.management.base import BaseCommand

from users.models import Permission, Role


class Command(BaseCommand):
    help = 'Создаёт базовые роли и права RBAC'

    def handle(self, *args, **options):
        permissions_data = [
            {
                'code': 'product.read.any',
                'resource': Permission.RESOURCE_PRODUCT,
                'action': Permission.ACTION_READ,
                'scope': Permission.SCOPE_ANY,
                'name': 'Чтение любых продуктов',
            },
            {
                'code': 'product.create.any',
                'resource': Permission.RESOURCE_PRODUCT,
                'action': Permission.ACTION_CREATE,
                'scope': Permission.SCOPE_ANY,
                'name': 'Создание продуктов',
            },
            {
                'code': 'product.update.any',
                'resource': Permission.RESOURCE_PRODUCT,
                'action': Permission.ACTION_UPDATE,
                'scope': Permission.SCOPE_ANY,
                'name': 'Обновление любых продуктов',
            },
            {
                'code': 'product.delete.any',
                'resource': Permission.RESOURCE_PRODUCT,
                'action': Permission.ACTION_DELETE,
                'scope': Permission.SCOPE_ANY,
                'name': 'Удаление любых продуктов',
            },
            {
                'code': 'product.update.own',
                'resource': Permission.RESOURCE_PRODUCT,
                'action': Permission.ACTION_UPDATE,
                'scope': Permission.SCOPE_OWN,
                'name': 'Обновление своих продуктов',
            },
            {
                'code': 'product.delete.own',
                'resource': Permission.RESOURCE_PRODUCT,
                'action': Permission.ACTION_DELETE,
                'scope': Permission.SCOPE_OWN,
                'name': 'Удаление своих продуктов',
            },
        ]

        created_permissions = 0
        for permission_data in permissions_data:
            _, created = Permission.objects.update_or_create(
                code=permission_data['code'],
                defaults=permission_data,
            )
            if created:
                created_permissions += 1

        roles_data = [
            {'code': Role.ADMIN, 'name': 'Администратор'},
            {'code': Role.MANAGER, 'name': 'Менеджер'},
            {'code': Role.USER, 'name': 'Пользователь'},
            {'code': Role.GUEST, 'name': 'Гость'},
        ]

        created_roles = 0
        for role_data in roles_data:
            _, created = Role.objects.update_or_create(
                code=role_data['code'],
                defaults=role_data,
            )
            if created:
                created_roles += 1

        role_permissions_map = {
            Role.ADMIN: [
                'product.read.any',
                'product.create.any',
                'product.update.any',
                'product.delete.any',
            ],
            Role.MANAGER: [
                'product.read.any',
                'product.create.any',
                'product.update.any',
            ],
            Role.USER: [
                'product.read.any',
                'product.create.any',
                'product.update.own',
                'product.delete.own',
            ],
            Role.GUEST: [
                'product.read.any',
            ],
        }

        for role_code, permission_codes in role_permissions_map.items():
            role = Role.objects.get(code=role_code)
            permissions = Permission.objects.filter(code__in=permission_codes)
            role.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f'RBAC заполнен: roles created={created_roles}, permissions created={created_permissions}'
            )
        )
