from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email обязательно для заполнения')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(
            email=email,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, phone_number=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        if not phone_number:
            raise ValueError('Для суперпользователя номер телефона обязателен')

        return self.create_user(email, password, phone_number=phone_number, **extra_fields)