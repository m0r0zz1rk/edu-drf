import os
from datetime import date

from django.db.models import QuerySet
from xlsxtpl.writerx import BookWriter

from apps.applications.consts.education import HIGHER, MIDDLE_PROFESSIONAL, STUDENT
from apps.applications.selectors.course_application import course_application_orm, course_application_model
from apps.authen.services.profile import profile_service
from apps.commons.utils.django.settings import settings_utils
from apps.edu.selectors.services.education_service import education_service_orm
from apps.edu.selectors.student_group import student_group_orm, student_group_model

# Путь к шаблону отчета ПК-1
pk_one_path = os.path.join(
    settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
    'Шаблоны',
    'Отчеты',
    'шаблон_ПК-1.xlsx'
)


class PKOneReport:
    """Класс для формирования отчета ПК-1 за выбранный год"""

    def __init__(self, report_data: dict):
        """
        Инициализация класса - фиксация года отчета
        :param report_data: параметры отчета, содержащие год
        """
        self.report_year = report_data.get('report_year')

    def _get_ous(self) -> QuerySet:
        """
        Получение queryset с образовательными услугами проведенным в год отчета
        :return: queryset с ОУ
        """
        return education_service_orm.get_filter_records(filter_by=dict(date_start__year=self.report_year))

    def _get_student_groups(self) -> QuerySet:
        """
        Получение queryset с учебным группами, образовательные услуги которых проведены в указанный год отчета
        :return: список UUID
        """
        ous = self._get_ous()
        ou_ids = [ou.object_id for ou in ous]
        return student_group_orm.get_filter_records(filter_by=dict(ou_id__in=ou_ids))

    def _get_count_upper_services(self) -> int:
        """
        Получение количества ДПП повышения квалификации
        :return: число
        """
        return self._get_ous().filter(program__type='Повышение квалификации').values("program_id").distinct().count()

    def _get_count_professional_services(self) -> int:
        """
        Получение количества ДПП профессиональной переподготовки
        :return: число
        """
        return self._get_ous().filter(program__type='Профессиональная переподготовка').\
            values("program_id").distinct().count()

    def _get_count_upper_or_professional_distance_groups(self, ou_type: str) -> int:
        """
        Получение количества учебных групп по программам повышения квалификации с использованием ДОТ
        :param ou_type: тип ОУ (Повышение квалификации, Профессиональная переподготовка)
        :return: число
        """
        groups = self._get_student_groups()
        dot_ou_ids = [group.ou_id for group in groups.filter(form='С использованием ДОТ')]
        ous = self._get_ous()
        ous = ous.filter(program__type=ou_type)
        return ous.filter(object_id__in=dot_ou_ids).values("program_id").distinct().count()

    @staticmethod
    def _add_health_count(students: dict, group_apps: QuerySet, dpp_type: str):
        """
        Добавить в словарь с информацией по заявкам количество обучающихся с ограничениями по здоровью
        :param students: словарь с информацией по заявкам
        :param group_apps: заявка учебной группы
        :param dpp_type: Тип ДПП учебной группы (Повышение квалификации, Профессиональная переподготовка)
        :return:
        """
        health_apps = group_apps.filter(profile__health=True)
        health_woman_apps_count = health_apps.filter(profile__sex=False).count()
        students['health_total'] = health_apps.count() if 'health_total' not in students.keys() else \
            students['health_total'] + health_apps.count()
        students['health_women'] = health_woman_apps_count if 'health_women' not in students.keys() else \
            students['health_women'] + health_woman_apps_count
        if dpp_type == 'Повышение квалификации':
            students['health_upper'] = health_apps.count() if 'health_upper' not in students.keys() else \
                students['health_upper'] + health_apps.count()
        else:
            students['health_prof'] = group_apps.count() if 'health_prof' not in students.keys() else \
                students['health_prof'] + group_apps.count()

    @staticmethod
    def _add_program_type_count(students: dict, group_apps: QuerySet, group: student_group_model):
        """
        Добавление в словарь с информацией по заявкам количество заявок по типам ДПП
        :param students: словарь с информацией по заявкам
        :param group_apps: заявка учебной группы
        :param group: Объект учебной группы
        :return:
        """
        total_count = group_apps.count()
        woman_count = group_apps.filter(profile__sex=False).count()
        with_dot = total_count if group.form != 'Без использования ДОТ' else 0
        only_dot = total_count if group.form == 'Исключительно ДОТ' else 0
        if group.ou.program.type == 'Повышение квалификации':
            students['count_upper'] = total_count if 'count_upper' not in students.keys() else \
                students['count_upper'] + total_count
            students['women_upper'] = woman_count if 'women_upper' not in students.keys() else \
                students['women_upper'] + woman_count
            students['upper_cntdot'] = with_dot if 'upper_cntdot' not in students.keys() else \
                students['upper_cntdot'] + with_dot
            students['upper_onlydot'] = only_dot if 'upper_onlydot' not in students.keys() else \
                students['upper_onlydot'] + only_dot
        else:
            students['count_prof'] = total_count if 'count_prof' not in students.keys() else \
                students['count_prof'] + total_count
            students['women_prof'] = woman_count if 'women_prof' not in students.keys() else \
                students['women_prof'] + woman_count
            students['prof_cntdot'] = with_dot if 'prof_cntdot' not in students.keys() else \
                students['prof_cntdot'] + with_dot
            students['prof_onlydot'] = only_dot if 'prof_onlydot' not in students.keys() else \
                students['prof_onlydot'] + only_dot

    @staticmethod
    def _add_woman_total(students: dict, group_apps: QuerySet):
        """
        Добавление в словарь с информацией по заявкам количество студентов женщин
        :param students: словарь с информацией по заявкам
        :param group_apps: заявка учебной группы
        :return:
        """
        woman_total = group_apps.filter(profile__sex=False).count()
        students['women_total'] = woman_total if 'women_total' not in students.keys() else \
            students['women_total'] + woman_total

    @staticmethod
    def _add_student_ages_info(students: dict, group_apps: QuerySet, dpp_type: str):
        """
        Добавление в словарь с информацией по заявкам данных по возрасту обучающихся
        :param students: словарь с информацией по заявкам
        :param group_apps: заявка учебной группы
        :param dpp_type: Тип ДПП учебной группы (Повышение квалификации, Профессиональная переподготовка)
        :return:
        """
        report_borders = [
            'lower_25',
            '25_29',
            '30_34',
            '35_39',
            '40_44',
            '45_49',
            '50_54',
            '55_59',
            '60_64',
            'higher_65'
        ]
        ages = {}
        ages_borders = {}
        for rb in report_borders:
            ages[f'total_{rb}'] = 0
            ages[f'woman_{rb}'] = 0
            spl = rb.split('_')
            if 'lower' in rb:
                ages_borders[rb] = (0, 24)
            elif 'higher' in rb:
                ages_borders[rb] = (65, 150)
            else:
                ages_borders[rb] = (int(spl[0]), int(spl[1]))
        today = date.today()
        for app in group_apps:
            birthday = app.profile.birthday
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
            for key, borders in ages_borders.items():
                if borders[0] <= age <= borders[1]:
                    ages[f'total_{key}'] += 1
                    if not app.profile.sex:
                        ages[f'woman_{key}'] += 1
        for key in ages.keys():
            students[key] = ages[key] if key not in students.keys() else \
                students[key] + ages[key]
            if dpp_type == 'Повышение квалификации':
                students[f'upper_{key}'] = ages[key] if f'upper_{key}' not in students.keys() else \
                    students[f'upper_{key}'] + ages[key]
            else:
                students[f'prof_{key}'] = ages[key]if f'prof_{key}' not in students.keys() else \
                    students[f'prof_{key}'] + ages[key]

    @staticmethod
    def _add_form_type_count(students: dict, group_apps: QuerySet):
        """
        Добавление в словарь с данными по заявкам количество заявок по типу лица (физ, юр)
        :param students: словарь с информацией по заявкам
        :param group_apps: заявка учебной группы

        :return:
        """
        physical_apps = group_apps.filter(physical=True).count()
        not_physical_apps = group_apps.exclude(physical=True).count()
        students['ind'] = physical_apps if 'ind' not in students.keys() else students['ind'] + physical_apps
        students['leg'] = not_physical_apps if 'leg' not in students.keys() else students['leg'] + not_physical_apps

    @staticmethod
    def _add_education_level_count(students: dict, group_apps: QuerySet, dpp_type: str):
        """
        Добавление в словарь с данными по заявкам количество заявок по уровню образования
        :param students: словарь с информацией по заявкам
        :param group_apps: заявка учебной группы
        :param dpp_type: Тип ДПП учебной группы (Повышение квалификации, Профессиональная переподготовка)
        :return:
        """
        edu_levels = {
            'st_v': {
                'level': STUDENT,
                'category': HIGHER
            },
            'st_m': {
                'level': STUDENT,
                'category': MIDDLE_PROFESSIONAL
            },
            'edmid': {
                'level': MIDDLE_PROFESSIONAL,
                'category': None
            },
            'edhigh': {
                'level': HIGHER,
                'category': None
            }
        }
        for key, value in edu_levels.items():
            apps = group_apps.filter(education_level=value.get('level'))
            if value.get('category'):
                apps = apps.filter(education_category=value.get('category'))
            woman_apps = apps.filter(profile__sex=False).count()
            physical_apps = apps.filter(physical=True).count()
            not_physical_apps = apps.filter(physical=False).count()
            students[f'{key}_women'] = woman_apps if f'{key}_women' not in students.keys() else \
                students[f'{key}_women'] + woman_apps
            students[f'{key}_ind'] = physical_apps if f'{key}_ind' not in students.keys() else \
                students[f'{key}_ind'] + physical_apps
            students[f'{key}_leg'] = not_physical_apps if f'{key}_leg' not in students.keys() else \
                students[f'{key}_leg'] + not_physical_apps
            students[f'{key}_total'] = apps.count() if f'{key}_total' not in students.keys() else \
                students[f'{key}_total'] + apps.count()
            if dpp_type == 'Повышение квалификации':
                students[f'{key}_upper'] = apps.count() if f'{key}_upper' not in students.keys() else \
                    students[f'{key}_upper'] + apps.count()
            else:
                students[f'{key}_prof'] = apps.count() if f'{key}_prof' not in students.keys() else \
                    students[f'{key}_prof'] + apps.count()

    @staticmethod
    def _add_work_type_to_students(prefix: str, students: dict, app: course_application_model, dpp_type: str):
        """
        Добавление одного балла в словарь с данными о заявках в полученных префикс
        :param prefix: префикс
        :param students: словарь с данными о заявках
        :param app: заявка обучающегося
        :param dpp_type: Тип ДПП учебной группы (Повышение квалификации, Профессиональная переподготовка)
        :return:
        """
        students[f'{prefix}_total'] = 1 if f'{prefix}_total' not in students.keys() else \
            students[f'{prefix}_total'] + 1
        if app.physical:
            students[f'{prefix}_ind'] = 1 if f'{prefix}_ind' not in students.keys() else \
                students[f'{prefix}_ind'] + 1
        else:
            students[f'{prefix}_leg'] = 1 if f'{prefix}_leg' not in students.keys() else \
                students[f'{prefix}_leg'] + 1
        if app.profile.sex is False:
            students[f'{prefix}_women'] = 1 if f'{prefix}_women' not in students.keys() else \
                students[f'{prefix}_women'] + 1
        if dpp_type == 'Повышение квалификации':
            students[f'{prefix}_upper'] = 1 if f'{prefix}_upper' not in students.keys() else \
                students[f'{prefix}_upper'] + 1
        else:
            students[f'{prefix}_prof'] = 1 if f'{prefix}_prof' not in students.keys() else \
                students[f'{prefix}_prof'] + 1

    def _add_work_type_count(self, students: dict, group_apps: QuerySet, dpp_type: str):
        """
        Добавление в словарь с данными по заявкам количество заявок по типу работника
        :param students: словарь с информацией по заявкам
        :param group_apps: заявка учебной группы
        :param dpp_type: Тип ДПП учебной группы (Повышение квалификации, Профессиональная переподготовка)
        :return:
        """
        work_types = {
            'ruk': {
                'category_in': 'руководители',
                'category_not_in': 'службы',
                'subcategories': {
                    'ruk_doo': 'дошкольных образовательных',
                    'ruk_oo': 'общеобразовательных',
                    'ruk_spo': 'профессиональных образовательных',
                    'ruk_vo': 'высшего образования',
                    'ruk_dpo': 'дополнительного профессионального',
                    'ruk_odo': 'дополнительного образования',
                }
            },
            'ped': {
                'category_in': 'пед. работники',
                'category_not_in': None,
                'subcategories': {
                    'ped_doo': 'дошкольных образовательных',
                    'ped_oo': 'общеобразовательных',
                    'ped_spo': 'профессиональных образовательных',
                    'ped_vo': 'высшего образования',
                    'ped_dpo': 'дополнительного профессионального',
                    'ped_odo': 'дополнительного образования',
                }
            },
            'gos': {
                'category_in': 'гос. гражд. службы',
                'category_not_in': None,
                'subcategories': {
                    'ruk_gos': 'руководители'
                }
            },
            'mun': {
                'category_in': 'муниципальной службы',
                'category_not_in': None,
                'subcategories': None
            },
            'mil': {
                'category_in': 'военной службы',
                'category_not_in': None,
                'subcategories': None
            },
            'empl': {
                'category_in': 'службы занятости',
                'category_not_in': None,
                'subcategories': None
            },
            'oth': {
                'category_in': 'другие',
                'category_not_in': None,
                'subcategories': None
            }
        }
        for app in group_apps:
            if app.work_less:
                self._add_work_type_to_students('empl', students, app, dpp_type)
                self._add_work_type_to_students('workl', students, app, dpp_type)
            else:
                for key, value in work_types.items():
                    if app.position_category is None:
                        continue
                    condition = value.get('category_in') in app.position_category.name and \
                        app.education_level != STUDENT
                    if value.get('category_not_in'):
                        condition = condition and value.get('category_not_in') not in app.position_category.name
                    if condition:
                        self._add_work_type_to_students(key, students, app, dpp_type)
                        if value.get('subcategories'):
                            for sub_key, sub_value in value.get('subcategories').items():
                                if sub_value in app.position_category.name:
                                    self._add_work_type_to_students(sub_key, students, app, dpp_type)

    @staticmethod
    def _add_summary_from_exist_data(students: dict):
        """
        Добавление итоговых данных на основе существующих в словаре с данными о заявках
        :param students: словарь с данными о заявках
        :return:
        """
        summary = {
            'total': ['count_prof', 'count_upper'],
            'edu_total': ['ruk_total', 'ped_total'],
            'edu_ind': ['ruk_ind', 'ped_ind'],
            'edu_leg': ['ruk_leg', 'ped_leg'],
            'edu_upper': ['ruk_upper', 'ped_upper'],
            'edu_prof': ['ruk_prof', 'ped_prof'],
            'edu_women': ['ruk_women', 'ped_women'],
        }
        for key, value in summary.items():
            students[key] = 0
            if value[0] in students.keys() and value[1] in students.keys():
                students[key] = students.get(value[0]) + students.get(value[1])
            elif value[0] in students.keys():
                students[key] = students.get(value[0])
            elif value[1] in students.keys():
                students[key] = students.get(value[1])
            else:
                pass

    def _get_students_info_dict(self) -> dict:
        """
        Получение словаря с данными по студентам учебных групп попадающим под параметры отчета
        :return: словарь
        """
        students = {}
        groups = self._get_student_groups()
        for group in groups:
            group_apps = course_application_orm.get_filter_records(filter_by=dict(group_id=group.object_id))
            self._add_health_count(students, group_apps, group.ou.program.type)
            self._add_program_type_count(students, group_apps, group)
            self._add_woman_total(students, group_apps)
            self._add_student_ages_info(students, group_apps, group.ou.program.type)
            self._add_form_type_count(students, group_apps)
            self._add_education_level_count(students, group_apps, group.ou.program.type)
            self._add_work_type_count(students, group_apps, group.ou.program.type)
            self._add_summary_from_exist_data(students)
        return students

    def _fill_excel(self, writer: BookWriter):
        """
        Заполнение книги Excel данными
        :param writer: объект райтера для записи данных
        :return:
        """
        # Информация для: Титульный лист, раздел 1.1 - 1.2
        info = {'year': self.report_year}

        # Информация для раздела 1.3
        info2 = {
            'dpp_upper': self._get_count_upper_services(),
            'dpp_prof': self._get_count_professional_services(),
            'upper_dot': self._get_count_upper_or_professional_distance_groups('Повышение квалификации'),
            'prof_dot': self._get_count_upper_or_professional_distance_groups('Профессиональная переподготовка'),
            # **students
        }

        # Получение информации по обучающимся и их заявкам по учебным группам заданного года отчета
        students = self._get_students_info_dict()

        # Получение недостающих данных из существующего словаря с данными
        if 'count_upper' in students:
            info2['count_upper'] = students['count_upper']
        if 'dpp_prof' in students:
            info2['count_prof'] = students['count_prof']
        if 'upper_cntdot' in students:
            info2['upper_cntdot'] = students['upper_cntdot']
        if 'upper_onlydot' in students:
            info2['upper_onlydot'] = students['upper_onlydot']
        if 'prof_cntdot' in students:
            info2['prof_cntdot'] = students['prof_cntdot']
        if 'prof_onlydot' in students:
            info2['prof_onlydot'] = students['prof_onlydot']

        # Информация для раздела 2.5
        info4 = {
            'health_total': students['health_total'] if 'health_total' in students.keys() else 0,
            'health_women': students['health_women'] if 'health_women' in students.keys() else 0,
            'health_upper': students['health_upper'] if 'health_upper' in students.keys() else 0,
            'health_prof': students['health_prof'] if 'health_prof' in students.keys() else 0
        }

        # Информация для раздела 3.4
        info5 = {'teachers_count': profile_service.get_coko_count()}

        # Информация для разделов 2.1 - 2.4
        info3 = {'dpp_upper': info2['dpp_upper']}
        if 'dpp_prof' in info2:
            info3['dpp_prof'] = info2['dpp_prof']
        for key, value in students.items():
            info3[key] = value

        # Пустой объект с информацией для пропуска страниц
        info_empty = {}

        # Заполнение листов книги Excel
        writer.render_sheet(info, 'Титульный лист', 0)
        writer.render_sheet(info, 'Раздел 1.1', 1)
        writer.render_sheet(info, 'Раздел 1.2', 2)
        writer.render_sheet(info2, 'Раздел 1.3', 3)
        writer.render_sheet(info, 'Раздел 1.4', 4)
        writer.render_sheet(info, 'Раздел 1.5', 5)
        writer.render_sheet(info3, 'Раздел 2.1', 6)
        writer.render_sheet(info3, 'Раздел 2.2', 7)
        writer.render_sheet(info3, 'Раздел 2.3.1', 8)
        writer.render_sheet(info3, 'Раздел 2.3.2', 9)
        writer.render_sheet(info3, 'Раздел 2.4', 10)
        writer.render_sheet(info4, 'Раздел 2.5', 11)
        writer.render_sheet(info_empty, 'Раздел 3.1', 12)
        writer.render_sheet(info_empty, 'Раздел 3.2', 13)
        writer.render_sheet(info_empty, 'Раздел 3.3.1', 14)
        writer.render_sheet(info_empty, 'Раздел 3.3.2', 15)
        writer.render_sheet(info5, 'Раздел 3.4', 16)
        writer.render_sheet(info_empty, 'Раздел 3.5', 17)
        writer.render_sheet(info_empty, 'Раздел 3.6', 18)
        writer.render_sheet(info_empty, 'Раздел 3.7', 19)
        writer.render_sheet(info_empty, 'Раздел 3.8.1', 20)
        writer.render_sheet(info_empty, 'Раздел 3.8.2', 21)
        writer.render_sheet(info_empty, 'Раздел 4.1', 22)
        writer.render_sheet(info_empty, 'Раздел 4.2', 23)
        writer.render_sheet(info_empty, 'Раздел 4.3', 24)
        writer.render_sheet(info_empty, 'Раздел 5.1', 25)
        writer.render_sheet(info_empty, 'Раздел 5.2', 26)
        writer.render_sheet(info_empty, 'Раздел 5.3', 27)
        writer.render_sheet(info_empty, 'Раздел 5.4', 28)
        writer.render_sheet(info_empty, 'Раздел 5.5', 29)
        writer.render_sheet(info_empty, 'Раздел 6.1', 30)
        writer.render_sheet(info_empty, 'Раздел 6.2', 31)
        writer.render_sheet(info_empty, 'Раздел 6.3', 32)
        writer.render_sheet(info_empty, 'Раздел 6.4', 33)
        writer.render_sheet(info_empty, 'Раздел 6.5', 34)

    def generate_file(self) -> BookWriter:
        """Генерация Excel файла с отчетом ПК-1"""
        # Объявление райтера для записи данных в шаблон отчета
        writer = BookWriter(pk_one_path)
        # Заполнение данными
        self._fill_excel(writer)
        return writer
