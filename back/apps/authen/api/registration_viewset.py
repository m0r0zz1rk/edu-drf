from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.authen.actions.registration_action import RegistrationAction
from apps.authen.serializers.registration_serializer import RegistrationSerializer, RegistrationUniquePhoneSerializer, \
    RegistrationUniqueEmailSerializer
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.utils.django.exception import ExceptionHandling
from apps.authen.utils.profile import ProfileUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils

from apps.commons.consts.journals.journal_rec_types import AUTHEN
from apps.journals.writer.journal_writer import JournalWriter


class RegistrationViewSet(viewsets.ViewSet):
    """Регистрация ОО в АИС"""

    journal = JournalWriter(AUTHEN)

    @swagger_auto_schema(
        tags=['Регистрация', ],
        operation_description="Проверка на уникальность номера телефона",
        request_body=RegistrationUniquePhoneSerializer,
        responses={
            '400': 'Ошибка при проверке',
            '200': 'Проверка пройдена - указанный номер телефона уникален'
        }
    )
    def check_unique_phone(self, request, *args, **kwargs):
        """Проверка на существующий профиль с полученным номером телефона"""
        params = ['phone', ]
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке уникальности номера телефона: '
                f'Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        try:
            if ProfileUtils.check_unique_phone(
                    ru.get_request_parameter_by_key(request, 'phone')
            ):
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_no_data()
        except Exception as e:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке уникальности номера телефона: {e}"'
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Регистрация', ],
        operation_description="Проверка на уникальность email",
        request_body=RegistrationUniqueEmailSerializer,
        responses={
            '400': 'Ошибка при проверке',
            '200': 'Проверка пройдена - указанный email уникален'
        }
    )
    def check_unique_email(self, request, *args, **kwargs):
        """Проверка на существующего пользователя с указанным email"""
        params = ['email', ]
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке уникальности email: Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        try:
            if ProfileUtils.check_unique_email(
                    ru.get_request_parameter_by_key(request, 'email')
            ):
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_no_data()
        except Exception as e:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке уникальности email: {e}"'
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Регистрация', ],
        request_body=RegistrationSerializer,
        operation_description="Регистрация пользователя",
        responses={'400': 'Произошла ошибка в процессе регистрации (error в ответе)',
                   '200': 'Сообщение "Регистрация успешно завершена"'}
    )
    def registration(self, request, *args, **kwargs):
        """Регистрация пользователя"""
        params = [
            'state',
            'surname',
            'name',
            'patronymic',
            'sex',
            'birthday',
            'phone',
            'email',
            'role',
            'oo_fullname',
            'oo_shortname',
            'password'
        ]
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                'Запрос не прошел валидацию'
            )
            return ResponseUtils().sorry_try_again_response()
        try:
            serialize = RegistrationSerializer(data=request.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при попытке сериализации данных: '
                f'{ExceptionHandling.get_traceback()}')
            return ResponseUtils().sorry_try_again_response()
        if serialize.is_valid():
            try:
                with transaction.atomic():
                    init_reg = RegistrationAction(serialize.data)
                    if not init_reg.registration():
                        return ResponseUtils.bad_request_response(
                            'Произошла ошибка при создании профиля пользователя. Повторите попытку позже'
                        )
                    return ResponseUtils.ok_response(
                        'Регистрация успешно завершена. Войдите, используя телефон/почту и заданный пароль'
                    )
            except Exception:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при регистрации пользователя: {ExceptionHandling.get_traceback()}'
                )
                return ResponseUtils().sorry_try_again_response()
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при валидации сериализованных данных: {serialize.errors}'
            )
            return ResponseUtils.bad_request_response(
                f'Произошла ошибка: {serialize.errors}'
            )
