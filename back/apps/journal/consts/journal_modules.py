COMMON = 'COMMON'
ADMINS = 'ADMINS'
APPLICATIONS = 'APPLICATIONS'
AUTHEN = 'AUTHEN'
CELERY = 'CELERY'
DOCS = 'DOCS'
EDU = 'EDU'
GUIDES = 'GUIDES'
JOURNAL = 'JOURNAL'
REPORTS = 'REPORTS'
SETTINGS = 'SETTINGS'
SURVEYS = 'SURVEYS'
USERS = 'USERS'
ORM = 'ORM'

# Список модулей АИС
JOURNAL_MODULES = (
    (COMMON, 'Общий'),
    (ADMINS, 'ЛК Администратора'),
    (APPLICATIONS, 'Модуль заявок'),
    (AUTHEN, 'Модуль авторизации/регистрации'),
    (CELERY, 'Модуль очереди задач Celery'),
    (DOCS, 'Модуль документов'),
    (EDU, 'Модуль учебной части'),
    (GUIDES, 'Модуль справочников'),
    (JOURNAL, 'Модуль журнала событий'),
    (REPORTS, 'Модуль отчетов'),
    (SETTINGS, 'Модуль настроек'),
    (SURVEYS, 'Модуль опросов'),
    (USERS, 'ЛК Пользователя'),
    (ORM, 'Модуль запросов к БД')
)
