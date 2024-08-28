import datetime
import re

from apps.edu.selectors.student_group import student_group_model
from apps.edu.services.service.education_service import EducationServiceService
from apps.edu.services.service.information_service import InformationServiceService


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
        except:
            pass
        return code
