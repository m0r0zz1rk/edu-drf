from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
from apps.commons.utils.django.response import ResponseUtils
from apps.docs.selectors.student_doc import StudentDocFilter, student_doc_queryset
from apps.docs.serializers.student_doc import StudentDocListSerializer, StudentDocCreateSerializer
from apps.docs.services.student_doc import StudentDocService
from apps.journal.consts.journal_modules import DOCS
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError


class StudentDocViewSet(viewsets.ModelViewSet):
    """Класс эндпоинтов для работы с документами студентов"""
    permission_classes = [IsAuthenticated, ]

    _journal_request_builder = JournalRequestBuilder()
    _profile_service = ProfileService()
    _student_doc_service = StudentDocService()
    _response_utils = ResponseUtils()

    queryset = student_doc_queryset()
    serializer_class = StudentDocListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = StudentDocFilter

    @swagger_auto_schema(
        tags=['Документы. Документы обучающегося', ],
        operation_description="Получение списка документов обучающегося",
        responses={
            '403': 'Пользователь не авторизован',
            '400': 'Ошибка при получении списка',
            '200': StudentDocListSerializer(many=True)
        }
    )
    @journal_api(
        DOCS,
        ERROR,
        'Ошибка при получении списка документов обучающегося',
        'Произошла ошибка при получении списка документов'
    )
    def get_student_docs(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            if 'profile_id' in request.GET:
                if not request.user.is_superuser:
                    journal_request = JournalRequest(
                        self._journal_request_builder
                        .set_module(DOCS)
                        .set_status(ERROR)
                        .set_description('Отказано в доступе')
                        .set_payload(f'ID пользователя: {request.user.id}, получение списка документов пользователя')
                        .set_output('-')
                        .set_response_message('Отказано в доступе')
                    )
                    return journal_request.create_response()
                user_id = self._profile_service.get_profile_or_info_by_attribute(
                    'object_id',
                    request.GET['profile_id'],
                    'user_id'
                )
            docs = self._student_doc_service.get_student_docs(user_id)
            queryset = self.filter_queryset(docs)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self._response_utils.ok_response_dict(serializer.data)
        except Exception:
            raise APIProcessError

    @swagger_auto_schema(
        tags=['Документы. Документы обучающегося', ],
        operation_description="Добавление документа",
        request_body=StudentDocCreateSerializer,
        responses={
            '403': 'Пользователь не авторизован',
            '400': 'Ошибка при получении списка',
            '200': 'Документ успешно добавлен'
        }
    )
    @journal_api(
        DOCS,
        ERROR,
        'Ошибка при загрузке документа обучающегося',
        'Произошла ошибка при загрузке документа'
    )
    def create_student_doc(self, request, *args, **kwargs):
        try:
            serialize = StudentDocCreateSerializer(
                data=request.data
            )
            if not serialize.is_valid():
                raise APIProcessError
            user_id = request.user.id
            if 'profile_id' in request.GET:
                if not request.user.is_superuser:
                    journal_request = JournalRequest(
                        self._journal_request_builder
                        .set_module(DOCS)
                        .set_status(ERROR)
                        .set_description('Отказано в доступе')
                        .set_payload(f'ID пользователя: {request.user.id}, получение списка документов пользователя')
                        .set_output('-')
                        .set_response_message('Отказано в доступе')
                    )
                    return journal_request.create_response()
                user_id = self._profile_service.get_profile_or_info_by_attribute(
                    'object_id',
                    request.GET['profile_id'],
                    'user_id'
                )
            self._student_doc_service.create_student_doc(user_id, serialize.validated_data)
            journal_request = JournalRequest(
                self._journal_request_builder
                .set_module(DOCS)
                .set_status(SUCCESS)
                .set_description('Добавлен документ обучающегося')
                .set_payload(f'ID пользователя: {request.user.id}, данные о файле: {repr(request.data)}')
                .set_output('-')
                .set_response_message('Документ успешно добавлен')
            )
            return journal_request.create_response()
        except Exception:
            raise APIProcessError
