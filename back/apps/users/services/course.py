from django.db.models import QuerySet

from apps.applications.selectors.course_application import course_application_model
from apps.authen.services.profile import profile_service
from apps.commons.services.ad.ad_centre import ad_centre_service
from apps.users.selectors.course import courses_queryset


class CourseService:
    """Класс методов для работы с курсами"""

    def get_departments_courses(self, user_id: int) -> list:
        """
        Получение списка курсов для регистрации по подразделениям
        :param user_id: ID пользователя Django
        :return: список словарей с подразделением и его группами
        """
        group_queryset = courses_queryset()
        res = []
        profile = profile_service.get_profile_or_info_by_attribute('django_user_id', user_id, 'profile')
        user_apps = course_application_model.objects.filter(profile_id=profile.object_id)
        apps_group_ids = list(user_apps.values_list('group__object_id', flat=True))
        not_apps_group = group_queryset.exclude(object_id__in=apps_group_ids)
        for group in not_apps_group:
            dep = group.ou.program.department_id
            if len(list(filter(lambda el: el['department_id'] == dep, res))) > 0:
                list(filter(lambda el: el['department_id'] == dep, res))[0]['services'].push(group)
            else:
                res.append({
                    'department': ad_centre_service.get_ad_centre('object_id', dep).display_name,
                    'department_id': dep,
                    'services': [group, ]
                })
        for dep in res:
            del dep['department_id']
        return res


course_service = CourseService()
