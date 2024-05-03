from django_auth_ldap.backend import LDAPBackend


class LDAPBackend1(LDAPBackend):
    """Подключение к первому LDAP серверу"""
    settings_prefix = "AUTH_LDAP_1_"


class LDAPBackend2(LDAPBackend):
    """Подключение ко второму LDAP серверу"""
    settings_prefix = "AUTH_LDAP_2_"
