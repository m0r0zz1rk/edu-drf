from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.commons.models.base_table import BaseTable
from apps.guides.models import State


class Profile(BaseTable):
    """Модель профиля пользователя"""
    django_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь Django'
    )
    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Государство'
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
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    age = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0),],
        verbose_name='Возраст'
    )
    sex = models.BooleanField(
        default=False,
        verbose_name='Пол'
    )
    phone = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        unique=True,
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
    curator_groups = models.BooleanField(
        default=False,
        verbose_name='Отображать только учебные группы как куратора'
    )

    def __str__(self):
        try:
            data = f'{self.surname} {self.name}'
            if len(str(self.patronymic)) > 0:
                data = f'{data} {self.patronymic}'
            data = f'{data} ({self.phone})'
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
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    """Создание профиля пользователя после добавления нового пользователя Django"""
    if created:
        new_profile = Profile(django_user_id=instance.id)
        new_profile.save()


@receiver(post_save, sender=User)
def check_groups_and_set_first_user_admin(instance, created, **kwargs):
    """Проверка на регистрацию первого пользователя и наличие групп пользователей"""
    if created:
        if User.objects.count() == 1:
            instance.is_superuser = True
            instance.is_staff = True
            instance.save()
            if not Group.objects.filter(name='Администраторы').exists():
                admins = Group(name='Администраторы')
                admins.save()
            else:
                admins = Group.objects.get(name='Администраторы')
            if not Group.objects.filter(name='Преподаватели').exists():
                teachers = Group(name='Преподаватели')
                teachers.save()
            if not Group.objects.filter(name='Участники').exists():
                participants = Group(name='Участники')
                participants.save()
            admins.user_set.add(instance)
