from django.contrib import admin

from apps.applications.admin.base_application import BaseApplicationAdmin
from apps.applications.selectors.course_application import (
    course_application_model)


@admin.register(course_application_model)
class CourseApplicationAdmin(BaseApplicationAdmin):
    """
    Класс для отображения заявок на участие в
    курсах в административной панели
    """
    pass
