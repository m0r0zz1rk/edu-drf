from typing import Union

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from apps.authen.serializers.profile_serializer import (ProfileMainPageSerializer, ProfileInputSerializer,
                                                        ProfileOutputSerializer)
from apps.authen.serializers.registration_serializer import RegistrationUniquePhoneSerializer, \
    RegistrationUniqueEmailSerializer, RegistrationUniqueSnilsSerializer
from apps.authen.utils.profile import ProfileUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR, JOURNAL_REC_STATUSES, SUCCESS
from apps.journal.utils.journal_utils import JournalUtils


class ProfileViewSet(viewsets.ViewSet):
    """Работа с профилем пользователя"""
    permission_classes = [IsAuthenticated, ]

    ju = JournalUtils()
    pu = ProfileUtils()
    respu = ResponseUtils()

    def _endpoint_rec_journal(
        self,
        user_id: int,
        message_type: JOURNAL_REC_STATUSES,
        description: str,
        payload: str,
        output: str = None
    ):
        """
        Внесение записи в журнал событий
        :param message_type: Тип сообщения в журнале событий
        :param user_id: ID пользователя Django
        :param description: описание ошибки
        :param payload: полезная нагрузка
        :param output: выходные данные (при наличии
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': self.pu.get_profile_or_info_by_attribute(
                    'django_user_id',
                    user_id,
                    'display_name'
                ),
                'module': AUTHEN,
                'status': message_type,
                'description': description
            },
            payload,
            output
        )

    def _check_unique_data(
        self,
        user_id: int,
        request_data: dict,
        serializer,
        attr_name: str,
    ) -> Union[str, bool]:
        """
        Проверка на уникальность полученного значения среди всех
        профилей пользователей АИС (кроме полученного по user_id)
        :param user_id: ID пользователя Django
        :param request_data: полученные данные из request
        :param serializer: сериализатор для обработки входящих данных из request
        :param attr_name: имя атрибута профиля на проверку
        :return: True - значение уникально,
                 False - значение используется другим пользователем,
                 str - ошибки сериализации
        """
        serialize = serializer(data=request_data)
        if serialize.is_valid():
            check = self.pu.check_unique_data_for_profile(
                user_id,
                attr_name,
                serialize.data[attr_name]
            )
            return check
        else:
            return serialize.errors

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Получение информации о пользователе для главной страницы",
        responses={
            '400': 'Сообщение "Повторите попытку позже"',
            '403': 'Пользователь не авторизован',
            '200': ProfileMainPageSerializer}
    )
    def get_main_page_profile_info(self, request, *args, **kwargs):
        output_data = self.pu.get_profile_main_page_info(request.user.id)
        if output_data is None:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при получении информации из профиля для главной страницы - профиль не найден',
                f'ID пользователя: {request.user.id}'
            )
            return self.respu.sorry_try_again_response()
        try:
            serialize = ProfileMainPageSerializer(output_data)
            return ResponseUtils.ok_response_dict(serialize.data)
        except Exception:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при получении информации из профиля для главной страницы - данные не прошли сериализацию',
                repr(output_data),
                ExceptionHandling.get_traceback()
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Просмотр профиля пользователя",
        responses={
            '400': 'Сообщение "Повторите попытку позже"',
            '403': 'Пользователь не авторизован',
            '200': ProfileOutputSerializer}
    )
    def get_profile_info(self, request, *args, **kwargs):
        """Получение информации из профиля пользователя"""
        prof = self.pu.get_profile_or_info_by_attribute(
            'django_user_id',
            request.user.id,
            'profile'
        )
        if prof is None:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при получении информации из профиля - профиль не найден',
                f'ID пользователя: {request.user.id}'
            )
            return self.respu.sorry_try_again_response()
        try:
            serialize = ProfileOutputSerializer(prof)
            self._endpoint_rec_journal(
                request.user.id,
                SUCCESS,
                'Получение данных из профиля',
                f'ID пользователя: {request.user.id}',
                repr(serialize.data)
            )
            return ResponseUtils.ok_response_dict(serialize.data)
        except Exception:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при получении информации из профиля - данные не прошли сериализацию',
                str(prof),
                ExceptionHandling.get_traceback()
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
            tags=['Профиль', ],
            operation_description="Проверка на возможность смены номера телефона",
            request_body=RegistrationUniquePhoneSerializer,
            responses={
                '403': 'Пользователь не авторизован',
                '400': 'Проверка не пройдена - указанный номер телефона уже используется',
                '200': 'Проверка пройдена - указанный номер телефона не используется'
            }
    )
    def check_profile_phone(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного номера телефона (за исключением пользователя, от которого
        пришел запрос)
        """
        proc = self._check_unique_data(
            request.user.id,
            request.data,
            RegistrationUniquePhoneSerializer,
            'phone'
        )
        if isinstance(proc, bool):
            if proc is True:
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_response('Номер телефона используется другим пользователем')
        else:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при проверке номера телефона профиля - данные не прошли сериализацию',
                repr(request.data),
                repr(proc)
            )
            return ResponseUtils().bad_request_response('Произошла системная ошибка при проверке номера телефона')

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Проверка на возможность смены email",
        request_body=RegistrationUniqueEmailSerializer,
        responses={
            '403': 'Пользователь не авторизован',
            '400': 'Проверка не пройдена - указанный email уже используется',
            '200': 'Проверка пройдена - указанный email не используется'
        }
    )
    def check_profile_email(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного email (за исключением пользователя, от которого
        пришел запрос)
        """
        proc = self._check_unique_data(
            request.user.id,
            request.data,
            RegistrationUniqueEmailSerializer,
            'email'
        )
        if isinstance(proc, bool):
            if proc is True:
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_response('Email используется другим пользователем')
        else:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при проверка email профиля - данные не прошли сериализацию',
                repr(request.data),
                repr(proc)
            )
            return ResponseUtils().bad_request_response('Произошла системная ошибка при проверке email')

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Проверка на возможность смены СНИЛС",
        request_body=RegistrationUniqueSnilsSerializer,
        responses={
            '403': 'Пользователь не авторизован',
            '400': 'Проверка не пройдена - указанный СНИЛС уже используется',
            '200': 'Проверка пройдена - указанный СНИЛС не используется'
        }
    )
    def check_profile_snils(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного СНИЛС (за исключением пользователя, от которого
        пришел запрос)
        """
        proc = self._check_unique_data(
            request.user.id,
            request.data,
            RegistrationUniqueSnilsSerializer,
            'snils'
        )
        if isinstance(proc, bool):
            if proc is True:
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_response('СНИЛС используется другим пользователем')
        else:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при проверка СНИЛС профиля - данные не прошли сериализацию',
                repr(request.data),
                repr(proc)
            )
            return ResponseUtils().bad_request_response('Произошла системная ошибка при проверке СНИЛС')

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Сохранение информации в профиль",
        request_body=ProfileInputSerializer,
        responses={
            '400': 'Ошибка при попытке изменения профиля',
            '403': 'Пользователь не авторизован',
            '200': 'Сообщение об успешном изменении профиля'
        }
    )
    def save_profile_info(self, request, *args, **kwargs):
        """Сохранение полученной информации в профиль пользователя"""
        serialize = ProfileInputSerializer(data=request.data)
        if serialize.is_valid():
            prof = self.pu.get_profile_or_info_by_attribute(
                'django_user_id',
                request.user.id,
                'profile'
            )
            save_info_proc = self.pu.set_student_profile_data(
                prof,
                serialize.data
            )
            if isinstance(save_info_proc, bool):
                self._endpoint_rec_journal(
                    request.user.id,
                    SUCCESS,
                    'Информация профиля пользователя успешно изменена',
                    repr(serialize.data)
                )
                return self.respu.ok_response('Информация успешно обновлена')
            else:
                self._endpoint_rec_journal(
                    request.user.id,
                    ERROR,
                    'В процессе записи произошла системная ошибка',
                    repr(serialize.data),
                    save_info_proc
                )
                return self.respu.bad_request_response('Произошла системная ошибка, обратитесь к администратору')
        else:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при сохранении информации в профиль - данные не прошли сериализацию',
                repr(request.data),
                repr(serialize.errors)
            )
            return ResponseUtils.bad_request_response(
                f'Произошла ошибка при изменении профиля пользователя: {repr(serialize.errors)}'
            )

    """@swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Смена пароля пользователя",
        request_body=ProfileChangePasswordSerializer,
        responses={
            '400': 'Ошибка при попытке смены пароля',
            '401': 'Пользователь не авторизован',
            '200': 'Пароль успешно изменен'
        }
    )
    def change_user_password(self, request, *args, **kwargs):
        "Смена пароля пользователя"
        params = ['password', ]
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении пароля пользователя {request.user.id}: '
                f'Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        pu = ProfileUtils()
        if pu.change_user_password(
            request.user.id,
            ru.get_request_parameter_by_key(request, 'password')
        ):
            self.journal.write(
                pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Пароль пользователя успешно изменен'
            )
            return ResponseUtils.ok_response('Пароль успешно изменен')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении пароля пользователя {request.user.id}'
            )
            return ResponseUtils().sorry_try_again_response()"""
