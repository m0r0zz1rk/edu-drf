from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.utils.profile import ProfileUtils
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.request import RequestUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.filters.program import ProgramFilter
from apps.edu.operations.program.add_update_program_operation import AddUpdateProgramOperation
from apps.edu.serializers.program_serializers import ProgramListSerializer, program_model, ProgramAddSerializer, \
    ProgramGetOrderSerializer
from apps.edu.utils.program import ProgramUtils
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.utils.journal_utils import JournalUtils


class ProgramViewSet(viewsets.ModelViewSet):
    """Работа с ДПП"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ru = RequestUtils()
    ju = JournalUtils()
    pu = ProfileUtils()
    pru = ProgramUtils()
    respu = ResponseUtils()

    queryset = program_model.objects.all().order_by('-date_create')
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
        operation_description="Добавление ДПП",
        request_body=ProgramAddSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении ДПП',
            '200': 'Сообщение "ДПП успешно добавлена"'
        }
    )
    def create(self, request, *args, **kwargs):
        serialize = ProgramAddSerializer(data=request.data)
        if serialize.is_valid():
            print(serialize.validated_data)
            process = AddUpdateProgramOperation(dict(serialize.validated_data))
            if process.process_completed:
                return self.respu.ok_response('ДПП успешно добавлена')
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
            '200': 'Файл приказа ДПП"'
        }
    )
    def get_order_file(self, request, *args, **kwargs):
        serialize = ProgramGetOrderSerializer(data={'object_id': self.kwargs['order_id']})
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