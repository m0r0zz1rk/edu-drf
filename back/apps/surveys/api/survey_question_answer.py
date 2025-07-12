from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import profile_service
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import SURVEYS
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.journal.services.journal import JournalService
from apps.surveys.exceptions.survey_question_answer import IncorrectAnswerData
from apps.surveys.selectors.survey_question_answer import survey_question_answer_queryset, SurveyQuestionAnswerFilter
from apps.surveys.serializers.survey_question_answer import SurveyQuestionAnswerBaseSerializer, \
    SurveyQuestionAnswerCreateSerializer, SurveyQuestionAnswerUpdateSerializer
from apps.surveys.services.survey_question_answer import SurveyQuestionAnswerService


class SurveyQuestionAnswerViewSet(viewsets.ModelViewSet):
    """Эндпоинты для работы с возможными ответами вопроса опроса"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    _answer_service = SurveyQuestionAnswerService()
    _respu = ResponseUtils()
    _js = JournalService()
    _journal_request_builder = JournalRequestBuilder()

    queryset = survey_question_answer_queryset()
    serializer_class = SurveyQuestionAnswerBaseSerializer
    lookup_field = "object_id"
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = SurveyQuestionAnswerFilter

    @swagger_auto_schema(
        tags=['Опросы. Возможные ответы вопроса', ],
        operation_description="Получение списка возможных ответов вопроса",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': SurveyQuestionAnswerBaseSerializer(many=True)
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при получении списка возможных ответов вопроса',
        'Произошла ошибка при получении списка возможных ответов вопроса'
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
        tags=['Опросы. Возможные ответы вопроса', ],
        operation_description="Добавление возможного ответа вопроса",
        request_body=SurveyQuestionAnswerCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении возможного ответа вопроса',
            '200': 'Возможный ответ успешно добавлен'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при добавлении возможного ответа вопроса',
        'Произошла ошибка в процессе добавления возможного ответа вопроса'
    )
    def create(self, request, *args, **kwargs):
        try:
            serialize = SurveyQuestionAnswerCreateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                self._answer_service.add_edit_answer(serialize.data)
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
                    .set_description('Добавлен возможный ответ вопроса')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Возможный ответ успешно добавлен ')
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
                    .set_description('Ошибка сериализации данных при добавлении возможного ответа вопроса')
                    .set_payload(repr(request.data) + f'\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.errors))
                    .set_response_message('Не удалось сериализовать данные для '
                                          'добавления возможного ответа вопроса')
                )
                return journal_request.create_response()
        except IncorrectAnswerData:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Получена некорректная информация о возможном ответе')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Получены невалидные данные для добавления возможного ответа вопроса')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Опросы. Возможные ответы вопроса', ],
        operation_description="Обновление возможного ответа вопроса",
        request_body=SurveyQuestionAnswerUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении возможного ответа вопроса',
            '200': 'Возможный ответ успешно обновлен'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при обновлении возможного ответа вопроса',
        'Произошла ошибка в процессе обновления возможного ответа вопроса'
    )
    def partial_update(self, request, *args, **kwargs):
        try:
            answer_data = dict(request.data)
            answer_data['object_id'] = self.kwargs['object_id']
            serialize = SurveyQuestionAnswerUpdateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                self._answer_service.add_edit_answer(answer_data)
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
                    .set_description('Возможный ответ вопроса обновлен')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Возможный ответ успешно обновлен')
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
                    .set_description('Ошибка сериализации данных при обновлении возможного ответа вопроса')
                    .set_payload(repr(request.data) + f'\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.errors))
                    .set_response_message('Не удалось сериализовать данные для '
                                          'обновления возможного ответа вопроса')
                )
                return journal_request.create_response()
        except IncorrectAnswerData:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Получена некорректная информация о возможном ответе вопроса')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Получены невалидные данные для обновления возможного ответа вопроса')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Опросы. Возможные ответы вопроса', ],
        operation_description="Удаление возможного ответа вопроса",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении возможного ответа вопроса',
            '200': 'Возможный ответ успешно удален'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при удалении возможного ответа вопроса',
        'Произошла ошибка в процессе удаления возможного ответа вопроса'
    )
    def destroy(self, request, *args, **kwargs):
        try:
            self._answer_service.delete_answer(self.kwargs['object_id'])
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
                .set_description('Возможный ответ вопроса удален')
                .set_payload(f'object_id объекта: {self.kwargs["object_id"]}')
                .set_output('-')
                .set_response_message('Возможный ответ вопроса удален')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
