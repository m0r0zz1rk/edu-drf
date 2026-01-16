from django.db.models import QuerySet

from apps.applications.consts.application_statuses import DRAFT
from apps.applications.selectors.course_application import course_application_orm
from apps.applications.selectors.event_application import event_application_orm
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from apps.docs.utils.excel_utils import set_cell_value


class Drafts(BaseStudentGroupDoc):
    """
    Класс для генерации Excel файла с данными заявок-черновиков
    """

    __data_columns = {
        'Фамилия': 'profile.surname',
        'Имя': 'profile.name',
        'Отчество': 'profile.patronymic',
        'Телефон': 'profile.phone',
        'Email': 'profile.django_user.email'
    }

    def _get_context(self) -> dict:
        pass

    def _get_drafts(self) -> QuerySet:
        """
        Получение списка заявок со статусом "Черновик"
        """
        if self.student_group.ou:
            return (course_application_orm.get_filter_records(
                filter_by={'group_id': self.student_group.object_id, 'status': DRAFT},
                order_by=['profile__surname', 'profile__name', 'profile__patronymic']
            ))
        return (event_application_orm.get_filter_records(
            filter_by={'group_id': self.student_group.object_id, 'status': DRAFT},
            order_by=['profile__surname', 'profile__name', 'profile__patronymic']
        ))

    def _set_columns(self, ws: Worksheet):
        """
        Установка заголовков на листе книги Excel
        :param ws: лист книги Excel
        :return:
        """
        for index, column in enumerate(self.__data_columns.keys(), start=1):
            set_cell_value(
                cell=ws.cell(row=1, column=index),
                value=column,
                font_bold=True,
                align_center=False,
                border=True
            )

    def _set_data(self, ws: Worksheet):
        """
        Установка данных на листе книги Excel
        :param ws: лист книги Excel
        :return:
        """
        drafts = self._get_drafts()
        for app_index, app in enumerate(drafts, start=2):
            for col_index, col in enumerate(self.__data_columns.values(), start=1):
                value = app
                for attribute in col.split('.'):
                    value = getattr(value, attribute, '-')
                set_cell_value(
                    cell=ws.cell(row=app_index, column=col_index),
                    value=value,
                    align_center=False,
                    border=True
                )

    def _fill_wb(self, wb: Workbook):
        """
        Заполнение данных из черновиков обучающихся в Excel файл
        :param wb: файл Excel
        :return:
        """
        worksheet = wb.active
        worksheet.title = 'Черновики'
        self._set_columns(worksheet)
        self._set_data(worksheet)