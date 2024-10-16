from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.applications.selectors.course_application import course_application_queryset, course_application_model
from apps.applications.serializers.base_application import RequestApplicationCreateSerializer, \
    ResponseApplicationCreateSerializer, BaseApplicationSerializer
from apps.applications.serializers.course_application import CourseApplicationListSerializer, \
    CourseApplicationDetailSerializer, CourseApplicationUpdateSerializer
from apps.applications.services.base_application import BaseApplicationService
from apps.applications.services.course_application import CourseApplicationService
from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_admin_or_student import IsAdminOrStudent
from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import USERS
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError


class CourseApplicationViewSet(viewsets.ModelViewSet):
    """Класс эндпоинтов для работы с заявками обучающихся на участие в курсах"""
    permission_classes = [IsAuthenticated, IsAdminOrStudent]

    _base_application_service = BaseApplicationService()
    _course_application_service = CourseApplicationService()
    _response_utils = ResponseUtils()
    _profile_service = ProfileService()
    _journal_request_builder = JournalRequestBuilder()

    queryset = course_application_queryset()
    serializer_class = CourseApplicationListSerializer
    pagination_class = CustomPagination
    lookup_field = "object_id"

    @swagger_auto_schema(
        tags=['Обучающиеся. Заявки на курс', ],
        operation_description="Получение списка активных заявок на участие в курсах",
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при получении списка',
            '200': CourseApplicationListSerializer(many=True) or BaseApplicationSerializer(many=True)
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении списка заявок на участие в курсах',
        'Произошла ошибка при получении списка заявок'
    )
    def list(self, request, *args, **kwargs):
        try:
            if 'profile_id' in request.GET:
                if not request.user.is_superuser:
                    raise APIProcessError
                apps = self._course_application_service.get_all_apps(
                    request.GET['profile_id'],
                    self.get_queryset()
                )
                page = self.paginate_queryset(apps)
                if page is not None:
                    serializer = BaseApplicationSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                serializer = BaseApplicationSerializer(apps, many=True)
            else:
                apps = self._course_application_service.get_departments_apps(
                    request.user.id,
                    self.get_queryset()
                )
                serializer = self.get_serializer(apps, many=True)
            return self._response_utils.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Обучающиеся. Заявки на курс', ],
        operation_description="Получение информации по заявке",
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при получении информации',
            '200': CourseApplicationDetailSerializer
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
            app = self._course_application_service.get_course_app(
                self.kwargs['object_id']
            )
            serialize = CourseApplicationDetailSerializer(app)
            return self._response_utils.ok_response_dict(serialize.data)
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Обучающиеся. Заявки на курс', ],
        operation_description="Создание заявки на участие в курсе",
        request_body=RequestApplicationCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при создании заявки',
            '200': ResponseApplicationCreateSerializer
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при создании заявки на участие в курсе',
        'Произошла ошибка при подачи заявки, обратитесь к администратору'
    )
    def create(self, request, *args, **kwargs):
        try:
            serialize = RequestApplicationCreateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                id_new_app = self._base_application_service.create_app(
                    request.user.id,
                    serialize.validated_data['group_id'],
                    course_application_model
                )
                JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        self._profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(USERS)
                    .set_status(SUCCESS)
                    .set_description('Создана заявка на участие в опросе')
                    .set_payload(repr(request.data))
                    .set_output('-')
                )
                return self._response_utils.ok_response_dict(
                    {
                        'app_id': id_new_app
                    }
                )
            else:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        self._profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(USERS)
                    .set_status(ERROR)
                    .set_description('Ошибка сериализации данных при создании заявки на участие в курсе')
                    .set_payload(repr(request.data) + f'\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.data))
                    .set_response_message('Не удалось сериализовать данные для подачи заявки')
                )
                return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Обучающиеся. Заявки на курс', ],
        operation_description="Обновление заявки на курс",
        request_body=CourseApplicationUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован',
            '400': 'Ошибка при обновлении заявки',
            '200': 'Заявка успешно сохранена'
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при обновлении заявки на курс',
        'Произошла ошибка в процессе обновления заявки'
    )
    def partial_update(self, request, *args, **kwargs):
        try:
            serialize = CourseApplicationUpdateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                self._course_application_service.save_app(
                    self.kwargs['object_id'],
                    serialize.validated_data
                )
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        self._profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(USERS)
                    .set_status(SUCCESS)
                    .set_description('Заявка на курс успешно обновлена')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Заявка успешно сохранена')
                )
                return journal_request.create_response()
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_source(
                    self._profile_service.get_profile_or_info_by_attribute(
                        'django_user_id',
                        request.user.id,
                        'display_name'
                    )
                )
                .set_module(USERS)
                .set_status(ERROR)
                .set_description('Ошибка сериализации при обновлении заявки на курс')
                .set_payload(repr(request.data))
                .set_output(repr(serialize.errors))
                .set_response_message('Произошла ошибка при попытке сохранить информацию по заявке')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
