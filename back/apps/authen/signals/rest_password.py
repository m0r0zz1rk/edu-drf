from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created

from apps.celery_app.tasks.worker.password_reset_email import password_reset_email_task
from apps.commons.utils.django.settings import settings_utils


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """Обработка поступившего запроса на восстановление пароля"""
    # send an e-mail to the user
    ais_address = settings_utils.get_parameter_from_settings('AIS_ADDRESS')
    context = {
        'reset_password_url': f"{ais_address}password_reset?token={reset_password_token.key}"
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    password_reset_email_task.delay(reset_password_token.user.email, email_html_message)
