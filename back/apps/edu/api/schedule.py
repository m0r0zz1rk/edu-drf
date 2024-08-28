from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.request import RequestUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.selectors.schedule import schedule_queryset
from apps.edu.serializers.schedule import ScheduleListSerializer
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class ScheduleViewSet(viewsets.ModelViewSet):
    """Работа с расписаниями занятий учебных групп"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ru = RequestUtils()
    ju = JournalService()
    pu = ProfileService()
    respu = ResponseUtils()

    lookup_field = "object_id"
    serializer_class = ScheduleListSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=['Учебная часть. Расписание занятий', ],
        operation_description="Получение расписания занятий учебной группы",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': ScheduleListSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = schedule_queryset(self.kwargs['group_id'])
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
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при получении расписания занятий для учебной группы'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()
