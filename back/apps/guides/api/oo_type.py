from drf_yasg.utils import swagger_auto_schema

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.guides.api.guide_viewset import GuideViewSet
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.selectors.oo_type import oo_type_queryset, oo_type_orm
from apps.guides.serializers.oo_type import OoTypeListUpdateSerializer, OoTypeBaseSerializer
from apps.journal.consts.journal_modules import GUIDES


class OoTypeViewSet(GuideViewSet):
    orm = oo_type_orm
    queryset = oo_type_queryset()
    serializer_class = OoTypeListUpdateSerializer
    base_serializer = OoTypeBaseSerializer
    create_serializer = OoTypeBaseSerializer
    update_serializer = OoTypeListUpdateSerializer
    filterset_class = NameFieldFilter
    swagger_object_name = 'Тип ОО'

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
        return super().create(request, *args, **kwargs)

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
        return super().partial_update(request, *args, **kwargs)

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
