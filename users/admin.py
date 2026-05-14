from django.contrib import admin
from users.models import User


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
        "groups",
        "user_permissions",
    )
