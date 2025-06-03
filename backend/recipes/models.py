from django.db import models
from django.core.validators import MinValueValidator

from users.models import CustomUser
from ingredients.models import Ingredient
from .constants import (
    RECIPE_NAME_MAX_LENGTH,
    COOKING_TIME_MIN_VALUE
)


class Recipe(models.Model):
    """
    Модель для рецептов
    """
    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Название рецепта',
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание рецепта',
    )
    cooking_time = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='Время приготовления(в минутах)',
        validators=[
            MinValueValidator(
                COOKING_TIME_MIN_VALUE, message=f'Время приготовлений'
                f' не должно быть меньше {COOKING_TIME_MIN_VALUE} минуты'),
        ],
    )
    image = models.ImageField(
        upload_to='recipe_images/',
        blank=False,
        null=False,
        verbose_name='Картинка',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        null=False,
        blank=False,
        related_name='user_recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        auto_created=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    """
    Модель для связи рецептов с ингредиентами
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        null=False,
        blank=False,
    )
    amount = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_composite_pk',
            )
        ]

    def __str__(self) -> str:
        return f"{self.recipe.name}, {self.ingredient.name}, {self.amount} {self.ingredient.measurement_unit}"


class FavouriteUserRecipe(models.Model):
    """
    Модель для хранения избранных рецептов
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        blank=False,
        null=False,
        related_name='user_favs',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        blank=False,
        null=False,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_recipe_favourite_composite_pk',
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.recipe.name}"


class ShoppingCart(models.Model):
    """
    Модель для хранения списка покупок
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        blank=False,
        null=False,
        related_name='user_shops',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        blank=False,
        null=False,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_recipe_shopcart_composite_pk',
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.recipe.name}"
