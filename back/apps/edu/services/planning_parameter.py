import datetime
from typing import Optional

from apps.edu.selectors.planning_parameter import planning_parameter_model, planning_parameter_orm


class PlanningParameterService:
    """Класс методов для работы с параметрами планирования"""

    @staticmethod
    def get_planning_parameter(attribute_name: str, value: str) -> Optional[planning_parameter_model]:
        """
        Получение параметра планирования
        :param attribute_name: имя атрибута для поиска (object_id, name, description)
        :param value: значение атрибута
        :return: None - параметр не найден, planning_parameter_model - объект параметра
        """
        return planning_parameter_orm.get_one_record_or_none({attribute_name: value})
        # if self.is_parameter_exist(attribute_name, value):
        #     find = {attribute_name: value}
        #     return planning_parameter_model.objects.filter(**find).first()
        # return None

    def check_planning_days(self, date_create: datetime) -> bool:
        """
        Проверка на параметр планирования
        "Количество дней для планирования (минимальный срок до которого можно создать ОУ или ИКУ)"
        :param date_create: дата создания, поступившая в запросе
        :return: True если условие выполняется, иначе False
        """
        parameter = self.get_planning_parameter(
            'name',
            'planningDays'
        )
        if not parameter:
            return True
        delta = date_create - datetime.date.today()
        return delta.days > int(parameter.value)


planning_parameter_service = PlanningParameterService()
