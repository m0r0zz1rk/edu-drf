from drf_yasg.utils import swagger_auto_schema

from apps.applications.api.applications_view_set import ApplicationsViewSet
from apps.applications.exceptions.course_certificate import DuplicateCertificateInfo
from apps.applications.selectors.course_certificate import course_certificate_orm, course_certificate_queryset, \
    CourseCertificateFilter
from apps.applications.serializers.course_certificate import CourseCertificateListSerializer, \
    CourseCertificateUpdateSerializer, CourseCertificateGenerateSerializer
from apps.applications.services.course_certificate import course_certificate_service
from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import APPLICATIONS


class CourseCertificateViewSet(ApplicationsViewSet):
    orm = course_certificate_orm
    queryset = course_certificate_queryset()
    serializer_class = CourseCertificateListSerializer
    base_serializer = CourseCertificateListSerializer
    update_serializer = CourseCertificateUpdateSerializer
    filterset_class = CourseCertificateFilter
    swagger_object_name = 'Удостоверения к заявкам на курсы'

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
        operation_description="Получение объекта курса (ОУ)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': serializer_class
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'"{swagger_object_name}" получен',
        f'Ошибка при получении "{swagger_object_name}"'
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Обновление объекта",
        request_body=update_serializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении',
            '200': 'Сообщение "Информация успешно обновлена"'
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'"{swagger_object_name}" успешно обновлен',
        f'Ошибка при обновлении "{swagger_object_name}"'
    )
    def partial_update(self, request, *args, **kwargs):
        serialize = self.update_serializer(data=request.data)
        if serialize.is_valid():
            try:
                course_certificate_service.save_certificate(
                    self.kwargs['object_id'],
                    serialize.validated_data
                )
                return response_utils.ok_response('Информация успешно обновлена')
            except DuplicateCertificateInfo:
                return response_utils.bad_request_response('Дубликат удостоверения')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Заявки. {swagger_object_name}', ],
        operation_description="Генерация информации для удостоверений группы",
        request_body=CourseCertificateGenerateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении',
            '200': 'Сообщение "Информация успешно сгенерирована"'
        }
    )
    @view_set_journal_decorator(
        APPLICATIONS,
        f'Генерация информации об удостоверениях успешно выполнена',
        f'Ошибка при генерации информации об удостоверениях"'
    )
    def generate(self, request, *args, **kwargs):
        serialize = CourseCertificateGenerateSerializer(data=request.data)
        if serialize.is_valid():
            try:
                course_certificate_service.generate_certificates_data(serialize.validated_data)
                return response_utils.ok_response('Информация успешно обновлена')
            except DuplicateCertificateInfo:
                return response_utils.bad_request_response('Дубликат удостоверения')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')
