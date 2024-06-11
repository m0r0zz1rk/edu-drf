from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.pagination import CustomPagination
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.serializers.state.state_registration import state_model, StateRegistrationSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class StateRegistrationViewSet(viewsets.ModelViewSet):
    """Класс эндпоинтов для работы с государствами"""
    serializer_class = StateRegistrationSerializer
    queryset = state_model.objects.all().order_by('name')
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NameFieldFilter

    ju = JournalService()
    respu = ResponseUtils()

    @swagger_auto_schema(
        tags=['Регистрация', ],
        operation_description="Получение списка государств",
        responses={
            '400': 'Ошибка при получении списка',
            '200': StateRegistrationSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при получении списка государств'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

