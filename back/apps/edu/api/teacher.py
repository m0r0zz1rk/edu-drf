from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.exceptions.date.incorrect_time_format import IncorrectTimeFormatError
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.selectors.schedule import TeachersFilter, user_teachers_queryset
from apps.edu.serializers.teacher import TeacherSerializer, CheckTeacherBusySerializer
from apps.edu.services.teacher import TeacherService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError


class TeacherViewSet(viewsets.ModelViewSet):
    """API для работы с преподавателями"""
    permission_classes = [IsAuthenticated, IsAdministrators]

    queryset = user_teachers_queryset()
    lookup_field = "object_id"
    serializer_class = TeacherSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TeachersFilter

    _journal_request_builder = JournalRequestBuilder()
    _response_utils = ResponseUtils()
    _teacher_service = TeacherService()

    @swagger_auto_schema(
        tags=['Учебная часть. Преподаватели', ],
        operation_description="Получение списка преподавателей",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': TeacherSerializer(many=True)
        }
    )
    @journal_api(
        EDU,
        ERROR,
        'Ошибка при получении списка преподавателей',
        'Произошла ошибка при получении списка преподавателей'
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self._response_utils.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Учебная часть. Преподаватели', ],
        operation_description="Проверка занятости преподавателя",
        request_body=CheckTeacherBusySerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при проверка занятости',
            '423': 'Преподаватель занят',
            '200': 'Преподаватель свободен'
        }
    )
    @journal_api(
        EDU,
        ERROR,
        'Ошибка при проверка занятости преподавателя',
        'Произошла ошибка при проверка занятости преподавателя'
    )
    def check_teacher_busy(self, request, *args, **kwargs):
        try:
            serialize = CheckTeacherBusySerializer(
                data=request.data
            )
            if serialize.is_valid():
                check = self._teacher_service.check_teacher_busy(
                    serialize.data['teacher_id'],
                    serialize.data['group_id'],
                    serialize.data['day'],
                    serialize.data['time_start_str'],
                )
                if check:
                    return self._response_utils.ok_response_no_data()
                return self._response_utils.locked_response()
            else:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_module(EDU)
                    .set_status(ERROR)
                    .set_description('Ошибка сериализации данных при проверке занятости преподавателя')
                    .set_payload(repr(request.data))
                    .set_output(repr(serialize.errors))
                    .set_response_message('Произошла ошибка при сериализации данных')
                )
                return journal_request.create_response()
        except IncorrectTimeFormatError:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(EDU)
                .set_status(ERROR)
                .set_description('Некорретный формат времени начала занятия')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Получен некорректный формат времени начала занятия')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
