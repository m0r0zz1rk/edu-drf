from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.operations.update_profile import UpdateProfile
from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.user import UserUtils
from apps.guides.selectors.user import UserFilter, student_profile_queryset
from apps.guides.serializers.user import UserSerializer, UserRetrieveSerializer, UserUniquePhoneSerializer, \
    UserUniqueEmailSerializer, UserUniqueSnilsSerializer, UserUpdateSerializer, UserChangePasswordSerializer
from apps.guides.services.user import UserService
from apps.journal.consts.journal_modules import GUIDES
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import JournalService


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями в модуле Справочники"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    pu = ProfileService()
    uu = UserUtils()
    us = UserService()
    ju = JournalService()
    respu = ResponseUtils()

    queryset = student_profile_queryset()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = UserFilter
    lookup_field = 'object_id'

    @swagger_auto_schema(
        tags=['Cправочники. Обучающиеся', ],
        operation_description="Получение списка пользователей",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': UserSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при получении списка пользователей'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочники. Обучающиеся', ],
        operation_description="Получение информации о пользователе",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении информации',
            '200': UserRetrieveSerializer
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = UserRetrieveSerializer(instance)
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при получении информации о пользователе'
                },
                repr(request),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Cправочники. Обучающиеся', ],
        operation_description="Проверка на возможность смены номера телефона пользователя",
        request_body=UserUniquePhoneSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Проверка не пройдена - указанный номер телефона уже используется',
            '200': 'Проверка пройдена - указанный номер телефона не используется'
        }
    )
    def check_user_phone(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного номера телефона
        """
        proc = self.us.check_unique_data(
            request.data,
            UserUniquePhoneSerializer,
            'phone'
        )
        if isinstance(proc, bool):
            if proc is True:
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_response('Номер телефона используется другим пользователем')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при проверке номера телефона пользователя - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(proc)
            )
            return ResponseUtils().bad_request_response('Произошла системная ошибка при проверке номера телефона')

    @swagger_auto_schema(
        tags=['Cправочники. Обучающиеся', ],
        operation_description="Проверка на возможность смены email пользователя",
        request_body=UserUniqueEmailSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Проверка не пройдена - указанный email уже используется',
            '200': 'Проверка пройдена - указанный email не используется'
        }
    )
    def check_user_email(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного email
        """
        proc = self.us.check_unique_data(
            request.data,
            UserUniqueEmailSerializer,
            'email'
        )
        if isinstance(proc, bool):
            if proc is True:
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_response('Email используется другим пользователем')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при проверке email пользователя - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(proc)
            )
            return ResponseUtils().bad_request_response('Произошла системная ошибка при проверке email')

    @swagger_auto_schema(
        tags=['Cправочники. Обучающиеся', ],
        operation_description="Проверка на возможность смены СНИЛС пользователя",
        request_body=UserUniqueSnilsSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Проверка не пройдена - указанный СНИЛС уже используется',
            '200': 'Проверка пройдена - указанный СНИЛС не используется'
        }
    )
    def check_user_snils(self, request, *args, **kwargs):
        """
        Проверка уникальности предложенного СНИЛС
        """
        proc = self.us.check_unique_data(
            request.data,
            UserUniqueSnilsSerializer,
            'snils'
        )
        if isinstance(proc, bool):
            if proc is True:
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_response('СНИЛС используется другим пользователем')
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Ошибка при проверке СНИЛС пользователя - данные не прошли сериализацию'
                },
                repr(request.data),
                repr(proc)
            )
            return ResponseUtils().bad_request_response('Произошла системная ошибка при проверке СНИЛС')

    @swagger_auto_schema(
        tags=['Cправочники. Обучающиеся', ],
        operation_description="Обновление информации о пользователе",
        request_body=UserUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при обновлении информации',
            '200': 'Сообщение "Информация успешно обновлена"'
        }
    )
    def update(self, request, *args, **kwargs):
        try:
            serialize = UserUpdateSerializer(data=request.data)
            if serialize.is_valid():
                prof = self.pu.get_profile_or_info_by_attribute(
                    'object_id',
                    serialize.data['object_id'],
                    'profile'
                )
                data = {
                    'django_user': prof.django_user,
                    'date_create': prof.date_create
                }
                for k, v in serialize.data.items():
                    data[k] = v
                update_profile_proc = UpdateProfile(
                    'StudentProfile',
                    data,
                    request
                )
                if update_profile_proc.update_profile_complete:
                    return self.respu.ok_response('Информация успешно обновлена')
                else:
                    return self.respu.bad_request_response('Произошла системная ошибка, обратитесь к администратору')
            else:
                self.ju.create_journal_rec(
                    {
                        'source': 'Внешний запрос',
                        'module': GUIDES,
                        'status': ERROR,
                        'description': 'Ошибка при обновлении профиля пользователя - данные не прошли сериализацию'
                    },
                    repr(request.data),
                    None
                )
                return self.respu.bad_request_response('Произошла ошибка - данные не прошли сериализацию')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Системная ошибка при обновлении профиля пользователя'
                },
                repr(request.data),
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_response('Произошла системная ошибка, обратитесь к администратору')

    @swagger_auto_schema(
        tags=['Cправочники. Обучающиеся', ],
        operation_description="Смена пароля пользователя",
        request_body=UserChangePasswordSerializer,
        responses={
            '400': 'Ошибка при попытке смены пароля',
            '403': 'Пользователь не авторизован или не является администратором',
            '200': 'Пароль успешно изменен'
        }
    )
    def change_user_password(self, request, *args, **kwargs):
        """Смена пароля пользователя"""
        serialize = UserChangePasswordSerializer(data=request.data)
        admin_display_name = self.pu.get_profile_or_info_by_attribute(
            'django_user_id',
            request.user.id,
            'display_name'
        )
        if serialize.is_valid():
            user_id = self.pu.get_profile_or_info_by_attribute(
                'object_id',
                serialize.data['profile_id'],
                'user_id'
            )
            process = self.uu.password_change(
                user_id,
                serialize.data['password']
            )
            if process is True:
                self.ju.create_journal_rec(
                    {
                        'source': admin_display_name,
                        'module': GUIDES,
                        'status': SUCCESS,
                        'description': 'Пароль пользователя успешно изменен'
                    },
                    repr({
                        'profile_id': serialize.data['profile_id'],
                        'password': '***************'
                    }),
                    None
                )
                return self.respu.ok_response('Пароль успешно изменен')
            else:
                self.ju.create_journal_rec(
                    {
                        'source': admin_display_name,
                        'module': GUIDES,
                        'status': ERROR,
                        'description': 'Произошла ошибка при смене пароля пользователя'
                    },
                    repr({
                        'profile_id': serialize.data['profile_id'],
                        'password': '***************'
                    }),
                    None
                )
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            self.ju.create_journal_rec(
                {
                    'source': admin_display_name,
                    'module': GUIDES,
                    'status': ERROR,
                    'description': 'Произошла ошибка при смене пароля пользователя - данные не прошли сериализацию'
                },
                repr({
                    'profile_id': serialize.data['profile_id'],
                    'password': '***************'
                }),
                None
            )
            return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
