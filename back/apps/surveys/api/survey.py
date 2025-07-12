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
from apps.surveys.exceptions.survey import SurveyDataNotValid, SurveyNotExist
from apps.surveys.selectors.survey import survey_queryset, SurveyFilter
from apps.surveys.serializers.survey import SurveyListSerializer, SurveyBaseSerializer, SurveyCreateSerializer
from apps.surveys.services.survey import survey_service


class SurveyViewSet(viewsets.ModelViewSet):

    """Класс эндпоинтов для работы с опросами"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    _respu = ResponseUtils()
    _js = JournalService()
    _journal_request_builder = JournalRequestBuilder()

    queryset = survey_queryset()
    serializer_class = SurveyListSerializer
    lookup_field = "object_id"
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = SurveyFilter

    @swagger_auto_schema(
        tags=['Опросы', ],
        operation_description="Получение списка опросов",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': SurveyListSerializer(many=True)
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при получении списка опросов',
        'Произошла ошибка при получении списка опросов'
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
        tags=['Опросы', ],
        operation_description="Добавление опроса",
        request_body=SurveyCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении опроса',
            '200': 'Опрос успешно добавлен'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при добавлении опроса',
        'Произошла ошибка в процессе добавления опроса'
    )
    def create(self, request, *args, **kwargs):
        try:
            serialize = SurveyCreateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                survey_service.create_survey(request.user.id, serialize.data)
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
                    .set_description('Добавлен новый опрос')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Опрос успешно добавлен')
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
                    .set_description('Ошибка сериализации данных при добавлении опроса')
                    .set_payload(f'{repr(request.data)}\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.data))
                    .set_response_message('Не удалось сериализовать данные для добавления опроса')
                )
                return journal_request.create_response()
        except SurveyDataNotValid:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Получены невалидные данные при добавлении опроса')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Получены невалидные данные для добавления опроса')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Опросы', ],
        operation_description="Обновление опроса",
        request_body=SurveyBaseSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении опроса',
            '200': 'Опрос успешно обновлен'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при обновлении опроса',
        'Произошла ошибка в процессе обновления опроса'
    )
    def partial_update(self, request, *args, **kwargs):
        try:
            serialize = SurveyBaseSerializer(
                data=request.data
            )
            if serialize.is_valid():
                survey_service.update_survey(
                    self.kwargs['object_id'],
                    serialize.data
                )
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
                    .set_description('Опрос успешно обновлен')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Опрос успешно обновлен')
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
                    .set_description('Ошибка сериализации данных при обновлении опроса')
                    .set_payload(repr(request.data))
                    .set_output(repr(serialize.data))
                    .set_response_message('Не удалось сериализовать данные для обновлении информации об опросе')
                )
                return journal_request.create_response()
        except SurveyNotExist:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Опрос не найден')
                .set_payload(f'object_id: {self.kwargs["object_id"]}')
                .set_output('-')
                .set_response_message('Не найден опрос при попытке обновить информацию')
            )
            return journal_request.create_response()
        except SurveyDataNotValid:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Получены невалидные данные при обновлении опроса')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Получены невалидные данные для обновлении информации об опросе')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
