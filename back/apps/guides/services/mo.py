from typing import Union

from django.db.models import QuerySet

from apps.guides.selectors.mo import mo_model, mo_orm


class MoService:
    """Класс действия для работы с МО"""

    @staticmethod
    def is_mo_exist(attribute: str, value: str) -> bool:
        """
        Проверка на существующее МО
        :param attribute: поле модели Mo
        :param value: значение атрибута
        :return: True - существует, False - не существует
        """
        find = {attribute: value}
        mo = mo_orm.get_filter_records(filter_by=find)
        return mo is not None

    def get_mo_object_by_name(self, name: str) -> Union[mo_model, None]:
        """
        Получение МО по полученному наименованию
        :param name: Наименование МО
        :return: Объект Mo (если не найден - None)
        """
        if self.is_mo_exist('name', name):
            return mo_orm.get_one_record_or_none(filter_by={'name': name})
        return None

    @staticmethod
    def get_all() -> QuerySet:
        """
        Получение полного списка МО
        :return: QuerySet с МО
        """
        return mo_orm.get_filter_records(order_by=['name',])


mo_service = MoService()
