from rest_framework import serializers
from rest_framework.serializers import ImageField
from djoser.serializers import UserCreateSerializer, SetPasswordSerializer
from django.contrib.auth.validators import UnicodeUsernameValidator
from drf_extra_fields.fields import Base64ImageField

from .constants import (
    USER_FIRST_NAME_MAX_LENGTH,
    USER_LAST_NAME_MAX_LENGTH,
    USER_USERNAME_MAX_LENGTH,
)
from .models import (
    CustomUser,
)


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
        return obj.followers.filter(user=request.user).exists()


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
        if len(value) > USER_USERNAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Username должен быть меньше '
                f'{USER_USERNAME_MAX_LENGTH} символов длиной!'
            )
        return value

    def validate_first_name(self, value):
        if len(value) > USER_FIRST_NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'First_name должен быть меньше '
                f'{USER_FIRST_NAME_MAX_LENGTH} символов длиной!'
            )
        return value

    def validate_last_name(self, value):
        if len(value) > USER_LAST_NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Last_name должен быть меньше '
                f'{USER_LAST_NAME_MAX_LENGTH} символов длиной!'
            )
        return value


class AvatarBaseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления и удаления аватара пользователя.
    """
    avatar = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('avatar',)
        extra_kwargs = {
            'avatar': {
                'required': True,
            }
        }


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
