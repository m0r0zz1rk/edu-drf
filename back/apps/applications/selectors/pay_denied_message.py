from django.apps import apps

from apps.commons.orm.base_orm import BaseORM

# Модель комментариев от отклоненной оплате в заявках
pay_denied_message_model = apps.get_model('applications', 'PayDeniedMessage')

# Класс ORM для комментариев от отклоненной оплате в заявках
pay_denied_message_orm = BaseORM(
    model=pay_denied_message_model,
    select_related=['course_application', 'event_application']
)

