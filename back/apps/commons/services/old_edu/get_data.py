from apps.commons.services.old_edu.queries.authen import AuthenData
from apps.commons.services.old_edu.queries.guides import GuidesData

authen_data = AuthenData()
guides_data = GuidesData()


def get_all_edu_data():
    """
    Получение всех данных из олдовой базы edu
    """

    # Модуль guides
    print('### Начало работы с модулем Справочники')
    # guides_data.get_audience_categories()
    # guides_data.get_event_types()
    # guides_data.get_mos()
    # guides_data.get_oo_types()
    # guides_data.get_oos()
    # guides_data.get_positions()
    # guides_data.get_position_categories()
    # guides_data.get_states()
    # guides_data.get_regions()
    print('### Окончание работы с модулем Справочники')

    # Модуль authen
    print('### Начало работы с модулем авторизации и аутентификации (пользователи и профили)')
    # authen_data.get_django_users()
    # authen_data.get_student_profile_info()
    # authen_data.add_student_to_group()
    # authen_data.get_coko_profile_info()
    # authen_data.add_coko_to_group()
    print('### Окончание работы с модулем авторизации и аутентификации (пользователи и профили)')
