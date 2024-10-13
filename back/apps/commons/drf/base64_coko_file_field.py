import datetime
import imghdr
import io

import PyPDF2
from PyPDF2.errors import PdfReadError
from drf_extra_fields.fields import Base64FileField


class Base64CokoFileField(Base64FileField):
    """Файловое поле для сохранения base64"""
    ALLOWED_TYPES = ['pdf', 'jpg', 'jpeg', 'png']

    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'title': 'Файл документа',
            'description': 'Файл в формате base64',
            'read_only': False
        }

    def get_file_name(self, decoded_file):
        return datetime.date.today().strftime('%d-%m-%Y')

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfReader(io.BytesIO(decoded_file))
            return 'pdf'
        except PdfReadError:
            try:
                ext = imghdr.what(filename, decoded_file)
                ext = 'jpg' if ext == 'jpeg' else ext
                return ext
            except Exception:
                raise
