from django.core.management.base import BaseCommand

from apps.guides.services.state import StateService


class Command(BaseCommand):
    """Базовая команда для добавления базовых государств"""

    def handle(self, *args, **options):
        StateService().add_based_states()
