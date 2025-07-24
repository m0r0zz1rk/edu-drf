import codecs
from typing import Any

from pymorphy2 import MorphAnalyzer

from apps.commons.utils.django.settings import settings_utils


class StringUtils:
    """
    Класс методов для работы с текстом
    """

    ais_address = settings_utils.get_parameter_from_settings('AIS_ADDRESS')
    morph_analyzer = MorphAnalyzer()

    def get_word_case(self, word: str, case: str) -> str:
        """
        Получение падежа слова
        :param word: слово
        :param case: падеж (gent - родительный, loct - дательный)
        :return: просклоненное слово
        """
        word_parse = self.morph_analyzer.parse(word)[0]
        return word_parse.inflect({case}).word

    def decode_ldap(self, data: Any) -> str:
        """
        Декодирование данных из LDAP
        :param data: данные
        :return: декодированная строка
        """
        # if isinstance(str(data), unicode):
        #     return codecs.decode(str(data), 'unicode-escape')
        # return str(data)

        if 'localhost' in self.ais_address:
            return str(data)
        return codecs.decode(str(data), 'unicode-escape')


string_utils = StringUtils()
