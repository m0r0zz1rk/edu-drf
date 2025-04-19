import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.celery_app.tasks import email_offer_pay
from apps.docs.selectors.student_group_offer import student_group_offer_orm
from apps.edu.consts.student_group.statuses import URL
from apps.edu.services.student_group import student_group_service


def upload_offer(group_id: uuid, doc: InMemoryUploadedFile):
    """
    Подгрузка договора оферты для учебной группы
    :param group_id: object_id учебной группы
    :param doc: отсканированный договор оферты в формате pdf
    :return:
    """
    filter_by = {'group_id': group_id}
    if student_group_offer_orm.get_one_record_or_none(filter_by=filter_by):
        student_group_offer_orm.update_record(
            filter_by=filter_by,
            update_object={'file': doc}
        )
    else:
        student_group_offer_orm.create_record(
            create_object={**filter_by, 'file': doc}
        )
    student_group_service.change_group_status(group_id, URL)
    email_offer_pay.delay(group_id)
