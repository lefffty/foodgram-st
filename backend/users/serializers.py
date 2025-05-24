from rest_framework import serializers
from rest_framework.serializers import ImageField
from djoser.serializers import UserCreateSerializer, SetPasswordSerializer
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import (
    CustomUser,
    Follow
)
from recipes.models import Recipe
from recipes.serializers import SimpleRecipeSerializer
from .utils import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения профиля пользователя.
    """
    avatar = serializers.ImageField(use_url=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        ]
        read_only_fields = ('id', 'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Follow.objects.filter(user=request.user, following=obj).exists()


class CreateUserSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователя.
    """
    username = serializers.CharField(
        required=True,
        validators=[UnicodeUsernameValidator()],
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        read_only_fields = ('id',)

    def validate_username(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'Username должен быть меньше 150 символов длиной!'
            )
        return value

    def validate_first_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'First_name должен быть меньше 150 символов длиной!'
            )
        return value

    def validate_last_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'Last_name должен быть меньше 150 символов длиной!'
            )
        return value


class AvatarBaseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления и удаления аватара пользователя.
    """
    avatar = Base64ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ('avatar',)


class AvatarSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с полем аватара пользователя.
    """
    avatar = ImageField(use_url=True)

    class Meta:
        model = CustomUser
        fields = ('avatar',)


class CustomSetPasswordSerializer(SetPasswordSerializer):
    """
    Сериализатор для установки пароля пользователя.
    """

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class FollowSerializer(UserSerializer):
    """
    Сериализатор для списка подписок пользователя.
    Возвращает данные автора и его рецепты.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

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
        query_params = self.context['request'].query_params
        recipes_limit = query_params.get('recipes_limit')
        recipes = Recipe.objects.filter(
            author__username=obj.username,
        )
        if recipes_limit:
            recipes_limit = int(recipes_limit)
            recipes = recipes[:recipes_limit]
        serializer = SimpleRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        following = CustomUser.objects.get(username=obj.username)
        recipes_count = Recipe.objects.filter(
            author=following,
        ).count()
        return recipes_count
