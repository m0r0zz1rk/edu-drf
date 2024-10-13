from django.core.management.base import BaseCommand

from apps.commons.utils.ldap import LdapUtils


class Command(BaseCommand):
    """Базовая команда для добавления подразделений уровня Центр из AD COKO"""

    def handle(self, *args, **options):
        LdapUtils().set_ad_centres()
