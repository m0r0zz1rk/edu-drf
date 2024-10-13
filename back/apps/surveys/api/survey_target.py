from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import SURVEYS
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.journal.services.journal import JournalService
from apps.surveys.exceptions.survey_target import TargetInfoNotCorrect
from apps.surveys.selectors.survey_target import SurveyTargetFilter, survey_target_model_queryset
from apps.surveys.serializers.survey_target import SurveyTargetListSerializer, SurveyTargetCreateSerializer
from apps.surveys.services.survey_target import SurveyTargetService


class SurveyTargetViewSet(viewsets.ModelViewSet):
    """Класс эндпоинтов для работы с таргетированиями опросов"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    _profile_service = ProfileService()
    _survey_target_service = SurveyTargetService()
    _respu = ResponseUtils()
    _js = JournalService()
    _journal_request_builder = JournalRequestBuilder()

    queryset = survey_target_model_queryset()
    serializer_class = SurveyTargetListSerializer
    lookup_field = "object_id"
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = SurveyTargetFilter

    @swagger_auto_schema(
        tags=['Опросы. Таргетирование', ],
        operation_description="Получение списка таргетирований опросов",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': SurveyTargetListSerializer(many=True)
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при получении списка таргетирований опросов',
        'Произошла ошибка при получении списка таргетирований опросов'
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
        tags=['Опросы. Таргетирование', ],
        operation_description="Добавление таргетирования опроса",
        request_body=SurveyTargetCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении таргетирования опроса',
            '200': 'Таргетирование успешно добавлено'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при добавлении таргетирования опроса',
        'Произошла ошибка в процессе добавления таргетирования опроса'
    )
    def create(self, request, *args, **kwargs):
        try:
            serialize = SurveyTargetCreateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                target_info = dict(serialize.data)
                target_info['object_id'] = None
                self._survey_target_service.add_edit_survey_target(target_info)
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        self._profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(SURVEYS)
                    .set_status(SUCCESS)
                    .set_description('Добавлено новое таргетирование опроса')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Таргетирование успешно добавлено')
                )
                return journal_request.create_response()
            else:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        self._profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(SURVEYS)
                    .set_status(ERROR)
                    .set_description('Ошибка сериализации данных при добавлении таргетирования опроса')
                    .set_payload(f'{repr(request.data)}\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.data))
                    .set_response_message('Не удалось сериализовать данные для добавления таргетирования опроса')
                )
                return journal_request.create_response()
        except TargetInfoNotCorrect:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Получены невалидные данные при добавлении таргетирования опроса')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Получены невалидные данные для добавления таргетирования опроса')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Опросы. Таргетирование', ],
        operation_description="Обновление таргетирования опроса",
        request_body=SurveyTargetCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении таргетирования опроса',
            '200': 'Таргетирование успешно обновлено'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при обновлении таргетирования опроса',
        'Произошла ошибка в процессе обновления таргетирования опроса'
    )
    def partial_update(self, request, *args, **kwargs):
        try:
            serialize = SurveyTargetCreateSerializer(
                data=request.data
            )
            if serialize.is_valid():
                target_info = dict(serialize.data)
                target_info['object_id'] = self.kwargs['object_id']
                self._survey_target_service.add_edit_survey_target(target_info)
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        self._profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(SURVEYS)
                    .set_status(SUCCESS)
                    .set_description('Таргетирование успешно обновлено')
                    .set_payload(repr(request.data))
                    .set_output('-')
                    .set_response_message('Таргероивание успешно обновлено')
                )
                return journal_request.create_response()
            else:
                journal_request = JournalRequest(
                    self._journal_request_builder
                    .set_source(
                        self._profile_service.get_profile_or_info_by_attribute(
                            'django_user_id',
                            request.user.id,
                            'display_name'
                        )
                    )
                    .set_module(SURVEYS)
                    .set_status(ERROR)
                    .set_description('Ошибка сериализации данных при обновлении таргетирования опроса')
                    .set_payload(repr(request.data))
                    .set_output(repr(serialize.data))
                    .set_response_message('Не удалось сериализовать данные для обновлении '
                                          'информации о таргетировании опроса')
                )
                return journal_request.create_response()
        except TargetInfoNotCorrect:
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(SURVEYS)
                .set_status(ERROR)
                .set_description('Некорректная информация при обновлении таргетирования опроса')
                .set_payload(f'object_id: {self.kwargs["object_id"]}')
                .set_output('-')
                .set_response_message('Получена некорректная информация при попытке '
                                      'изменения таргетирования опроса')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Опросы. Таргетирование', ],
        operation_description="Удаление таргетирования опроса",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении таргетирования опроса',
            '200': 'Таргетирование успешно удалено'
        }
    )
    @journal_api(
        SURVEYS,
        ERROR,
        'Ошибка при удалении таргетирования опроса',
        'Произошла ошибка в процессе удаления таргетирования опроса'
    )
    def destroy(self, request, *args, **kwargs):
        try:
            self._survey_target_service.delete_survey_target(self.kwargs['object_id'])
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_source(
                    self._profile_service.get_profile_or_info_by_attribute(
                        'django_user_id',
                        request.user.id,
                        'display_name'
                    )
                )
                .set_module(SURVEYS)
                .set_status(SUCCESS)
                .set_description('Таргетирование опроса удалено')
                .set_payload(repr(request.data))
                .set_output('-')
                .set_response_message('Таргетирование успешно удалено')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
