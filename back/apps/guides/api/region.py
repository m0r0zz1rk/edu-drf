from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
from apps.commons.utils.django.response import ResponseUtils
from apps.guides.operations.add_update_guides_rec import AddUpdateGuidesRec
from apps.guides.operations.delete_guides_rec import DeleteGuidesRec
from apps.guides.selectors.name_field import NameFieldFilter
from apps.guides.selectors.region import region_queryset
from apps.guides.serializers.region import RegionListUpdateSerializer, RegionBaseSerializer
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.journal.services.journal import JournalService


class RegionViewSet(viewsets.ModelViewSet):
    """Работа с должностями в модуле Справочников"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    _journal_service = JournalService()
    _response_utils = ResponseUtils()
    _profile_service = ProfileService()
    _journal_request_builder = JournalRequestBuilder()

    queryset = region_queryset()
    serializer_class = RegionListUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = NameFieldFilter

    @swagger_auto_schema(
        tags=['Cправочники. Регионы РФ', ],
        operation_description="Получение списка регионов РФ",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': RegionListUpdateSerializer(many=True)
        }
    )
    @journal_api(
        GUIDES,
        ERROR,
        'Ошибка при получении списка регионов РФ',
        'Произошла ошибка при получении списка регионов'
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
        tags=['Cправочники. Регионы РФ', ],
        operation_description="Добавление региона",
        request_body=RegionBaseSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении региона',
            '200': 'Сообщение "Регион успешно добавлен"'
        }
    )
    @journal_api(
        GUIDES,
        ERROR,
        'Ошибка при добавлении региона РФ',
        'Произошла ошибка при добавлении региона'
    )
    def create(self, request, *args, **kwargs):
        try:
            serialize = RegionBaseSerializer(data=request.data)
            if serialize.is_valid():
                process = AddUpdateGuidesRec(
                    'Region',
                    serialize.data
                )
                if process.process_completed:
                    return self._response_utils.ok_response('Регион успешно добавлен')
                else:
                    return self._response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')
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
                    .set_module(GUIDES)
                    .set_status(ERROR)
                    .set_description('Ошибка сериализации данных при добавлении региона')
                    .set_payload(repr(request.data) + f'\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.data))
                    .set_response_message('Не удалось сериализовать данные для добавления региона')
                )
                return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Cправочники. Регионы РФ', ],
        operation_description="Обновление региона",
        request_body=RegionListUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении региона',
            '200': 'Сообщение "Регион успешно обновлен"'
        }
    )
    @journal_api(
        GUIDES,
        ERROR,
        'Ошибка при обновлении региона РФ',
        'Произошла ошибка при обновлении региона'
    )
    def update(self, request, *args, **kwargs):
        try:
            serialize = RegionListUpdateSerializer(data=request.data)
            if serialize.is_valid():
                process = AddUpdateGuidesRec(
                    'Region',
                    serialize.data
                )
                if process.process_completed:
                    return self._response_utils.ok_response('Регион успешно обновлен')
                else:
                    return self._response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')
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
                    .set_module(GUIDES)
                    .set_status(ERROR)
                    .set_description('Ошибка сериализации данных при обновлении региона')
                    .set_payload(repr(request.data) + f'\n ID пользователя: {request.user.id}')
                    .set_output(repr(serialize.data))
                    .set_response_message('Не удалось сериализовать данные для обновления региона')
                )
                return journal_request.create_response()
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Cправочники. Регионы РФ', ],
        operation_description="Удаление региона",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении региона',
            '200': 'Сообщение "Регион успешно удален"'
        }
    )
    @journal_api(
        GUIDES,
        ERROR,
        'Ошибка при удалении региона РФ',
        'Произошла ошибка при удалении региона'
    )
    def destroy(self, request, *args, **kwargs):
        try:
            process = DeleteGuidesRec(
                'Region',
                {
                    'object_id': self.kwargs['object_id'],
                }
            )
            if process.process_completed:
                return self._response_utils.ok_response('Регион успешно удален')
            else:
                return self._response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')
        except Exception:
            raise APIProcessError
