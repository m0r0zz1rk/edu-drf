from typing import Optional

from django.contrib.auth.models import Group


class GroupUtils:
    """Класс методов для работы с пользовательскими группами Django"""

    @staticmethod
    def is_group_exist(name: str) -> bool:
        """
        Проверка на существующую группу
        :param name: наименование группы
        :return: true - группа существует, false - группы не существует
        """
        return Group.objects.filter(name=name).exists()

    def create_group(self, name: str):
        """
        Добавление новой группы
        :param name: наименование группы
        :return:
        """
        if not self.is_group_exist(name):
            new_group = Group(name=name)
            new_group.save()

    def get_group_by_name(self, name: str) -> Optional[Group]:
        """
        Получение группы пользователей
        :param name: наименование группы
        :return: None - группа не найдена, Group - найденная группа
        """
        if not self.is_group_exist(name):
            self.create_group(name)
        return Group.objects.get(name=name)

