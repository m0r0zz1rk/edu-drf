from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.authen.operations.registration import Registration
from apps.authen.serializers.registration_serializer import RegistrationSerializer, RegistrationUniquePhoneSerializer, \
    RegistrationUniqueEmailSerializer
from apps.commons.utils.django.exception import ExceptionHandling
from apps.authen.utils.profile import ProfileUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.commons.utils.django.user import UserUtils
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR

from apps.journal.utils.journal_utils import JournalUtils


class RegistrationViewSet(viewsets.ViewSet):
    """Регистрация обучающегося в АИС"""

    ju = JournalUtils()
    ru = RestUtils()
    respu = ResponseUtils()
    pu = ProfileUtils()
    uu = UserUtils()

    @swagger_auto_schema(
        tags=['Регистрация', ],
        operation_description="Проверка на уникальность номера телефона",
        request_body=RegistrationUniquePhoneSerializer,
        responses={
            '400': 'Ошибка при проверке',
            '409': 'Проверка не пройдена - указанный номер телефон уже используется',
            '200': 'Проверка пройдена - указанный номер телефона уникален'
        }
    )
    def check_unique_phone(self, request, *args, **kwargs):
        """Проверка на существующий профиль с полученным номером телефона"""
        params = ['phone', ]
        if not self.ru.validate_params_to_list(request, params):
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Ошибка при проверке уникальности номера телефона: данные не прошли валидацию'
                },
                repr(request.data),
                None
            )
            return self.respu.bad_request_no_data()
        try:
            if not self.pu.is_profile_exist(
                    'phone',
                    self.ru.get_request_parameter_by_key(request, 'phone')
            ):
                return self.respu.ok_response_no_data()
            else:
                return self.respu.conflict_failed_response_no_data()
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Системная ошибка при проверке уникальности номера телефона'
                },
                repr(request.data),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Регистрация', ],
        operation_description="Проверка на уникальность email",
        request_body=RegistrationUniqueEmailSerializer,
        responses={
            '400': 'Ошибка при проверке',
            '409': 'Проверка не пройдена - указанный email уже используется',
            '200': 'Проверка пройдена - указанный email уникален'
        }
    )
    def check_unique_email(self, request, *args, **kwargs):
        """Проверка на существующего пользователя с указанным email"""
        params = ['email', ]
        if not self.ru.validate_params_to_list(request, params):
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Ошибка при проверке уникальности email: данные не прошли валидацию'
                },
                repr(request.data),
                None
            )
            return self.respu.bad_request_no_data()
        try:
            if self.uu.is_user_exists(
                    'email',
                    self.ru.get_request_parameter_by_key(request, 'email')
            ):
                return self.respu.ok_response_no_data()
            else:
                return self.respu.conflict_failed_response_no_data()
        except Exception as e:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Системная ошибка при проверке уникальности email'
                },
                repr(request.data),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

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
            'surname',
            'name',
            'patronymic',
            'phone',
            'email',
            'snils',
            'state',
            'birthday',
            'sex',
            'health',
            'password'
        ]
        if not self.ru.validate_params_to_list(request, params):
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Ошибка при проверке регистрации обучающегося: данные не прошли валидацию'
                },
                repr(request.data),
                None
            )
            return self.respu.bad_request_response('Произошла ошибка, данные не прошли валидацию')
        try:
            serialize = RegistrationSerializer(data=request.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Ошибка при проверке регистрации обучающегося: данные не прошли сериализацию'
                },
                repr(request.data),
                None
            )
            return self.respu.bad_request_response('Произошла ошибка, данные не прошли сериализацию')
        if serialize.is_valid():
            try:
                with transaction.atomic():
                    registration_process = Registration(
                        {
                            'source': 'Неизвестный пользователь',
                            'module': AUTHEN,
                            'process_data': serialize.data
                        }
                    )
                    if registration_process.process_completed:
                        return self.respu.ok_response('Регистрация успешно завершена')
                    else:
                        return self.respu.bad_request_response(registration_process.reg_error)
            except Exception:
                self.ju.create_journal_rec(
                    {
                        'source': 'Внешний запрос',
                        'module': AUTHEN,
                        'status': ERROR,
                        'description': 'Системная ошибка в процессе регистрации обучающегося'
                    },
                    repr(serialize.data),
                    ExceptionHandling.get_traceback()
                )
                return self.respu.bad_request_response('Произошла системная ошибка, обратитесь к администратору')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Ошибка сериализации данных при регистрации обучающегося'
                },
                repr(serialize.data),
                serialize.errors
            )
            return self.respu.bad_request_response(
                f'Ошибка валидации данных: {serialize.errors}'
            )
