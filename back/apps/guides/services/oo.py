import uuid

from django.db.models import QuerySet

from apps.guides.selectors.oo import oo_queryset


class OoService:
    """Класс методов для работы с ОО"""

    @staticmethod
    def get_mo_oos(mo_id: uuid) -> QuerySet:
        """
        Получение списка ОО для конкретного МО
        :param mo_id: object_id МО
        :return: QuerySet с попадающими под параметры ОО
        """
        return oo_queryset().filter(mo_id=mo_id).order_by('short_name')
