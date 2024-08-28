import datetime
from typing import Optional

from apps.edu.selectors.program import program_model
from apps.edu.selectors.services.education_service import education_service_model


class EducationServiceService:
    """Класс методов для работы с ОУ (курсами)"""

    @staticmethod
    def is_service_exists(attribute_name: str, value: str) -> bool:
        """
        Проверка на существующую ОУ (курс)
        :param attribute_name: наименование атрибута для поиска
        :param value: значение атрибута
        :return: True - существует, False - не существует
        """
        find = {attribute_name: value}
        return education_service_model.objects.filter(**find).exists()

    def get_info_by_service(self, attribute_name: str, value: str, info: str) -> Optional[str]:
        """
        Получение информации о услуги
        :param attribute_name: наименование атриубта для поиска
        :param value: значения атрибута
        :param info: информация (dep_name, date_start, service_name)
        :return: str - display_name подразделения AD, None - ОУ не найдена
        """
        if self.is_service_exists(attribute_name, value):
            find = {attribute_name: value}
            service = education_service_model.objects.filter(**find).first()
            if info == 'dep_name':
                return service.program.department.display_name
            elif info == 'date_start':
                return service.date_start.strftime('%d.%m.%Y')
            elif info == 'date_end':
                return service.date_end.strftime('%d.%m.%Y')
            else:
                return service.program.name
        return None

    @staticmethod
    def service_count(department: str) -> int:
        """
        Получение количества ОУ (курсов) для подразделения в текущем году
        :param department: display_name подразделения AD
        :return: количество ОУ (курсов)
        """
        return education_service_model.objects. \
            filter(
                program__in=program_model.objects.filter(department__display_name=department)
            ).filter(
                date_start__year=datetime.datetime.now().year
            ).count()
