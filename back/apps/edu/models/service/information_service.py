from django.db import models

from apps.edu.models.service.base_service import BaseService


class InformationService(BaseService):
    """Модель информационно-консультационных услуг (мероприятия)"""
    department = models.ForeignKey(
        'commons.AdCentre',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Подразделение'
    )
    type = models.ForeignKey(
        'guides.EventType',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Тип мероприятия'
    )
    name = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        default='Новое мероприятие',
        verbose_name='Наименование'
    )
    duration = models.PositiveIntegerField(
        default=0,
        verbose_name='Объем (кол-во часов)'
    )
    categories = models.ManyToManyField(
        'guides.AudienceCategory',
        verbose_name='Категории слушателей'
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name='Стоимость'
    )

    def __str__(self):
        return f'{self.name} (ID: {self.object_id})'

    class Meta:
        verbose_name = 'Информационно-консультационная услуга'
        verbose_name_plural = 'Информационно-консультационные услуги'
