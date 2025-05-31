from django.contrib import admin

from .models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Админка для модели подписок
    """
    list_display = [
        'user', 'following',
    ]
