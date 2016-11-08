from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class BookLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
