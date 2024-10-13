from django.core.management.base import BaseCommand

from apps.commons.services.old_edu.get_data import get_all_edu_data


class Command(BaseCommand):
    """Базовая команда для получения данных из олдовой базы edu и сохранения в новую базу"""

    def handle(self, *args, **options):
        get_all_edu_data()
