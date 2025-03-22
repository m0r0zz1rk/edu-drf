from apps.docs.services.student_group.docx import InformationLetter, ServiceMemo, ServiceOrder, OfferProject, \
    TransferOrder, DeductionOrder
from apps.docs.services.student_group.excel import FormsDoc
from apps.edu.consts.student_group.doc_types import INFORMATION_LETTER, SERVICE_MEMO, SERVICE_ORDER, OFFER_PROJECT, \
    TRANSFER_ORDER, DEDUCTION_ORDER, FORMS

# Маппинг типа документа учебной группы и класса обработки
STUDENT_GROUP_DOC_TYPE_MAPPING = {
    INFORMATION_LETTER: InformationLetter,
    SERVICE_MEMO: ServiceMemo,
    SERVICE_ORDER: ServiceOrder,
    OFFER_PROJECT: OfferProject,
    TRANSFER_ORDER: TransferOrder,
    DEDUCTION_ORDER: DeductionOrder,
    FORMS: FormsDoc,
}
