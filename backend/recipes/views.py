import base64
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Recipe,
    FavouriteUserRecipe,
    ShoppingCart,
    RecipeIngredient
)
from .filters import RecipeFilter
from users.paginators import PageLimitPagination
from .serializers import (
    RecipeListDetailSerializer,
    RecipePostPatchSerializer,
    SimpleRecipeSerializer
)
from .permissions import OwnerOrReadOnly


@api_view(['POST', 'DELETE'])
def add_favourite_recipe(request: HttpRequest, id):
    """
    Функция добавления рецепта в избранное
    и удаления рецепта из избранного
    """
    if not request.user.is_authenticated:
        return Response(
            {'detail': 'Учетные данные не были предоставлены.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    recipe = get_object_or_404(
        Recipe,
        pk=id,
    )
    if request.method == 'POST':
        if FavouriteUserRecipe.objects.filter(
            user=request.user,
            recipe=recipe,
        ).exists():
            return Response(
                {'detail': 'Рецепт уже добавлен в избранное'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        FavouriteUserRecipe.objects.create(
            user=request.user,
            recipe=recipe,
        )
        serializer = SimpleRecipeSerializer(recipe)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )
    elif request.method == 'DELETE':
        if not FavouriteUserRecipe.objects.filter(
            user=request.user,
            recipe=recipe,
        ).exists():
            return Response(
                {'detail': 'Рецепта нет в избранном'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        FavouriteUserRecipe.objects.filter(
            user=request.user,
            recipe=recipe,
        ).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(['POST', 'DELETE'])
def add_shopping_cart(request: HttpRequest, id):
    """
    Функция добавления рецепта в список покупок
    и удаления рецепта из списка покупок
    """
    if not request.user.is_authenticated:
        return Response(
            {'detail': 'Учетные данные не были предоставлены.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    recipe = get_object_or_404(
        Recipe,
        pk=id,
    )
    if request.method == 'POST':
        if ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe,
        ).exists():
            return Response(
                {'detail': 'Рецепт уже есть в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ShoppingCart.objects.create(
            user=request.user,
            recipe=recipe,
        )
        serializer = SimpleRecipeSerializer(recipe)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )
    elif request.method == 'DELETE':
        if not ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe,
        ).exists():
            return Response(
                {'detail': 'Рецепта нет в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe,
        ).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(['GET'])
def shopping_cart_list(request: HttpRequest):
    """
    Функция получения списка покупок пользователя в формате .txt файла
    """
    if not request.user.is_authenticated:
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
        )
    _shopping_cart_list = ShoppingCart.objects.filter(
        user=request.user
    )
    ingredients = RecipeIngredient.objects.filter(
        recipe__in=_shopping_cart_list.values_list('recipe_id', flat=True)
    ).values(
        'ingredient__id',
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(
        total_amount=Sum('amount'),
    )
    content = 'Список ингредиентов:\n'
    for ingredient in ingredients:
        content += f'{ingredient["ingredient__name"]} ('
        content += f'{ingredient["ingredient__measurement_unit"]}'
        content += f') - {ingredient["total_amount"]}\n'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; '
    'filename="shopping_cart_list.txt"'
    return response


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсетсет, который обеспечивает реализацию следующих функций:
        - получения списка рецептов
        - создание рецепта
        - получение рецепта по идентификатору
        - обновление рецепта
        - удаления рецепта
        - получения короткой ссылки на рецепт
    """
    queryset = Recipe.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """
        Если метод 'безопасный', то используется сериализатор
        RecipeListDetailSerializer, иначе - RecipePostPatchSerializer
        """
        if self.action in ('list', 'retrieve', 'get_link'):
            return RecipeListDetailSerializer
        return RecipePostPatchSerializer

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        """
        Функция получения короткой ссылки на рецепт
        """
        recipe = self.get_object()
        return Response(
            {
                'short-link': recipe.get_short_url()
            },
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        """
        Переопределение функции создания объекта(метод POST)
        Ваш комментарий: Избыточно переопределять целые методы.
                Достаточно для нужных методов получить подходящий сериализатор.
        В данном случае, на мой взгляд, переопределение нужно, так как
        в них реализуется пользовательская(в смысле нестандартная) логика
        работы с моделями.
        """
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        recipe = create_serializer.save()
        read_serializer = RecipeListDetailSerializer(
            recipe, context={'request': request}
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """
        Переопределение функции частиного обновлени объекта(PATCH-запрос)
        """
        instance = self.get_object()
        serializer = RecipePostPatchSerializer(
            instance,
            data=request.data,
            partial=False,
            context={
                'request': request
            },
        )
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        response_data = RecipeListDetailSerializer(
            recipe,
            context={
                'request': request
            },
        )
        return Response(
            response_data.data,
            status=status.HTTP_200_OK
        )


class ShortLinkViewSet(viewsets.ViewSet):
    """
    Обработка коротких ссылок вида /s/<encoded_id>/
    """
    @action(
        detail=False,
        methods=['get'],
        url_path='https://foodgram.example.org/s/(?P<encoded_id>[a-zA-Z0-9_-]+)'
    )
    def redirect_from_short_link(self, request, encoded_id=None):
        """Редирект по короткой ссылке"""
        try:
            decoded_bytes = base64.urlsafe_b64decode(
                encoded_id + '=' * (4 - len(encoded_id) % 4)
            )
            recipe_id = int(decoded_bytes.decode())
            return redirect('recipe-detail', pk=recipe_id)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Неправильная короткая ссылка'},
                status=status.HTTP_404_NOT_FOUND
            )
