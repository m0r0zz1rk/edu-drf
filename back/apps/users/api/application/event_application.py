from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from apps.applications.selectors.event_application import event_application_queryset
from apps.applications.serializers.base_application import BaseApplicationSerializer
from apps.applications.services.event_application import event_application_service
from apps.applications.serializers.event_application import EventApplicationListSerializer, \
    EventApplicationDetailSerializer
from apps.commons.pagination import CustomPagination
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import USERS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.users.api.users_viewset import UsersViewSet


class EventApplicationViewSet(UsersViewSet):
    """Класс эндпоинтов для работы с заявками обучающихся на участие в мероприятиях"""
    permission_classes = [IsAuthenticated, ]

    queryset = event_application_queryset()
    serializer_class = EventApplicationListSerializer
    pagination_class = CustomPagination
    lookup_field = "object_id"

    @swagger_auto_schema(
        tags=['Обучающиеся. Заявки на мероприятие', ],
        operation_description="Получение списка активных заявок на участие в мероприятиях",
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при получении списка',
            '200': EventApplicationListSerializer(many=True) or BaseApplicationSerializer(many=True)
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении списка заявок на участие в мероприятиях',
        'Произошла ошибка при получении списка заявок'
    )
    def list(self, request, *args, **kwargs):
        try:
            if 'profile_id' in request.GET:
                if not request.user.is_superuser:
                    raise APIProcessError
                apps = event_application_service.get_all_apps(request.GET['profile_id'])
                page = self.paginate_queryset(apps)
                if page is not None:
                    serializer = BaseApplicationSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                serializer = BaseApplicationSerializer(apps, many=True)
            else:
                apps = event_application_service.get_departments_apps(request.user.id)
                serializer = self.get_serializer(apps, many=True)
            return response_utils.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Обучающиеся. Заявки на мероприятия', ],
        operation_description="Получение информации по заявке",
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при получении информации',
            '200': EventApplicationDetailSerializer
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении информации по заявке на курс',
        'Произошла ошибка при получении информации по заявке'
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            app = event_application_service.get_event_app(self.kwargs['object_id'])
            serialize = EventApplicationDetailSerializer(app)
            return response_utils.ok_response_dict(serialize.data)
        except Exception:
            raise APIProcessError
