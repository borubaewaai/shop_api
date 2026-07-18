from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    birthdate = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    is_active = models.BooleanField(default=False)  # неактивен, пока не подтвердит код
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    registration_source = models.CharField(max_length=20, default='local', verbose_name='Источник регистрации')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if self.is_superuser and not self.phone_number:
            raise ValidationError({'phone_number': 'Номер телефона обязателен для суперпользователя'})


class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Код подтверждения для {self.user.email}'