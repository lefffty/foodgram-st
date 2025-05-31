from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    Serializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    ValidationError
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
    amount = IntegerField(required=True)
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']

    def validate_amount(self, value):
        """
        Функция, валидирующая добавляемые ингредиенты.
        Осуществляет проверку на количество ингредиента
        """
        if value < INGREDIENT_MIN_VALUE:
            raise ValidationError(
                f'Количество ингредиентов не '
                f'должно быть меньше {INGREDIENT_MIN_VALUE}!'
            )
        return value
