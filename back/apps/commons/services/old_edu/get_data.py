from apps.commons.services.old_edu.queries.applications import ApplicationsData
from apps.commons.services.old_edu.queries.authen import AuthenData
from apps.commons.services.old_edu.queries.docs import DocsData
from apps.commons.services.old_edu.queries.edu import EduData
from apps.commons.services.old_edu.queries.guides import GuidesData
from apps.commons.services.old_edu.queries.surveys import SurveysData

application_data = ApplicationsData()
authen_data = AuthenData()
guides_data = GuidesData()
docs_data = DocsData()
edu_data = EduData()
surveys_data = SurveysData()


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

    # Модуль docs
    print('### Начало работы с модулем Документы')
    # docs_data.get_program_orders()
    # docs_data.get_student_docs()
    # docs_data.get_pay_docs()
    print('### Окончание работы с модулем Документы')

    # Модуль edu
    print('### Начало работы с модулем Учебная часть')
    # edu_data.get_information_services()
    # edu_data.get_info_service_categories()
    # edu_data.get_programs()
    # edu_data.get_program_calendar_chapters()
    # edu_data.get_program_calendar_themes()
    # edu_data.get_program_categories()
    # edu_data.get_education_services()
    # edu_data.get_student_groups()
    # edu_data.set_group_curator()
    # edu_data.get_course_schedule()
    # edu_data.set_course_schedule_theme_teacher()
    # edu_data.get_event_schedule()
    # edu_data.set_event_schedule_teacher()
    print('### Окончание работы с модулем Учебная часть')

    # Получение договоров оферт для учебных групп
    print('### Работа с договорами оферты')
    # docs_data.get_offers()
    print('### Окончание работы с договорами оферты')

    # Модуль applications
    print('### Начало работы с модулем Заявки')
    # application_data.get_course_applications()
    application_data.get_course_certificates()
    # application_data.get_event_applications()
    print('### Окончание работы с модулем Заявки')

    # Модуль surveys
    print('### Начало работы с модулем Опросы')
    # surveys_data.get_surveys()
    # surveys_data.get_survey_questions()
    # surveys_data.get_student_answers()
    print('### Окончание работы с модулем Опросы')
