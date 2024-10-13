from rest_framework import pagination


class CustomPagination(pagination.LimitOffsetPagination):
    limit_query_param = 'size'
    offset_query_param = 'start'

    limit_query_description = 'Количество записей'
    offset_query_description = 'Сдвиг'
