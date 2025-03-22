from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.selectors.state import state_queryset, state_orm
from apps.guides.serializers.state.state_registration import StateRegistrationSerializer
from apps.journal.consts.journal_modules import GUIDES


class StateRegistrationViewSet(BaseViewSet):
    permission_classes = [permissions.AllowAny, ]
    module = GUIDES
    orm = state_orm
    queryset = state_queryset()
    serializer_class = StateRegistrationSerializer
    filterset_class = NameFieldFilter
    swagger_object_name = 'Государство (Регистрация)'

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
