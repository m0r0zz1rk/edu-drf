INFORMATION_LETTER = 'information_letter'
SERVICE_MEMO = 'service_memo'
SERVICE_ORDER = 'service_order'
OFFER_PROJECT = 'offer_project'
TRANSFER_ORDER = 'transfer_order'
DEDUCTION_ORDER = 'deduction_order'
FORMS = 'forms'
STUDENT_JOURNAL = 'student_journal'
CLOSE_DOC = 'close_doc'
SCHEDULE = 'schedule'
CERTIFICATES_LIST = 'certificates_list'

# Типы документов для выгрузки по учебной группе
STUDENT_GROUP_DOC_TYPES = (
    (INFORMATION_LETTER, 'Информационное письмо'),
    (SERVICE_MEMO, 'Служебная записка об оказании услуги'),
    (SERVICE_ORDER, 'Приказ об оказании услуги'),
    (OFFER_PROJECT, 'Проект договора оферты'),
    (TRANSFER_ORDER, 'Приказ о зачислении'),
    (DEDUCTION_ORDER, 'Приказ об отчислении'),
    (FORMS, 'Анкеты'),
    (STUDENT_JOURNAL, 'Журнал'),
    (CLOSE_DOC, 'Закрывной документ'),
    (SCHEDULE, 'Расписание'),
    (CERTIFICATES_LIST, 'Ведомость удостоверений'),
)
