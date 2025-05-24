from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ImageField,
    IntegerField,
    ValidationError
)
from django.core.validators import MinValueValidator
from django.db import transaction

from users.utils import Base64ImageField
from ingredients.models import Ingredient
from ingredients.serializers import (
    IngredientForRecipeSerializer,
    IngredientPatchSerializer
)
from .models import (
    Recipe,
    FavouriteUserRecipe,
    ShoppingCart,
    RecipeIngredient
)


class RecipeListDetailSerializer(ModelSerializer):
    """
    Сериализатор для функций:
        - получения списка рецептов
        - получения отдельного рецепта по его идентификатору
    """
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    ingredients = IngredientForRecipeSerializer(many=True, read_only=True)
    author = SerializerMethodField(read_only=True)
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = IngredientForRecipeSerializer(
            instance.ingredients.all(),
            many=True,
            context={
                'recipe': instance,
                **self.context
            }
        ).data
        return representation

    def get_author(self, obj):
        """
        Функция, обеспечивающая получение значения для поля author
        """
        from users.serializers import UserSerializer
        return UserSerializer(
            obj.author,
            context=self.context,
        ).data

    def get_is_favorited(self, obj):
        """
        Функция, обеспечивающая получение значения для поля is_favorited
        """
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        if FavouriteUserRecipe.objects.filter(
            user=user,
            recipe=obj,
        ).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        """
        Функция, обеспечивающая получение значения для поля is_in_shopping_cart
        """
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        if ShoppingCart.objects.filter(
            user=user,
            recipe=obj,
        ).exists():
            return True
        return False


class RecipePostPatchSerializer(ModelSerializer):
    """
    Сериализатор для функций:
        - создания модели рецепта
        - частичного обновления объекта рецепта
    """
    ingredients = IngredientPatchSerializer(many=True, required=True)
    image = Base64ImageField(use_url=True)
    cooking_time = IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не должно быть меньше 1 минуты'
            )
        ]
    )

    class Meta:
        model = Recipe
        fields = (
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

    def validate_ingredients(self, value):
        """
        Функция валидирующая добавляемые ингредиенты.
        Осуществляет проверку на количество ингредиентов(кол-во
        должно быть >= 1), осуществляет проверку
        на количество отдельного ингредиента, а также проверку
        на уникальность ингредиентов.
        """
        if not value:
            raise ValidationError("Нужно добавить хотя бы один ингредиент!")

        ids = []

        for val in value:
            ids.append(val['ingredient'])
            if int(val['amount']) < 1:
                raise ValidationError(
                    "Количество ингредиентов не должно быть меньше 1!"
                )

        if len(ids) != len(set(ids)):
            raise ValidationError("Ингредиенты должны быть уникальными!")

        return value

    def __init__(self, *args, **kwargs):
        """
        Переопределение конструктора класса для установки атрибуту REQUIRED
        поля IMAGE значения FALSE, если поступил PATCH-запрос
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            self.fields['image'].required = False

    def save_ingredients(self, recipe, ingredients):
        """
        Функция сохранения ингредиентов
        """
        RecipeIngredient.objects.filter(
            recipe=recipe,
        ).delete()

        _ingredients = []

        for ingredient in ingredients:
            ingr_instance = Ingredient.objects.get(
                pk=ingredient['ingredient'].id)

            _ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingr_instance,
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

    def update(self, instance, validated_data):
        """
        Функция обновления данных в существующем рецепте
        """
        ingredients = validated_data.pop('ingredients', None)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        if ingredients:
            self.save_ingredients(instance, ingredients)
        instance.save()
        return instance


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
