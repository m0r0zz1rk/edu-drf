from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.utils.django.response import ResponseUtils
from apps.docs.serializers.doc_viewer import DocViewerSerializer
from apps.docs.services.doc_viewer import DocViewerService
from apps.journal.consts.journal_modules import DOCS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError


class DovViewerViewSet(viewsets.ViewSet):
    """
    Класс эндпоинтов для просмотра документов
    """
    permission_classes = [IsAuthenticated, ]

    _doc_viewer_service = DocViewerService()
    _response_utils = ResponseUtils()

    @swagger_auto_schema(
        tags=['Документы. Просмотр документа', ],
        operation_description="Получение документа для просмотра на web форме",
        responses={
            '403': 'Пользователь не авторизован',
            '400': 'Ошибка при получении файла',
            '200': DocViewerSerializer
        }
    )
    @journal_api(
        DOCS,
        ERROR,
        'Ошибка при получении документа для просмотра на web форме',
        'Произошла ошибка при получении файла документа'
    )
    def doc_view(self, request, *args, **kwargs):
        try:
            data = {
                'file_name': self._doc_viewer_service.get_file_attr(
                    self.kwargs['file_type'],
                    self.kwargs['file_id'],
                    'name'
                ),
                'file': self._doc_viewer_service.get_file_attr(
                    self.kwargs['file_type'],
                    self.kwargs['file_id'],
                    'file'
                )
            }
            serialize = DocViewerSerializer(data)
            return self._response_utils.ok_response_dict(serialize.data)
        except Exception:
            raise APIProcessError
