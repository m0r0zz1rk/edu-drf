from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.pagination import CustomPagination
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.selectors.oo import oo_queryset, OoFilter
from apps.guides.serializers.oo import OoListSerializer
from apps.guides.services.oo import oo_service
from apps.journal.consts.journal_modules import USERS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError


class FormDataOoViewSet(viewsets.ModelViewSet):
    """
    Класс эндпоинтов для работы с ОО в анкете заявки обучающегося
    """
    permission_classes = [IsAuthenticated, ]

    _response_utils = ResponseUtils()

    queryset = oo_queryset()
    serializer_class = OoListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = OoFilter

    @swagger_auto_schema(
        tags=['Обучающиеся. Данные для заполнения анкеты', ],
        operation_description="Получение списка ОО для МО из анкеты",
        responses={
            '403': 'Пользователь не авторизован',
            '400': 'Ошибка при получении списка',
            '200': OoListSerializer(many=True)
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении списка ОО для анкеты заявки',
        'Произошла ошибка при получении списка ОО'
    )
    def list(self, request, *args, **kwargs):
        try:
            qs = oo_service.get_mo_oos(self.kwargs['mo_id'])
            queryset = self.filter_queryset(qs)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self._response_utils.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError
