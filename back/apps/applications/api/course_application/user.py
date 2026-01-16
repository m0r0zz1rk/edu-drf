from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from apps.applications.api.applications_view_set import ApplicationsViewSet
from apps.applications.consts.application_statuses import DRAFT
from apps.applications.selectors.course_application import course_application_orm, course_application_queryset, \
    CourseApplicationFilter
from apps.applications.serializers.base_application import BaseApplicationSerializer
from apps.applications.serializers.base_application.payment_data_serializer import PaymentDataSerializer
from apps.applications.serializers.base_application.response_application_create_serializer import \
    ApplicationCreateSerializer
from apps.applications.serializers.base_application.study_url_serializer import StudyUrlSerializer
from apps.applications.serializers.course_application import CourseApplicationDetailSerializer, CourseApplicationUpdateSerializer
from apps.applications.services.base_application import base_application_service
from apps.applications.services.course_application import course_application_service
from apps.authen.services.profile import profile_service
from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import APPLICATIONS


class CourseApplicationUserViewSet(ApplicationsViewSet):
    permission_classes = [IsAuthenticated, ]

    orm = course_application_orm
    queryset = course_application_queryset()
    filterset_class = CourseApplicationFilter
    serializer_class = BaseApplicationSerializer
    base_serializer = CourseApplicationDetailSerializer
    create_serializer = ApplicationCreateSerializer
    update_serializer = CourseApplicationUpdateSerializer
    swagger_object_name = 'Заявка на курс (ОУ) (обучающийся)'

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
        profile_id = profile_service.get_profile_or_info_by_attribute(
            'django_user_id',
            request.user.id,
            'profile_id'
        )
        # apps = course_application_service.get_departments_apps(request.user.id)
        apps = course_application_service.get_active_apps(profile_id)
        queryset = self.filter_queryset(apps)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Получение списка архивных заявок",
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
    def archive_list(self, request, *args, **kwargs):
        profile_id = profile_service.get_profile_or_info_by_attribute(
            'django_user_id',
            request.user.id,
            'profile_id'
        )
        # apps = course_application_service.get_departments_apps(request.user.id)
        apps = course_application_service.get_archive_apps(profile_id)
        queryset = self.filter_queryset(apps)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
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
        operation_description="Получение данных об оплате",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': PaymentDataSerializer
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'Данные об оплате "{swagger_object_name}" получены',
        f'Ошибка при получении данных об оплате "{swagger_object_name}"'
    )
    def payment(self, request, *args, **kwargs):
        data = base_application_service.get_payment_data(course_application_orm, self.kwargs['app_id'])
        serializer = PaymentDataSerializer(data)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Получение ссылки на обучение",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении ссылки',
            '200': 'Ссылка на обучение'
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        'Ссылка на обучение получена',
        'Ошибка при получении ссылки на обучение'
    )
    def study_url(self, request, *args, **kwargs):
        data = base_application_service.get_study_url(course_application_orm, self.kwargs['app_id'])
        serializer = StudyUrlSerializer(data)
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
                course_application_orm
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
        serialize = self.update_serializer(data=request.data)
        if serialize.is_valid():
            base_application_service.save_app(
                self.orm,
                course_application_service.get_course_app,
                self.kwargs['object_id'],
                serialize.validated_data
            )
            return response_utils.ok_response('Обновление выполнено')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Удаление записи",
        responses=SWAGGER_TEXT['delete']
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'Запись "{swagger_object_name}" успешно удалена',
        f'Ошибка при удалении записи "{swagger_object_name}"'
    )
    def destroy(self, request, *args, **kwargs):
        app = course_application_service.get_course_app(self.kwargs.get('object_id'))
        if app.status == DRAFT:
            return super().destroy(request, *args, **kwargs)
        return response_utils.bad_request_response('Нельзя удалить заявку (удаление только для черновиков)')
