from rest_framework.filters import SearchFilter


class IngredientFilter(SearchFilter):
    """
    Поисковый фильтр для получения списка ингредиентов
    """
    search_param = 'name'
