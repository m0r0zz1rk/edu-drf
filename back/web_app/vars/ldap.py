import ldap

from .journal import *
from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType


"""Первый LDAP сервер для аутентификации"""
AUTH_LDAP_1_SERVER_URI = env('LDAP_1_SERVER_URI')
AUTH_LDAP_1_BIND_DN = env('LDAP_BIND_DN')
AUTH_LDAP_1_BIND_PASSWORD = env('LDAP_BIND_PASSWORD')
AUTH_LDAP_1_USER_SEARCH = LDAPSearch(
    env('LDAP_USER_SEARCH'),
    ldap.SCOPE_SUBTREE,
    "sAMAccountName=%(user)s"
)
AUTH_LDAP_1_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
AUTH_LDAP_1_GROUP_SEARCH = LDAPSearch(
    "OU=Groups,OU=CMN,OU=COKO,DC=coko38,DC=ru",
    ldap.SCOPE_SUBTREE,
    "(objectCategory=Group)"
)
AUTH_LDAP_1_GROUP_TYPE = ActiveDirectoryGroupType(name_attr="cn")
AUTH_LDAP_1_USER_FLAGS_BY_GROUP = {
    "is_superuser": env('LDAP_IS_SUPERUSER'),
    "is_staff": env('LDAP_IS_STAFF')
}
AUTH_LDAP_1_FIND_GROUP_PERMS = True
AUTH_LDAP_1_CACHE_GROUPS = True
AUTH_LDAP_1_GROUP_CACHE_TIMEOUT = 1  # 1 час - время кэширования

"""Второй LDAP сервер для аутентификации"""
AUTH_LDAP_2_SERVER_URI = env('LDAP_2_SERVER_URI')
AUTH_LDAP_2_BIND_DN = env('LDAP_BIND_DN')
AUTH_LDAP_2_BIND_PASSWORD = env('LDAP_BIND_PASSWORD')
AUTH_LDAP_2_USER_SEARCH = LDAPSearch(
    env('LDAP_USER_SEARCH'),
    ldap.SCOPE_SUBTREE,
    "sAMAccountName=%(user)s"
)
AUTH_LDAP_2_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
AUTH_LDAP_2_GROUP_SEARCH = LDAPSearch(
    "OU=Groups,OU=CMN,OU=COKO,DC=coko38,DC=ru",
    ldap.SCOPE_SUBTREE,
    "(objectCategory=Group)"
)
AUTH_LDAP_2_GROUP_TYPE = ActiveDirectoryGroupType(name_attr="cn")
AUTH_LDAP_2_USER_FLAGS_BY_GROUP = {
    "is_superuser": env('LDAP_IS_SUPERUSER'),
    "is_staff": env('LDAP_IS_STAFF')
}
AUTH_LDAP_2_FIND_GROUP_PERMS = True
AUTH_LDAP_2_CACHE_GROUPS = True
AUTH_LDAP_2_GROUP_CACHE_TIMEOUT = 1  # 1 час - время кэширования

"""Классы аутентификации приложения"""
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'web_app.vars.ldap_classes.LDAPBackend1',
    'web_app.vars.ldap_classes.LDAPBackend2',
]

"""Данные для ldap3 - получение информации о пользователе из каталога AD"""
AD_SERVER = env('AD_SERVER')
AD_USER = env('AD_USER')
AD_PASSWORD = env('AD_PASSWORD')
AD_SEARCH_TREE = env('AD_SEARCH_TREE')
