import uuid
from typing import Optional

from apps.applications.selectors.pay_denied_message import pay_denied_message_orm
from apps.applications.services.course_application import course_application_service
from apps.applications.services.event_application import event_application_service


class PayDeniedMessageService:
    """Класс методов для работы с комментариями об отклоненной оплате в заявках"""

    @staticmethod
    def get_message(app_id: uuid) -> Optional[str]:
        """
        Получение комментария об отклоненной оплате в заявке
        :param app_id: object_id заявки
        :return: Комментарий или None
        """
        pdm = pay_denied_message_orm.get_one_record_or_none(filter_by=dict(course_application_id=app_id))
        if not pdm:
            pdm = pay_denied_message_orm.get_one_record_or_none(filter_by=dict(event_application_id=app_id))
        if pdm:
            return pdm.message

    @staticmethod
    def save_message(service_type: str, app_id: uuid, message: str):
        """
        Сохранить комментарий об отклоненной оплате в заявке
        :param service_type: тип услуги (course, event)
        :param app_id: object_id заявки
        :param message: комментарий
        :return:
        """
        save_info = {
            f'{service_type}_application_id': app_id,
            'message': message
        }
        pay_denied_message_orm.create_record(create_object=save_info)

    @staticmethod
    def delete_message(service_type: str, app_id: uuid):
        """
        Удалить комментарий об отклоненной оплате в заявке
        :param service_type: тип услуги (course, event)
        :param app_id: object_id заявки
        :return:
        """
        pay_denied_message_orm.delete_record(filter_by={f'{service_type}_application_id': app_id})


pay_denied_message_service = PayDeniedMessageService()
