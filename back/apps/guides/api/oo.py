from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.pagination import CustomPagination
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.selectors.oo import OoFilter
from apps.guides.operations.add_update_guides_rec import AddUpdateGuidesRec
from apps.guides.operations.delete_guides_rec import DeleteGuidesRec
from apps.guides.serializers.oo import oo_model, OoListSerializer, OoCreateSerializer, \
    OoUpdateSerializer
from apps.guides.services.mo import MoService
from apps.guides.services.oo_type import OoTypeService
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class OoViewSet(viewsets.ModelViewSet):
    """Работа с ОО в модуле Справочников"""
    ju = JournalService()
    respu = ResponseUtils()
    mu = MoService()
    otu = OoTypeService()

    queryset = oo_model.objects.all().order_by('date_create')
    serializer_class = OoListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = OoFilter

    @swagger_auto_schema(
        tags=['Cправочник "ОО"', ],
        operation_description="Получение списка ОО",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': OoListSerializer(many=True)
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
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при получении списка ОО'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочник "ОО"', ],
        operation_description="Добавление ОО",
        request_body=OoCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении ОО',
            '200': 'Сообщение "ОО успешно добавлена"'
        }
    )
    def create(self, request, *args, **kwargs):
        serialize = OoCreateSerializer(data=request.data)
        if serialize.is_valid():
            process_data = serialize.data
            for key in process_data.keys():
                if key == 'mo':
                    process_data[key] = self.mu.get_mo_object_by_name(serialize.data[key])
                if key == 'oo_type':
                    process_data[key] = self.otu.get_oo_type_object_by_name(serialize.data[key])
            process = AddUpdateGuidesRec(
                'Oo',
                process_data
            )
            if process.process_completed:
                return self.respu.ok_response('ОО успешно добавлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при добавлении ОО - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочник "ОО"', ],
        operation_description="Обновление ОО",
        request_body=OoUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении ОО',
            '200': 'Сообщение "ОО успешно обновлена"'
        }
    )
    def update(self, request, *args, **kwargs):
        serialize = OoUpdateSerializer(data=request.data)
        if serialize.is_valid():
            process_data = serialize.data
            for key in process_data.keys():
                if key == 'mo':
                    process_data[key] = self.mu.get_mo_object_by_name(serialize.data[key])
                if key == 'oo_type':
                    process_data[key] = self.otu.get_oo_type_object_by_name(serialize.data[key])
            process = AddUpdateGuidesRec(
                'Oo',
                process_data
            )
            if process.process_completed:
                return self.respu.ok_response('ОО успешно обновлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при обновлении ОО - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочник "ОО"', ],
        operation_description="Удаление ОО",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении ОО',
            '200': 'Сообщение "ОО успешно удалена"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            process = DeleteGuidesRec(
                'Oo',
                {
                    'object_id': self.kwargs['object_id'],
                }
            )
            if process.process_completed:
                return self.respu.ok_response('ОО успешно удалена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Системная ошибка при удалени ОО'
                },
                repr(self.kwargs),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка')
