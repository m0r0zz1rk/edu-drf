from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.pagination import CustomPagination
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.filters.state_filter import StateFilter
from apps.guides.serializers.state_serializer import state_model, StateSerializer
from apps.journal.consts.journal_modules import JOURNAL, GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.utils.journal_utils import JournalUtils


class StateViewSet(viewsets.ModelViewSet):
    """Класс эндпоинтов для работы с государствами"""
    serializer_class = StateSerializer
    queryset = state_model.objects.all().order_by('name')
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = StateFilter

    ju = JournalUtils()
    respu = ResponseUtils()

    @swagger_auto_schema(
        tags=['Справочники', ],
        operation_description="Получение списка государств",
        responses={
            '400': 'Ошибка при получении списка',
            '200': StateSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
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
            return self.respu.bad_request_no_data()

