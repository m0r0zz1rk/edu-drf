from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.exceptions.schedule.day_info_validate_error import DayInfoValidateError
from apps.edu.exceptions.schedule.schedule_generate_error import ScheduleGenerateError
from apps.edu.serializers.schedule import ScheduleListSerializer, GenerateScheduleSerializer, DayInfoSerializer
from apps.edu.services.schedule import ScheduleService
from apps.guides.services.user import UserService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError


class ScheduleViewSet(viewsets.ViewSet):
    """Работа с расписаниями занятий учебных групп"""
    permission_classes = [IsAuthenticated, IsAdministrators]

    __response_utils = ResponseUtils()
    _user_service = UserService()
    _journal_request_builder = JournalRequestBuilder()

    @swagger_auto_schema(
        tags=['Учебная часть. Расписание занятий', ],
        operation_description="Получение расписания занятий учебной группы",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': ScheduleListSerializer(many=True)
        }
    )
    @journal_api(
        EDU,
        ERROR,
        'Ошибка при получении расписания занятий для учебной группы',
        'Произошла ошибка при получении расписания занятий учебной группы'
    )
    def get_group_schedule(self, request, *args, **kwargs):
        try:
            schedule = ScheduleService(self.kwargs['group_id']).get_group_schedule()
            serializer = ScheduleListSerializer(schedule, many=True)
            return self.__response_utils.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Учебная часть. Расписание занятий', ],
        operation_description="Генерация расписания занятий",
        request_body=GenerateScheduleSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка в процессе генерации',
            '200': 'Сообщение "Расписание успешно сгенерировано"'
        }
    )
    @journal_api(
        EDU,
        ERROR,
        'Ошибка при генерации расписания занятий',
        'Произошла ошибка при генерации расписания занятий учебной группы'
    )
    def generate_schedule(self, request, *args, **kwargs):
        try:
            serialize = GenerateScheduleSerializer(data=request.data)
            if serialize.is_valid():
                ScheduleService(serialize.data['group_id']).generate_schedule(serialize.data['generate'])
                return self.__response_utils.ok_response('Расписание успешно сгенерировано')
            else:
                raise APIProcessError
        except ScheduleGenerateError:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(EDU)
                .set_status(ERROR)
                .set_description('Системная ошибка при генерации расписания занятий')
                .set_payload(repr(request.data))
                .set_output(ExceptionHandling.get_traceback())
                .set_response_message('Произошла системная ошибка, повторите попытку позже')
            )
            return journal_request.create_response()
        except RuntimeError:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Учебная часть. Расписание занятий', ],
        operation_description="Сохранения расписания учебного дня",
        request_body=DayInfoSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка в процессе сохранения расписания',
            '200': 'Сообщение "Расписание успешно сохранено"'
        }
    )
    @journal_api(
        EDU,
        ERROR,
        'Ошибка при сохранении расписания учбеного дня',
        'Произошла ошибка при сохранении расписания'
    )
    def save_day_info(self, request, *args, **kwargs):
        try:
            serialize = DayInfoSerializer(
                data=request.data
            )
            if serialize.is_valid():
                ScheduleService(serialize.data['group_id']).save_day_info(serialize.data)
                return self.__response_utils.ok_response('Расписание успешно сохранено')
            else:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_module(EDU)
                    .set_status(ERROR)
                    .set_description('Системная ошибка при сериализации расписания учебного дня')
                    .set_payload(repr(request.data))
                    .set_output(repr(serialize.errors))
                    .set_response_message('Полученные данные учебного дня не прошли сериализацию')
                )
                return journal_request.create_response()
        except DayInfoValidateError:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(EDU)
                .set_status(ERROR)
                .set_description('Ошибка при валидации информации по расписанию учебного дня')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Информация по расписанию учебного дня не прошла валидацию')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
