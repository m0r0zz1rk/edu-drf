from apps.commons.utils.django.auth.auth_backend import AuthBackend


class AuthorizationAuthenticationUtils:
    """Класс дополнительных действий при работе с авторизацией/аутентификацией пользователей"""

    @staticmethod
    def is_request_auth_admin(request, admin_check: bool = None) -> bool:
        """Проверка поступившего запроса на авторизацию и администратора АИС (по ситуации)"""
        auth = AuthBackend()
        __user = auth.authenticate(request)
        if admin_check is None:
            return __user is not None
        if __user is not None and __user[0] is not None:
            return __user[0].is_superuser
        return False
