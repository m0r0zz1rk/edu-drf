from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.utils.django.response import response_utils
from apps.docs.serializers.pay_doc_serializer import PayDocSerializer
from apps.docs.services.pay_doc import pay_doc_service
from apps.journal.consts.journal_modules import DOCS


class PayDocViewSet(viewsets.ViewSet):
    """Класс эндпоинтов для работы с документами об оплате"""

    @swagger_auto_schema(
        tags=[f'Документы. Документы об оплате', ],
        operation_description="Добавление документа об оплате",
        request_body=PayDocSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при добавлении документа',
            '200': 'ОК'
        }
    )
    @view_set_journal_decorator(
        DOCS,
        f'Документ об оплате успешно добавлен',
        f'Ошибка при добавлении документа об оплате'
    )
    def create(self, request, *args, **kwargs):
        serialize = PayDocSerializer(data=request.data)
        if serialize.is_valid():
            pay_doc_service.save_pay_doc(serialize.validated_data)
            return response_utils.ok_response('OK')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')
