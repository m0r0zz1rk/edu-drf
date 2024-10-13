from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.pagination import CustomPagination
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.selectors.oo_type import oo_type_queryset
from apps.guides.serializers.oo_type import OoTypeListUpdateSerializer
from apps.journal.consts.journal_modules import USERS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError


class FormDataOoTypeViewSet(viewsets.ModelViewSet):
    """
    Класс эндпоинтов для работы с типами ОО в анкете заявки обучающегося
    """
    permission_classes = [IsAuthenticated, ]

    _response_utils = ResponseUtils()

    queryset = oo_type_queryset()
    serializer_class = OoTypeListUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NameFieldFilter

    @swagger_auto_schema(
        tags=['Обучающиеся. Данные для заполнения анкеты', ],
        operation_description="Получение списка типов ОО для анкеты заявки обучающегося",
        responses={
            '403': 'Пользователь не авторизован',
            '400': 'Ошибка при получении списка',
            '200': OoTypeListUpdateSerializer(many=True)
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении списка типов ОО для анкеты заявки',
        'Произошла ошибка при получении списка типов ОО'
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self._response_utils.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError
