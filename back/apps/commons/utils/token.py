import jwt

from datetime import timedelta, datetime
from django.conf import settings

from apps.commons.consts.jwt_algorythms import SUPPORTED_ALG
from apps.commons.utils.django.django import DjangoUtils


class TokenUtils:
    """Класс работы с токенами JWT"""
    du = DjangoUtils()
    user_id = 0
    access_token_expires = 120
    jwt_algorithm = du.get_parameter_from_settings('JWT_ALGORITHM')

    def __init__(self, user_id: int):
        """
            Инициализация класса - установка значения ID пользователя Django,
            времени жизни токена и алгоритма шифрования
        """
        self._set_access_token_expire()
        self._set_jwt_algorithm()
        self.user_id = user_id

    def _set_access_token_expire(self):
        """Установка значения времени жизни токена"""
        if hasattr(settings, 'JWT_ACCESS_TOKEN_EXPIRE_MINUTES'):
            temp = self.du.get_parameter_from_settings('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')
            if temp is not None:
                self.access_token_expires = temp

    def _set_jwt_algorithm(self):
        """Установка значения алгоритма шифрования для токена"""
        if self.du.is_settings_parameter_exists('JWT_ALGORITHM'):
            temp = self.du.get_parameter_from_settings('JWT_ALGORITHM')
            if temp in SUPPORTED_ALG:
                self.jwt_algorithm = temp

    def jwt_token(self) -> dict:
        """Формирование словаря с ID пользователя и созданным токеном"""
        return {
            'user_id': self.user_id,
            'access_token': self._new_access_token(),
        }

    def _new_access_token(self):
        """Создание JWT токена"""
        timed = timedelta(minutes=self.access_token_expires)
        if timed is not None:
            expire = datetime.now() + timed
        else:
            expire = datetime.now() + timedelta(minutes=self.access_token_expires)
        data = {
            'user_id': self.user_id,
            'exp': expire
        }
        print(self.jwt_algorithm)
        jwt_token = jwt.encode(
            data,
            self.du.get_parameter_from_settings('SECRET_KEY'),
            algorithm=self.jwt_algorithm)
        return jwt_token
