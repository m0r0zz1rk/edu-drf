from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.serializers.schedule import ScheduleListSerializer
from apps.edu.services.schedule import ScheduleService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
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
