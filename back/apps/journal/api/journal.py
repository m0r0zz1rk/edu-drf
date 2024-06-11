from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import JOURNAL
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.selectors.journal import JournalFilter
from apps.journal.serializers.journal import JournalSerializer
from apps.journal.services.journal import JournalService


class JournalViewSet(viewsets.ModelViewSet):
    """Получение записей из журнала событий"""
    ju = JournalService()
    respu = ResponseUtils()

    permission_classes = [IsAuthenticated, IsAdministrators]
    queryset = ju.journal_model.objects.all().order_by('-date_create')
    serializer_class = JournalSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = JournalFilter

    @swagger_auto_schema(
        tags=['Журнал событий', ],
        operation_description="Получение записей журнала событий",
        responses={
            '400': 'Ошибка при получении записей',
            '403': 'Пользователь не авторизован или не является администратором',
            '200': JournalSerializer(many=True)
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
                    'module': JOURNAL,
                    'status': ERROR,
                    'description': 'Системная ошибка при получении записей журнала событий'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.sorry_try_again_response()
