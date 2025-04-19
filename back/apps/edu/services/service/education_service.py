import datetime
import uuid
from typing import Optional

from apps.edu.exceptions.planning_parameter.planning_days_error import PlanningDaysError
from apps.edu.selectors.program import program_model
from apps.edu.selectors.services.education_service import education_service_model, education_service_orm
from apps.edu.services.planning_parameter import planning_parameter_service


class EducationServiceService:
    """Класс методов для работы с ОУ (курсами)"""

    @staticmethod
    def get_count() -> int:
        """
        Получение общего количества курсов в АИС
        """
        return education_service_model.objects.count()

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
                program__in=(program_model.objects.
                             select_related('department').
                             select_related('kug_edit').
                             prefetch_related('categories').
                             select_related('program_order').
                             filter(department__display_name=department))
            ).filter(
                date_start__year=datetime.datetime.now().year
            ).count()

    @staticmethod
    def create_service(validated_data: dict):
        """
        Создание курса (ОУ)
        :param validated_data: Словарь с валидированными данными из EducationServiceAddUpdateSerializer
        :return:
        """
        create_data = dict(validated_data)
        del create_data['program']
        create_data['program_id'] = validated_data.get('program')
        if planning_parameter_service.check_planning_days(validated_data.get('date_start')):
            education_service_orm.create_record(create_data)
        else:
            raise PlanningDaysError

    @staticmethod
    def update_service(service_id: uuid, validated_data: dict):
        """
        Обновление курса (ОУ)
        :param service_id: UUID курса (ОУ)
        :param validated_data: Словарь с валидированными данными из EducationServiceAddUpdateSerializer
        :return:
        """
        update_data = dict(validated_data)
        del update_data['object_id']
        del update_data['program']
        update_data['program_id'] = validated_data.get('program')
        if planning_parameter_service.check_planning_days(validated_data.get('date_start')):
            education_service_orm.update_record({'object_id': service_id}, update_data)
        else:
            raise PlanningDaysError


education_service_service = EducationServiceService()
