from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.commons.models import BaseTable


class CokoProfile(BaseTable):
    """Модель профиля сотрудника ЦОКО"""
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
    curator_groups = models.BooleanField(
        default=False,
        verbose_name='Отображать только учебные группы как куратора'
    )

    def __str__(self):
        try:
            data = f'{self.surname} {self.name}'
            if len(str(self.patronymic)) > 0:
                data = f'{data} {self.patronymic}'
            return data
        except Exception:
            return '(Данные не найдены)'

    def get_display_name(self):
        """Получение ФИО пользователя"""
        try:
            display_name = f'{self.surname} {self.name}'
            if len(self.patronymic) > 0:
                display_name += f' {self.patronymic}'
            return display_name
        except Exception:
            return '(Данные не найдены)'

    class Meta:
        verbose_name = 'Профиль сотрудника ЦОКО'
        verbose_name_plural = 'Профили сотрудников ЦОКО'


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    """Создание профиля сотрудника ЦОКО после добавления нового пользователя Django"""
    if created:
        if instance.is_staff or instance.is_superuser:
            new_profile = CokoProfile(django_user_id=instance.id)
            new_profile.save()
