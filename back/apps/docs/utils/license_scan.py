import base64
import datetime
import os
import uuid
from typing import Optional

import rarfile
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.applications.consts.application_statuses import ARCHIVE
from apps.applications.selectors.course_application import course_application_orm
from apps.applications.services.course_application import course_application_service
from apps.applications.services.course_certificate import course_certificate_service
from apps.commons.utils.django.exception import exception_handling
from apps.commons.utils.django.settings import settings_utils
from apps.docs.exceptions.extract_scans_exception import ExtractScansException
from apps.docs.serializers.student_doc import StudentDocCreateSerializer
from apps.docs.services.student_doc import student_doc_service
from apps.edu.services.student_group import student_group_service
from apps.journal.consts.journal_modules import DOCS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import journal_service

license_scan_base_folder = os.path.join(
    settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
    'Сертификаты'
)


class LicenseScanService:
    """
    Класс для работы со сканами сертификатами обучающихся
    """

    @staticmethod
    def extract_file_from_archive(file: InMemoryUploadedFile, group_id: uuid) -> Optional[str]:
        """
        Распаковка файла из архива в папку
        :param file: полученный файл с расширением .rar
        :param group_id: object_id учебной группы
        :return: Путь к папке с разархивированными файлами или None если было вызвано исключение
        """
        try:
            archive = rarfile.RarFile(file)
            student_group = student_group_service.get_student_group('object_id', group_id)
            folder_path = os.path.join(
                license_scan_base_folder,
                student_group.code,
                datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')
            )
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            archive.extractall(path=folder_path)
            return folder_path
        except Exception:
            e = ExtractScansException()
            e.traceback = exception_handling.get_traceback()
            raise e

    def upload_licenses(self, file: InMemoryUploadedFile, group_id: uuid) -> Optional[int]:
        """
        Подгрузка сканов сертификатов учебной группы из архива
        :param file: архив с сертификатами, имена которых содержат регистрационный номер и формат .pdf
        :param group_id: object_id учебной группы
        :return: Количество обработанных сканов или None в случае ошибки
        """
        try:
            scans_path = self.extract_file_from_archive(file, group_id)
            files = os.listdir(scans_path)
            for file in files:
                try:
                    dot_split = file.split('.')
                    if len(dot_split) != 2 or dot_split[1] != 'pdf':
                        continue
                    cert = course_certificate_service.get_certificate('registration_number', dot_split[0])
                    if not cert:
                        continue
                    app = course_application_service.get_course_app(cert.application_id)
                    if not app:
                        continue
                    if app.certificate_doc_id:
                        student_doc_service.delete_student_doc(str(app.certificate_doc_id))
                    with open(os.path.join(scans_path, file), "rb") as pdf:
                        pdf_data = pdf.read()
                    serialize = StudentDocCreateSerializer(
                        data=dict(
                            doc_type='license_scan',
                            file=base64.b64encode(pdf_data).decode('utf-8')
                        )
                    )
                    if serialize.is_valid():
                        new_license_id = student_doc_service.create_student_doc(
                            app.profile.django_user_id,
                            serialize.validated_data
                        )
                        course_application_orm.update_record(
                            dict(object_id=app.object_id),
                            dict(certificate_doc_id=new_license_id, status=ARCHIVE)
                        )
                    else:
                      continue
                except Exception as e:
                    pass
            # os.remove(scans_path)
        except ExtractScansException as e:
            journal_service.create_journal_rec(
                {
                    'source': "Сервис сканов удостоверений",
                    'module': DOCS,
                    'status': ERROR,
                    'description': 'Системная ошибка при распаковке архива с '
                },
                f'group_id: {group_id}',
                e.traceback
            )
            return None


license_scan_service = LicenseScanService()

