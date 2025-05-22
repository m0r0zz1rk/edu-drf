from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from apps.applications.api.applications_view_set import ApplicationsViewSet
from apps.applications.selectors.event_application import event_application_orm, event_application_queryset, \
    event_application_model
from apps.applications.serializers.base_application import ResponseApplicationCreateSerializer
from apps.applications.serializers.event_application import EventApplicationListSerializer, \
    EventApplicationDetailSerializer, EventApplicationUpdateSerializer
from apps.applications.services.base_application import base_application_service
from apps.applications.services.event_application import event_application_service
from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import APPLICATIONS


class EventApplicationUserViewSet(ApplicationsViewSet):
    permission_classes = [IsAuthenticated, ]

    orm = event_application_orm
    queryset = event_application_queryset()
    serializer_class = EventApplicationListSerializer
    base_serializer = EventApplicationDetailSerializer
    create_serializer = ResponseApplicationCreateSerializer
    update_serializer = EventApplicationUpdateSerializer
    swagger_object_name = 'Заявка на мероприятие (ИКУ) (обучающийся)'

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Получение списка",
        responses={
            **SWAGGER_TEXT['list'],
            '200': serializer_class(many=True)
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'Список "{swagger_object_name}" получен',
        f'Ошибка при получении списка "{swagger_object_name}"'
    )
    def list(self, request, *args, **kwargs):
        apps = event_application_service.get_departments_apps(request.user.id)
        serializer = self.get_serializer(apps, many=True)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Получение объекта заявка на курс (ОУ)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': base_serializer
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'"{swagger_object_name}" получен',
        f'Ошибка при получении "{swagger_object_name}"'
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.base_serializer(instance)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Добавление записи",
        request_body=create_serializer,
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при добавлении записи',
            '200': 'app_id с UUID новой заявки'
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'Запись "{swagger_object_name}" успешно добавлена',
        f'Ошибка при добавлении записи "{swagger_object_name}"'
    )
    def create(self, request, *args, **kwargs):
        serialize = self.create_serializer(data=request.data)
        if serialize.is_valid():
            id_new_app = base_application_service.create_app(
                request.user.id,
                serialize.validated_data['group_id'],
                event_application_model
            )
            return response_utils.ok_response_dict({'app_id': id_new_app})
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Обновление записи",
        request_body=update_serializer,
        responses=SWAGGER_TEXT['update']
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'Запись "{swagger_object_name}" успешно обновлена',
        f'Ошибка при обновлении записи "{swagger_object_name}"'
    )
    def partial_update(self, request, *args, **kwargs):
        serialize = self.update_serializer(
            data=request.data
        )
        if serialize.is_valid():
            base_application_service.save_app(
                self.orm,
                event_application_service.get_event_app,
                self.kwargs['object_id'],
                serialize.validated_data
            )
            return response_utils.ok_response('Обновление выполнено')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')
