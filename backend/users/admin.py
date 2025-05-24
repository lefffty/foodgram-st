from django.contrib import admin

from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Админка для модели пользователя
    """
    list_filter = [
        'username', 'first_name', 'last_name', 'email',
    ]
    list_display = [
        'id', 'username', 'first_name', 'last_name', 'email',
    ]
    search_fields = [
        'email', 'username'
    ]
    ordering = [
        'first_name', 'last_name',
    ]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Админка для модели подписок
    """
    list_display = [
        'user', 'following',
    ]
