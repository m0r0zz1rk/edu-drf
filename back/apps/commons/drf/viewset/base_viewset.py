from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.response import response_utils
from apps.docs.services.table_export import TableExport
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import journal_service


class BaseViewSet(viewsets.ModelViewSet):
    """
    Класс вьюсета для справочников
    """

    # Статика
    dfb = DjangoFilterBackend()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    lookup_field = 'object_id'

    # Изменяемые параметры
    permission_classes = [IsAuthenticated, IsAdministrators]
    orm = queryset = None
    module = COMMON
    serializer_class = base_serializer = create_serializer = update_serializer = Serializer
    swagger_object_name = 'Объект'

    def list(self, request, *args, **kwargs):
        """Эндпоинт на получение списка записей"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response_utils.ok_response_dict(serializer.data)

    def create(self, request, *args, **kwargs):
        """Эндпоинт на добавление новой записи"""
        serialize = self.create_serializer(data=request.data)
        if serialize.is_valid():
            self.orm.create_record(serialize.data)
            return response_utils.ok_response('Добавление выполнено')
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Ошибка при добавлении типа мероприятий - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    def partial_update(self, request, *args, **kwargs):
        """Эндпоинт на обновление записи"""
        serialize = self.update_serializer(data=request.data)
        if serialize.is_valid():
            self.orm.update_record(
                {'object_id': self.kwargs['object_id']},
                serialize.validated_data
            )
            return response_utils.ok_response('Обновление выполнено')
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': self.module,
                    'status': ERROR,
                    'description': f'Ошибка при обновлении "{self.swagger_object_name}" - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    def destroy(self, request, *args, **kwargs):
        """Эндпоинт на удаление записи"""
        self.orm.delete_record({'object_id': self.kwargs['object_id']})
        return response_utils.ok_response('Удаление выполнено')

    def export(self, request, *args, **kwargs):
        """Эндпоинт для выгрузки записей в excel"""
        if len(request.GET) == 0 or request.GET.get('all') == 'true':
            queryset = self.get_queryset()
        else:
            queryset = self.filter_queryset(self.get_queryset())
        excel_export = TableExport(
            model=self.orm.model,
            queryset=queryset
        )
        return excel_export.get_excel()
