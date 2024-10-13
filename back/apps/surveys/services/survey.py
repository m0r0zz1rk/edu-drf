from apps.surveys.exceptions.survey import SurveyNotExist, SurveyDataNotValid
from apps.surveys.selectors.survey import survey_model


class SurveyService:
    """Класс методов для работы с опросами"""

    _create_update_fields = [
        'object_id',
        'description'
    ]

    def validate_data_for_create_update(self, data: dict) -> bool:
        """
        Валидация полученных данных об опросе для его создания или изменения
        :param data: словарь с данными об опросе
        :return: True - данные валидны, False - данные не валидны
        """
        for key in data:
            if key not in self._create_update_fields:
                return False
        return True

    @staticmethod
    def is_survey_exists(attribute_name: str, value) -> bool:
        """
        Проверка на существующий опрос
        :param attribute_name: наименование поля модели Survey
        :param value: значение атрибута для поиска
        :return: True - объект найден, False - объект не найден
        """
        return survey_model.objects.filter(**{attribute_name: value}).exists()

    def get_survey(self, attribute_name: str, value) -> survey_model:
        """
        Получение объекта опроса по поисковому атрибуту
        :param attribute_name: наименования поля модели Survey
        :param value: значения атрибута для поиска
        :return: объект модели Survey
        """
        if self.is_survey_exists(attribute_name, value):
            return survey_model.objects.filter(**{attribute_name: value}).first()
        raise SurveyNotExist

    def create_survey(self, user_id: int, serialize_data: dict):
        """
        Создание опроса
        :param user_id: id пользователя Django,
        :param serialize_data: данные о создаваемом опросе
        """
        if not self.validate_data_for_create_update(serialize_data):
            raise SurveyDataNotValid
        survey_model.objects.create(**{
            'creator_id': user_id,
            **serialize_data
        })

    def update_survey(self, survey_id: int, serialize_data: dict):
        """
        Обновление информации об опросе
        :param survey_id: object_id объекта опроса
        :param serialize_data: словарь с информацией об опросе (description)
        """
        if 'description' not in serialize_data:
            raise SurveyDataNotValid
        survey = self.get_survey('object_id', survey_id)
        survey.description = serialize_data['description']
        survey.save()
