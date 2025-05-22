import jwt

from datetime import timedelta, datetime
from django.conf import settings

from apps.commons.consts.jwt_algorythms import SUPPORTED_ALG
from apps.commons.services.ad.ad_centre import ad_centre_service
from apps.commons.services.ad.ad_centre_coko_user import ad_centre_coko_user_utils
from apps.commons.utils.django.settings import SettingsUtils
from apps.commons.utils.django.user import UserUtils, user_utils
from apps.commons.utils.ldap import ldap_utils


class TokenUtils:
    """Класс работы с токенами JWT"""
    su = SettingsUtils()
    user_id = 0
    access_token_expires = 120
    jwt_algorithm = su.get_parameter_from_settings('JWT_ALGORITHM')

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
            temp = self.su.get_parameter_from_settings('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')
            if temp is not None:
                self.access_token_expires = temp

    def _set_jwt_algorithm(self):
        """Установка значения алгоритма шифрования для токена"""
        if self.su.is_settings_parameter_exists('JWT_ALGORITHM'):
            temp = self.su.get_parameter_from_settings('JWT_ALGORITHM')
            if temp in SUPPORTED_ALG:
                self.jwt_algorithm = temp

    def jwt_token(self) -> dict:
        """Формирование словаря с ID пользователя и созданным токеном"""
        user = user_utils.get_user('id', self.user_id)
        dep = ad_centre_coko_user_utils.get_user_centre_object_guid(user)
        dep_display = ad_centre_coko_user_utils.get_user_centre_display_name(user)
        try:
            if dep == '-':
                ad_user_centre = ldap_utils.get_ad_user_centre(user)
                ad_centre = ad_centre_service.get_ad_centre('object_guid', ad_user_centre[1])
                if not ad_centre:
                    ldap_utils.set_ad_centres()
                    ad_user_centre = ldap_utils.get_ad_user_centre(user)
                ad_centre_coko_user_utils.add_rec(user, ad_user_centre[1])
                dep = ad_user_centre[1]
                dep_display = ad_user_centre[0]
        except TypeError:
            pass
        return {
            'coko_token': self._new_access_token(),
            'coko_role': UserUtils().get_user_role_by_id(self.user_id),
            'coko_dep': dep,
            'coko_dep_display': dep_display,
            'coko_user_id': self.user_id
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
        jwt_token = jwt.encode(
            data,
            self.su.get_parameter_from_settings('SECRET_KEY'),
            algorithm=self.jwt_algorithm)
        return jwt_token
