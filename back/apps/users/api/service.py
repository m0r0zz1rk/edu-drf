from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.permissions.is_students import IsStudent
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import USERS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.users.selectors.course import courses_queryset
from apps.users.selectors.event import events_queryset
from apps.users.serializers.service import ServiceListSerializer
from apps.users.services.course import CourseService
from apps.users.services.event import EventService


class ServicesViewSet(viewsets.ViewSet):
    """Класс эндпоинтов для получения курсов и мероприятий в ЛК пользователя"""
    permission_classes = [IsAuthenticated, IsStudent]

    _courses = courses_queryset()
    _events = events_queryset()
    _course_service = CourseService()
    _event_service = EventService()
    _response_utils = ResponseUtils()

    @swagger_auto_schema(
        tags=['Обучающиеся. Курсы', ],
        operation_description="Получение списка доступных курсов",
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при получении списка',
            '200': ServiceListSerializer(many=True)
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении списка курсов для регистрации',
        'Произошла ошибка при получении списка курсов для регистрации'
    )
    def get_courses_list(self, request, *args, **kwargs):
        try:
            data = self._course_service.get_departments_courses(
                request.user.id,
                self._courses
            )
            serialize = ServiceListSerializer(data, many=True)
            return self._response_utils.ok_response(
                serialize.data
            )
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Обучающиеся. Мероприятия', ],
        operation_description="Получение списка доступных мероприятий",
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при получении списка',
            '200': ServiceListSerializer(many=True)
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении списка мероприятий для регистрации',
        'Произошла ошибка при получении списка курсов для регистрации'
    )
    def get_events_list(self, queryset, *args, **kwargs):
        try:
            data = self._event_service.get_departments_events(self._events)
            serialize = ServiceListSerializer(data, many=True)
            return self._response_utils.ok_response(
                serialize.data
            )
        except Exception:
            raise APIProcessError
