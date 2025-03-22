from django.core.management.base import BaseCommand

from apps.commons.utils.ldap import ldap_utils


class Command(BaseCommand):
    """Базовая команда для тестирования получения подразделения-центра из AD для сотрудника ЦОКО"""

    def handle(self, *args, **options):
        ldap_utils.get_ad_user_centre()
