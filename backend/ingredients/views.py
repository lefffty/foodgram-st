from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .serializers import IngredientSerializer
from .models import Ingredient
from .filters import IngredientFilter


class IngredientListViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin):
    """
    Вьюсет, который обеспечивает реализацию следующих функций:
        - получение списка ингредиентов с возможностью поиск по частичному
            совпадению названия ингредиента
        - получение отдельного ингредиента по его идентификатору
    """
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None
