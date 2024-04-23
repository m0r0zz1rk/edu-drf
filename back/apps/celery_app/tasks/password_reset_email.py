from django.conf import settings
from django.core.mail import send_mail

from apps.commons.utils.django.exception import ExceptionHandling
from web_app.init_celery import app


@app.task
def password_reset_email_task(email, html_message):
    """Отправка пользователю письма со ссылкой на сброс пароля"""
    try:
        send_mail(
            'АИС "Мероприятия ИОХК": Сброс пароля',
            None,
            settings.EMAIL_HOST_USER,
            [email, ],
            fail_silently=False,
            html_message=html_message
        )
        return 'Письмо отправлено'
    except BaseException:
        return f'Ошибка: {ExceptionHandling.get_traceback()}'
