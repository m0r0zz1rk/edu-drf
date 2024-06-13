from typing import Optional

from django.apps import apps

audience_category_model = apps.get_model('guides', 'AudienceCategory')


class AudienceCategoryService:
    """Класс методов для работы с категорями слушателей"""

    @staticmethod
    def is_category_exists(attribute_name: str, value: str) -> bool:
        """
        Проверка на существующую категорию
        :param attribute_name: поле модели AudienceCategory
        :param value: значение для поля
        :return: True - существует, False - не существует
        """
        find = {attribute_name: value}
        return audience_category_model.objects.filter(**find).exists()

    def get_category_object_by_name(self, category_name: str) -> Optional[audience_category_model]:
        """
        Получение объекта категории слушателей по наименованию
        :param category_name: наименование категории
        :return: None - категория не найдена, audicence_category_model - объект AudienceCategory
        """
        if self.is_category_exists('name', category_name):
            return audience_category_model.objects.get(name=category_name)
        return None
