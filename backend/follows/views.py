from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status, viewsets

from .models import Follow
from .serializers import FollowSerializer
from users.paginators import PageLimitPagination

User = get_user_model()


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

    @action(detail=True, methods=['POST', 'DELETE'], url_path='subscribe')
    def subscription(self, request, pk=None):
        """
        Функция подписки на пользователя
        """
        author = self.get_object()
        if request.method == 'POST':
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
            Follow.objects.create(
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
        elif request.method == 'DELETE':
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
