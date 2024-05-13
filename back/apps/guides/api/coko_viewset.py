from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.utils.profile import ProfileUtils
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.filters.coko_filter import CokoFilter
from apps.guides.serializers.coko_serializers import coko_profile_model, CokoSerializer, \
    CokoChangeCuratorGroupsSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.utils.journal_utils import JournalUtils


class CokoViewSet(viewsets.ModelViewSet):
    """Работа с сотрудниками ЦОКО в модуле Справочник"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ju = JournalUtils()
    pu = ProfileUtils()
    respu = ResponseUtils()

    queryset = coko_profile_model.objects.all().order_by('surname', 'name', 'patronymic')
    serializer_class = CokoSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = CokoFilter

    @swagger_auto_schema(
        tags=['Cправочник "Сотрудники"', ],
        operation_description="Получение списка пользователей",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': CokoSerializer(many=True)
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
                    'description': 'Ошибка при получении списка сотрудников'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочник "Сотрудники"', ],
        operation_description="Изменение параметра отображение только кураторских учебных групп",
        request_body=CokoChangeCuratorGroupsSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при изменении параметра',
            '200': 'Сообщение "Информация успешно обновлена"'
        }
    )
    def change_curator_groups(self, request, *args, **kwargs):
        serialize = CokoChangeCuratorGroupsSerializer(data=request.data)
        if serialize.is_valid():
            prof = self.pu.get_profile_or_info_by_attribute(
                'object_id',
                serialize.data['object_id'],
                'profile'
            )
            if not prof:
                self.ju.create_journal_rec(
                    {
                        'source': 'Внешний запрос',
                        'module': GUIDES,
                        'status': ERROR,
                        'description': 'Ошибка при изменении кураторских групп - профиль не найден'
                    },
                    serialize.data,
                    None
                )
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
            data = {}
            for key in ['surname', 'name', 'patronymic']:
                data[key] = getattr(prof, key)
            data['curator_groups'] = serialize.data['curator_groups']
            proc = self.pu.set_coko_profile_data(
                prof,
                data
            )
            if isinstance(proc, bool):
                if proc:
                    self.ju.create_journal_rec(
                        {
                            'source': self.pu.get_profile_or_info_by_attribute(
                                'django_user_id',
                                request.user.id,
                                'display_name'
                            ),
                            'module': GUIDES,
                            'status': SUCCESS,
                            'description': 'Параметр отображения кураторских групп успешно изменен'
                        },
                        repr(serialize.data),
                        None
                    )
                    return self.respu.ok_response('Информация успешно обновлена')
                else:
                    self.ju.create_journal_rec(
                        {
                            'source': 'Процесс установки параметров профилю сотрудников',
                            'module': GUIDES,
                            'status': ERROR,
                            'description': 'Ошибка при изменении кураторских групп - данные не прошли валидацию'
                        },
                        repr(data),
                        None
                    )
                    return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
            else:
                self.ju.create_journal_rec(
                    {
                        'source': 'Процесс установки параметров профилю сотрудников',
                        'module': GUIDES,
                        'status': ERROR,
                        'description': 'Ошибка при изменении кураторских групп - данные не прошли валидацию'
                    },
                    repr(data),
                    None
                )
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при изменении кураторских групп - данные не прошли валидацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
        return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
