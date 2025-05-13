from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.celery_app.tasks.worker import email_survey_report
from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import SURVEYS
from apps.surveys.serializers.survey_report import ReportParametersSerializer


class SurveyReportViewSet(viewsets.ViewSet):
    """
    Вьюсет для выполнения задания на генерацию и отправки на почту файла отчет по результатам опроса
    """

    @swagger_auto_schema(
        tags=[f'Опросы. Формирование отчета', ],
        operation_description="Формирование отчета по результатам опроса",
        request_body=ReportParametersSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при формировании отчета',
            '200': 'Сообщение "Отчет будет сформирован и отправлен на вашу почту"'
        }
    )
    @view_set_journal_decorator(
        SURVEYS,
        f'Запрос на получение отчета по опросу успешно выполнен',
        f'Ошибка при формировании запроса на получение отчета по опросу"'
    )
    def generate_report(self, request, *args, **kwargs):
        serialize = ReportParametersSerializer(data=request.data)
        if serialize.is_valid():
            email_survey_report.delay(request.user.email, serialize.validated_data)
            return response_utils.ok_response('Отчет будет сформирован и отправлен на вашу почту')
        else:
            return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')
