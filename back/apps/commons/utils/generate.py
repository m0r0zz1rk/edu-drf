import random

from django.contrib.auth.models import User

from apps.commons.utils.transliterate import TransliterateUtils


class GenerateUtils:
    """Класс методов для генерации данных"""

    @staticmethod
    def generate_username(
            surname: str,
            name: str,
            patronymic: str
    ) -> str:
        """Генерация имени пользователя"""
        tu = TransliterateUtils()
        username = f'{tu.translit(surname)}.{tu.translit(name)[:1]}'
        if len(patronymic) > 0:
            username += f'.{tu.translit(patronymic)[:1]}'
        while User.objects.filter(username=username).exists():
            username += str(random.randint(1, 1000))
        return username
