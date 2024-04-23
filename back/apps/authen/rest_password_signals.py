from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created

from apps.celery_app.tasks.password_reset_email import password_reset_email_task


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """Обработка поступившего запроса на восстановление пароля"""
    # send an e-mail to the user
    context = {
        'reset_password_url': "{}?token={}".format(
            settings.AIS_ADDRESS+'password_reset',
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    password_reset_email_task.delay(reset_password_token.user.email, email_html_message)

    """send_mail(
        "АИС подачи заявок ИОХК: Сброс пароля",
        None,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email, ],
        fail_silently=False,
        html_message=email_html_message
    )"""
