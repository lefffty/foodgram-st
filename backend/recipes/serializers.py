from rest_framework.serializers import (
    SerializerMethodField,
    ValidationError,
    ModelSerializer,
    IntegerField,
    ImageField,
)
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

from ingredients.serializers import (
    IngredientForRecipeSerializer,
    IngredientPatchSerializer
)
from users.serializers import UserSerializer
from .models import (
    RecipeIngredient,
    Recipe,
)
from .constants import (
    COOKING_TIME_MIN_VALUE,
)

User = get_user_model()


class RecipeListDetailSerializer(ModelSerializer):
    """
    Сериализатор для функций:
        - получения списка рецептов
        - получения отдельного рецепта по его идентификатору
    """
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    ingredients = IngredientForRecipeSerializer(
        many=True,
        read_only=True,
        source='recipeingredient_set',
    )
    author = UserSerializer(read_only=True)
    image = ImageField(
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """
        Функция, обеспечивающая получение значения для поля is_favorited
        """
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return user.user_favs.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """
        Функция, обеспечивающая получение значения для поля is_in_shopping_cart
        """
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return user.user_shops.filter(recipe=obj).exists()


class RecipePostPatchSerializer(ModelSerializer):
    """
    Сериализатор для функций:
        - создания модели рецепта
        - частичного обновления объекта рецепта
    """
    ingredients = IngredientPatchSerializer(many=True, required=True)
    image = Base64ImageField(required=True)
    cooking_time = IntegerField(
        validators=[
            MinValueValidator(
                COOKING_TIME_MIN_VALUE,
                message=f'Время приготовления не должно '
                f'быть меньше {COOKING_TIME_MIN_VALUE} минуты'
            )
        ]
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'text',
            'cooking_time',
            'ingredients',
        )
        extra_kwargs = {
            'ingredients': {
                'required': True,
            },
            'name': {
                'required': True,
            },
            'text': {
                'required': True,
            },
            'cooking_time': {
                'required': True,
            },
        }

    def __init__(self, *args, **kwargs):
        """
        Переопределение конструктора класса для установки атрибуту REQUIRED
        поля IMAGE значения FALSE, если поступил PATCH-запрос
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            self.fields['image'].required = False

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError(
                'Нужно добавить хотя бы один ингредиент!'
            )
        ids = [val['ingredient'].id for val in value]
        if len(ids) != len(set(ids)):
            raise ValidationError(
                'Ингредиенты должны быть уникальными!',
            )
        return value

    def save_ingredients(self, recipe, ingredients):
        """
        Функция сохранения ингредиентов
        """
        RecipeIngredient.objects.filter(
            recipe=recipe,
        ).delete()

        _ingredients = []

        for ingredient in ingredients:
            _ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient['ingredient'],
                    amount=ingredient['amount'],
                )
            )

        RecipeIngredient.objects.bulk_create(
            objs=_ingredients,
        )

    def create(self, validated_data):
        """
        Функция создания рецепта
        """
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context['request'].user
        )
        self.save_ingredients(recipe, ingredients)
        return recipe

    def validate(self, attrs):
        """
        Функция валидации данных
        """
        if attrs.get('ingredients') is None:
            raise ValidationError(
                'Нужно добавить хотя бы один ингредиент!'
            )
        return attrs

    def update(self, instance, validated_data):
        """
        Функция обновления данных в существующем рецепте
        """
        ingredients = validated_data.pop('ingredients', None)
        super().update(instance, validated_data)
        self.save_ingredients(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Переопределяем метод для возврата данных в нужном формате
        """
        return RecipeListDetailSerializer(instance, context=self.context).data


class SimpleRecipeSerializer(ModelSerializer):
    """
    Сериализатор модели РЕЦЕПТ для функции МОИ_ПОДПИСКИ
    """
    image = ImageField(
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
