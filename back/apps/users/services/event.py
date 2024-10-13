from django.db.models import QuerySet

from apps.commons.services.ad.ad_centre import AdCentreService
from apps.edu.selectors.services.information_service import information_service_queryset


class EventService:
    """Класс методов для работы с курсами"""

    _info_service_qs = information_service_queryset()
    _ad_centre_service = AdCentreService()

    def get_departments_events(self, group_queryset: QuerySet) -> list:
        """
        Получение списка мероприятий для регистрации по подразделениям
        :param group_queryset: QuerySet с группами для мероприятий и статусом "Регистрация"
        :return: список словарей с подразделением и его группами
        """
        res = []
        deps = {department for department in
                group_queryset.values_list('iku__department_id', flat=True)}
        for dep in deps:
            res.append({
                'department': self._ad_centre_service.get_ad_centre(
                    'object_id',
                    dep
                ).display_name,
                'services': group_queryset.filter(
                    iku__in=self._info_service_qs.filter(
                        department_id=dep
                    )
                )
            })
        return res
