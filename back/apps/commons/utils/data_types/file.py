from io import BytesIO

from PIL import Image


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

    @staticmethod
    def jpg_to_pdf(image_path: str) -> bytes:
        """
        Преобразование изображений (jpg, jpeg) в pdf
        :param image_path: путь до изображения
        :return: буфер с полученным PDF
        """
        with open(image_path, "rb") as f:
            jpg_data = f.read()
        img = Image.open(BytesIO(jpg_data))
        # Преобразование в RGB
        if img.mode != "RGB":
            img = img.convert("RGB")
        pdf_bytes = BytesIO()
        img.save(pdf_bytes, format="PDF")
        pdf_bytes.seek(0)
        return pdf_bytes.getvalue()

file_utils = FileUtils()