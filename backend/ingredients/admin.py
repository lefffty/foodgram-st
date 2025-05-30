from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Админка для модели ингредиентов
    """
    list_display = [
        'id', 'name', 'measurement_unit',
    ]
    search_fields = [
        'name'
    ]
