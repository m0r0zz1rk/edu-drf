from django.db import models

from apps.commons.models import BaseTable


class PayDeniedMessage(BaseTable):
    """Таблица с комментариями при некорректной оплате заявки"""
    course_application = models.ForeignKey(
        'applications.CourseApplication',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Заявка на курс (ОУ)'
    )
    event_application = models.ForeignKey(
        'applications.EventApplication',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Заявка на мероприятие (ИКУ)'
    )
    message = models.TextField(
        max_length=500,
        blank=True,
        null=False,
        default='',
        verbose_name='Комментарий об отклоненной оплате'
    )

    def __str__(self):
        if self.course_application:
            app = self.course_application
        else:
            app = self.event_application
        return f'Комментарий об отклоненной оплате заявки "{app.profile.display_name}" в группу "{app.group.code}"'

    class Meta:
        verbose_name = 'Коментарий об отклонненой оплате заявки'
        verbose_name_plural = 'Коментарии об отклонненых оплатах заявок'
