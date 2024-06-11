from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.serializers.ad_centre import AdCentreSerializer, ad_centre_model
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class AdCentreViewSet(viewsets.ModelViewSet):
    """Работа с подразделениями-центрами из AD"""
    respu = ResponseUtils()
    ju = JournalService()

    queryset = ad_centre_model.objects.all().order_by('display_name')
    serializer_class = AdCentreSerializer

    @swagger_auto_schema(
        tags=['Общее. AD', ],
        operation_description="Получение списка подразделений-центров из AD",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': AdCentreSerializer(many=True)
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
                    'module': COMMON,
                    'status': ERROR,
                    'description': 'Ошибка при получении списка подразделений-центров'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()
