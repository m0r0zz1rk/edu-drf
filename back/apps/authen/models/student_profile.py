from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.authen.models.base_profile import BaseProfile
from apps.commons.utils.django.group import GroupUtils
from apps.guides.models import State


class StudentProfile(BaseProfile):
    """Модель профиля обучающегося"""
    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Государство'
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    snils = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        verbose_name='СНИЛС'
    )
    sex = models.BooleanField(
        default=False,
        verbose_name='Пол'
    )
    phone = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        default='+7 (999) 999-99-99',
        verbose_name='Номер телефона'
    )
    teacher = models.BooleanField(
        default=False,
        verbose_name='Пользователь является преподавателем'
    )
    health = models.BooleanField(
        default=False,
        verbose_name='У пользователя имеются ограничения по здоровью'
    )

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = 'Профиль обучающегося'
        verbose_name_plural = 'Профили обучающихся'


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    """Создание профиля пользователя после добавления нового пользователя Django"""
    if created:
        if not instance.is_staff and not instance.is_superuser:
            new_profile = StudentProfile(django_user_id=instance.id)
            new_profile.save()


@receiver(post_save, sender=User)
def check_groups_and_set_first_user_admin(instance, created, **kwargs):
    """Проверка на регистрацию первого пользователя и наличие групп пользователей"""
    if created:
        if User.objects.count() == 1:
            instance.is_superuser = True
            instance.is_staff = True
            instance.save()
            gu = GroupUtils()
            gu.create_group('Администраторы')
            gu.create_group('Сотрудники')
            gu.create_group('Обучающиеся')
            gu.get_group_by_name('Администраторы').user_set.add(instance)
