from typing import Union

from apps.guides.selectors.mo import mo_model


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
        return mo_model.objects.filter(**find).exists()

    def get_mo_object_by_name(self, name: str) -> Union[mo_model, None]:
        """
        Получение МО по полученному наименованию
        :param name: Наименование МО
        :return: Объект Mo (если не найден - None)
        """
        if self.is_mo_exist(
            'name',
            name
        ):
            return mo_model.objects.get(name=name)
        return None


mo_service = MoService()
