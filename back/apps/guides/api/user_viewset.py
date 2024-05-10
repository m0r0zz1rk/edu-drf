from django.apps import apps
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.pagination import CustomPagination
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.filters.user_filter import UserFilter
from apps.guides.serializers.user_serializer import UserSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.utils.journal_utils import JournalUtils

student_profile_model = apps.get_model('authen', 'StudentProfile')


class UserViewSet(viewsets.ModelViewSet):
    """Работы с пользователями в модуле Справочники"""
    queryset = student_profile_model.objects.all().order_by('surname', 'name', 'patronymic')
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = UserFilter

    ju = JournalUtils()
    respu = ResponseUtils()

    @swagger_auto_schema(
        tags=['Справочники', ],
        operation_description="Получение списка пользователей",
        responses={
            '400': 'Ошибка при получении списка',
            '200': UserSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return ResponseUtils.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при получении списка пользователей'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()
