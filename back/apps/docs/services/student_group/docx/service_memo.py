import datetime

from pandas._libs.tslibs.offsets import BDay
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker

from apps.commons.utils.data_types.string import string_utils
from apps.commons.utils.django.settings import settings_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc
from apps.edu.consts.planning_parameters import PlanningParameters
from apps.edu.serializers.schedule import date_utils
from apps.edu.services.planning_parameter import planning_parameter_service

# Библиотека для работы с падежами
lib = PetrovichDeclinationMaker()


class ServiceMemo(BaseStudentGroupDoc):
    """
    Класс для генерации СЗ об оказании услуги в учебной группе
    """

    @staticmethod
    def _get_manager_initials_case_and_fio(manager_fio: str) -> tuple:
        """
        Получение инициалов руководителя центра в родительном падеже
        :param manager_fio: ФИО руководителя
        :return: Кортеж Фамилия И.О. в родительном падеже, Фамилия И.О.
        """
        fio_list = manager_fio.split(' ')
        surname = lib.make(NamePart.LASTNAME, Gender.FEMALE, Case.GENITIVE, fio_list[0])
        initials = f'{fio_list[1][:1]}.{fio_list[2][:1]}.'
        return f'{surname} {initials}', f'{fio_list[0]} {fio_list[1][:1]}.{fio_list[2][:1]}.'

    @staticmethod
    def _get_department_name_reduction_and_position(department_name: str) -> tuple:
        """
        Получение сокращения от наименования центра и должность
        :param department_name: наименование центра
        :return: сокращение и должность
        """
        list_dep = department_name.split(' ')
        for i in range(2):
            check_first = True
            if 'центр' in list_dep:
                if list_dep.index('центр') != 0:
                    check_first = False
            if 'Центр' in list_dep:
                if list_dep.index('Центр') != 0:
                    check_first = False
            if check_first is False:
                for el in list_dep:
                    if el != 'центр' and el != 'Центр':
                        list_dep[list_dep.index(el)] = el.replace('ый', 'ого')
                    else:
                        break
            if i == 0:
                position = 'руководителя '
                position_footer = 'Руководитель '
                for el in list_dep:
                    if el != 'центр' and el != 'Центр':
                        position += el.lower() + ' '
                        position_footer += el.lower() + ' '
                    else:
                        position += el.lower() + 'a '
                        position_footer += el.lower() + 'a '
        department_reduction = ''
        for el in list_dep:
            if el != 'центр' and el != 'Центр':
                department_reduction += el.lower() + ' '
            else:
                department_reduction += el.lower() + 'ом '
        return department_reduction, position, position_footer

    def _get_sz_date(self) -> datetime:
        """
        Получение даты служебной записки
        :return: дата
        """

        if self.student_group.ou:
            date = self.student_group.ou.date_start
        else:
            date = self.student_group.iku.date_start
        return date - BDay(
            int(planning_parameter_service.get_parameter_value_by_name(PlanningParameters.SERVICE_MEMO_DAYS))
        )

    def _get_curator_fio_accusative_case(self) -> str:
        """
        Получение ФИО куратора в винительном падеже
        :return: ФИО в родительном падеже
        """
        curator = self.student_group.curator
        return (f'{lib.make(NamePart.LASTNAME, Gender.FEMALE, Case.ACCUSATIVE, curator.surname)} '
                f'{lib.make(NamePart.FIRSTNAME, Gender.FEMALE, Case.ACCUSATIVE, curator.name)} '
                f'{lib.make(NamePart.MIDDLENAME, Gender.FEMALE, Case.ACCUSATIVE, curator.patronymic)}')

    def _get_context(self) -> dict:
        """
        Получение словаря с данными для вставки
        :return: словарь с данными
        """
        date_start, date_end = self._get_date_start_and_end()
        dep, manager = self._get_department_and_manager()
        department_reduction, position, position_footer = self._get_department_name_reduction_and_position(dep)
        initials, fio = self._get_manager_initials_case_and_fio(manager)
        context = {
            'manager': initials,
            'position': position,
            'date_sz': date_utils.get_text_date_genitive_case(self._get_sz_date()),
            'dep': department_reduction,
            'date_start': f'{date_start.strftime("%d.%m.%Y")}',
            'date_end': f'{date_end.strftime("%d.%m.%Y")}',
            'duration': str(self._get_duration()),
            'number_students': str(self._get_application_count()),
            'curator': self._get_curator_fio_accusative_case(),
            'position_footer': position_footer,
            'fio': fio
        }
        if self.student_group.ou:
            context['dpp_name'] = self.student_group.ou.program.name
        else:
            context['event_name'] = self.student_group.iku.name
            context['type'] = string_utils.get_word_case(
                self.student_group.iku.type.name,
                'gent'
            )
        return context
