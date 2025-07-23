import os

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.docs.serializers.manual_serializer import ManualSerializer
from apps.commons.utils.django.response import response_utils
from apps.commons.utils.django.settings import settings_utils
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api


class ManualViewSet(viewsets.ViewSet):
    """Класс для эндпоинта на скачивание руководства обучающегося"""

    @swagger_auto_schema(
        tags=['Общее. Руководство пользователя', ],
        operation_description="Получение руководство пользователя",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении документа',
            '200': ManualSerializer
        }
    )
    @journal_api(
        COMMON,
        ERROR,
        'Ошибка при получении руководства пользователя',
        'Произошла ошибка при получении руководства пользователя'
    )
    def get_manual(self, request, *args, **kwargs):
        data = {'file': os.path.join(settings_utils.get_parameter_from_settings('MEDIA_ROOT'), 'Инструкция.docx')}
        serialize = ManualSerializer(data)
        return response_utils.ok_response_dict(serialize.data)
