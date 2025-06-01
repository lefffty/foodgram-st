from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    AvatarBaseSerializer,
    CustomSetPasswordSerializer
)
from .paginators import PageLimitPagination

User = get_user_model()


class UserListCreateViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """
    Вьюсет, который обеспечивает реализацию следующих функций:
        - получения списка пользователей
        - регистрации пользователя
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer


class UserDetailViewSet(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin):
    """
    Вьюсет, который обеспечивает реализацию следующей функции:
        - получение пользователя по его идентификатору
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class AvatarViewSet(viewsets.GenericViewSet):
    """
    Вьюсет, который обеспечивает реализацию следующих функций:
        - добавление аватара
        - удаление аватара
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['PUT',])
    def set_avatar(self, request):
        serializer = AvatarBaseSerializer(
            request.user,
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'avatar': serializer.data['avatar'],
        })

    @action(detail=False, methods=['DELETE'])
    def delete_avatar(self, request):
        request.user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SetPasswordViewSet(viewsets.GenericViewSet):
    """
    Вьюсет, который обеспечивает реализацию следующих функций:
        - изменение пароля
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        serializer = CustomSetPasswordSerializer(
            data=request.data,
            context={
                'request': request,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class ProfileViewSet(viewsets.GenericViewSet):
    """
    Вьюсет, который обеспечивает реализацию следующих функций:
        - получение профиля текущего пользователя
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='me')
    def me(self, request):
        """
        Функция получения профиля текущего пользователя
        """
        serializer = UserSerializer(
            request.user,
            context={
                'request': request,
            }
        )
        return Response(serializer.data)
