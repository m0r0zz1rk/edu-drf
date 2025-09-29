from typing import Optional
from apps.guides.selectors.audience_category import audience_category_model, audience_category_orm


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
        category = audience_category_orm.get_one_record_or_none(filter_by=find)
        return category is not None

    def get_category_object_by_name(self, category_name: str) -> Optional[audience_category_model]:
        """
        Получение объекта категории слушателей по наименованию
        :param category_name: наименование категории
        :return: None - категория не найдена, audicence_category_model - объект AudienceCategory
        """
        if self.is_category_exists('name', category_name):
            return audience_category_orm.get_one_record_or_none(filter_by={'name': category_name})
        return None


audience_category_service = AudienceCategoryService()
