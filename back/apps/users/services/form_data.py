from apps.guides.selectors.mo import mo_queryset
from apps.guides.selectors.position import position_queryset
from apps.guides.selectors.position_category import position_category_queryset
from apps.guides.selectors.region import region_queryset


class FormDataService:
    """Класс методов для работы с данными, необходимыми для заполнения анкеты обучающихся"""

    _form_data_models = [
        {
            'key': 'region',
            'qs': region_queryset
        },
        {
            'key': 'mo',
            'qs': mo_queryset
        },
        {
            'key': 'position_category',
            'qs': position_category_queryset
        },
        {
            'key': 'position',
            'qs': position_queryset
        }
    ]

    def get_form_data(self) -> dict:
        """
        Получение массива данных для заполнения анкеты пользователем
        """
        data = {}
        for obj in self._form_data_models:
            data[obj['key']] = obj['qs']()
        return data
