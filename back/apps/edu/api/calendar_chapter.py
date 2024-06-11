from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.request import RequestUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.serializers.calendar_chart import CalendarChartGetSerializer, CalendarChartUpdateSerializer
from apps.edu.services.calendar_chart import CalendarChartService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class CalendarChartViewSet(viewsets.ViewSet):
    """Работа с КУГ"""

    #permission_classes = [IsAuthenticated, IsAdministrators]
    ru = RequestUtils()
    ju = JournalService()
    pu = ProfileService()
    respu = ResponseUtils()
    ccu = CalendarChartService()

    @swagger_auto_schema(
        tags=['Учебная часть. КУГ ДПП', ],
        operation_description="Получение КУГ",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении КУГ',
            '200': CalendarChartGetSerializer
        }
    )
    def get_kug(self, request, *args, **kwargs):
        try:
            kug = self.ccu.get_program_calendar_chart(
                self.kwargs['program_id'],
                request.user.id
            )
            serialize = CalendarChartGetSerializer(data=kug)
            if serialize.is_valid():
                return self.respu.ok_response_dict(serialize.data)
            else:
                self.ju.create_journal_rec(
                    {
                        'source': 'Внешний запрос',
                        'module': EDU,
                        'status': ERROR,
                        'description': 'Ошибка сериализации при получении КУГ ДПП'
                    },
                    repr(kug),
                    repr(serialize.errors)
                )
                return self.respu.bad_request_response(
                    f'Ошибка сериализации: {repr(serialize.errors)}'
                )
        except:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при получении КУГ ДПП'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка, повторите попытку позже')

    @swagger_auto_schema(
        tags=['Учебная часть. КУГ ДПП', ],
        operation_description="Обновление КУГ ДПП",
        request_body=CalendarChartUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Сообщение об ошибке при обновлении КУГ ДПП',
            '200': 'Сообщение "КУГ успешно обновлен"'
        }
    )
    def update_kug(self, request, *args, **kwargs):
        serialize = CalendarChartUpdateSerializer(data=request.data)
        if serialize.is_valid():
            proc = self.ccu.update_program_calendar_chart(
                serialize.data['program_id'],
                request.user.id,
                serialize.data['chapters']
            )
            if proc:
                return self.respu.ok_response('КУГ успешно обновлен')
            else:
                return self.respu.bad_request_response('Ошибка при обновлении КУГ. Подробная информация в журнале')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка сериализации при обновлении КУГ ДПП'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(
                f'Ошибка сериализации: {repr(serialize.errors)}'
            )
