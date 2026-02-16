from typing import Union

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from apps.applications.consts.application_statuses import PAY, STUDY, STUDY_COMPLETE, ARCHIVE

from apps.applications.selectors.course_application import course_application_model
from apps.applications.selectors.event_application import event_application_model
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc
from apps.docs.utils.excel_utils import set_cell_value, set_cells_width


class FormsDoc(BaseStudentGroupDoc):
    """
    Класс для генерации excel файла с анкетами обучающихся на основе заявок
    """

    _event_forms_columns = {
        'Дата подачи заявки': 'date_create',
        'Телефон': 'profile.phone',
        'Email': 'profile.django_user.email',
        'Фамилия': 'profile.surname',
        'Имя': 'profile.name',
        'Отчество': 'profile.patronymic',
        'Регион': 'region.name',
        'Муниципальное образование': 'mo.name',
        'Организация': 'oo',
        'Категория должности': 'position_category.name',
        'Должность': 'position.name',
        'Тип оплаты': 'type',
        'Тип ОО': 'oo.oo_type.name',
        'Оплачено': 'pay',
        'Опрос пройден': 'check_survey'
    }

    _course_forms_columns = {
        **_event_forms_columns,
        'Уровень образования': 'education_level',
        'Категория получаемого образования': 'education_category',
        'Фамилия в дипломе': 'diploma_surname',
        'Cерия документа об образовании': 'education_serial',
        'Номер документа об образовании': 'education_number',
        'Дата выдачи документа об образовании': 'education_date',
        'Получение удостоверения почтой': 'certificate_mail',
        'Физический адрес доставки удостоверения': 'mail_address'
    }

    def _get_context(self) -> dict:
        pass

    def _get_columns(self) -> dict:
        """
        Получение списка столбцов в зависимости от типа учебной группы
        :return: Словарь со столбцами
        """
        return self._course_forms_columns if self.student_group.ou else self._event_forms_columns

    def _set_columns(self, ws: Worksheet):
        """
        Установка заголовков на листе книги Excel
        :param ws: лист книги Excel
        :return:
        """
        columns = self._get_columns()
        for index, column in enumerate(columns.keys(), start=1):
            set_cell_value(
                cell=ws.cell(row=1, column=index),
                value=column,
                font_bold=True,
                align_center=False,
                border=True
            )

    @staticmethod
    def _get_application_oo(app: Union[course_application_model, event_application_model]):
        """
        Получение образовательной организации из заявки обучающегося
        :param app: заявка обучающегося
        :return: наименование образовательной организации
        """
        if app.oo is None:
            if app.oo_new == '':
                return '-'
            else:
                return app.oo_new
        else:
            return app.oo.short_name

    def _set_data(self, ws: Worksheet):
        """
        Установка данных на листе книги Excel
        :param ws: лист книги Excel
        :return:
        """
        columns = self._get_columns()
        applications = self._get_group_applications()
        for app_index, app in enumerate(applications, start=2):
            for col_index, col in enumerate(columns.values(), start=1):
                if col == 'education_level':
                    value = app.get_education_level_display()
                elif col == 'education_category':
                    value = app.get_education_category_display()
                elif col == 'oo':
                    value = self._get_application_oo(app)
                elif col == 'type':
                    value = 'Физическое лицо' if app.physical else 'Юридическое лицо'
                elif col == 'certificate_mail':
                    value = 'Да' if app.certificate_mail else 'Нет'
                elif col == 'check_survey':
                    value = 'Да' if app.check_survey else 'Нет'
                elif col == 'pay':
                    value = 'Да' if app.status in [PAY, STUDY, STUDY_COMPLETE, ARCHIVE] else 'Нет'
                else:
                    value = app
                    for attribute in col.split('.'):
                        value = getattr(value, attribute, '-')
                if 'date' in col:
                    value = value.strftime('%d.%m.%Y')
                set_cell_value(
                    cell=ws.cell(row=app_index, column=col_index),
                    value=value,
                    align_center=False,
                    border=True
                )

    def _fill_wb(self, wb: Workbook):
        """
        Заполнение данных из заявок обучающихся в Excel файл
        :param wb: файл Excel
        :return:
        """
        worksheet = wb.active
        worksheet.title = 'Анкеты'
        self._set_columns(worksheet)
        self._set_data(worksheet)
        # set_cells_width(worksheet, 50)
