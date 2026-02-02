from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.response import response_utils
from apps.edu.api.edu_viewset import EduViewSet
from apps.edu.selectors.planning_parameter import planning_parameter_queryset, PlanningParameterFilter, \
    planning_parameter_orm
from apps.edu.serializers.planning_parameter import PlanningParameterSerializer
from apps.journal.consts.journal_modules import EDU


class PlanningParameterViewSet(EduViewSet):
    """Работа с параметрами планирования мероприятий"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    orm = planning_parameter_orm
    queryset = planning_parameter_queryset()
    serializer_class = PlanningParameterSerializer
    update_serializer = PlanningParameterSerializer
    filterset_class = PlanningParameterFilter
    swagger_object_name = 'Параметры планирования'

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Получение списка",
        responses={
            **SWAGGER_TEXT['list'],
            '200': serializer_class(many=True)
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'Список "{swagger_object_name}" получен',
        f'Ошибка при получении списка "{swagger_object_name}"'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Получение объекта курса (ОУ)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': serializer_class
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'"{swagger_object_name}" получен',
        f'Ошибка при получении "{swagger_object_name}"'
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Обновление параметра планирования",
        request_body=PlanningParameterSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении параметра планирования',
            '200': 'Сообщение "Параметр успешно обновлен"'
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'"{swagger_object_name}" обновлен',
        f'Ошибка при обновлении "{swagger_object_name}"'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
