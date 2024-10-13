from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.operations.add_update_guides_rec import AddUpdateGuidesRec
from apps.guides.operations.delete_guides_rec import DeleteGuidesRec
from apps.guides.selectors.oo_type import oo_type_queryset
from apps.guides.serializers.oo_type import OoTypeListUpdateSerializer, OoTypeBaseSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class OoTypeViewSet(viewsets.ModelViewSet):
    """Работа с типами ОО в модуле Справочников"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ju = JournalService()
    respu = ResponseUtils()

    queryset = oo_type_queryset()
    serializer_class = OoTypeListUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NameFieldFilter

    @swagger_auto_schema(
        tags=['Cправочники. Типы ОО', ],
        operation_description="Получение списка типов ОО",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': OoTypeListUpdateSerializer(many=True)
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
                    'description': 'Ошибка при получении списка типов ОО'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочники. Типы ОО', ],
        operation_description="Добавление типа ОО",
        request_body=OoTypeBaseSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении типа ОО',
            '200': 'Сообщение "Тип ОО успешно добавлен"'
        }
    )
    def create(self, request, *args, **kwargs):
        serialize = OoTypeBaseSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'OoType',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('Тип ОО успешно добавлен')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при добавлении типа ОО - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочники. Типы ОО', ],
        operation_description="Обновление типа ОО",
        request_body=OoTypeListUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении типа ОО',
            '200': 'Сообщение "Тип ОО успешно обновлен"'
        }
    )
    def update(self, request, *args, **kwargs):
        serialize = OoTypeListUpdateSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'OoType',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('Тип ОО успешно обновлен')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при обновлении типа ОО - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочники. Типы ОО', ],
        operation_description="Удаление типа ОО",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении типа ОО',
            '200': 'Сообщение "Тип ОО успешно удален"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            process = DeleteGuidesRec(
                'OoType',
                {
                    'object_id': self.kwargs['object_id'],
                }
            )
            if process.process_completed:
                return self.respu.ok_response('Тип ОО успешно удален')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Системная ошибка при удалени типа ОО'
                },
                repr(self.kwargs),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка')
