from typing import Union

from django.db.models import QuerySet

from apps.guides.selectors.oo_type import oo_type_model, oo_type_orm


class OoTypeService:
    """Класс действия для работы с типами ОО"""

    @staticmethod
    def is_oo_type_exist(attribute: str, value: str) -> bool:
        """
        Проверка на существующий тип ОО
        :param attribute: поле модели OoType
        :param value: значение атрибута
        :return: True - существует, False - не существует
        """
        find = {attribute: value}
        return oo_type_model.objects.filter(**find).exists()

    def get_oo_type_object_by_name(self, name: str) -> Union[oo_type_model, None]:
        """
        Получение типа ОО по полученному наименованию
        :param name: наименование типа ОО
        :return: Объект OoType (если не найдено - None)
        """
        if self.is_oo_type_exist(
            'name',
            name
        ):
            return oo_type_model.objects.get(name=name)
        return None

    @staticmethod
    def get_all() -> QuerySet:
        """
        Получение полного списка типов ОО
        :return: QuerySet с типами ОО
        """
        return oo_type_orm.get_filter_records(order_by=['name', ])


oo_type_service = OoTypeService()
