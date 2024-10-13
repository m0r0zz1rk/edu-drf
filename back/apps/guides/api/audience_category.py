from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.selectors.audience_category import audience_category_queryset
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.operations.add_update_guides_rec import AddUpdateGuidesRec
from apps.guides.operations.delete_guides_rec import DeleteGuidesRec
from apps.guides.serializers.audience_category import AudienceCategoryListUpdateSerializer, \
    AudienceCategoryBaseSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class AudienceCategoryViewSet(viewsets.ModelViewSet):
    """Работа с категориями слушателей в модуле Справочников"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ju = JournalService()
    respu = ResponseUtils()

    queryset = audience_category_queryset()
    serializer_class = AudienceCategoryListUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NameFieldFilter

    @swagger_auto_schema(
        tags=['Cправочники. Категории слушателей', ],
        operation_description="Получение списка категорий слушателей",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': AudienceCategoryListUpdateSerializer(many=True)
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
                    'description': 'Ошибка при получении списка категорий слушателей'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочники. Категории слушателей"', ],
        operation_description="Добавление категории слушателей",
        request_body=AudienceCategoryBaseSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении категории слушателей',
            '200': 'Сообщение "Категория слушателей успешно добавлена"'
        }
    )
    def create(self, request, *args, **kwargs):
        serialize = AudienceCategoryBaseSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'AudienceCategory',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('Категория слушателей успешно добавлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при добавлении категории слушателей - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочники. Категории слушателей', ],
        operation_description="Обновление категории слушателей",
        request_body=AudienceCategoryListUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении категории слушателей',
            '200': 'Сообщение "Категория слушателей успешно обновлена"'
        }
    )
    def update(self, request, *args, **kwargs):
        serialize = AudienceCategoryListUpdateSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateGuidesRec(
                'AudienceCategory',
                serialize.data
            )
            if process.process_completed:
                return self.respu.ok_response('Категория слушателей успешно обновлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при обновлении категории слушателей- данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return self.respu.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=['Cправочники. Категории слушателей', ],
        operation_description="Удаление категории слушателей",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении категории слушателей',
            '200': 'Сообщение "Категория слушателей успешно удалена"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            process = DeleteGuidesRec(
                'AudienceCategory',
                {
                    'object_id': self.kwargs['object_id'],
                }
            )
            if process.process_completed:
                return self.respu.ok_response('Категория слушателей успешно удалена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Системная ошибка при удалени категории слушателей'
                },
                repr(self.kwargs),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка')
