from django.core.management.base import BaseCommand

from apps.authen.utils.state import StateUtils


class Command(BaseCommand):
    """Базовая команда для добавления начальных государств"""

    def handle(self, *args, **options):
        su = StateUtils()
        if not su.check_states_exists():
            su.add_base_states()
