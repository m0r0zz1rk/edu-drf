from django.db import models

from apps.edu.models.service.base_service import BaseService


class EducationService(BaseService):
    """Модель образовательных услуг (курсы)"""
    program = models.ForeignKey(
        'edu.Program',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='ДПП'
    )

    def __str__(self):
        if self.program:
            return f'{self.program.name} (ID: {self.object_id})'
        return self.object_id

    class Meta:
        verbose_name = 'Образовательная услуга'
        verbose_name_plural = 'Образовательные услуги'
