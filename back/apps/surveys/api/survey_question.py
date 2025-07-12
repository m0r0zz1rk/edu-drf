from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import profile_service
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import SURVEYS
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.journal.services.journal import JournalService
from apps.surveys.exceptions.survey_question import IncorrectQuestionInfo, QuestionCreateUpdateError
from apps.surveys.selectors.survey_question import survey_question_queryset, SurveyQuestionFilter
from apps.surveys.serializers.survey_question import SurveyQuestionListSerializer, SurveyQuestionCreateSerializer
from apps.surveys.services.survey_question import SurveyQuestionService


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    """Эндпоинты для работы с вопросами опроса"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    _respu = ResponseUtils()
    _js = JournalService()
    _journal_request_builder = JournalRequestBuilder()

    queryset = survey_question_queryset()
    serializer_class = SurveyQuestionListSerializer
    lookup_field = "object_id"
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = SurveyQuestionFilter

    @swagger_auto_schema(
        tags=['Опросы. Вопросы опросов', ],
        operation_description="Получение списка вопросов опроса",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': SurveyQuestionListSerializer(many=True)
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при получении списка вопросов опроса',
        'Произошла ошибка при получении списка вопросов опроса'
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self._respu.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Опросы. Вопросы опросов', ],
        operation_description="Добавление вопроса опроса",
        request_body=SurveyQuestionCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении вопроса опроса',
            '200': 'Вопрос успешно добавлен'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при добавлении вопроса опроса',
        'Произошла ошибка в процессе добавления вопроса опроса'
    )
    def create(self, request, *args, **kwargs):
        try:
            serialize = SurveyQuestionCreateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                service = SurveyQuestionService(request.data['survey_id'])
                service.add_edit_question(serialize.data)
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(SURVEYS)
                    .set_status(SUCCESS)
                    .set_description('Добавлен вопрос опроса')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Вопрос успешно добавлен ')
                )
                return journal_request.create_response()
            else:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(SURVEYS)
                    .set_status(ERROR)
                    .set_description('Ошибка сериализации данных при добавлении вопроса опроса')
                    .set_payload(repr(request.data) + f'\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.errors))
                    .set_response_message('Не удалось сериализовать данные для '
                                          'добавления вопроса опроса')
                )
                return journal_request.create_response()
        except IncorrectQuestionInfo:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Получена некорректная информация о вопросе опроса')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Получены невалидные данные для добавления вопроса опроса')
            )
            return journal_request.create_response()
        except QuestionCreateUpdateError:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Произошла системная ошибка при добавлении вопроса опроса')
                .set_payload(repr(request.data))
                .set_output(ExceptionHandling.get_traceback())
                .set_response_message('Произошла системная ошибка при добавлении вопроса опроса')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Опросы. Вопросы опросов', ],
        operation_description="Обновление вопроса опроса",
        request_body=SurveyQuestionCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении вопроса опроса',
            '200': 'Вопрос успешно обновлен'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при обновлении вопроса опроса',
        'Произошла ошибка в процессе обновления вопроса опроса'
    )
    def partial_update(self, request, *args, **kwargs):
        try:
            serialize = SurveyQuestionCreateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                service = SurveyQuestionService(request.data['survey_id'])
                question_info = dict(request.data)
                question_info['object_id'] = kwargs.get('object_id')
                service.add_edit_question(question_info)
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(SURVEYS)
                    .set_status(SUCCESS)
                    .set_description('Вопрос опроса обновлен')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Вопрос успешно обновлен')
                )
                return journal_request.create_response()
            else:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(SURVEYS)
                    .set_status(ERROR)
                    .set_description('Ошибка сериализации данных при обновлении вопроса опроса')
                    .set_payload(repr(request.data) + f'\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.errors))
                    .set_response_message('Не удалось сериализовать данные для '
                                          'обновления вопроса опроса')
                )
                return journal_request.create_response()
        except IncorrectQuestionInfo:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Получена некорректная информация о вопросе опроса')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Получены невалидные данные для обновления вопроса опроса')
            )
            return journal_request.create_response()
        except QuestionCreateUpdateError:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Произошла системная ошибка при обновлении вопроса опроса')
                .set_payload(repr(request.data))
                .set_output(ExceptionHandling.get_traceback())
                .set_response_message('Произошла системная ошибка при обновлении вопроса опроса')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Опросы. Вопросы опросов', ],
        operation_description="Удаление вопроса опроса",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении вопроса опроса',
            '200': 'Вопрос успешно удален'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при удалении вопроса опроса',
        'Произошла ошибка в процессе удаления вопроса опроса'
    )
    def destroy(self, request, *args, **kwargs):
        try:
            service = SurveyQuestionService(None)
            service.delete_question(self.kwargs['object_id'])
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_source(
                    profile_service.get_profile_or_info_by_attribute(
                        'django_user_id',
                        request.user.id,
                        'display_name'
                    )
                )
                .set_module(SURVEYS)
                .set_status(SUCCESS)
                .set_description('Вопрос опроса удален')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Вопрос успешно удален')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
