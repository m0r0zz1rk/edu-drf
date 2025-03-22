from drf_yasg.utils import swagger_auto_schema

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.edu.api.edu_viewset import EduViewSet
from apps.edu.selectors.services.education_service import education_service_queryset, EducationServiceFilter, \
    education_service_orm

from apps.edu.serializers.services.education_service import EducationServiceListSerializer, \
    EducationServiceRetrieveSerializer, EducationServiceAddUpdateSerializer
from apps.edu.services.service.education_service import education_service_service
from apps.journal.consts.journal_modules import EDU


class EducationServiceViewSet(EduViewSet):
    orm = education_service_orm
    queryset = education_service_queryset()
    serializer_class = EducationServiceListSerializer
    base_serializer = EducationServiceAddUpdateSerializer
    create_serializer = EducationServiceAddUpdateSerializer
    update_serializer = EducationServiceAddUpdateSerializer
    filterset_class = EducationServiceFilter
    swagger_object_name = 'Курс (ОУ)'

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
            '200': EducationServiceRetrieveSerializer
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'"{swagger_object_name}" получен',
        f'Ошибка при получении "{swagger_object_name}"'
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serialize = EducationServiceRetrieveSerializer(instance)
        return response_utils.ok_response_dict(serialize.data)

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
        serialize = EducationServiceAddUpdateSerializer(data=request.data)
        if serialize.is_valid():
            education_service_service.create_service(serialize.validated_data)
            return response_utils.ok_response('Добавление выполнено')
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
        serialize = EducationServiceAddUpdateSerializer(data=request.data)
        if serialize.is_valid():
            education_service_service.update_service(self.kwargs['object_id'], serialize.validated_data)
            return response_utils.ok_response('Обновление выполнено')
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
