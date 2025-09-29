from apps.applications.consts.application_statuses import CHECK
from apps.applications.selectors.course_application import course_application_orm
from apps.applications.selectors.event_application import event_application_orm
from apps.applications.services.course_application import course_application_service
from apps.applications.services.event_application import event_application_service
from apps.docs.selectors.pay_doc import pay_doc_orm


class PayDocService:
    """Класс методов для работы с документами об оплате"""

    @staticmethod
    def save_pay_doc(pay_doc_data: dict):
        """
        Сохранение документа об оплате
        :param pay_doc_data: словарь с информацией об оплате - profile_id, app_id, file
        :return:
        """
        app = course_application_service.get_course_app(pay_doc_data.get('app_id'))
        orm = course_application_orm
        if not app:
            app = event_application_service.get_event_app(pay_doc_data.get('app_id'))
            orm = event_application_orm
        if app.pay_doc_id:
            pay_doc_orm.delete_record(filter_by=dict(object_id=app.pay_doc_id))
        new_pay_doc = pay_doc_orm.create_record(
            create_object={'profile_id': pay_doc_data.get('profile_id'), 'file': pay_doc_data.get('file')}
        )
        orm.update_record(
            filter_by={'object_id': app.object_id},
            update_object={'pay_doc_id': new_pay_doc.object_id, 'status': CHECK, 'updated_from_new': True}
        )


pay_doc_service = PayDocService()
