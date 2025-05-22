from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.permissions.is_admin_or_coko import IsAdminOrCoko
from apps.commons.utils.django.response import response_utils
from apps.guides.api.guide_viewset import GuideViewSet
from apps.guides.selectors.profiles.coko import CokoFilter, coko_orm, coko_queryset
from apps.guides.serializers.coko import CokoSerializer, \
    CokoChangeCuratorGroupsSerializer
from apps.guides.services.coko import change_curator_groups
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import journal_service


class CokoViewSet(GuideViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrCoko]
    orm = coko_orm
    queryset = coko_queryset()
    serializer_class = CokoSerializer
    filterset_class = CokoFilter
    swagger_object_name = 'Профиль сотрудника ЦОКО'

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
        operation_description="Изменение параметра отображения только кураторских учебных групп",
        request_body=CokoChangeCuratorGroupsSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при изменении параметра',
            '200': 'Сообщение "Информация успешно обновлена"'
        }
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Отображение кураторских групп успешно изменено',
        f'Ошибка при изменении отображения кураторских групп"'
    )
    def change_curator_groups(self, request, *args, **kwargs):
        """Эндпоинт для изменения отображения кураторских групп у сотрудников ЦОКО"""
        serialize = CokoChangeCuratorGroupsSerializer(data=request.data)
        if serialize.is_valid():
            return change_curator_groups(request, serialize.data)
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при изменении кураторских групп - данные не прошли валидацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
        return response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')


# class CokoViewSet(viewsets.ModelViewSet):
#     """Работа с сотрудниками ЦОКО в модуле Справочник"""
#     permission_classes = [IsAuthenticated, IsAdministrators]
#     ju = JournalService()
#     pu = ProfileService()
#     respu = ResponseUtils()
#
#     queryset = coko_profile_queryset()
#     serializer_class = CokoSerializer
#     pagination_class = CustomPagination
#     filter_backends = [DjangoFilterBackend, ]
#     filterset_class = CokoFilter
#
#     @swagger_auto_schema(
#         tags=['Cправочники. Сотрудники ЦОКО', ],
#         operation_description="Получение списка пользователей",
#         responses={
#             '403': 'Пользователь не авторизован или не является администратором',
#             '400': 'Ошибка при получении списка',
#             '200': CokoSerializer(many=True)
#         }
#     )
#     def list(self, request, *args, **kwargs):
#         try:
#             queryset = self.filter_queryset(self.get_queryset())
#             page = self.paginate_queryset(queryset)
#             if page is not None:
#                 serializer = self.get_serializer(page, many=True)
#                 return self.get_paginated_response(serializer.data)
#             serializer = self.get_serializer(queryset, many=True)
#             return self.respu.ok_response_dict(serializer.data)
#         except Exception:
#             self.ju.create_journal_rec(
#                 {
#                     'source': 'Внешний запрос',
#                     'module': GUIDES,
#                     'status': ERROR,
#                     'description': 'Ошибка при получении списка сотрудников'
#                 },
#                 '-',
#                 ExceptionHandling.get_traceback()
#             )
#             return self.respu.bad_request_no_data()
#
#     @swagger_auto_schema(
#         tags=['Cправочники. Сотрудники ЦОКО', ],
#         operation_description="Изменение параметра отображение только кураторских учебных групп",
#         request_body=CokoChangeCuratorGroupsSerializer,
#         responses={
#             '403': 'Пользователь не авторизован или не является администратором',
#             '400': 'Ошибка при изменении параметра',
#             '200': 'Сообщение "Информация успешно обновлена"'
#         }
#     )
#     def change_curator_groups(self, request, *args, **kwargs):
#         serialize = CokoChangeCuratorGroupsSerializer(data=request.data)
#         if serialize.is_valid():
#             return change_curator_groups(request, serialize.data)
#         else:
#             journal_service.create_journal_rec(
#                 {
#                     'source': 'Внешний запрос',
#                     'module': GUIDES,
#                     'status': ERROR,
#                     'description': 'Ошибка при изменении кураторских групп - данные не прошли валидацию'
#                 },
#                 repr(request.data),
#                 repr(serialize.errors)
#             )
#         return response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')
