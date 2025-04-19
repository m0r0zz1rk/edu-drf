from django.contrib import admin

from apps.applications.admin.base_application import BaseApplicationAdmin
from apps.applications.selectors.course_certificate import course_certificate_model


@admin.register(course_certificate_model)
class CourseCertificateAdmin(BaseApplicationAdmin):
    """
    Класс для отображения модели сертификатов обучающихся в административной панели
    """

    list_display = (
        'date_create',
        'group_code',
        'student_display_name',
        'registration_number',
        'blank_serial',
        'blank_number'
    )
    search_fields = (
        'application__group__code',
        'application__profile__surname',
        'application__profile__name',
        'application__profile__patronymic'
        'registration_number',
        'blank_serial',
        'blank_number'
    )

    def group_code(self, obj):
        if obj.application:
            return obj.application.group.code
        return '-'

    def student_display_name(self, obj):
        if obj.application:
            return obj.application.profile.display_name
        return '-'
