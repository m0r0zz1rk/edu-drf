from drf_yasg.utils import swagger_auto_schema

from apps.applications.api.applications_view_set import ApplicationsViewSet
from apps.applications.consts.application_statuses import WAIT_PAY
from apps.applications.selectors.application_filter import ApplicationFilter
from apps.applications.selectors.course_application import course_application_orm, course_application_queryset
from apps.applications.serializers.base_application import ApplicationOOUpdateSerializer, \
    ApplicationPayAcceptSerializer, ApplicationPayDenySerializer
from apps.applications.serializers.base_application.check_data.base_application_move import AppMoveSerializer, \
    AppMoveAllSerializer
from apps.applications.serializers.course_application import CourseAppGroupListSerializer, \
    CourseApplicationDetailSerializer, CourseApplicationUpdateSerializer, CourseApplicationEduUpdateSerializer
from apps.applications.services.base_application import base_application_service
from apps.applications.services.course_application import course_application_service
from apps.celery_app.tasks import email_pay_accept, email_pay_denied
from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import APPLICATIONS


class CourseApplicationAdminViewSet(ApplicationsViewSet):
    orm = course_application_orm
    queryset = course_application_queryset()
    serializer_class = CourseAppGroupListSerializer
    base_serializer = CourseApplicationDetailSerializer
    update_serializer = CourseApplicationUpdateSerializer
    filterset_class = ApplicationFilter
    swagger_object_name = 'Заявка на курс (ОУ) (администратор)'

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
        return super().list(request, *args, **kwargs)

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
        serializer = self.update_serializer
        # При запросе проверки ОО
        if len(request.data.keys()) == 2:
            serializer = ApplicationOOUpdateSerializer
        # При запросе проверки документов об образовании
        if len(request.data.keys()) == 5:
            serializer = CourseApplicationEduUpdateSerializer
        # При подтверждении оплаты
        if len(request.data.keys()) == 1 and 'status' in request.data.keys():
            serializer = ApplicationPayAcceptSerializer
        serialize = serializer(
            data=request.data
        )
        if serialize.is_valid():
            base_application_service.save_app(
                course_application_orm,
                course_application_service.get_course_app,
                self.kwargs['object_id'],
                serialize.validated_data
            )
            # Отправка письма об успешной оплате
            if serializer == ApplicationPayAcceptSerializer:
                email_pay_accept.delay(self.kwargs['object_id'])
            return response_utils.ok_response('Обновление выполнено')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Перемещение заявки группы",
        request_body=AppMoveSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при переносе заявки',
            '200': 'Сообщение "Перемещение выполнено"'
        },
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        'Заявка на курс успешно перенесена',
        'Ошибка при переносе заявки на курс"'
    )
    def one_move(self, request, *args, **kwargs):
        serialize = AppMoveSerializer(data=request.data)
        if serialize.is_valid():
            base_application_service.move_application(
                course_application_orm,
                serialize.validated_data.get('application_id'),
                serialize.validated_data.get('group_id')
            )
            return response_utils.ok_response('Перемещение выполнено')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Перемещение всех заявок группы",
        request_body=AppMoveAllSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при переносе заявки',
            '200': 'Сообщение "Перемещение выполнено"'
        },
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        'Заявки на курс учебной группы успешно перенесены',
        'Ошибка при переносе заявок на курс учебной группы"'
    )
    def all_move(self, request, *args, **kwargs):
        serialize = AppMoveAllSerializer(data=request.data)
        if serialize.is_valid():
            base_application_service.move_group_applications(
                course_application_orm,
                serialize.validated_data.get('source_group_id'),
                serialize.validated_data.get('destination_group_id')
            )
            return response_utils.ok_response('Перемещение выполнено')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Отклонение оплаты",
        request_body=ApplicationPayDenySerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при выполнении запроса',
            '200': 'Сообщение "Оплата успешно отклонена"'
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'Оплата в "{swagger_object_name}" успешно отклонена',
        f'Ошибка при отклонении оплаты в "{swagger_object_name}"'
    )
    def pay_denied(self, request, *args, **kwargs):
        serialize = ApplicationPayDenySerializer(data=request.data)
        if serialize.is_valid():
            base_application_service.save_app(
                course_application_orm,
                course_application_service.get_course_app,
                self.kwargs['object_id'],
                {'status': WAIT_PAY}
            )
            email_pay_denied.delay(
                self.kwargs['object_id'],
                serialize.validated_data.get('message')
            )
            return response_utils.ok_response('Оплата успешно отклонена')
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
        return super().destroy(request, *args, **kwargs)
