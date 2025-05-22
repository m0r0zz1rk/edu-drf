from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import USERS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.users.serializers.form_data import FormDataSerializer
from apps.users.services.form_data import FormDataService


class FormDataViewSet(viewsets.ViewSet):
    """
    Класс эндпоинтов для получения массива данных, необходимых для
    заполнения анкеты в заявке обучающегося
    """
    permission_classes = [IsAuthenticated, ]

    _form_data_service = FormDataService()
    _response_utils = ResponseUtils()

    @swagger_auto_schema(
        tags=['Обучающиеся. Данные для заполнения анкеты', ],
        operation_description="Получение массива данных для заполнения анкеты заявки",
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при получении массива',
            '200': FormDataSerializer
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении массива данных для заполнения анкеты заявки',
        'Произошла ошибка при получении данных для заполнения анкеты'
    )
    def get_form_data(self, request, *args, **kwargs):
        try:
            data = self._form_data_service.get_form_data()
            serialize = FormDataSerializer(data)
            return self._response_utils.ok_response(
                serialize.data
            )
        except Exception:
            raise APIProcessError
