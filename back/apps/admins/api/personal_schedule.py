from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.permissions.is_admin_or_coko import IsAdminOrCoko
from apps.commons.utils.django.response import response_utils
from apps.edu.serializers.schedule import PersonalScheduleSerializer
from apps.edu.services.schedule import ScheduleService


class PersonalScheduleViewSet(viewsets.ViewSet):
    """Класс эндпоинта для получения списка своих занятий"""

    permission_classes = [IsAuthenticated, IsAdminOrCoko]

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
        schedule_service = ScheduleService(None)
        schedule = schedule_service.get_personal_schedule(
            request.user.id
        )
        return response_utils.ok_response_dict(schedule)
