from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.selectors.planning_parameter import planning_parameter_queryset, PlanningParameterFilter
from apps.edu.serializers.planning_parameter import PlanningParameterSerializer
from apps.edu.services.planning_parameter import PlanningParameterService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import JournalService


class PlanningParameterViewSet(viewsets.ModelViewSet):
    """Работа с параметрами планирования мероприятий"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    queryset = planning_parameter_queryset()
    serializer_class = PlanningParameterSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = PlanningParameterFilter

    ps = ProfileService()
    respu = ResponseUtils()
    js = JournalService()
    pps = PlanningParameterService()

    @swagger_auto_schema(
        tags=['Учебная часть. Планирование', ],
        operation_description="Получение списка параметров планирования",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': PlanningParameterSerializer(many=True)
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
        except:
            self.js.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при получении списка параметров планирования'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка, повторите попытку позже')

    @swagger_auto_schema(
        tags=['Учебная часть. Планирование', ],
        operation_description="Обновление параметра планирования",
        request_body=PlanningParameterSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении параметра планирования',
            '200': 'Сообщение "Параметр успешно обновлен"'
        }
    )
    def update(self, request, *args, **kwargs):
        try:
            if 'object_id' in request.data.keys():
                instance = self.pps.get_planning_parameter(
                    'object_id',
                    request.data['object_id']
                )
                serializer = self.get_serializer(instance, data=request.data)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    self.js.create_journal_rec(
                        {
                            'source': self.ps.get_profile_or_info_by_attribute(
                                'django_user_id',
                                request.user.id,
                                'display_name'
                            ),
                            'module': EDU,
                            'status': SUCCESS,
                            'description': 'Ошибка сериализации при обновлении параметра планирования'
                        },
                        repr(request.data),
                        repr(serializer.errors)
                    )
                    return self.respu.ok_response('Параметр успешно обновлен')
            self.js.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка сериализации при обновлении параметра планирования'
                },
                repr(request.data),
                '-'
            )
            return self.respu.bad_request_response('Ошибка сериализации данных, повторите попытку позже')
        except:
            self.js.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при обновлении параметра планирования'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка, повторите попытку позже')
