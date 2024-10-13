from django.db.models import QuerySet

from apps.applications.selectors.course_application import course_application_model
from apps.authen.services.profile import ProfileService
from apps.commons.services.ad.ad_centre import AdCentreService
from apps.edu.selectors.program import program_queryset
from apps.edu.selectors.services.education_service import education_service_queryset


class CourseService:
    """Класс методов для работы с курсами"""

    _profile_service = ProfileService()
    _program_qs = program_queryset()
    _edu_service_qs = education_service_queryset()
    _ad_centre_service = AdCentreService()

    def get_departments_courses(self, user_id: int, group_queryset: QuerySet) -> list:
        """
        Получение списка курсов для регистрации по подразделениям
        :param user_id: ID пользователя Django
        :param group_queryset: QuerySet с группами для курсов и статусом "Регистрация"
        :return: список словарей с подразделением и его группами
        """
        res = []
        profile = self._profile_service.get_profile_or_info_by_attribute(
            'django_user_id',
            user_id,
            'profile'
        )
        not_apps_group = group_queryset.exclude(
            object_id__in=course_application_model.objects.filter(
                profile_id=profile.object_id
            ).values_list('group__object_id', flat=True)
        )
        programs = {program for program in
                    not_apps_group.values_list('ou__program', flat=True)}
        deps = {department for department in
                self._program_qs.filter(object_id__in=programs).values_list('department__object_id', flat=True)}
        for dep in deps:
            res.append({
                'department': self._ad_centre_service.get_ad_centre(
                    'object_id',
                    dep
                ).display_name,
                'services': group_queryset.filter(
                    ou__in=self._edu_service_qs.filter(
                        program__in=self._program_qs.filter(
                            department_id=dep
                        )
                    )
                )
            })
        return res
