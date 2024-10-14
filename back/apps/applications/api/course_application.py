from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.applications.selectors.course_application import course_application_queryset, CourseApplicationFilter
from apps.applications.serializers.course_application import CourseAppGroupListSerializer
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import APPLICATIONS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError


class CourseApplicationAdminViewSet(viewsets.ModelViewSet):
    """Класс эндпоинтов для работы с заявками на курсы"""
    permission_classes = [IsAuthenticated, IsAdministrators]

    _response_utils = ResponseUtils()

    queryset = course_application_queryset()
    lookup_field = "object_id"
    serializer_class = CourseAppGroupListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = CourseApplicationFilter

    @swagger_auto_schema(
        tags=['Заявки. Заявки учебной группы', ],
        operation_description="Получение списка заявок для учебной группы",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': CourseAppGroupListSerializer(many=True)
        }
    )
    @journal_api(
        APPLICATIONS,
        ERROR,
        'Ошибка при получении списка заявок',
        'Произошла ошибка при получении списка заявок'
    )
    def list(self, request, *args, **kwargs):
        try:

            queryset = self.filter_queryset(
                self.get_queryset().filter(group_id=self.kwargs['group_id'])
            )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self._response_utils.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError

