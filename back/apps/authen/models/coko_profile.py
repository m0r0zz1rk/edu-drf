from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.authen.models.base_profile import BaseProfile


class CokoProfile(BaseProfile):
    """Модель профиля сотрудника ЦОКО"""
    internal_phone = models.PositiveIntegerField(
        default=100,
        verbose_name='Внутренний номер телефона'
    )
    curator_groups = models.BooleanField(
        default=False,
        verbose_name='Отображать только учебные группы как куратора'
    )

    def __str__(self):
        return self.display_name

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
