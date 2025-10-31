from django.http import HttpResponse
from num2words import num2words

from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc
from apps.docs.utils.docx_utils import generate_word_file


class CloseDoc(BaseStudentGroupDoc):
    """
    Класс для формирования закрывного документа по учебной группе (только для ОУ)
    """

    def _get_total_price(self) -> str:
        """
        Получение общей суммы по оказанной услуге (кол-во студентов на стоимость услуги)
        :return: числовое, общая сумма
        """
        price = self.student_group.ou.program.price if self.student_group.ou else self.student_group.iku.price
        summary = price * self._get_application_count()
        return f'{summary} ({num2words(summary, lang="ru")})'

    def _get_context(self) -> dict:
        """
        Получение словаря с данными для подстановки
        :return: словарь с данными
        """
        date_start, date_end = self._get_date_start_and_end()
        context = {
            'date_start': date_start.strftime('%d.%m.%Y'),
            'date_end': date_end.strftime('%d.%m.%Y'),
            'code': self.student_group.code,
            'students_count': self._get_application_count(),
            'sum': self._get_total_price()
        }
        if self.student_group.ou:
            type_dpp, _ = self._get_program_and_certificates_types()
            program = self.student_group.ou.program
            context['type_dpp'] = type_dpp
            context['prog_name'] = program.name
            context['duration'] = program.duration
        else:
            context['theme'] = self.student_group.iku.name
            context['duration'] = self.student_group.iku.duration
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
        doc = self._set_student_data_into_table(doc, 1)
        doc.save(response)
        return response
