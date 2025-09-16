from django.core.management.base import BaseCommand

from apps.commons.services.old_edu.get_data import get_all_edu_data
from apps.commons.utils.ldap import ldap_utils


class Command(BaseCommand):
    """Базовая команда для получения данных из олдовой базы edu и сохранения в новую базу"""

    def handle(self, *args, **options):
        ldap_utils.set_ad_centres()
        get_all_edu_data()
