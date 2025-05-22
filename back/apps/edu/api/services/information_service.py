from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.permissions.is_admin_or_coko import IsAdminOrCoko
from apps.commons.utils.django.response import response_utils
from apps.edu.api.edu_viewset import EduViewSet
from apps.edu.consts.planning_days_error_text import PLANNING_DAYS_ERROR_TEXT
from apps.edu.exceptions.planning_parameter.planning_days_error import PlanningDaysError
from apps.edu.selectors.services.information_service import information_service_queryset, InformationServiceFilter, \
    information_service_orm

from apps.edu.serializers.services.information_service import InformationServiceListSerializer, \
    InformationServiceRetrieveAddUpdateSerializer
from apps.edu.services.service.information_service import information_service_service
from apps.journal.consts.journal_modules import EDU


class InformationServiceViewSet(EduViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrCoko]
    orm = information_service_orm
    queryset = information_service_queryset()
    serializer_class = InformationServiceListSerializer
    base_serializer = InformationServiceRetrieveAddUpdateSerializer
    create_serializer = InformationServiceRetrieveAddUpdateSerializer
    update_serializer = InformationServiceRetrieveAddUpdateSerializer
    filterset_class = InformationServiceFilter
    swagger_object_name = 'Мероприятие (ИКУ)'

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
            '200': base_serializer
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'"{swagger_object_name}" получен',
        f'Ошибка при получении "{swagger_object_name}"'
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InformationServiceRetrieveAddUpdateSerializer(
            information_service_service.prepare_to_serialize(instance.object_id)
        )
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Добавление записи",
        request_body=create_serializer,
        responses=SWAGGER_TEXT['create']
    )
    @view_set_journal_decorator(
        EDU,
        f'Запись "{swagger_object_name}" успешно добавлена',
        f'Ошибка при добавлении записи "{swagger_object_name}"'
    )
    def create(self, request, *args, **kwargs):
        serialize = InformationServiceRetrieveAddUpdateSerializer(data=request.data)
        if serialize.is_valid():
            try:
                information_service_service.create_service(serialize.validated_data)
                return response_utils.ok_response('Добавление выполнено')
            except PlanningDaysError:
                return response_utils.bad_request_response(PLANNING_DAYS_ERROR_TEXT)
        else:
            return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Обновление записи",
        request_body=update_serializer,
        responses=SWAGGER_TEXT['update']
    )
    @view_set_journal_decorator(
        EDU,
        f'Запись "{swagger_object_name}" успешно обновлена',
        f'Ошибка при обновлении записи "{swagger_object_name}"'
    )
    def partial_update(self, request, *args, **kwargs):
        serialize = InformationServiceRetrieveAddUpdateSerializer(data=request.data)
        if serialize.is_valid():
            try:
                information_service_service.update_service(self.kwargs['object_id'], serialize.validated_data)
                return response_utils.ok_response('Обновление выполнено')
            except PlanningDaysError:
                return response_utils.bad_request_response(PLANNING_DAYS_ERROR_TEXT)
        else:
            return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Удаление записи",
        responses=SWAGGER_TEXT['delete']
    )
    @view_set_journal_decorator(
        EDU,
        f'Запись "{swagger_object_name}" успешно удалена',
        f'Ошибка при удалении записи "{swagger_object_name}"'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Экспорт записей",
        responses=SWAGGER_TEXT['export']
    )
    @view_set_journal_decorator(
        EDU,
        f'Экспорт записей "{swagger_object_name}" успешно выполнен',
        f'Ошибка при выполнении экспорта записей "{swagger_object_name}"'
    )
    def export(self, request, *args, **kwargs):
        return super().export(request, *args, **kwargs)
