from pymorphy2 import MorphAnalyzer


class StringUtils:
    """
    Класс методов для работы с текстом
    """

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


string_utils = StringUtils()
