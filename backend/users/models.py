from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import (
    USER_FIRST_NAME_MAX_LENGTH,
    USER_LAST_NAME_MAX_LENGTH,
    USER_USERNAME_MAX_LENGTH
)


class CustomUser(AbstractUser):
    """
    Модель пользователя
    """
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        blank=False,
        null=False,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_FIRST_NAME_MAX_LENGTH,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_LAST_NAME_MAX_LENGTH,
        blank=False,
        null=False,
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        null=True,
        blank=True,
        upload_to='avatars/',
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        null=False,
        blank=False,
        max_length=USER_USERNAME_MAX_LENGTH,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self) -> str:
        return self.username
