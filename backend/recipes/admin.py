from django.contrib import admin

from .models import (
    FavouriteUserRecipe,
    RecipeIngredient,
    ShoppingCart,
    Recipe,
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Админка для модели рецепта
    """
    search_fields = [
        'author', 'name'
    ]
    list_display = [
        'id', 'name', 'pub_date',
    ]
    fields = (
        'name', 'text', 'cooking_time',
        'image', 'author', 'favourite_counter',
        'pub_date',
    )
    readonly_fields = (
        'favourite_counter', 'pub_date'
    )
    inlines = [RecipeIngredientInline]

    def favourite_counter(self, obj) -> int:
        return FavouriteUserRecipe.objects.filter(
            recipe=obj
        ).count()

    favourite_counter.short_description = 'Общее число добавлений в избранное'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """
    Админка для ингредиентов рецепта
    """
    fields = ['recipe', 'ingredient']
    list_display = [
        'get_recipe_name', 'get_ingredient_name',
        'get_ingredient_mu', 'get_amount',
    ]

    def get_recipe_name(self, obj):
        return obj.recipe.name
    get_recipe_name.short_description = 'Название рецепта'

    def get_ingredient_name(self, obj):
        return obj.ingredient.name
    get_ingredient_name.short_description = 'Название ингредиента'

    def get_ingredient_mu(self, obj):
        return obj.ingredient.measurement_unit
    get_ingredient_mu.short_description = 'Единица измерения ингредиента'

    def get_amount(self, obj):
        return obj.amount
    get_amount.short_description = 'Количество ингредиента'


@admin.register(FavouriteUserRecipe)
class FavouriteUserRecipeAdmin(admin.ModelAdmin):
    """
    Админка для модели избранных рецептов пользователей
    """
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Админка для модели списка покупок пользователей
    """
    pass
