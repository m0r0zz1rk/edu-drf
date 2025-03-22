from django.http import HttpResponse

from apps.commons.utils.data_types.date import date_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc
from apps.docs.utils.docx_utils import generate_word_file


class DeductionOrder(BaseStudentGroupDoc):
    """
    Класс для генерации приказа об отчислении в учебной группе
    """

    def _get_context(self) -> dict:
        """
        Получение словаря с данными для вставки
        :return: словарь с данными
        """
        date_start, date_end = self._get_date_start_and_end()
        context = {
            'prog_name': self.student_group.ou.program.name,
            'duration': self._get_duration(),
            'day_exp': date_end.strftime('%d'),
            'month_exp': date_utils.get_month_genitive_case(date_end.strftime('%B')),
            'year_exp': date_end.strftime('%Y'),
            'day_start': date_start.strftime('%d'),
            'month_start': date_utils.get_month_genitive_case(date_start.strftime('%B')),
            'year_start': date_start.strftime('%Y'),
            'code': self.student_group.code
        }
        return context

    def get_response(self, folder_tuple: tuple, xlsx: bool = True) -> HttpResponse:
        """
        Получение HTTP респонза с файлом
        :param folder_tuple: Кортеж с директориями после "Шаблоны" до файла шаблона
        :param xlsx: Булево, если True - выгрузка эксель, иначе ворд
        :return:
        """
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = f'attachment; filename="info_{self.student_group.code}.docx"'
        doc = generate_word_file(
            self._get_template_path(folder_tuple),
            self._get_context()
        )
        doc = self._set_student_data_into_table(doc)
        doc.save(response)
        return response
