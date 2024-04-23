import sys
import traceback


class ExceptionHandling:
    """Класс методов для обработки исключений"""

    @staticmethod
    def get_traceback() -> str:
        """Получение traceback исключения"""
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trb = repr(
            traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
        )
        return trb
