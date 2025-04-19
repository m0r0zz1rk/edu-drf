import uuid

from apps.commons.utils.data_types.date import date_utils
from apps.commons.utils.data_types.string import string_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc


class ServiceOrder(BaseStudentGroupDoc):
    """
    Класс для генерации приказа об оказании услуги в учебной группе
    """

    @staticmethod
    def _get_manager_fio(manager_fio: str) -> str:
        """
        Получение инициалов руководителя центра
        :param manager_fio: ФИО руководителя
        :return: Фамилия И.О.
        """
        fio_list = manager_fio.split(' ')
        return f'{fio_list[0]} {fio_list[1][:1]}.{fio_list[2][:1]}.'

    @staticmethod
    def _get_centre_name(department_name: str) -> str:
        """
        Получение наименования центра без слова "Центр"
        :param department_name: наименование подразделения
        :return: Строка с наименованием центра
        """
        list_words = department_name.split(' ')
        name = ''
        for word in list_words:
            if word not in ['Центр', 'центр']:
                name += f'{word} '
        return name[:-1]

    def _get_context(self) -> dict:
        """
        Получение словаря с данными для подстановки
        :return: Словарь с данными
        """
        dep, manager = self._get_department_and_manager()
        date_start, date_end = self._get_date_start_and_end()
        context = {
            'dep': self._get_centre_name(dep),
            'manager': self._get_manager_fio(manager),
            'code': self.student_group.code,
            'date_start': f'{date_utils.get_text_date_genitive_case(date_start)}',
            'date_end': f'{date_utils.get_text_date_genitive_case(date_end)}',
            'duration': str(self._get_duration()),
            'price': str(self._get_price())
        }
        if self.student_group.ou:
            context['program'] = self.student_group.ou.program.name
        else:
            context['type'] = string_utils.get_word_case(
                self.student_group.iku.type.name,
                'gent'
            )
            context['type_classic'] = self.student_group.iku.type.name.lower()
            context['type_loct'] = string_utils.get_word_case(
                self.student_group.iku.type.name,
                'loct'
            )
            context['event_name'] = self.student_group.iku.name
        return context
