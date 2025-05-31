from django.contrib import admin

from .models import CustomUser


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
