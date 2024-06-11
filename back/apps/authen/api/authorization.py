from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.authen.operations.auth_check import AuthCheck
from apps.authen.operations.authorization import Authorization
from apps.authen.serializers.auth import AuthSerializer, AuthorizationResponseSerializer

from apps.authen.serializers.user_role import UserRoleSerializer
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class AuthorizationViewSet(viewsets.ViewSet):
    """Авторизация пользователей"""

    ru = ResponseUtils()

    @swagger_auto_schema(
        tags=['Авторизация/Аутентификация', ],
        operation_description="Проверка на авторизованного пользователя",
        security=[
            {
                'Token': {
                    'type': 'apiKey',
                    'name': 'Авторизация по токену (шаблон: Token (JWT-токен)',
                    'in': 'header'
                }
            }
        ],
        responses={'401': 'Пользователь не авторизован',
                   '200': 'Пользователь авторизован'}
    )
    def check_auth(self, request, *args, **kwargs):
        """Проверка авторизации пользователя"""
        ac = AuthCheck(request)
        if ac.is_request_auth:
            return self.ru.ok_response_no_data()
        else:
            return self.ru.unauthorized_no_data()

    @swagger_auto_schema(
        tags=['Авторизация/Аутентификация', ],
        operation_description="Получение роли пользователя",
        security=[
            {
                'Token': {
                    'type': 'apiKey',
                    'name': 'Авторизация по токену (шаблон: Token (JWT-токен)',
                    'in': 'header'
                }
            }
        ],
        responses={'401': 'Пользователь не авторизован',
                   '200': UserRoleSerializer}
    )
    def get_user_role(self, request, *args, **kwargs):
        """Получение роли пользователя"""
        role = AuthCheck(request).get_user_role
        if role is None:
            return self.ru.unauthorized_no_data()
        return self.ru.ok_response_dict(
            {'role': role}
        )

    @swagger_auto_schema(
        tags=['Авторизация/Аутентификация', ],
        operation_description="Авторизация пользователя",
        request_body=AuthSerializer,
        responses={'401': 'Ошибка в процессе авторизации',
                   '200': AuthorizationResponseSerializer}
    )
    def user_login(self, request, *args, **kwargs):
        """Авторизация пользователя"""
        serialize = AuthSerializer(data=request.data)
        if serialize.is_valid():
            authorization = Authorization({
                'source': 'Неавторизованный пользователь',
                'module': AUTHEN,
                'process_data': {
                    'request': request,
                    'login': serialize.data['login'],
                    'password': serialize.data['password'],
                    'centre_auth': serialize.data['centre_auth']
                }
            })
            if not authorization.process_completed:
                return self.ru.auth_failed_response(authorization.auth_error)
            return self.ru.ok_response_dict(authorization.auth_data)
        else:
            JournalService().create_journal_rec(
                {
                    'source': 'Запрос на авторизацию пользователя',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Полученный данные не прошли валидацию'
                },
                repr(request.data),
                None
            )
            return self.ru.auth_failed_response('Данные не прошли валидацию')
