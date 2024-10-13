from apps.applications.models.base_application import BaseApplication


class EventApplication(BaseApplication):
    """Модель заявок на участие в мероприятии"""

    class Meta:
        verbose_name = 'Заявка на участие в мероприятии'
        verbose_name_plural = 'Заявки на участие в мероприятиях'
