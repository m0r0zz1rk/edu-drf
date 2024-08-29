from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.request import RequestUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.selectors.program import ProgramFilter, program_queryset, approved_program_queryset
from apps.edu.operations.program.add_update_program import AddUpdateProgramOperation
from apps.edu.operations.program.delete_program import DeleteProgramOperation
from apps.edu.serializers.program import (ProgramListSerializer,
                                          ProgramRetrieveAddUpdateSerializer,
                                          ProgramGetOrderSerializer)
from apps.edu.services.program import ProgramService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import JournalService


class ProgramViewSet(viewsets.ModelViewSet):
    """Работа с ДПП"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ru = RequestUtils()
    ju = JournalService()
    pu = ProfileService()
    pru = ProgramService()
    respu = ResponseUtils()

    queryset = program_queryset()
    lookup_field = "object_id"
    serializer_class = ProgramListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ProgramFilter

    @swagger_auto_schema(
        tags=['Учебная часть. ДПП', ],
        operation_description="Получение списка ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': ProgramListSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при получении списка ДПП'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. ДПП', ],
        operation_description="Получение списка утвержденных приказом ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': ProgramListSerializer(many=True)
        }
    )
    def approved_list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(approved_program_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при получении списка утвержденных приказом ДПП'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. ДПП', ],
        operation_description="Получение объекта ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': ProgramRetrieveAddUpdateSerializer
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProgramRetrieveAddUpdateSerializer(
                self.pru.transform_instance_to_serializer(instance)
            )
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при получении объекта ДПП'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. ДПП', ],
        operation_description="Создание копии ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при создании копии ДПП',
            '200': 'Сообщение "Копия ДПП успешно создана"'
        }
    )
    def copy(self, request, *args, **kwargs):
        try:
            proc = self.pru.copy_program(
                self.kwargs['object_id'],
            )
            if proc:
                return self.respu.ok_response('Копия ДПП успешно создана')
            else:
                return self.respu.bad_request_response('Ошибка при создании копии, повторите попытку позже')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при создании копии ДПП'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. ДПП', ],
        operation_description="Изменение пользователя, редактирующего КУГ ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': 'Пользователь успешно установлен'
        }
    )
    def set_kug_edit(self, request, *args, **kwargs):
        try:
            proc = self.pru.set_kug_edit(
                self.kwargs['program_id'],
                request.user.id
            )
            if proc:
                return self.respu.ok_response_no_data()
            else:
                return self.respu.bad_request_no_data()
        except:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при измении пользователя, редактурующего КУГ ДПП'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. ДПП', ],
        operation_description="Добавление/обновление ДПП",
        request_body=ProgramRetrieveAddUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении/обновлении ДПП',
            '200': 'Сообщение "ДПП успешно добавлена/обновлена"'
        }
    )
    def create_update(self, request, *args, **kwargs):
        serialize = ProgramRetrieveAddUpdateSerializer(
            data=self.ru.convert_form_data_data(request.data)
        )
        if serialize.is_valid():
            form_data = dict(serialize.data)
            if form_data['order_file'] is not None:
                del form_data['order_file']
                form_data['order_file'] = request.FILES['order_file']
            process = AddUpdateProgramOperation(
                form_data,
                request
            )
            if process.process_completed:
                return self.respu.ok_response('ДПП успешно добавлена/обновлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            return self.respu.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=['Учебная часть. ДПП', ],
        operation_description="Получение файла приказа ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении ДПП',
            '200': 'Файл приказа ДПП'
        }
    )
    def get_order_file(self, request, *args, **kwargs):
        serialize = ProgramGetOrderSerializer(
            data={'object_id': self.kwargs['order_id']}
        )
        if serialize.is_valid():
            file = self.pru.get_order_file(
                'object_id',
                serialize.data['object_id']
            )
            self.ju.create_journal_rec(
                {
                    'source': self.ru.get_source_display_name(request),
                    'module': EDU,
                    'status': SUCCESS,
                    'description': 'Получение приказа ДПП'
                },
                serialize.data,
                None
            )
            return self.respu.file_response(file)
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при получении файла приказа ДПП - данные не прошли сериализацию'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Данные не прошли валидацию')

    @swagger_auto_schema(
        tags=['Учебная часть. ДПП', ],
        operation_description="Удаление ДПП",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении ДПП',
            '200': 'Сообщение "ДПП успешно удалена"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            proc = DeleteProgramOperation(
                {'object_id': instance.object_id},
                request
            )
            if proc.process_completed:
                return self.respu.ok_response('ДПП успешно удалена')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при удалении ДПП'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
        return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
