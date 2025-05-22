from drf_yasg.utils import swagger_auto_schema

from apps.celery_app.tasks import (email_report_dpp, email_report_service_chart, email_report_pk_one,
                                   email_report_fis_frdo, email_report_year_forms)
from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import REPORTS
from apps.reports.api.reports_viewset import ReportsViewSet
from apps.reports.serializers.dpp_serializer import DppSerializer
from apps.reports.serializers.fis_frdo_serializer import FisFrdoSerializer
from apps.reports.serializers.pk_one_serializer import PKOneSerializer
from apps.reports.serializers.year_forms_serializer import YearFormsSerializer

# Словарь ответов на запросы
responses = {
    '403': 'Пользователь не авторизован или не является администратором',
    '400': 'Ошибка при обработке запроса',
    '200': 'Сообщение "Запрос обработан, отчет будет отправлен на почту"'
}


class ReportMainViewSet(ReportsViewSet):
    """
    Класс эндпоинтов для обработки запросов на формирование отчетов
    """

    @swagger_auto_schema(
        tags=[f'Отчеты', ],
        operation_description="Получение отчета ДПП",
        request_body=DppSerializer,
        responses=responses
    )
    @view_set_journal_decorator(
        REPORTS,
        f'Запрос на получение отчета ДПП успешно обработан',
        f'Ошибка при обработке запроса на получение отчета ДПП'
    )
    def dpp(self, request, *args, **kwargs):
        serialize = DppSerializer(data=request.data)
        if serialize.is_valid():
            email_report_dpp.delay(request.user.email, serialize.validated_data)
            return response_utils.ok_response("Запрос обработан, отчет будет отправлен на почту")
        return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Отчеты', ],
        operation_description="Получение отчета График услуг",
        request_body=DppSerializer,
        responses=responses
    )
    @view_set_journal_decorator(
        REPORTS,
        f'Запрос на получение отчета с графиком оказанных услуг успешно обработан',
        f'Ошибка при обработке запроса на получение отчета с графиком оказанных услуг'
    )
    def service_chart(self, request, *args, **kwargs):
        serialize = DppSerializer(data=request.data)
        if serialize.is_valid():
            email_report_service_chart.delay(request.user.email, serialize.validated_data)
            return response_utils.ok_response("Запрос обработан, отчет будет отправлен на почту")
        return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Отчеты', ],
        operation_description="Получение отчета ПК-1",
        request_body=PKOneSerializer,
        responses=responses
    )
    @view_set_journal_decorator(
        REPORTS,
        f'Запрос на получение отчета ПК-1 успешно обработан',
        f'Ошибка при обработке запроса на получение отчета ПК-1'
    )
    def pk_one(self, request, *args, **kwargs):
        serialize = PKOneSerializer(data=request.data)
        if serialize.is_valid():
            email_report_pk_one.delay(request.user.email, serialize.validated_data)
            return response_utils.ok_response("Запрос обработан, отчет будет отправлен на почту")
        return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Отчеты', ],
        operation_description="Получение отчета ФИС ФРДО",
        request_body=FisFrdoSerializer,
        responses=responses
    )
    @view_set_journal_decorator(
        REPORTS,
        f'Запрос на получение отчета ФИС ФРДО успешно обработан',
        f'Ошибка при обработке запроса на получение отчета ФИС ФРДО'
    )
    def fis_frdo(self, request, *args, **kwargs):
        serialize = FisFrdoSerializer(data=request.data)
        if serialize.is_valid():
            email_report_fis_frdo.delay(request.user.email, serialize.validated_data)
            return response_utils.ok_response("Запрос обработан, отчет будет отправлен на почту")
        return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Отчеты', ],
        operation_description="Получение анкет за год",
        request_body=YearFormsSerializer,
        responses=responses
    )
    @view_set_journal_decorator(
        REPORTS,
        f'Запрос на получение анкет за год успешно обработан',
        f'Ошибка при обработке запроса на получение анкет за год'
    )
    def year_forms(self, request, *args, **kwargs):
        serialize = YearFormsSerializer(data=request.data)
        if serialize.is_valid():
            email_report_year_forms.delay(request.user.email, serialize.validated_data)
            return response_utils.ok_response("Запрос обработан, файл будет отправлен на почту")
        return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')
