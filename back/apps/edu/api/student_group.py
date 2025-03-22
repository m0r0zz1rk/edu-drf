from drf_yasg.utils import swagger_auto_schema

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.edu.api.edu_viewset import EduViewSet
from apps.edu.selectors.student_group import student_group_queryset, StudentGroupFilter, student_group_orm
from apps.edu.serializers.student_group import StudentGroupListSerializer, StudentGroupAddSerializer, \
    StudentGroupUpdateSerializer, StudentGroupServiceTypeSerializer, StudentGroupDocRequestSerializer
from apps.edu.services.student_group import student_group_service
from apps.journal.consts.journal_modules import EDU


class StudentGroupViewSet(EduViewSet):
    orm = student_group_orm
    queryset = student_group_queryset()
    serializer_class = StudentGroupListSerializer
    base_serializer = StudentGroupAddSerializer
    create_serializer = StudentGroupAddSerializer
    update_serializer = StudentGroupUpdateSerializer
    filterset_class = StudentGroupFilter
    swagger_object_name = 'Учебная группа'

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
        serializer = StudentGroupListSerializer(instance)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Получение типа услуги учебной группы",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении типа',
            '200': StudentGroupServiceTypeSerializer
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'Тип услуги учебной группы получен',
        f'Ошибка при получении типа услуги учебной группы'
    )
    def get_service_type(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.ou is not None:
            return response_utils.ok_response_dict({'service_type': 'ou'})
        return response_utils.ok_response_dict({'service_type': 'iku'})

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
        serialize = StudentGroupAddSerializer(data=request.data)
        if serialize.is_valid():
            student_group_service.create_group(serialize.validated_data)
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
        return super().partial_update(request, *args, **kwargs)

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

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Получение документа по учебной группе",
        request_body=StudentGroupDocRequestSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении документа',
            '200': 'HttpResponse с документом'
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'Документ по учебной группе успешно сформирован и отправлен',
        f'Ошибка при получении документа по учебной группе'
    )
    def doc(self, request, *args, **kwargs):
        serialize = StudentGroupDocRequestSerializer(data=request.data)
        if serialize.is_valid():
            return student_group_service.get_doc_response(
                group_id=serialize.validated_data.get('group_id'),
                doc_type=serialize.validated_data.get('doc_type')
            )
        else:
            return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')