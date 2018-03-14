from rest_framework.pagination import LimitOffsetPagination

class PlatformPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
