from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Serializer,
    IntegerField,
    PrimaryKeyRelatedField
)

from .models import Ingredient
from recipes.models import RecipeIngredient


class IngredientSerializer(ModelSerializer):
    """
    Сериализатор для получения списка ингредиентов и получения
    отдельного ингредиента
    """
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        read_only_fields = fields


class IngredientForRecipeSerializer(ModelSerializer):
    """
    Сериализатор для вывода ингредиентов рецепта методов "get" списка рецептов
    и вывода отдельного рецепта по его идентификатору.
    """
    amount = SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    def get_amount(self, obj):
        recipe = self.context.get('recipe')
        if RecipeIngredient.objects.filter(
            recipe=recipe,
            ingredient=obj
        ).exists():
            amount = RecipeIngredient.objects.get(
                recipe=recipe,
                ingredient=obj,
            ).amount
            return amount


class IngredientPatchSerializer(Serializer):
    """
    Сериализатор для методов "post" и "patch" вюьсета рецептов.
    """
    amount = IntegerField(required=True)
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
