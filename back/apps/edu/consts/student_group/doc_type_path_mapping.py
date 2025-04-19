from apps.edu.consts.student_group.doc_types import INFORMATION_LETTER, SERVICE_MEMO, SERVICE_ORDER, \
    OFFER_PROJECT, TRANSFER_ORDER, DEDUCTION_ORDER, FORMS, STUDENT_JOURNAL, CLOSE_DOC, SCHEDULE

# Маппинг типа документа учебной группы и пути хранения шаблона
STUDENT_GROUP_DOC_TYPE_PATH_MAPPING = {
    INFORMATION_LETTER: ('Информационное письмо',),
    SERVICE_MEMO: ('Оказание услуги', 'СЗ'),
    SERVICE_ORDER: ('Оказание услуги', 'Приказ'),
    OFFER_PROJECT: ('Договор оферты',),
    TRANSFER_ORDER: ('Приказы', 'Зачисление'),
    DEDUCTION_ORDER: ('Приказы', 'Отчисление'),
    FORMS: ('Анкеты',),
    STUDENT_JOURNAL: ('Журнал',),
    CLOSE_DOC: ('Закрывной документ', ),
    SCHEDULE: ('Расписание', )
}
