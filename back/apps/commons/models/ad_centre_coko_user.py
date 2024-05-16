from django.contrib.auth.models import User
from django.db import models

from apps.commons.models import BaseTable
from apps.commons.models.ad_centre import AdCentre


class AdCentreCokoUser(BaseTable):
    """Модель привязки работника ЦОКО"""
    coko_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь Django'
    )
    ad_centre = models.ForeignKey(
        AdCentre,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Подразделение-центр из AD'
    )

    def __str__(self):
        text = f'{self.coko_user.username} - '
        if self.ad_centre:
            text += self.ad_centre.display_name
        else:
            text += '(не установлено)'
        return text

    class Meta:
        verbose_name = 'Связь Пользователь ЦОКО - Подразделение-центр АД'
        verbose_name_plural = 'Связи Пользователь ЦОКО - Подразделение-центр АД'
