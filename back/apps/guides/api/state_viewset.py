from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.serializers.state_serializer import state_model, StateSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.utils.journal_utils import JournalUtils


class StateViewSet(viewsets.ModelViewSet):
    """Класс эндпоинтов для работы с государствами"""
    serializer_class = StateSerializer
    queryset = state_model.objects.all().order_by('name')
    ju = JournalUtils()

    @swagger_auto_schema(
        tags=['Справочники', ],
        operation_description="Получение списка всех государств",
        responses={
            '400': 'Ошибка при получении списка',
            '200': StateSerializer(many=True)
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
            return ResponseUtils.ok_response_dict(serializer.data)
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
            return ResponseUtils.bad_request_no_data()

