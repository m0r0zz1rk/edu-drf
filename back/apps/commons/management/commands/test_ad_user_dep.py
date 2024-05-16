from django.core.management.base import BaseCommand

from apps.commons.utils.ldap import LdapUtils


class Command(BaseCommand):
    """Базовая команда для тестирования получения подразделения-центра из AD для сотрудника ЦОКО"""

    def handle(self, *args, **options):
        LdapUtils().get_ad_user_centre()
