from django.db.models import QuerySet

from apps.guides.selectors.position_category import position_category_orm


class PositionCategoryService:
    """
    Класс методов для работы с категориями должностей
    """

    @staticmethod
    def get_all() -> QuerySet:
        """
        Получение списка со всеми должностями
        :return: QuerySet со всеми должностями
        """
        return position_category_orm.get_filter_records(order_by=['name', ])


position_category_service = PositionCategoryService()
