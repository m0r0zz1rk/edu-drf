from drf_yasg.utils import swagger_auto_schema

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.guides.api.guide_viewset import GuideViewSet
from apps.guides.selectors.oo import OoFilter, oo_queryset, oo_orm
from apps.guides.serializers.oo import OoListSerializer, OoCreateSerializer, \
    OoUpdateSerializer
from apps.guides.services.oo import oo_service
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import journal_service


class OoViewSet(GuideViewSet):
    orm = oo_orm
    queryset = oo_queryset()
    serializer_class = OoListSerializer
    base_serializer = OoCreateSerializer
    create_serializer = OoCreateSerializer
    update_serializer = OoUpdateSerializer
    filterset_class = OoFilter
    swagger_object_name = 'ОО'

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Получение списка",
        responses={
            **SWAGGER_TEXT['list'],
            '200': serializer_class(many=True)
        }
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Список "{swagger_object_name}" получен',
        f'Ошибка при получении списка "{swagger_object_name}"'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Добавление записи",
        request_body=create_serializer,
        responses=SWAGGER_TEXT['create']
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Запись "{swagger_object_name}" успешно добавлена',
        f'Ошибка при добавлении записи "{swagger_object_name}"'
    )
    def create(self, request, *args, **kwargs):
        serialize = OoCreateSerializer(data=request.data)
        if serialize.is_valid():
            return oo_service.create_oo(serialize.data)
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при добавлении ОО - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Обновление записи",
        request_body=update_serializer,
        responses=SWAGGER_TEXT['update']
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Запись "{swagger_object_name}" успешно обновлена',
        f'Ошибка при обновлении записи "{swagger_object_name}"'
    )
    def partial_update(self, request, *args, **kwargs):
        serialize = OoUpdateSerializer(data=request.data)
        if serialize.is_valid():
            return oo_service.update_oo(serialize.data)
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при обновлении ОО - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Удаление записи",
        responses=SWAGGER_TEXT['delete']
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Запись "{swagger_object_name}" успешно удалена',
        f'Ошибка при удалении записи "{swagger_object_name}"'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Экспорт записей",
        responses=SWAGGER_TEXT['export']
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Экспорт записей "{swagger_object_name}" успешно выполнен',
        f'Ошибка при выполнении экспорта записей "{swagger_object_name}"'
    )
    def export(self, request, *args, **kwargs):
        return super().export(request, *args, **kwargs)