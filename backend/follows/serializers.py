from rest_framework.serializers import (
    SerializerMethodField,
    IntegerField
)
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer
from recipes.serializers import SimpleRecipeSerializer

User = get_user_model()


class FollowSerializer(UserSerializer):
    """
    Сериализатор для списка подписок пользователя.
    Возвращает данные автора и его рецепты.
    """
    recipes = SerializerMethodField()
    recipes_count = IntegerField(source='user_recipes.count')

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
        recipes = obj.user_recipes.all()
        if recipes_limit and recipes_limit.isdigit():
            recipes_limit = int(recipes_limit)
            recipes = recipes[:recipes_limit]
        serializer = SimpleRecipeSerializer(recipes, many=True)
        return serializer.data
