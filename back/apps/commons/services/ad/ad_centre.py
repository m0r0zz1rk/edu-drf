from typing import Optional

from django.apps import apps

from apps.commons.utils.validate import ValidateUtils

ad_centre_model = apps.get_model('commons', 'AdCentre')


class AdCentreService:
    """Класс методов для работы с моделью AdCentre"""

    @staticmethod
    def is_ad_centre_exist(attribute: str, value: str) -> bool:
        """
        Проверка на существующее подразделение-центр AD в базе
        :param attribute: Поле модели AdCentre
        :param value: Значение атрибута
        :return: True - существует, False - не существует
        """
        find = {attribute: value}
        return ad_centre_model.objects.filter(**find).exists()

    def get_ad_centre(self, attribute: str, value: str) -> Optional[ad_centre_model]:
        """
        Получение объекта AdCentre по полученному атрибуту и его значению
        :param attribute: Поле модели AdCentre
        :param value: Значение атрибута
        :return: Объект модели AdCentre, None - если объект не найден
        """
        if self.is_ad_centre_exist(attribute, value):
            find = {attribute: value}
            return ad_centre_model.objects.filter(**find).first()
        return None

    @staticmethod
    def add_ad_centre(ad_centre_data: dict):
        """
        Добавление нового подразделения-центра AD в БД
        :param ad_centre_data: Словарь с данными о новом подразделении
        :return:
        """
        if ValidateUtils().validate_data(
            ['display_name', 'object_guid'],
            ad_centre_data
        ):
            ad_centre_model.objects.update_or_create(
                **ad_centre_data
            )


ad_centre_service = AdCentreService()
