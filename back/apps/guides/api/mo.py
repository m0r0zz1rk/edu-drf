from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.selectors.mo import mo_queryset
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.operations.add_update_guides_rec import AddUpdateGuidesRec
from apps.guides.operations.delete_guides_rec import DeleteGuidesRec
from apps.guides.serializers.mo import MoListUpdateSerializer, MoBaseSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class MoViewSet(viewsets.ModelViewSet):
    """Работа с муниципальными образованиями в модуле Справочников"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ju = JournalService()
    respu = ResponseUtils()

    queryset = mo_queryset()
    serializer_class = MoListUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NameFieldFilter

    @swagger_auto_schema(
        tags=['Cправочник "МО"', ],
        operation_description="Получение списка МО",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': MoListUpdateSerializer(many=True)
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
                    'description': 'Ошибка при получении списка МО'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочник "МО"', ],
        operation_description="Добавление МО",
        request_body=MoBaseSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении МО',
            '200': 'Сообщение "МО успешно добавлено"'
        }
    )
    def create(self, request, *args, **kwargs):
        serialize = MoBaseSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'Mo',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('МО успешно добавлено')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при добавлении МО - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочник "МО"', ],
        operation_description="Обновление МО",
        request_body=MoListUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении МО',
            '200': 'Сообщение "МО успешно обновлено"'
        }
    )
    def update(self, request, *args, **kwargs):
        serialize = MoListUpdateSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'Mo',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('МО успешно обновлено')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при обновлении МО - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочник "МО"', ],
        operation_description="Удаление МО",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении МО',
            '200': 'Сообщение "МО успешно удалено"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            process = DeleteGuidesRec(
                'Mo',
                {
                    'object_id': self.kwargs['object_id'],
                }
            )
            if process.process_completed:
                return self.respu.ok_response('МО успешно удалено')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Системная ошибка при удалени МО'
                },
                repr(self.kwargs),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка')
