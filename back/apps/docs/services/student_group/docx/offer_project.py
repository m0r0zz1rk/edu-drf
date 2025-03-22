from num2words import num2words

from apps.commons.utils.data_types.date import date_utils
from apps.commons.utils.data_types.string import string_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc


class OfferProject(BaseStudentGroupDoc):
    """
    Класс для генерации проекта договора оферты в учебной группе
    """

    def _get_context(self) -> dict:
        """
        Получение словаря с данными для подстановки
        :return: словарь с данными
        """
        date_start, date_end = self._get_date_start_and_end()
        order_date = self._get_order_date(date_start)
        pay_date = self._get_pay_date(date_start)
        price = self._get_price()
        context = {
            'code': self.student_group.code,
            'day_order': order_date.strftime('%d'),
            'month_order': date_utils.get_month_genitive_case(order_date.strftime('%B')),
            'year_order': order_date.strftime('%Y'),
            'duration': str(self._get_duration()),
            'day_start': date_start.strftime('%d'),
            'month_start': date_utils.get_month_genitive_case(date_start.strftime('%B')),
            'year_start': date_start.strftime('%Y'),
            'day_end': date_end.strftime('%d'),
            'month_end': date_utils.get_month_genitive_case(date_end.strftime('%B')),
            'year_end': date_end.strftime('%Y'),
            'curator_email': self.student_group.curator.django_user.email,
            'price': str(price),
            'price_letter': num2words(price, lang='ru'),
            'day_pay': pay_date.strftime('%d'),
            'month_pay': date_utils.get_month_genitive_case(pay_date.strftime('%B')),
            'year_pay': pay_date.strftime('%Y'),
        }
        if self.student_group.ou:
            program_type, certificate_type = self._get_program_and_certificates_types()
            context['type_dpp'] = program_type
            context['dpp_name'] = self.student_group.ou.program.name
            context['cert_type'] = certificate_type
        else:
            context['theme'] = self.student_group.iku.name
            context['type_iku'] = string_utils.get_word_case(
                self.student_group.iku.type.name,
                'gent'
            )
            context['loct_iku'] = string_utils.get_word_case(
                self.student_group.iku.type.name,
                'loct'
            )
        return context
