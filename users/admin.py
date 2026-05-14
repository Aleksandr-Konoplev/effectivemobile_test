from django.contrib import admin
from users.models import Permission, Role, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'is_active'
    )
    search_fields = ('email',)
    ordering = ('email',)
    fields = (
        "email",
        "password",
        "first_name",
        "middle_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "role",
        "groups",
        "user_permissions",
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'resource', 'action', 'scope', 'name')
    search_fields = ('code', 'name', 'resource', 'action', 'scope')
    list_filter = ('resource', 'action', 'scope')
    ordering = ('resource', 'action', 'scope')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)
    filter_horizontal = ('permissions',)
