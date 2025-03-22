from drf_yasg.utils import swagger_auto_schema

from apps.commons.decorators.viewset.view_set_journal_decorator import view_set_journal_decorator
from apps.commons.drf.viewset.consts.swagger_text import SWAGGER_TEXT
from apps.commons.utils.django.response import response_utils
from apps.guides.api.guide_viewset import GuideViewSet
from apps.guides.selectors.profiles.student import UserFilter, student_profile_queryset, student_profile_orm
from apps.guides.serializers.user import UserSerializer, UserRetrieveSerializer, UserUniquePhoneSerializer, \
    UserUniqueEmailSerializer, UserUniqueSnilsSerializer, UserUpdateSerializer, UserChangePasswordSerializer
from apps.guides.services.user import user_service
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import journal_service


class StudentProfileViewSet(GuideViewSet):
    orm = student_profile_orm
    queryset = student_profile_queryset()
    serializer_class = UserSerializer
    update_serializer = UserUpdateSerializer
    filterset_class = UserFilter
    swagger_object_name = 'Профиль обучающегося'

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Получение списка",
        responses={
            **SWAGGER_TEXT['list'],
            '200': serializer_class(many=True)
        }
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Список "{swagger_object_name}" получен',
        f'Ошибка при получении списка "{swagger_object_name}"'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Получение профиля пользователя",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении информации',
            '200': UserRetrieveSerializer
        }
    )
    @view_set_journal_decorator(
        GUIDES,
        f'"{swagger_object_name}" получен',
        f'Ошибка при получении "{swagger_object_name}"'
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserRetrieveSerializer(instance)
        return response_utils.ok_response_dict(serializer.data)

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Проверка на возможность смены номера телефона",
        request_body=UserUniquePhoneSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Проверка не пройдена - указанный номер телефона уже используется',
            '200': 'Проверка пройдена - указанный номер телефона не используется'
        }
    )
    @view_set_journal_decorator(
        GUIDES,
        f'"Номер телефона проверен',
        f'Ошибка при проверке уникальности номера телефона'
    )
    def check_user_phone(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного номера телефона
        """
        serialize = UserUniquePhoneSerializer(data=request.data)
        if serialize.is_valid():
            proc = user_service.check_unique_data(serialize.data, 'phone')
            if proc is True:
                return response_utils.ok_response_no_data()
            else:
                return response_utils.bad_request_response('Номер телефона используется другим пользователем')
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при проверке номера телефона пользователя - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response('Произошла системная ошибка при проверке номера телефона')

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Проверка на возможность смены email",
        request_body=UserUniqueEmailSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Проверка не пройдена - указанный email уже используется',
            '200': 'Проверка пройдена - указанный email не используется'
        }
    )
    @view_set_journal_decorator(
        GUIDES,
        f'"Email проверен',
        f'Ошибка при проверке уникальности Email'
    )
    def check_user_email(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного email
        """
        serialize = UserUniqueEmailSerializer(data=request.data)
        if serialize.is_valid():
            proc = user_service.check_unique_data(serialize.data, 'email')
            if proc is True:
                return response_utils.ok_response_no_data()
            else:
                return response_utils.bad_request_response('Email используется другим пользователем')
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при проверке email пользователя - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response('Произошла системная ошибка при проверке email')

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Проверка на возможность смены СНИЛС",
        request_body=UserUniqueSnilsSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Проверка не пройдена - указанный СНИЛС уже используется',
            '200': 'Проверка пройдена - указанный СНИЛС не используется'
        }
    )
    @view_set_journal_decorator(
        GUIDES,
        f'"СНИЛС проверен',
        f'Ошибка при проверке уникальности СНИЛС'
    )
    def check_user_snils(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного СНИЛС
        """
        serialize = UserUniqueSnilsSerializer(data=request.data)
        if serialize.is_valid():
            proc = user_service.check_unique_data(request.data, 'snils')
            if proc is True:
                return response_utils.ok_response_no_data()
            else:
                return response_utils.bad_request_response('СНИЛС используется другим пользователем')
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при проверке СНИЛС пользователя - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response('Произошла системная ошибка при проверке СНИЛС')

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Обновление записи",
        request_body=update_serializer,
        responses=SWAGGER_TEXT['update']
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Запись "{swagger_object_name}" успешно обновлена',
        f'Ошибка при обновлении записи "{swagger_object_name}"'
    )
    def partial_update(self, request, *args, **kwargs):
        serialize = UserUpdateSerializer(data=request.data)
        if serialize.is_valid():
            user_service.update_profile(serialize.data)
            return response_utils.ok_response('Информация успешно обновлена')
        else:
            journal_service.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при обновлении профиля пользователя - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response('Произошла ошибка - данные не прошли сериализацию')

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Смена пароля",
        request_body=UserChangePasswordSerializer,
        responses={
            '400': 'Ошибка при попытке смены пароля',
            '403': 'Пользователь не авторизован или не является администратором',
            '200': 'Пароль успешно изменен'
        }
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Пароль обучающегося успешно обновлен',
        f'Ошибка при изменении пароля обучающегося"'
    )
    def change_user_password(self, request, *args, **kwargs):
        """Смена пароля пользователя"""
        serialize = UserChangePasswordSerializer(data=request.data)
        if serialize.is_valid():
            user_service.change_password(serialize.data)
            return response_utils.ok_response('Пароль успешно изменен')
        else:
            journal_service.create_journal_rec(
                {
                    'source': f'{request.user.last_name} {request.user.first_name}',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Произошла ошибка при смене пароля пользователя - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(serialize.errors)
            )
            return response_utils.bad_request_response('Произошла ошибка, повторите попытку позже')

    @swagger_auto_schema(
        tags=[f'Cправочники. {swagger_object_name}', ],
        operation_description="Экспорт записей",
        responses=SWAGGER_TEXT['export']
    )
    @view_set_journal_decorator(
        GUIDES,
        f'Экспорт записей "{swagger_object_name}" успешно выполнен',
        f'Ошибка при выполнении экспорта записей "{swagger_object_name}"'
    )
    def export(self, request, *args, **kwargs):
        return super().export(request, *args, **kwargs)
