from django.core.management.base import BaseCommand

from apps.guides.utils.state import StateUtils


class Command(BaseCommand):
    """Базовая команда для добавления базовых государств"""

    def handle(self, *args, **options):
        StateUtils().add_based_states()
