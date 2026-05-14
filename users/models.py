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


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email} - {self.last_name} {self.first_name}'
