import datetime
from typing import Optional

from apps.edu.consts.planning_parameters import PlanningParameters
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

    @staticmethod
    def get_parameter_value_by_name(name: PlanningParameters) -> Optional[str]:
        """
        Получение значение параметра планирования по имени
        :param name: наименование параметра
        :return: Значение параметра
        """
        rec = planning_parameter_orm.get_one_record_or_none(dict(name=name.value))
        if rec:
            return rec.value
        return None

    def check_planning_days(self, date_create: datetime) -> bool:
        """
        Проверка на параметр планирования
        "Количество дней для планирования (минимальный срок до которого можно создать ОУ или ИКУ)"
        :param date_create: дата создания, поступившая в запросе
        :return: True если условие выполняется, иначе False
        """
        parameter = self.get_planning_parameter('name', str(PlanningParameters.PLANNING_DAYS.value))
        if not parameter:
            return True
        delta = date_create - datetime.date.today()
        return delta.days > int(parameter.value)


planning_parameter_service = PlanningParameterService()
