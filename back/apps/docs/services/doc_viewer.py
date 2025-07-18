import os
import uuid

from apps.docs.selectors.pay_doc import pay_doc_model
from apps.docs.selectors.student_doc import student_doc_model
from apps.docs.selectors.student_group_offer import student_group_offer_orm


class DocViewerService:
    """
    Класс методов для просмотра документов на web форме
    """

    @staticmethod
    def get_file_attr(doc_type: str, doc_id: uuid, attr: str):
        """
        Получение файла
        :param doc_type: тип файла (student, pay или offer)
        :param doc_id: object_id документа
        :param attr: атрибут записи (name или file)
        """
        if doc_type == 'student':
            file = student_doc_model.objects.get(object_id=doc_id).file
        elif doc_type == 'offer':
            file = student_group_offer_orm.get_one_record_or_none(filter_by=dict(object_id=doc_id)).file
        else:
            file = pay_doc_model.objects.get(object_id=doc_id).file
        if attr == 'name':
            return os.path.basename(file.name)
        return file


doc_viewer_service = DocViewerService()
