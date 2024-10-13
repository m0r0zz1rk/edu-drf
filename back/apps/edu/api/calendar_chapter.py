from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.services.journal_request import JournalRequest, JournalRequestBuilder
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.request import RequestUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.exceptions.calendar_chart.get_kug_remains_error import GetKugRemainsError
from apps.edu.exceptions.calendar_chart.kug_not_found import KugNotFound
from apps.edu.exceptions.student_group.student_group_incorrect_service import StudentGroupIncorrectService
from apps.edu.exceptions.student_group.student_group_not_found import StudentGroupNotFound
from apps.edu.serializers.calendar_chart import CalendarChartGetSerializer, CalendarChartUpdateSerializer, \
    CalendarChartRemainHoursSerializer
from apps.edu.services.calendar_chart import CalendarChartService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.journal.services.journal import JournalService


class CalendarChartViewSet(viewsets.ViewSet):
    """Работа с КУГ"""

    permission_classes = [IsAuthenticated, IsAdministrators]
    ru = RequestUtils()
    ju = JournalService()
    pu = ProfileService()
    respu = ResponseUtils()
    ccu = CalendarChartService()
    _journal_request_builder = JournalRequestBuilder()

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
        except Exception:
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
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(EDU)
                .set_status(ERROR)
                .set_description('Ошибка сериализации при обновлении КУГ ДПП')
                .set_payload(repr(request.data))
                .set_output(repr(serialize.errors))
                .set_response_message(f'Ошибка сериализации: {repr(serialize.errors)}')
            )
            return journal_request.create_response()

    @swagger_auto_schema(
        tags=['Учебная часть. КУГ ДПП', ],
        operation_description="Получение остаточных часов КУГ ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Сообщение об ошибке при обновлении КУГ ДПП',
            '200': CalendarChartRemainHoursSerializer
        }
    )
    @journal_api(
        EDU,
        ERROR,
        'Ошибка при получении оставшихся часов КУГ',
        'Произошла ошибка при получении оставшихся часов КУГ'
    )
    def get_remain_hours(self, request, *args, **kwargs):
        try:
            try:
                kug_remain = self.ccu.get_kug_remains_for_schedule(
                    self.kwargs['group_id']
                )
            except StudentGroupNotFound:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_module(EDU)
                    .set_status(ERROR)
                    .set_description('Ошибка при получении остаточных часов КУГ ДПП')
                    .set_payload(repr(request.data))
                    .set_output('Не найдена учебная группа')
                    .set_response_message('Ошибка получения остаточных часов КУГ: не найдена учебная группа')
                )
                return journal_request.create_response()
            except StudentGroupIncorrectService:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_module(EDU)
                    .set_status(ERROR)
                    .set_description('Ошибка при получении остаточных часов КУГ ДПП')
                    .set_payload(repr(request.data))
                    .set_output('Неверный тип услуги учебной группы')
                    .set_response_message('Ошибка получения остаточных часов КУГ: '
                                          'получить часы можно только для групп курсов')
                )
                return journal_request.create_response()
            except KugNotFound:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_module(EDU)
                    .set_status(ERROR)
                    .set_description('Ошибка при получении остаточных часов КУГ ДПП')
                    .set_payload(repr(request.data))
                    .set_output('Не найден КУГ')
                    .set_response_message('Ошибка получения остаточных часов КУГ: '
                                          'не найден КУГ ДПП')
                )
                return journal_request.create_response()
            except GetKugRemainsError:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_module(EDU)
                    .set_status(ERROR)
                    .set_description('Ошибка при полученных остаточных часов КУГ ДПП')
                    .set_payload(repr(request.data))
                    .set_output(ExceptionHandling.get_traceback())
                    .set_response_message('Системная ошибка при получении остаточных часов КУГ')
                )
                return journal_request.create_response()
            serialize = CalendarChartRemainHoursSerializer(
                data={'kug_remain': kug_remain}
            )
            if serialize.is_valid():
                return self.respu.ok_response_dict(serialize.data)
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(EDU)
                .set_status(ERROR)
                .set_description('Ошибка сериализации при получении остаточных часов КУГ ДПП')
                .set_payload(repr(request.data))
                .set_output(ExceptionHandling.get_traceback())
                .set_response_message('Системная ошибка при получении остаточных часов КУГ')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
