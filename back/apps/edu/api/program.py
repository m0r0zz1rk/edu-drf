from drf_yasg.utils import swagger_auto_schema

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.request import request_utils
from apps.commons.utils.django.response import response_utils
from apps.edu.api.edu_viewset import EduViewSet
from apps.edu.selectors.program import ProgramFilter, program_queryset, approved_program_queryset, program_orm
from apps.edu.serializers.program import ProgramListSerializer, ProgramRetrieveAddUpdateSerializer
from apps.edu.services.calendar_chart import calendar_chart_service
from apps.edu.services.program import program_service
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import SUCCESS
from apps.journal.services.journal import journal_service


class ProgramViewSet(EduViewSet):
    orm = program_orm
    queryset = program_queryset()
    serializer_class = ProgramListSerializer
    filterset_class = ProgramFilter
    swagger_object_name = 'ДПП'

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
        operation_description="Получение списка утвержденных приказом ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': ProgramListSerializer(many=True)
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'Список утвержденных ДПП получен',
        f'Ошибка при получении списка утвержденных ДПП'
    )
    def approved_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(approved_program_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Получение объекта ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': ProgramRetrieveAddUpdateSerializer
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'ДПП получен',
        f'Ошибка при получении ДПП'
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProgramRetrieveAddUpdateSerializer(
            program_service.transform_instance_to_serializer(instance)
        )
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Создание копии ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при создании копии ДПП',
            '200': 'Сообщение "Копия ДПП успешно создана"'
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'Копия ДПП создана',
        f'Ошибка при создании копии ДПП'
    )
    def copy(self, request, *args, **kwargs):
        program_id = program_service.copy_program(
            self.kwargs['object_id'],
        )
        calendar_chart_service.copy_calendar_chart(
            self.kwargs['object_id'],
            program_id
        )
        return response_utils.ok_response('Копия ДПП успешно создана')

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Изменение пользователя, редактирующего КУГ ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': 'Пользователь успешно установлен'
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'Изменен пользователь, редактирующий КУГ ДПП',
        f'Ошибка при изменении пользователя, редактирующего КУГ ДПП'
    )
    def set_kug_edit(self, request, *args, **kwargs):
        proc = program_service.set_kug_edit(
            self.kwargs['program_id'],
            request.user.id
        )
        if proc:
            return response_utils.ok_response_no_data()
        else:
            return response_utils.bad_request_no_data()

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Добавление записи",
        request_body=ProgramRetrieveAddUpdateSerializer,
        responses=SWAGGER_TEXT['create']
    )
    @view_set_journal_decorator(
        EDU,
        f'Запись "{swagger_object_name}" успешно добавлена',
        f'Ошибка при добавлении записи "{swagger_object_name}"'
    )
    def create(self, request, *args, **kwargs):
        serialize = ProgramRetrieveAddUpdateSerializer(
            data=request_utils.convert_form_data_data(request.data)
        )
        if serialize.is_valid():
            program_service.create_program(request, serialize.data)
            return response_utils.ok_response('Добавление выполнено')
        else:
            return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Обновление записи",
        request_body=ProgramRetrieveAddUpdateSerializer,
        responses=SWAGGER_TEXT['update']
    )
    @view_set_journal_decorator(
        EDU,
        f'Запись "{swagger_object_name}" успешно обновлена',
        f'Ошибка при обновлении записи "{swagger_object_name}"'
    )
    def partial_update(self, request, *args, **kwargs):
        serialize = ProgramRetrieveAddUpdateSerializer(
            data=request_utils.convert_form_data_data(request.data)
        )
        if serialize.is_valid():
            program_service.create_program(request, serialize.data, False)
            return response_utils.ok_response('Обновление выполнено')
        else:
            return response_utils.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=[f'Учебная часть. {swagger_object_name}', ],
        operation_description="Получение файла приказа ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении ДПП',
            '200': 'Файл приказа ДПП'
        }
    )
    @view_set_journal_decorator(
        EDU,
        f'Файл приказа ДПП успешно получен',
        f'Ошибка при получении файла приказа ДПП"'
    )
    def get_order_file(self, request, *args, **kwargs):
        file = program_service.get_order_file(
            'object_id',
            self.kwargs.get('order_id')
        )
        journal_service.create_journal_rec(
            {
                'source': request_utils.get_source_display_name(request),
                'module': EDU,
                'status': SUCCESS,
                'description': 'Получение приказа ДПП'
            },
            {'order_id': self.kwargs.get('order_id')},
            None
        )
        return response_utils.file_response(file)

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
