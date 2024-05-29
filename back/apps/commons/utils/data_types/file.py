class FileUtils:
    """Класс методов для работы с файлами"""

    @staticmethod
    def file_to_binary_array(filename):
        """
        Преобразование файла в bytearray
        :return:
        """
        with open(filename, 'rb') as file:
            binary_data = bytearray(file.read())
        return binary_data
