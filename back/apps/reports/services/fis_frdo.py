import os

from ruopenrefs.providers.mosru import OksmRef
from xlsxtpl.writerx import BookWriter

from apps.applications.consts.education import MIDDLE_PROFESSIONAL
from apps.applications.selectors.course_application import course_application_orm
from apps.applications.selectors.course_certificate import course_certificate_orm
from apps.commons.utils.django.settings import settings_utils
from apps.edu.selectors.student_group import student_group_orm

oksm = OksmRef()

fis_frdo_path = os.path.join(
    settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
    'Шаблоны',
    'Отчеты',
    'шаблон_ФИС_ФРДО.xlsx'
)


class FisFrdo:
    """
    Класс для формирования отчета ФИС ФРДО
    """

    group_ids = None
    oksm_countries = None

    def __init__(self, report_parameters: dict):
        """
        Инициализация класса - установка списка object_id учебных групп и получение списка
        стран по ОКСМ
        :param report_parameters: словарь с параметрами отчета
        """
        self._get_oksm_countries()
        self.group_ids = report_parameters.get('group_ids')

    def _get_oksm_countries(self):
        """
        Получение справочника стран ОКСМ
        :return:
        """
        countries = []
        try:
            for country in oksm.iter_items():
                countries.append(country)
            self.oksm_countries = countries
        except Exception:
            self.oksm_countries = 643

    def _get_country_code(self, country: str) -> int:
        """
        Получение кода страны ОКСМ по ее названию
        :param country: название страны
        :return: код страны
        """
        if isinstance(self.oksm_countries, int):
            return self.oksm_countries
        for oksm_country in self.oksm_countries:
            if oksm_country[4] == country.upper():
                return oksm_country[0]

    def _get_docs(self):
        """Получение списка документов"""
        docs = []
        for group_id in self.group_ids:
            group = student_group_orm.get_one_record_or_none(filter_by=dict(object_id=group_id))
            if group:
                program = group.ou.program
                view = ("Удостоверение о повышении квалификации" if program.type == 'Повышение квалификации' else
                        "Диплом о профессиональной переподготовке")
                for app in course_application_orm.get_filter_records(filter_by=dict(group_id=group_id)):
                    cert = course_certificate_orm.get_one_record_or_none(filter_by=dict(application_id=app.object_id))
                    if app.education_level != 'Студент':
                        if app.education_level == MIDDLE_PROFESSIONAL:
                            edu_level = 'Среднее профессиональное образование'
                        else:
                            edu_level = 'Высшее образование'
                    else:
                        edu_level = 'Справка'
                    doc = {
                        'view': view,
                        'serial': cert.blank_serial if cert else '',
                        'number': cert.blank_number if cert else '',
                        'reg': cert.registration_number if cert else '',
                        'date_give': group.ou.date_end.strftime('%d.%m.%Y'),
                        'type_dpp': program.type,
                        'name_dpp': program.name,
                        'edu_level': edu_level,
                        'surn_diploma': app.diploma_surname if app.education_level != 'Студент' else '',
                        'edu_ser': app.education_serial if app.education_level != 'Студент' else '',
                        'edu_numb': app.education_number if app.education_level != 'Студент' else '',
                        'year_study': group.ou.date_start.strftime('%Y'),
                        'duration': program.duration,
                        'surname': app.profile.surname,
                        'name': app.profile.name,
                        'patronymic': app.profile.patronymic,
                        'birthday': app.profile.birthday.strftime('%d.%m.%Y'),
                        'sex': 'Муж' if app.profile.sex else 'Жен',
                        'snils': app.profile.snils,
                        'country': self._get_country_code(app.profile.state.name)
                    }
                    docs.append(doc)
        return docs

    def _fill_excel(self, writer: BookWriter):
        """
        Заполнение листа книги Excel
        :param writer: объект райтера для записи данных
        :return:
        """
        info = {'docs': self._get_docs()}
        writer.render_sheet(info, 'Шаблон', 0)

    def generate_file(self) -> BookWriter:
        """Генерация Excel файла с отчетом ПК-1"""
        # Объявление райтера для записи данных в шаблон отчета
        writer = BookWriter(fis_frdo_path)
        # Заполнение данными
        self._fill_excel(writer)
        return writer
