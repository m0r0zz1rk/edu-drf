from django.core.management.base import BaseCommand

from apps.commons.utils.ldap import ldap_utils


class Command(BaseCommand):
    """Базовая команда для добавления подразделений уровня Центр из AD COKO"""

    def handle(self, *args, **options):
        ldap_utils.set_ad_centres()
