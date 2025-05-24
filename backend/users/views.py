from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    AvatarBaseSerializer,
    FollowSerializer,
    CustomSetPasswordSerializer
)
from .paginators import PageLimitPagination
from .models import Follow

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


class FollowViewSet(viewsets.GenericViewSet):
    """
    Вьюсет, который обеспечивает реализацию следующих функций:
        - получение всех подписок текущего пользователя
        - подписка на пользователя
        - отписка от пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageLimitPagination

    @action(detail=True, methods=['POST'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        """
        Функция подписки на пользователя
        """
        author = self.get_object()
        if request.user == author:
            return Response(
                {
                    'detail': 'Нельзя подписаться на самого себя'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
            user=request.user,
            following=author
        ).exists():
            return Response(
                {
                    'detail': 'Такая подписка уже существует!',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.get_or_create(
            user=request.user,
            following=author
        )
        data = FollowSerializer(
            author,
            context={
                'request': request
            }
        ).data
        return Response(
            data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['DELETE'], url_path='subscribe')
    def unsubscribe(self, request, pk=None):
        """
        Функция отписки от пользователя
        """
        author = self.get_object()
        if not Follow.objects.filter(
            user=request.user,
            following=author
        ).exists():
            return Response(
                {
                    'detail': 'Такой подписки не существует!'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.filter(
            user=request.user,
            following=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='subscriptions')
    def list_subscriptions(self, request):
        """
        Функция получения списка подписок текущего пользователя
        """
        authors = User.objects.filter(followers__user=request.user)
        page = self.paginate_queryset(authors)
        serializer = FollowSerializer(
            page,
            many=True,
            context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)
