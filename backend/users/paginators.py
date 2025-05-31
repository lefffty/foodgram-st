from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100
