from django.apps import AppConfig


class AuthenConfig(AppConfig):
    name = 'apps.authen'
    verbose_name = 'Приложение регистрации/авторизации пользователей'

    def ready(self):
        import apps.authen.signals
