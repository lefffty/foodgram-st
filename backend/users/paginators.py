from rest_framework.pagination import PageNumberPagination

from users.constants import USERS_MAX_PAGE_SIZE


class PageLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = USERS_MAX_PAGE_SIZE
