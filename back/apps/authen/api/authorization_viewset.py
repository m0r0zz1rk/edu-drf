from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.authen.actions.authorization_action import AuthorizationAction
from apps.authen.serializers.auth_serializer import AuthSerializer, AuthorizationResponseSerializer
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import AUTHEN
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.journals.writer.journal_writer import JournalWriter


class AuthorizationViewSet(viewsets.ViewSet):
    """Авторизация пользователей"""

    journal = JournalWriter(AUTHEN)

    @staticmethod
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
    def check_auth(request, *args, **kwargs):
        """Проверка авторизации пользователя"""
        init = AuthorizationAction(request=request)
        if init.is_request_auth:
            return ResponseUtils.ok_response_no_data()
        else:
            return ResponseUtils.unauthorized_no_data()

    @staticmethod
    @swagger_auto_schema(
        tags=['Авторизация/Аутентификация', ],
        operation_description="Проверка пользователя на администратора",
        security=[
            {
                'Token': {
                    'type': 'apiKey',
                    'name': 'Авторизация по токену (шаблон: Token (JWT-токен)',
                    'in': 'header'
                }
            }
        ],
        responses={'403': 'Пользователь не является администратором',
                   '200': 'Пользователь является администратором'}
    )
    def check_admin(request, *args, **kwargs):
        """Проверка пользователя на права администратора"""
        init = AuthorizationAction(request=request)
        if init.is_request_admin:
            return ResponseUtils.ok_response_no_data()
        else:
            return ResponseUtils.forbidden_no_data()

    @swagger_auto_schema(
        tags=['Авторизация/Аутентификация', ],
        operation_description="Авторизация пользователя",
        request_body=AuthSerializer,
        responses={'400': 'Ошибка в процессе авторизации (сообщение "Повторите попытку позже" или ошибка)',
                   '200': AuthorizationResponseSerializer}
    )
    def user_login(self, request, *args, **kwargs):
        """Авторизация пользователя"""
        params = ['username', 'password']
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                'Ошибка при попытке входа в систему: Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        try:
            serialize = AuthSerializer(data=request.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                'Ошибка при попытке входа в систему: Ошибка сериализации данных'
            )
            return ResponseUtils().sorry_try_again_response()
        if serialize.is_valid(raise_exception=True):
            init_auth = AuthorizationAction(request, serialize.data)
            auth_data = init_auth.authorization_user()
            du = DictUtils()
            if du.exist_key_in_dict('error', auth_data):
                return ResponseUtils().bad_request_response(
                    du.get_str_value_in_dict_by_key("error", auth_data)
                )
            else:
                return ResponseUtils.ok_response_dict(
                    auth_data
                )
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при попытке входа в систему: Валидация данных сериализатора не пройдена'
            )
            return ResponseUtils().sorry_try_again_response()
