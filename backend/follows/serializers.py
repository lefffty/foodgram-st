from rest_framework.serializers import (
    SerializerMethodField
)

from users.serializers import UserSerializer
from recipes.serializers import SimpleRecipeSerializer
from recipes.models import Recipe


class FollowSerializer(UserSerializer):
    """
    Сериализатор для списка подписок пользователя.
    Возвращает данные автора и его рецепты.
    """
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        ]

    def get_recipes(self, obj):
        """
        Метод, возвращающий рецепты, созданные пользователем
        """
        query_params = self.context['request'].query_params
        recipes_limit = query_params.get('recipes_limit')
        recipes = Recipe.objects.filter(
            author__username=obj.username,
        )
        if recipes_limit and isinstance(recipes_limit, str):
            try:
                recipes_limit = int(recipes_limit)
                recipes = recipes[:recipes_limit]
            except ValueError:
                pass
        serializer = SimpleRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """
        Метод, подсчитывающий количество рецептов, созданных пользователем
        """
        recipes_count = Recipe.objects.filter(
            author=obj,
        ).count()
        return recipes_count
