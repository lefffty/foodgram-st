from django.db import models
from django.contrib.auth.models import AbstractUser


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
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
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
        max_length=150,
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


class Follow(models.Model):
    """
    Модель для хранения подписок пользователя
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f"{self.user.username} подписан на {self.following.username}"
