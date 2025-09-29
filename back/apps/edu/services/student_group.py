import datetime
import re
import uuid
from typing import Optional

from django.db.models import QuerySet
from django.http import HttpResponse
from pandas._libs.tslibs.offsets import BDay

from apps.commons.utils.data_types.string import string_utils
from apps.commons.utils.django.settings import settings_utils
from apps.docs.selectors.student_group_offer import student_group_offer_orm
from apps.docs.services.student_group.excel.certificates_list import CertificatesList
from apps.edu.consts.student_group.doc_type_class_mapping import STUDENT_GROUP_DOC_TYPE_MAPPING
from apps.edu.consts.student_group.doc_type_path_mapping import STUDENT_GROUP_DOC_TYPE_PATH_MAPPING
from apps.edu.consts.student_group.doc_types import STUDENT_GROUP_DOC_TYPES, FORMS, STUDENT_JOURNAL, SCHEDULE, \
    CERTIFICATES_LIST
from apps.edu.consts.student_group.statuses import STUDENT_GROUP_STATUSES
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
        group = student_group_orm.get_one_record_or_none(filter_by=find)
        return group is not None

    def get_student_group(self, attribute_name: str, value: str) -> Optional[student_group_model]:
        """
        Получение объекта учебной группы
        :param attribute_name: атрибута модели StudentGroup
        :param value: значение атрибута
        :return: StudentGroup или None если группа не найдена
        """
        if self.is_group_exists(attribute_name, value):
            find = {attribute_name: value}
            return student_group_orm.get_one_record_or_none(filter_by=find)
        return None

    @staticmethod
    def get_offer(group_id: uuid):
        """
        Получение договора оферты (при наличии)
        :param group_id: object_id учебной группы
        :return: Файл договора оферты если существует, иначе None
        """
        return student_group_offer_orm.get_one_record_or_none(filter_by={'group_id': group_id})

    def generate_group_code(self, department: str, service_type: str) -> str:
        """
        Генерация кода для учебной группы
        :param department: Наименование подразделения из AD (display_name)
        :param service_type: Тип услуги (ou, iku)
        :return: сгенерированный код
        """
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
            service_count = EducationServiceService.service_count(department)
            type_sign = 'ПК'
            if service_type != 'ou':
                service_count = InformationServiceService.service_count(department)
                type_sign = 'С'
            code += f'-{type_sign}{str(service_count+1)}' if service_count != 0 else f'-{type_sign}1'
            code += f'-{month}-{year[2:]}'
            groups = student_group_orm.get_filter_records(filter_by={'code': code})
            if self.is_group_exists('code', code):
                code += f'-{str(groups.count())}'
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
    def get_doc_response(
            group_id: uuid,
            doc_type: STUDENT_GROUP_DOC_TYPES,
            orders_info: dict = None
    ) -> HttpResponse:
        """
        Получение респонза с запрашиваемым документом по учебной группе
        :param group_id: object_id учебной группы
        :param doc_type: Тип документа
        :param orders_info: Словарь с информацией о приказах об зачислении и отчислении
        :return: HttpResponse с документом
        """
        if doc_type == CERTIFICATES_LIST:
            doc_class = CertificatesList(group_id, orders_info)
            return doc_class.get_response((), True)
        xlsx = False
        doc_class = STUDENT_GROUP_DOC_TYPE_MAPPING[doc_type](group_id)
        if doc_type in [FORMS, STUDENT_JOURNAL, SCHEDULE]:
            xlsx = True
        return doc_class.get_response(
            STUDENT_GROUP_DOC_TYPE_PATH_MAPPING[doc_type],
            xlsx
        )

    @staticmethod
    def change_group_status(group_id: uuid, status: STUDENT_GROUP_STATUSES):
        """
        Изменение статуса учебной группы
        :param group_id: object_id учебной группы
        :param status: новый статус
        :return:
        """
        student_group_orm.update_record(
            filter_by={'object_id': group_id},
            update_object={'status': status}
        )

    @staticmethod
    def get_group_service_type(group_id: uuid) -> str:
        """
        Получение типа услуги учебной группы
        :param group_id: object_id учебной группы
        :return: ou - если курс (ОУ), иначе iku
        """
        group = student_group_orm.get_one_record_or_none(filter_by={'object_id': group_id})
        return 'ou' if group.ou is not None else 'iku'

    @staticmethod
    def get_data_for_offer_pay_task(group_id: uuid) -> tuple:
        """
        Получение информации для выполнения задачи отправки писем с офертой пользователям АИС
        :param group_id: object_id учебной группы
        :return: кортеж из 5 значений - тип мероприятия, наименование, дата начала, URL, дедлайна оплаты
        """
        group = student_group_orm.get_one_record_or_none(dict(object_id=group_id))
        if group.ou:
            if group.ou.program.type == 'Повышение квалификации':
                event_type = 'курсе повышения квалификации'
            else:
                event_type = 'курсе профессиональной переподготовки'
            name = group.ou.program.name
            date_start = group.ou.date_start
        else:
            event_type = string_utils.get_word_case(
                group.iku.type.name,
                'loct'
            )
            name = group.iku.name
            date_start = group.iku.date_start
        deadline = date_start - BDay(settings_utils.get_parameter_from_settings('PAY_DATE_DAYS'))
        return event_type, name, date_start, deadline

    @staticmethod
    def get_groups_with_status(statuses: list[STUDENT_GROUP_STATUSES]) -> QuerySet:
        """
        Получение учебных групп со статусом
        :param statuses: Статусы учебной группы
        :return: QuerySet с группами
        """
        return student_group_orm.get_filter_records(filter_by=dict(status__in=statuses))

    @staticmethod
    def update_group_status(group_id: uuid, status: STUDENT_GROUP_STATUSES):
        """
        Обновление статуса учебной группы
        :param group_id: object_id учебной группы
        :param status: Новый статус
        :return:
        """
        student_group_orm.update_record(
            filter_by=dict(object_id=group_id),
            update_object={'status': status}
        )

    @staticmethod
    def show_group_survey(group_id: uuid):
        """
        Отобразить прохождение опроса в учебной группе
        :param group_id: object_id учебной группы
        :return:
        """
        student_group_orm.update_record(
            filter_by=dict(object_id=group_id),
            update_object=dict(survey_show=True)
        )


student_group_service = StudentGroupService()
