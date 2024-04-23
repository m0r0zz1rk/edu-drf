from rest_framework import status
from rest_framework.response import Response


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
