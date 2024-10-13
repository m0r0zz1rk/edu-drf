class IncorrectQuestionInfo(Exception):
    """Исключение, возникающие при поступлении некорректных данных о вопросе"""
    pass


class QuestionCreateUpdateError(Exception):
    """Исключение, возникающие при ошибке во время добавления или обновления вопроса опроса"""
    pass


class QuestionDoesNotExist(Exception):
    """Исключение, возникающие в случае отсутствия вопроса опроса"""
    pass
