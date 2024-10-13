from typing import Optional


class FileFormatUtils:
    """Класс методов для работы с форматами файлов"""

    format_content_type = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }

    def get_format_content_type(self, extension: str) -> Optional[str]:
        """
        Получение Content-Type в зависимости от расширения файла
        :param extension: расширение файла
        :return: str - соответствующий Content-Type, None - Content-Type не найден
        """
        try:
            if extension in self.format_content_type.keys():
                return self.format_content_type[extension]
            return None
        except Exception:
            return None
