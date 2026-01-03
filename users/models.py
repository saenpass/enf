from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.html import strip_tags


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле Email обязательно для заполнения.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Email'
    )

    fist_name = models.CharField(  # не переименовываем, чтобы не ломать БД
        max_length=50,
        verbose_name='Имя'
    )

    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )

    company = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Компания'
    )

    address1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Адрес (строка 1)'
    )

    address2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Адрес (строка 2)'
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Город'
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Страна'
    )

    province = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Регион / область'
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Почтовый индекс'
    )

    phone = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Телефон'
    )

    username = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def clean(self):
        for field in [
            'company', 'address1', 'address2',
            'city', 'country', 'province',
            'postal_code', 'phone'
        ]:
            value = getattr(self, field)
            if value:
                setattr(self, field, strip_tags(value))



