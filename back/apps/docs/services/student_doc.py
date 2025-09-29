import uuid

from django.db.models import QuerySet

from apps.authen.exceptions.student_profile import StudentNotExist
from apps.authen.selectors.student_profile import student_profile_orm
from apps.authen.services.profile import profile_service
from apps.commons.utils.django.settings import SettingsUtils
from apps.docs.consts.student_doc_types import STUDENT_DOC_TYPES
from apps.docs.exceptions.student_doc import StudentDocNotValidInfo, StudentDocNotFound
from apps.docs.selectors.student_doc import student_doc_orm


class StudentDocService:
    """Класс методов для работы с документами обучающегося"""

    _su = SettingsUtils()

    _doc_info_keys = ('doc_type', 'file')

    @staticmethod
    def get_student_docs(user_id: int) -> QuerySet:
        """
        Получение списка документов обучающегося
        :param user_id: ID пользователя Django
        :return: QuerySet с документами пользователя
        """
        try:
            profile = student_profile_orm.get_one_record_or_none(filter_by={'django_user_id': user_id})
            if not profile:
                raise StudentNotExist
            return student_doc_orm.get_filter_records(filter_by={'profile_id': profile.object_id})
        except Exception:
            raise StudentNotExist

    def create_student_doc(self, user_id: int, doc_info: dict) -> uuid:
        """
        Добавление нового документа обучающегося
        :param user_id: ID пользователя Django
        :param doc_info: Словарь с информацией о новом документе
        """
        for key in self._doc_info_keys:
            if key not in doc_info:
                raise StudentDocNotValidInfo
        profile = profile_service.get_profile_or_info_by_attribute('django_user_id', user_id, 'profile')
        if not profile:
            raise StudentNotExist
        doc_info['profile'] = profile
        for sdt in STUDENT_DOC_TYPES:
            if sdt[1] == doc_info['doc_type']:
                doc_info['doc_type'] = sdt[0]
        doc = student_doc_orm.create_record(doc_info)
        return doc.object_id

    @staticmethod
    def delete_student_doc(object_id: str):
        """
        Удаление документа пользователя
        :param object_id: object_id документа в базе
        :return:
        """
        try:
            student_doc_orm.delete_record(filter_by={'object_id': object_id})
        except Exception:
            raise StudentDocNotFound


student_doc_service = StudentDocService()
