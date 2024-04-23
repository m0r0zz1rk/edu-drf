class NetworkUtils:
    """Класс для работы с сетью"""

    @staticmethod
    def get_ip_address(request) -> str:
        """Получение IP адреса источника запроса"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
