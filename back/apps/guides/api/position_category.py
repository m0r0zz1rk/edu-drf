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
from apps.guides.selectors.position_category import position_category_queryset
from apps.guides.serializers.position_category import PositionCategoryListUpdateSerializer, \
    PositionCategoryBaseSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class PositionCategoryViewSet(viewsets.ModelViewSet):
    """Работа с категориями должностей в модуле Справочников"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ju = JournalService()
    respu = ResponseUtils()

    queryset = position_category_queryset()
    serializer_class = PositionCategoryListUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NameFieldFilter

    @swagger_auto_schema(
        tags=['Cправочник "Категории должностей"', ],
        operation_description="Получение списка категорий должностей",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': PositionCategoryListUpdateSerializer(many=True)
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
                    'description': 'Ошибка при получении списка категорий должностей'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочник "Категории должностей"', ],
        operation_description="Добавление категории должностей",
        request_body=PositionCategoryBaseSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении категории должностей',
            '200': 'Сообщение "Категория должностей успешно добавлена"'
        }
    )
    def create(self, request, *args, **kwargs):
        serialize = PositionCategoryBaseSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'PositionCategory',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('Категория должностей успешно добавлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при добавлении категории должностей - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочник "Категории должностей"', ],
        operation_description="Обновление категории должностей",
        request_body=PositionCategoryListUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении категории должностей',
            '200': 'Сообщение "Категория должностей успешно обновлена"'
        }
    )
    def update(self, request, *args, **kwargs):
        serialize = PositionCategoryListUpdateSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'PositionCategory',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('Категория должностей успешно обновлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при обновлении категории должностей- данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочник "Категории должностей"', ],
        operation_description="Удаление категории должностей",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении категории должностей',
            '200': 'Сообщение "Категория должностей успешно удалена"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            process = DeleteGuidesRec(
                'PositionCategory',
                {
                    'object_id': self.kwargs['object_id'],
                }
            )
            if process.process_completed:
                return self.respu.ok_response('Категория должностей успешно удалена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Системная ошибка при удалени категории должностей'
                },
                repr(self.kwargs),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка')
