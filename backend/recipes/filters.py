from django_filters.rest_framework import (
    FilterSet,
    NumberFilter
)

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    """
    Фильтр для рецептов, которая обеспечивает фильтрацию по следующим полям:
        - автор рецепта
        - находится ли рецепт в избранном
        - находится ли рецепт в списке покупок
    """
    author = NumberFilter(field_name='author')
    is_favorited = NumberFilter(method='filter_by_is_favorited')
    is_in_shopping_cart = NumberFilter(method='filter_by_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = [
            'author',
        ]

    def filter_by_is_favorited(self, queryset, name, value):
        user = self.request.user

        if not user.is_authenticated:
            return queryset.none() if value == 1 else queryset

        if value == 1:
            return queryset.filter(favorites__user=user)
        elif value == 0:
            return queryset.exclude(favorites__user=user)

        return queryset

    def filter_by_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user

        if not user.is_authenticated:
            return queryset.none() if value == 1 else queryset

        if value == 1:
            return queryset.filter(shopping_cart__user=user)
        elif value == 0:
            return queryset.exclude(shopping_cart__user=user)

        return queryset
