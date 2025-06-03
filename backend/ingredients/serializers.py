from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    Serializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
)

from .models import Ingredient
from .constants import INGREDIENT_MIN_VALUE
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
    id = ReadOnlyField(
        source='ingredient.id'
    )
    name = ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit',
    )
    amount = IntegerField(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientPatchSerializer(Serializer):
    """
    Сериализатор для методов "post" и "patch" вюьсета рецептов.
    """
    amount = IntegerField(
        min_value=INGREDIENT_MIN_VALUE,
        error_messages={
            'min_value': f'Количество не может '
            f'быть меньше {INGREDIENT_MIN_VALUE}'
        }
    )
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    def to_internal_value(self, data):
        """
        Переопределяем метод "to_internal_value"
        """
        ret = super().to_internal_value(data)
        return {
            'ingredient': ret['id'],
            'amount': ret['amount']
        }
