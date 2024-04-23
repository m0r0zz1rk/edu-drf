from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.serializers.profile_serializer import ProfileSerializer, \
    ProfileChangePasswordSerializer
from apps.authen.serializers.registration_serializer import RegistrationUniquePhoneSerializer, \
    RegistrationUniqueEmailSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR, INFO
from apps.commons.utils.django.exception import ExceptionHandling
from apps.authen.utils.profile import ProfileUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils

from apps.commons.consts.journals.journal_rec_types import PROFILE
from apps.journals.writer.journal_writer import JournalWriter


class ProfileViewSet(viewsets.ViewSet):
    """Работа с профилем пользователя"""
    permission_classes = [IsAuthenticated, ]

    journal = JournalWriter(PROFILE)

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Проверка на возможность смены номера телефона",
        request_body=RegistrationUniquePhoneSerializer,
        responses={
            '400': 'Ошибка при проверке',
            '200': 'Проверка пройдена - указанный номер телефона не используется другими пользователями'
        }
    )
    def check_change_phone(self, request, *args, **kwargs):
        """Проверка на другой профиль с полученным номером телефона"""
        params = ['phone', ]
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке возможности смены номера телефона: '
                f'Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        try:
            if ProfileUtils.check_unique_phone(
                ru.get_request_parameter_by_key(request, 'phone'),
                request.user.id
            ):
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_no_data()
        except Exception as e:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке возможности смены номера телефона: {e}"'
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Проверка на возможность смены email",
        request_body=RegistrationUniqueEmailSerializer,
        responses={
            '400': 'Ошибка при проверке',
            '200': 'Проверка пройдена - указанный email не используется другими пользователями'
        }
    )
    def check_change_email(self, request, *args, **kwargs):
        """Проверка на существующего пользователя с указанным email"""
        params = ['email', ]
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке возможности смены email: Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        try:
            if ProfileUtils.check_unique_email(
                ru.get_request_parameter_by_key(request, 'email'),
                request.user.id
            ):
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_no_data()
        except Exception as e:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке возможности смены email: {e}"'
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Просмотр профиля пользователя",
        responses={
            '400': 'Ошибка при попытке просмотра данных профиля (сообщение "Повторите попытку позже" или ошибка)',
            '403': 'Пользователь не авторизован',
            '200': ProfileSerializer}
    )
    def get_user_information(self, request, *args, **kwargs):
        """Получение информации из профиля пользователя"""
        pu = ProfileUtils()
        profile_info = pu.get_profile_info(
            'django_user_id',
            request.user.id,
            'all'
        )
        profile_info.update({
            'role': pu.get_user_role(request.user.id)
        })
        try:
            serialize = ProfileSerializer(profile_info)
            self.journal.write(
                pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Просмотр данных профиля'
            )
            return ResponseUtils.ok_response_dict(serialize.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при сериализации данных профиля пользователя {request.user.id}: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Изменение профиля пользователя",
        request_body=ProfileSerializer,
        responses={
            '400': 'Ошибка при попытке изменения профиля',
            '403': 'Пользователь не авторизован',
            '200': 'Сообщение об успешном изменении профиля'
        }
    )
    def save_profile_changes(self, request, *args, **kwargs):
        """Внесение изменений в профиль пользователя"""
        params = [
            'state',
            'surname',
            'name',
            'patronymic',
            'sex',
            'age',
            'birthday',
            'oo_shortname',
            'oo_fullname',
            'phone',
            'email',
            'role'
        ]
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении профиля пользователя {request.user.id}: '
                f'Ошибка валидации тела запроса'
            )
            return ResponseUtils().sorry_try_again_response()
        serialize = ProfileSerializer(request.data)
        pu = ProfileUtils()
        changes = pu.change_profile_info(request.user.id, serialize.data)
        if changes is True:
            if pu.change_user_role(
                request.user.id,
                ru.get_request_parameter_by_key(request, 'role')
            ):
                self.journal.write(
                    pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Профиль пользователя успешно изменен'
                )
                return ResponseUtils.ok_response('Информация профиля успешно изменена')
            else:
                self.journal.write(
                    pu.get_display_name('django_user_id', request.user.id),
                    INFO,
                    f'Профиль пользователя успешно изменен, но роль не была изменена'
                )
                return ResponseUtils.ok_response('Информация профиля успешно изменена')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении профиля пользователя {request.user.id}"'
            )
            return ResponseUtils.bad_request_response(
                f'Произошла ошибка при изменении профиля пользователя: {changes}'
            )

    @swagger_auto_schema(
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
        """Смена пароля пользователя"""
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
            return ResponseUtils().sorry_try_again_response()
