import codecs

from ldap3 import Server, Connection, SUBTREE
from ldap3.core.exceptions import LDAPSocketOpenError

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.settings import SettingsUtils
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.utils.journal_utils import JournalUtils


class LdapUtils:
    """Класс методов для получения данных из Active Directory COKO"""

    su = SettingsUtils()
    ju = JournalUtils()
    AD_SERVER = AD_USER = AD_PASSWORD = AD_SEARCH_TREE = conn = None

    def __init__(self):
        """Инициализация класса - установка параметров и соединения с LDAP"""
        self.AD_SERVER = self.su.get_parameter_from_settings('AD_SERVER')
        self.AD_USER = self.su.get_parameter_from_settings('AD_USER')
        self.AD_PASSWORD = self.su.get_parameter_from_settings('AD_PASSWORD')
        self.AD_SEARCH_TREE = self.su.get_parameter_from_settings('AD_SEARCH_TREE')
        try:
            self.conn = Connection(
                Server(self.AD_SERVER),
                user=self.AD_USER,
                password=self.AD_PASSWORD
            )
        except Exception:
            self.ju.create_journal_rec(
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
            self.conn = None

    def get_ad_attribute_coko_user(self, attribute: str, username: str) -> str:
        """
        Получение атрибута AD для сотрудника ЦОКО по username
        :param attribute: наименование атрибута
        :param username: имя пользователя (sAMAccountName)
        :return: значение атрибута (пустая строка - если атрибут не найден)
        """
        if len(username) > 0 and self.conn is not None:
            try:
                self.conn.bind()
                self.conn.search(
                    self.AD_SEARCH_TREE,
                    '(sAMAccountName=' + username + ')',
                    SUBTREE,
                    attributes=[attribute]
                )
                users = self.conn.entries
            except LDAPSocketOpenError:
                self.ju.create_journal_rec(
                    {
                        'source': 'Получение ФИО сотрудника из AD',
                        'module': COMMON,
                        'status': ERROR,
                        'description': 'Ошибка открытия сокета LDAP'
                    },
                    repr({
                        'AD_SERVER': self.AD_SERVER,
                        'AD_USER': self.AD_USER,
                        'AD_PASSWORD': self.AD_PASSWORD,
                    }),
                    ExceptionHandling.get_traceback()
                )
                return ''
            if len(users) > 0:
                if users[0][attribute].value is None:
                    return ''
                return users[0][attribute].value
        return ''
