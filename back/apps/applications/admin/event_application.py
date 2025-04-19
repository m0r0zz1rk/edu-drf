from django.contrib import admin

from apps.applications.admin.base_application import BaseApplicationAdmin
from apps.applications.selectors.event_application import (
    event_application_model)


@admin.register(event_application_model)
class EventApplicationAdmin(BaseApplicationAdmin):
    """
    Класс для отображения заявок пользователей на
    участие в мероприятиях в административной панели
    """
    pass
