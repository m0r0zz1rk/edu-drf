from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.selectors.event_type import event_type_queryset
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.operations.add_update_guides_rec import AddUpdateGuidesRec
from apps.guides.operations.delete_guides_rec import DeleteGuidesRec
from apps.guides.serializers.event_type import EventTypeListUpdateSerializer, \
    EventTypeBaseSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class EventTypeViewSet(viewsets.ModelViewSet):
    """Работа с типами мероприятий в модуле Справочников"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ju = JournalService()
    respu = ResponseUtils()

    queryset = event_type_queryset()
    serializer_class = EventTypeListUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NameFieldFilter

    @swagger_auto_schema(
        tags=['Cправочники. Типы мероприятий', ],
        operation_description="Получение списка типов мероприятий",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': EventTypeListUpdateSerializer(many=True)
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
                    'description': 'Ошибка при получении списка типов мероприятий'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочники. Типы мероприятий', ],
        operation_description="Добавление типа мероприятий",
        request_body=EventTypeBaseSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении типа мероприятий',
            '200': 'Сообщение "Тип мероприятий успешно добавлен"'
        }
    )
    def create(self, request, *args, **kwargs):
        serialize = EventTypeBaseSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'EventType',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('Тип мероприятий успешно добавлен')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при добавлении типа мероприятий - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочники. Типы мероприятий', ],
        operation_description="Обновление типа мероприятий",
        request_body=EventTypeListUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении типа мероприятий',
            '200': 'Сообщение "Тип мероприятий успешно обновлен"'
        }
    )
    def update(self, request, *args, **kwargs):
        serialize = EventTypeListUpdateSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'EventType',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('Тип мероприятий успешно обновлен')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при обновлении типа мероприятий - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочники. Типы мероприятий', ],
        operation_description="Удаление типа мероприятий",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении типа мероприятий',
            '200': 'Сообщение "Тип мероприятий успешно удален"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            process = DeleteGuidesRec(
                'EventType',
                {
                    'object_id': self.kwargs['object_id'],
                }
            )
            if process.process_completed:
                return self.respu.ok_response('Тип мероприятий успешно удалено')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Системная ошибка при удалени типа мероприятий'
                },
                repr(self.kwargs),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка')
