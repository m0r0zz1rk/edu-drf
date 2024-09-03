from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.exceptions.schedule.schedule_generate_error import ScheduleGenerateError
from apps.edu.serializers.schedule import ScheduleListSerializer, GenerateScheduleSerializer
from apps.edu.services.schedule import ScheduleService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api, journal_service
from apps.journal.exceptions.api_process_error import APIProcessError


class ScheduleViewSet(viewsets.ViewSet):
    """Работа с расписаниями занятий учебных групп"""
    permission_classes = [IsAuthenticated, IsAdministrators]

    __response_utils = ResponseUtils()

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
        'Внешний запрос',
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
        except:
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
        'Внешний запрос',
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
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при генерации расписания занятий'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.__response_utils.bad_request_response('Произошла системная ошибка, повторите попытку позже')
        except RuntimeError:
            raise APIProcessError
