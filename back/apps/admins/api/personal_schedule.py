from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.authen.services.profile import ProfileService
from apps.commons.services.journal_request import JournalRequestBuilder
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.serializers.schedule import PersonalScheduleSerializer
from apps.edu.services.schedule import ScheduleService


class PersonalScheduleViewSet(viewsets.ViewSet):
    """Класс эндпоинта для получения списка своих занятий"""

    _schedule_serivce = ScheduleService(None)
    _resp_utils = ResponseUtils()
    _journal_request_builder = JournalRequestBuilder()
    _profile_service = ProfileService()

    @swagger_auto_schema(
        tags=['Администраторы. Личное расписание', ],
        operation_description="Получение списка своих занятий "
                              "(преподаватели)",
        responses={
            '400': 'Сообщение "Повторите попытку позже"',
            '403': 'Пользователь не авторизован или не '
                   'является администратором',
            '200': PersonalScheduleSerializer(many=True)}
    )
    def get_personal_schedule(self, request, *args, **kwargs):
        schedule = self._schedule_serivce.get_personal_schedule(
            request.user.id
        )
        return self._resp_utils.ok_response_dict(schedule)
