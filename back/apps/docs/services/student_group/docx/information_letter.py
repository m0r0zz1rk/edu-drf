from apps.commons.utils.data_types.date import date_utils
from apps.commons.utils.data_types.string import string_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc


class InformationLetter(BaseStudentGroupDoc):
    """Класс для генерации информационного письма в учебной группе"""

    def _get_context(self) -> dict:
        """
        Получение словаря с данными для подстановки
        :return: словарь с данными
        """
        date_start, date_finish = self._get_date_start_and_end()
        order_date = self._get_order_date(date_start)
        pay_date = self._get_pay_date(date_start)
        context = {
            'cats_aud_plural': self._get_audience_categories_str(),
            'date_start': date_utils.get_text_date_genitive_case(date_start),
            'date_finish': date_utils.get_text_date_genitive_case(date_finish),
            'price': str(self._get_price()),
            'order_day': date_utils.get_text_date_genitive_case(order_date),
            'pay_day': date_utils.get_text_date_genitive_case(pay_date),
            'email_curator': self.student_group.curator.django_user.email,
            'phone_ad_curator': self.student_group.curator.internal_phone,
            'duration': self._get_duration()
        }
        if self.student_group.ou:
            context['theme'] = self.student_group.ou.program.name
        else:
            context['theme'] = self.student_group.iku.name
            context['paid_iku'] = f'платный {self.student_group.iku.type.name.lower()}'
            context['type_iku'] = string_utils.get_word_case(
                self.student_group.iku.type.name,
                'gent'
            )
            context['type_loct_iku'] = string_utils.get_word_case(
                self.student_group.iku.type.name,
                'loct'
            )
        return context
