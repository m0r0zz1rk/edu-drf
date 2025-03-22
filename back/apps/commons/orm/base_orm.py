from typing import Optional

from django.db.models import QuerySet

from apps.commons.models import BaseTable
from apps.commons.orm.journal_orm_decorator import journal_orm_decorator


class BaseORM:
    """Базовый класс для работы с БД через ORM"""

    def __init__(self, model: BaseTable, select_related: list = None, prefetch_related: list = None):
        """
        Инициализация класса - установка модели, параметров select_related и prefetch_related
        :param model: модель БД
        :param select_related: Список параметров для оптимизации через select_related
        :param prefetch_related: Список параметров для оптимизации через prefetch_related
        """
        self.model = model
        self.select_related = select_related
        self.prefetch_related = prefetch_related

    def orm_with_select_or_prefetch_related(self) -> QuerySet:
        """
        Получение QuerySet с использованием select_related или prefetch_related
        :return: QuerySet
        """
        if self.select_related:
            return self.model.objects.select_related(*self.select_related).all()
        return self.model.objects.prefetch_related(*self.prefetch_related).all()

    def get_filter_records(
            self,
            filter_by: dict = None,
            exclude: dict = None,
            order_by: list = None) -> QuerySet:
        """
        Получение списка записей
        :param filter_by: Словарь с параметрами фильтрации
        :param order_by: Список полей для сортировки
        :return: QuerySet
        """
        payload = {}
        if filter_by:
            payload = {**filter_by}
        if exclude:
            payload['exclide'] = exclude
        if order_by:
            payload['order_by'] = order_by

        @journal_orm_decorator(
            model=self.model,
            request_type='Получение списка записей',
            payload=repr(payload)
        )
        def function() -> QuerySet:
            if self.select_related or self.prefetch_related:
                res = self.orm_with_select_or_prefetch_related()
            else:
                res = self.model.objects.all()
            if filter_by:
                res = res.filter(**filter_by)
            if exclude:
                res = res.exclude(**exclude)
            if order_by:
                res = res.order_by(*order_by)
            return res

        return function()

    def get_one_record_or_none(self, filter_by: dict) -> Optional[BaseTable]:
        """
        Получение одной записи из БД
        :param filter_by: Словарь с параметрами сортировки
        :return: Одна запись из БД или None
        """

        @journal_orm_decorator(
            model=self.model,
            request_type='Получение одной записи',
            payload=repr(filter_by)
        )
        def function():
            if self.select_related or self.prefetch_related:
                return self.orm_with_select_or_prefetch_related().get(**filter_by)
            return self.model.objects.get(**filter_by)

        return function()

    def create_record(self, create_object: dict):
        """
        Создание новой записи в БД
        :param create_object: Словарь с данными новой записи
        :return: None
        """

        @journal_orm_decorator(
            model=self.model,
            request_type='Добавление записи',
            payload=repr(create_object)
        )
        def function():
            self.model.objects.create(**create_object)

        return function()

    def update_record(self, filter_by: dict, update_object: dict):
        """
        Редактирование записей в БД
        :param filter_by: Словарь с параметрами поиска
        :param update_object: Словарь с обновленными данными по записи
        :return: None
        """
        payload = {**filter_by, **update_object}

        @journal_orm_decorator(
            model=self.model,
            request_type='Изменение записи',
            payload=repr(payload)
        )
        def function():
            if 'object_id' in update_object:
                del update_object['object_id']
            if self.select_related or self.prefetch_related:
                records = self.orm_with_select_or_prefetch_related().filter(**filter_by)
            else:
                records = self.model.objects.filter(**filter_by)
            for record in records:
                self.model.objects.update_or_create(
                    object_id=record.object_id, defaults=update_object
                )

        return function()

    def delete_record(self, filter_by: dict):
        """
        Удаление записей из БД
        :param filter_by: Словарь с параметрами поиска
        :return: None
        """

        @journal_orm_decorator(
            model=self.model,
            request_type='Удаление записи',
            payload=repr(filter_by)
        )
        def function():
            if self.select_related or self.prefetch_related:
                records = self.orm_with_select_or_prefetch_related().filter(**filter_by)
            else:
                records = self.model.objects.filter(**filter_by)
            for record in records:
                record.delete()

        return function()

    def clear_many_to_many(self, filter_by: dict, field: str):
        """
        Удаление объектов для связи ManyToMany
        :param filter_by: Словарь с параметрами поиска
        :param field: Поле ManyToMany
        :return: None
        """

        @journal_orm_decorator(
            model=self.model,
            request_type='Удаление объектов ManyToMany',
            payload=repr({**filter_by, 'field': field})
        )
        def function():
            if self.select_related or self.prefetch_related:
                records = self.orm_with_select_or_prefetch_related().filter(**filter_by)
            else:
                records = self.model.objects.filter(**filter_by)
            for record in records:
                record_field = getattr(record, field)
                record_field.clear()

        return function()

    def add_many_to_many(self, filter_by: dict, field: str, objects: list):
        """
        Добавление объектов для связи ManyToMany
        :param filter_by: Словарь с параметрами поиска
        :param field: Поле ManyToMany
        :param objects: список объектов на добавление
        :return: None
        """

        @journal_orm_decorator(
            model=self.model,
            request_type='Добавление объектов ManyToMany',
            payload=repr({**filter_by, 'field': field, 'objects': objects})
        )
        def function():
            if self.select_related or self.prefetch_related:
                records = self.orm_with_select_or_prefetch_related().filter(**filter_by)
            else:
                records = self.model.objects.filter(**filter_by)
            for record in records:
                record_field = getattr(record, field)
                record_field.add(*objects)

        return function()
