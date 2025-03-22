import codecs
from typing import Optional

from django.contrib.auth.models import User
from ldap3 import Server, Connection, SUBTREE

from apps.commons.decorators.ldap_utils_journal_decorator import ldap_utils_journal_decorator
from apps.commons.services.ad.ad_centre import AdCentreService
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.settings import settings_utils
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import journal_service


class LdapUtils:
    """Класс методов для получения данных из Active Directory COKO"""

    high_positions = [
        'Руководитель',
        'руководитель',
        'Начальник',
        'начальник',
        'Заместитель',
        'заместитель',
        'Главный бухгалтер'
    ]
    AD_SERVER = AD_USER = AD_PASSWORD = AD_USER_SEARCH_TREE = conn = None

    def __init__(self):
        """Инициализация класса - установка параметров и соединения с LDAP"""
        self.AD_SERVER = settings_utils.get_parameter_from_settings('AD_SERVER')
        self.AD_USER = settings_utils.get_parameter_from_settings('AD_USER')
        self.AD_PASSWORD = settings_utils.get_parameter_from_settings('AD_PASSWORD')
        self.AD_USER_SEARCH_TREE = settings_utils.get_parameter_from_settings('AD_USER_SEARCH_TREE')
        self.AD_GROUP_SEARCH_TREE = settings_utils.get_parameter_from_settings('AD_GROUP_SEARCH_TREE')
        try:
            self.connection = Connection(
                Server(self.AD_SERVER),
                user=self.AD_USER,
                password=self.AD_PASSWORD
            )
        except Exception:
            journal_service.create_journal_rec(
                {
                    'source': 'Инициализация LDAP подключения',
                    'module': COMMON,
                    'status': ERROR,
                    'description': 'Ошибка при подключении к LDAP'
                },
                repr({
                    'AD_SERVER': self.AD_SERVER,
                    'AD_USER': self.AD_USER,
                    'AD_PASSWORD': self.AD_PASSWORD,
                }),
                ExceptionHandling.get_traceback()
            )
            self.connection = None

    @ldap_utils_journal_decorator(
        'Атрибут сотрудника ЦОКО успешно получен',
        'Ошибка при получении атрибута сотрудника ЦОКО'
    )
    def get_ad_attribute_coko_user(self, attribute: str, username: str) -> str:
        """
        Получение атрибута AD для сотрудника ЦОКО по username
        :param attribute: наименование атрибута
        :param username: имя пользователя (sAMAccountName)
        :return: значение атрибута (пустая строка - если атрибут не найден)
        """
        if len(username) > 0 and self.connection is not None:
            self.connection.bind()
            self.connection.search(
                self.AD_USER_SEARCH_TREE,
                '(sAMAccountName=' + username + ')',
                SUBTREE,
                attributes=[attribute]
            )
            users = self.connection.entries
            if len(users) > 0:
                if users[0][attribute].value is None:
                    return ''
                return users[0][attribute].value
        return ''

    @ldap_utils_journal_decorator(
        'Подразделения Центры успешно получены',
        'Ошибка при получении подразделений Центров '
    )
    def set_ad_centres(self):
        """Получение подразделений уровня Центра из AD COKO"""
        self.connection.bind()
        self.connection.search(
            'ou=Groups,ou=CMN,ou=COKO,dc=coko38,dc=ru',
            '(cn=centre_*)',
            SUBTREE,
            attributes=['ObjectGUID', 'DisplayName']
        )
        deps = self.connection.entries
        for dep in deps:
            AdCentreService().add_ad_centre(
                {
                    'display_name': dep.DisplayName,
                    'object_guid': dep.ObjectGUID
                }
            )

    @ldap_utils_journal_decorator(
        'Подразделение успешно записано в модель AdCentreCokoUser',
        'Ошибка при записи подразделения в модель  AdCentreCokoUser'
    )
    def get_ad_user_centre(self, user: User) -> Optional[str]:
        """
        Получение подразделения-центра из AD сотрудника ЦОКО и запись в модель AdCentreCokoUser
        :param user: Пользователь Django
        :return:
        """
        self.connection.bind()
        self.connection.search(
            self.AD_USER_SEARCH_TREE,
            f'(sAMAccountName={user.username})',
            SUBTREE,
            attributes=['department', 'title', 'manager']
        )
        data = self.connection.entries
        if not any(s in str(data[0].title) for s in self.high_positions):
            self.connection.search(
                self.AD_USER_SEARCH_TREE,
                f"(distinguishedName={str(data[0].manager)})",
                SUBTREE,
                attributes=['manager', 'department', 'title'])
            data = self.connection.entries
            if any(s in str(data[0].title) for s in ['Заведующий', 'заведующий']):
                self.connection.search(
                    self.AD_USER_SEARCH_TREE,
                    f"(distinguishedName={data[0].manager})",
                    SUBTREE,
                    attributes=['manager', 'title', 'department']
                )
                data = self.connection.entries
                if not any(s in str(data[0].title) for s in self.high_positions):
                    self.connection.search(
                        self.AD_USER_SEARCH_TREE,
                        f"(distinguishedName={data[0].manager})",
                        SUBTREE,
                        attributes=['department']
                    )
                    data = self.connection.entries
        self.connection.search(
            'ou=Groups,ou=CMN,ou=COKO,dc=coko38,dc=ru',
            f"(info={data[0].department})",
            SUBTREE,
            attributes=['displayName']
        )
        data = self.connection.entries
        return str(data[0].displayName)

    @ldap_utils_journal_decorator(
        'Центры с менеджерами успешно получены',
        'Ошибка при получении центров с менеджерами'
    )
    def get_departments_with_managers(self) -> dict:
        """
        Получение словаря подразделений Центров с менеджерами
        :return: словарь с информацией о Центрах
        """
        self.connection.bind()
        self.connection.search(
            self.AD_GROUP_SEARCH_TREE,
            '(cn=centre_*)',
            SUBTREE,
            attributes=['displayName', 'managedBy']
        )
        deps = self.connection.entries
        voc = {}
        for dep in deps:
            dn = dep.displayName
            # mngby = codecs.decode(str(dep.managedBy), 'unicode-escape')
            # manager = mngby[3:mngby.find(',')]
            managed_by = str(dep.managedBy)
            manager = managed_by[3:managed_by.find(',')]
            if len(str(dn)) > 2:
                voc[str(dn)] = manager
        return voc


ldap_utils = LdapUtils()
