from django.contrib.auth.models import User
from django.db import models

from apps.commons.models import BaseTable


class BaseProfile(BaseTable):
    """Базовая модель профиля пользователя"""
    django_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь Django'
    )
    surname = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        default='Фамилия',
        verbose_name='Фамилия'
    )
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        default='Имя',
        verbose_name='Имя'
    )
    patronymic = models.CharField(
        max_length=150,
        null=False,
        blank=True,
        verbose_name='Отчество'
    )

    @property
    def display_name(self) -> str:
        """Получение ФИО пользователя"""
        try:
            display_name = f'{self.surname} {self.name}'
            if len(self.patronymic) > 0:
                display_name += f' {self.patronymic}'
            return display_name
        except Exception:
            return '(Данные не найдены)'

    class Meta:
        abstract = True
