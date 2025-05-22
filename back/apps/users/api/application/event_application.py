from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from apps.applications.selectors.event_application import event_application_orm, event_application_queryset
from apps.applications.serializers.base_application import RequestApplicationCreateSerializer, BaseApplicationSerializer
from apps.applications.serializers.event_application import EventApplicationListSerializer, \
    EventApplicationUpdateSerializer, EventApplicationDetailSerializer
from apps.applications.services.event_application import event_application_service
from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import USERS
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.users.api.users_viewset import UsersViewSet


class EventApplicationViewSet(UsersViewSet):
    permission_classes = [IsAuthenticated, ]

    orm = event_application_orm
    queryset = event_application_queryset()
    serializer_class = EventApplicationListSerializer
    base_serializer = BaseApplicationSerializer
    retrieve_serializer = EventApplicationDetailSerializer
    create_serializer = RequestApplicationCreateSerializer
    update_serializer = EventApplicationUpdateSerializer
    swagger_object_name = 'Заявки на мероприятия (ИКУ)'

    @swagger_auto_schema(
        tags=[f'Обучающиеся. {swagger_object_name}', ],
        operation_description="Получение списка",
        responses={
            **SWAGGER_TEXT['list'],
            '200': serializer_class(many=True)
        }
    )
    @view_set_journal_decorator(
        USERS,
        f'Список "{swagger_object_name}" получен',
        f'Ошибка при получении списка "{swagger_object_name}"'
    )
    def list(self, request, *args, **kwargs):
        if 'profile_id' in request.GET:
            if not request.user.is_superuser:
                raise APIProcessError
            apps = event_application_service.get_all_apps(
                request.GET['profile_id']
            )
            page = self.paginate_queryset(apps)
            if page is not None:
                serializer = self.base_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.base_serializer(apps, many=True)
        else:
            apps = event_application_service.get_departments_apps(request.user.id)
            serializer = self.get_serializer(apps, many=True)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Обучающиеся. {swagger_object_name}', ],
        operation_description="Получение объекта",
        responses={
            **SWAGGER_TEXT['retrieve'],
            '200': serializer_class(many=True)
        }
    )
    @view_set_journal_decorator(
        USERS,
        f'Список "{swagger_object_name}" получен',
        f'Ошибка при получении списка "{swagger_object_name}"'
    )
    def retrieve(self, request, *args, **kwargs):
        app = event_application_service.get_course_app(
            self.kwargs['object_id']
        )
        serialize = self.retrieve_serializer(app)
        return response_utils.ok_response_dict(serialize.data)
