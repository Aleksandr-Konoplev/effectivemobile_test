from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email обязательное поле')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class Permission(models.Model):
    RESOURCE_PRODUCT = 'product'

    ACTION_READ = 'read'
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    SCOPE_ANY = 'any'
    SCOPE_OWN = 'own'

    RESOURCE_CHOICES = (
        (RESOURCE_PRODUCT, 'Продукт'),
    )

    ACTION_CHOICES = (
        (ACTION_READ, 'Чтение'),
        (ACTION_CREATE, 'Создание'),
        (ACTION_UPDATE, 'Обновление'),
        (ACTION_DELETE, 'Удаление'),
    )

    SCOPE_CHOICES = (
        (SCOPE_ANY, 'Любой'),
        (SCOPE_OWN, 'Свой'),
    )

    code = models.CharField(max_length=100, unique=True)
    resource = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Право'
        verbose_name_plural = 'Права'
        constraints = [
            models.UniqueConstraint(
                fields=('resource', 'action', 'scope'),
                name='unique_permission_resource_action_scope'
            )
        ]

    def __str__(self):
        return f'{self.code} ({self.name})'


class Role(models.Model):
    ADMIN = 'admin'
    MANAGER = 'manager'
    USER = 'user'
    GUEST = 'guest'

    ROLE_CHOICES = (
        (ADMIN, 'Админ'),
        (MANAGER, 'Менеджер'),
        (USER, 'Пользователь'),
        (GUEST, 'Гость'),
    )

    code = models.CharField(max_length=20, unique=True, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return f'{self.name} ({self.code})'


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='users',
        blank=True,
        null=True,
        verbose_name='Роль'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email} - {self.last_name} {self.first_name}'
