from typing import Union

from django.apps import apps

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.settings import SettingsUtils


class ModelUtils:
    """Класс методов для работы с моделями приложений Django"""

    @staticmethod
    def is_model_exist_in_app(app_name: str, model_name: str) -> Union[bool, str]:
        """
        Проверка на существующую модель в приложении
        :param app_name: название приложения (в формате "apps.(name)")
        :param model_name: название модели
        :return: true - модель существует, false - модель не существует, str - ошибка при выполнении
        """
        project_apps = SettingsUtils().get_parameter_from_settings('PROJECT_APPS')
        if f'apps.{app_name}' in project_apps:
            try:
                app_models = [model for model in apps.all_models[app_name]]
                return str.lower(model_name) in app_models
            except Exception:
                return ExceptionHandling.get_traceback()
        return 'Приложение не найдено'
