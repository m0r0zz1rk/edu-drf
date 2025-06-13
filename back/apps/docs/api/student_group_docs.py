from drf_yasg.utils import swagger_auto_schema

from apps.celery_app.tasks import email_print_file
from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.docs.api.doc_viewset import DocsViewSet
from apps.docs.selectors.student_group_offer import student_group_offer_orm
from apps.docs.serializers.licenses import UploadLicenses
from apps.docs.serializers.print_file import PrintFileSerializer
from apps.docs.serializers.student_group_offer import StudentGroupOfferSerializer
from apps.docs.services.student_group.upload_offer import upload_offer
from apps.docs.utils.license_scan import license_scan_service
from apps.journal.consts.journal_modules import DOCS


class StudentGroupDocsViewSet(DocsViewSet):
    orm = student_group_offer_orm
    swagger_object_name = 'Документ учебной группы'

    @swagger_auto_schema(
        tags=[f'Документы. {swagger_object_name}', ],
        operation_description="Обновление договора оферты учебной группы",
        request_body=StudentGroupOfferSerializer,
        responses=SWAGGER_TEXT['update']
    )
    @view_set_journal_decorator(
        DOCS,
        f'Договор оферты учебной группы успешно обновлен',
        f'Ошибка при обновлении договора оферты учебной группы"'
    )
    def partial_update(self, request, *args, **kwargs):
        serialize = StudentGroupOfferSerializer(data=request.data)
        if serialize.is_valid():
            upload_offer(
                self.kwargs['group_id'],
                serialize.validated_data.get('file'),
            )
            return response_utils.ok_response('Обновление выполнено')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=[f'Документы. {swagger_object_name}', ],
        operation_description="Отправка файла печати с удостоверениями на почту",
        request_body=PrintFileSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при выполнении запроса',
            '200': 'Сообщение "Запрос обработан, ожидайте письма с файлом"'
        }
    )
    @view_set_journal_decorator(
        DOCS,
        f'Файл печати успешно сформирован и отправлен',
        f'Ошибка при формировании или отправке файла печати "'
    )
    def print_file(self, request, *args, **kwargs):
        serialize = PrintFileSerializer(data=request.data)
        if serialize.is_valid():
            email_print_file.delay(
                serialize.validated_data.get('group_id'),
                request.user.email,
                serialize.validated_data.get('to_print_office'),
            )
            return response_utils.ok_response('Запрос обработан, ожидайте письма с файлом')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {serialize.errors}')

    @swagger_auto_schema(
        tags=[f'Документы. {swagger_object_name}', ],
        operation_description="Подгрузка сканов удостоверений",
        request_body=UploadLicenses,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка в работе сервиса',
            '200': 'Сообщение "Файлы успешно подгружены"'
        }
    )
    @view_set_journal_decorator(
        DOCS,
        f'Сканы успешно подгружены',
        f'Ошибка при подгрузке сканов удостоверений обучающихся"'
    )
    def upload_licenses(self, request, *args, **kwargs):
        serialize = UploadLicenses(data=request.data)
        if serialize.is_valid():
            license_scan_service.upload_licenses(
                serialize.validated_data.get('file'),
                serialize.validated_data.get('group_id')
            )
            return response_utils.ok_response('Файлы успешно подгружены')
        else:
            return response_utils.bad_request_response(f'Ошибка в работе сервиса: {serialize.errors}')
