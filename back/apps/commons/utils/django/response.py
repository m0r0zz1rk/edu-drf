import os
from urllib.parse import quote

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from apps.commons.utils.file_format import FileFormatUtils


class ResponseUtils:
    """Класс для генерации ответов на запросы"""

    @staticmethod
    def bad_request_response(message) -> Response:
        """Генерация ответа с кодом 400 и ошибкой error"""
        return Response(
            {'error': message},
            status=status.HTTP_400_BAD_REQUEST
        )

    def sorry_try_again_response(self) -> Response:
        """Генерация ответа с кодом 400 и текстом 'Произошла ошибка, повторите попытку позже'"""
        return self.bad_request_response(
            'Произошла ошибка, повторите попытку позже'
        )

    @staticmethod
    def ok_response(message) -> Response:
        """Генерация ответа с кодом 200 и словарем с ключом success и сообщением"""
        return Response(
            {
                'success': message
            },
            status=status.HTTP_200_OK
        )

    @staticmethod
    def no_content_response() -> Response:
        """Генерация ответа со статусом 204 - No Content"""
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def ok_response_dict(d: dict) -> Response:
        """Генерация ответа с кодом 200 и телом полученного словаря"""
        return Response(
            d,
            status=status.HTTP_200_OK
        )

    @staticmethod
    def ok_response_list(arr: list) -> Response:
        """Генерация ответа с кодом 200 и телом полученного словаря"""
        return Response(
            arr,
            status=status.HTTP_200_OK
        )

    @staticmethod
    def bad_request_no_data() -> Response:
        """Генерация ответа с кодом 400 без данных"""
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def unauthorized_no_data() -> Response:
        """Генерация ответа с кодом 401 без данных"""
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden_no_data() -> Response:
        """Генерация ответа с кодом 403 без данных"""
        return Response(status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def ok_response_no_data() -> Response:
        """Генерация ответа с кодом 200 без данных"""
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def auth_failed_response(text: str) -> Response:
        """Генерация ответа с кодом 400 при ошибке авторизации"""
        return Response(
            {'error': text},
            status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def conflict_failed_response_no_data() -> Response:
        """Генерация пустого ответа с кодом 409"""
        return Response(status=status.HTTP_409_CONFLICT)

    @staticmethod
    def not_acceptable_response_no_data() -> Response:
        """Генерация пустого ответа с кодом 406"""
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def file_response(file) -> HttpResponse:
        """
        Генерация ответа с файлом
        :param file: файл
        :return: Response
        """
        _, file_extension = os.path.splitext(file.path)
        _, file_name = os.path.split(file.path)
        response = HttpResponse(file, content_type=FileFormatUtils().get_format_content_type(file_extension))
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(file_name)}"
        response['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response

    @staticmethod
    def locked_response() -> Response:
        """Генерация пустого ответа с кодом 423"""
        return Response(status=status.HTTP_423_LOCKED)


response_utils = ResponseUtils()
