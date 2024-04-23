from apps.authen.models import States


class StateUtils:
    """Класс методов для работы с государствами"""

    states = [
        'Азербайджан',
        'Армения',
        'Грузия',
        'Казахстан',
        'Киргизия',
        'Латвия',
        'Литва',
        'Молдавия',
        'Республика Беларусь',
        'Россия',
        'Таджикистан',
        'Туркменистан',
        'Узбекистан',
        'Украина',
        'Эстония'
    ]

    @staticmethod
    def get_russia():
        """Получение uuid государства 'Россия'"""
        if States.objects.filter(name='Россия').exists():
            return States.objects.get(name='Россия').object_uuid
        else:
            rec = States(name='Россия')
            rec.save()
            return rec.object_id

    @staticmethod
    def get_all_states() -> dict:
        """Получение списка государств"""
        states = []
        for state in States.objects.all().order_by('name'):
            states.append({
                'id': state.object_id,
                'name': state.name
            })
        return {'states': states}

    @staticmethod
    def check_states_exists() -> bool:
        """Проверка на наличие государств"""
        return States.objects.count() > 0

    def add_base_states(self):
        """Добавление базовых государств в БД"""
        for state in self.states:
            new_state = States(name=state)
            new_state.save()
