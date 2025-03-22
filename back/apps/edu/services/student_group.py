import datetime
import re
import uuid
from typing import Optional

from django.http import HttpResponse

from apps.docs.services.student_group.docx.deduction_order import DeductionOrder
from apps.docs.services.student_group.docx.information_letter import InformationLetter
from apps.docs.services.student_group.docx.offer_project import OfferProject
from apps.docs.services.student_group.docx.service_memo import ServiceMemo
from apps.docs.services.student_group.docx.service_order import ServiceOrder
from apps.docs.services.student_group.docx.transfer_order import TransferOrder
from apps.docs.services.student_group.excel.forms import FormsDoc
from apps.edu.consts.student_group.doc_type_class_mapping import STUDENT_GROUP_DOC_TYPE_MAPPING
from apps.edu.consts.student_group.doc_type_path_mapping import STUDENT_GROUP_DOC_TYPE_PATH_MAPPING
from apps.edu.consts.student_group.doc_types import STUDENT_GROUP_DOC_TYPES, INFORMATION_LETTER, \
    SERVICE_MEMO, SERVICE_ORDER, OFFER_PROJECT, TRANSFER_ORDER, DEDUCTION_ORDER, FORMS
from apps.edu.exceptions.student_group.generate_code_error import GenerateCodeError
from apps.edu.selectors.student_group import student_group_model, student_group_orm
from apps.edu.services.service.education_service import EducationServiceService, education_service_service
from apps.edu.services.service.information_service import InformationServiceService, information_service_service


class StudentGroupService:
    """Класс методов для работы с учебными группами"""

    @staticmethod
    def is_group_exists(attribute_name: str, value: str) -> bool:
        """
        Проверка на существующую учебную группу
        :param attribute_name: название атрибута для поиска
        :param value: значение атрибута
        :return: True - объекты существуют, False - объекты не найдены
        """
        find = {attribute_name: value}
        return student_group_model.objects.filter(**find).exists()

    def get_student_group(self, attribute_name: str, value: str) -> Optional[student_group_model]:
        """
        Получение объекта учебной группы
        :param attribute_name: атрибута модели StudentGroup
        :param value: значение атрибута
        :return: StudentGroup или None если группа не найдена
        """
        if self.is_group_exists(attribute_name, value):
            find = {attribute_name: value}
            return student_group_model.objects.filter(**find).first()
        return None

    def generate_group_code(self, department: str, service_type: str) -> str:
        """
        Генерация кода для учебной группы
        :param department: Наименование подразделения из AD (display_name)
        :param service_type: Тип услуги (ou, iku)
        :return: сгенерированный код
        """
        code = '-'
        try:
            dep_letters = re.split(' |-', department)
            short_name = ''
            for letter in dep_letters:
                if letter == 'и':
                    short_name += letter
                else:
                    short_name += letter[:1].upper()
            month = str(datetime.datetime.now().month)
            if len(month) == 1:
                month = '0' + month
            year = str(datetime.datetime.now().year)
            code = short_name
            if service_type == 'ou':
                code += '-ПК' + str(EducationServiceService.service_count(department))
            else:
                code += '-С' + str(InformationServiceService.service_count(department))
            code += '-' + month + '-' + year[2:]
            if self.is_group_exists('code', code):
                count = student_group_model.objects.filter(code=code).count()
                code += '-' + str(count)
        except RuntimeError:
            raise GenerateCodeError
        return code

    def create_group(self, validated_data: dict):
        """
        Создание учебной группы
        :param validated_data: словарь валидированных данных из StudentGroupAddSerializer
        :return:
        """
        create_data = dict(validated_data)
        department = ''
        if validated_data.get('type') == 'ou':
            create_data['ou_id'] = validated_data.get('service_id')
            dep = education_service_service.get_info_by_service(
                'object_id',
                validated_data.get('service_id'),
                'dep_name'
            )
        else:
            create_data['iku_id'] = validated_data.get('service_id')
            dep = information_service_service.get_info_by_service(
                'object_id',
                validated_data.get('service_id'),
                'dep_name'
            )
        if dep is not None:
            department = dep
        del create_data['service_id']
        create_data['code'] = self.generate_group_code(department, create_data.get('type'))
        del create_data['type']
        student_group_orm.create_record(create_data)

    @staticmethod
    def get_doc_response(group_id: uuid, doc_type: STUDENT_GROUP_DOC_TYPES) -> HttpResponse:
        """
        Получение респонза с запрашиваемым документом по учебной группе
        :param group_id: object_id учебной группы
        :param doc_type: Тип документа
        :return: HttpResponse с документом
        """
        xlsx = False
        doc_class = STUDENT_GROUP_DOC_TYPE_MAPPING[doc_type](group_id)
        if doc_type == FORMS:
            xlsx = True
        return doc_class.get_response(
            STUDENT_GROUP_DOC_TYPE_PATH_MAPPING[doc_type],
            xlsx
        )


student_group_service = StudentGroupService()
