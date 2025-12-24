DRAFT = 'draft'
WORK = 'work'
WAIT_PAY = 'wait_pay'
CHECK = 'check'
PAY = 'pay'
STUDY = 'study'
STUDY_COMPLETE = 'study_complete'
ARCHIVE = 'archive'

# Статусы заявок обучающихся
APPLICATION_STATUSES = (
    (DRAFT, 'Черновик'),
    (WORK, 'В работе'),
    (WAIT_PAY, 'Ждем оплаты'),
    (CHECK, 'На проверке'),
    (PAY, 'Оплачено'),
    (STUDY, 'Проходит обучение'),
    (STUDY_COMPLETE, 'Обучение завершено'),
    (ARCHIVE, 'Архив'),
)

# Статусы для активных заявок
ACTIVE_STATUSES = (DRAFT, WORK, WAIT_PAY, CHECK, PAY, STUDY, STUDY_COMPLETE)

# Статусы для заявок с проверенным документом об оплате
PAY_STATUSES = (PAY, STUDY, STUDY_COMPLETE, ARCHIVE)