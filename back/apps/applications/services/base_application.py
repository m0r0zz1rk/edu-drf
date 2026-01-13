import uuid
from typing import Callable, Optional

from django.db.models import Model, QuerySet

from apps.applications.consts.application_statuses import CHECK, WORK, WAIT_PAY, PAY, STUDY, STUDY_COMPLETE
from apps.applications.exceptions.application import ApplicationCreateError
from apps.applications.selectors.course_application import course_application_orm
from apps.applications.selectors.event_application import event_application_orm
from apps.applications.services.course_application import course_application_service
from apps.applications.services.event_application import event_application_service
from apps.applications.services.pay_denied_message import pay_denied_message_service
from apps.authen.services.profile import profile_service
from apps.commons.orm.base_orm import BaseORM
from apps.commons.utils.django.settings import settings_utils
from apps.docs.selectors.student_group_offer import student_group_offer_orm
from apps.edu.exceptions.student_group.student_group_not_found import StudentGroupNotFound
from apps.edu.services.student_group import student_group_service
from apps.guides.selectors.region import irkutsk_state_object


class BaseApplicationService:
    """
    Класс методов для работы с заявками
    """

    _check_edu_fields = [
        'education_doc_id',
        'diploma_surname',
        'surname_doc_id',
        'education_serial',
        'education_number',
        'education_date'
    ]

    _pass_fields = [
        'object_id',
        'old_id',
        'date_create',
        'group',
        'profile',
        'oo_new',
        'coursecertificate',
        'paydeniedmessage'
    ]

    _fk_fields = [
        'region',
        'mo',
        'position_category',
        'position',
        'education_doc',
        'surname_doc'
    ]

    _new_event_app_fields = [
        'work_less',
        'region_id',
        'mo_id',
        'oo_id',
        'oo_new',
        'position_category_id',
        'position_id',
        'physical'
    ]

    _new_course_app_fields = [
        *_new_event_app_fields,
        'certificate_mail',
        'mail_address'
    ]

    def create_app(self, user_id: int, group_id: uuid, application_orm: BaseORM) -> uuid:
        """
        Создание заявки
        :param user_id: ID пользователя Django
        :param group_id: object_id учебной группы
        :param application_orm: Класс ORM для работы с заявками
        :return: object_id созданной заявки
        """
        try:
            profile_id = profile_service.get_profile_or_info_by_attribute(
                'django_user_id',
                user_id,
                'profile_id'
            )
            app = {
                'profile_id': profile_id,
                'group_id': group_id,
                'region': irkutsk_state_object()
            }
            last_app = course_application_service.get_last_app(profile_id)
            if application_orm.model.__name__ == 'EventApplication':
                last_app = event_application_service.get_last_app(profile_id)
            if last_app:
                fields = self._new_course_app_fields
                if application_orm.model.__name__ == 'EventApplication':
                    fields = self._new_event_app_fields
                for field in fields:
                    app[field] = getattr(last_app, field)
            new_app = application_orm.create_record(app)
            return new_app.object_id
        except Exception as e:
            raise ApplicationCreateError

    @staticmethod
    def apps_count() -> int:
        """
        Получение общего количества заявок в АИС
        """
        return (course_application_service.get_total_apps_count() +
                event_application_service.get_total_apps_count())

    @staticmethod
    def get_app_count_for_group(group_id: uuid, course_group: bool) -> int:
        """
        Получение количества заявок для учебной группы
        :param group_id: object_id учебной группы
        :param course_group: группа для ОУ (курса)
        :return: количество заявок
        """
        if course_group:
            return course_application_service.get_group_apps(group_id).count()
        return event_application_service.get_group_apps(group_id).count()

    def get_check_data(self, group_id: uuid) -> dict:
        """
        Получение данных заявок для проверки
        :param group_id: object_id учебной группы
        :return: словарь с ключами:
                 oo - список заявок для проверки ОО,
                 edu - список заявок для проверки документов об образовании,
                 pay - список заявок для проверки документов об оплате
        """
        data = {
            'oo': [],
            'edu': [],
            'pay': []
        }
        is_ou = student_group_service.get_group_service_type(group_id) == 'ou'
        if is_ou:
            applications = course_application_service.get_group_apps(group_id)
        else:
            applications = event_application_service.get_group_apps(group_id)
        for app in applications:
            base_obj = {
                'app_id': app.object_id,
                'student': app.profile.display_name,
            }
            if app.oo_new:
                data.get('oo').append({
                    **base_obj,
                    'mo': app.mo.name if app.mo else '-',
                    'oo_new': app.oo_new
                })
            if app.status == CHECK and app.pay_doc_id is not None:
                data.get('pay').append({
                    **base_obj,
                    'student': app.profile.display_name,
                    'pay_doc_id': app.pay_doc_id
                })
            if is_ou and not app.education_check:
                obj = {**base_obj}
                for field in self._check_edu_fields:
                    if field == 'education_date':
                        obj[field] = getattr(app, field).strftime('%d.%m.%Y') if getattr(app, field) else None
                    else:
                        obj[field] = getattr(app, field)
                data.get('edu').append(obj)
        return data

    def save_app(
            self,
            orm: BaseORM,
            get_app_func: Callable,
            app_id: uuid,
            app_info: dict
    ):
        """
        Сохранение информации по заявке
        :param orm: Класс ORM для работы с типами заявки
        :param get_app_func: функция для получения объекта заявки
        :param app_id: object_id изменяемой заявки
        :param app_info: словарь с информацией по заявке
        """
        app = get_app_func(app_id)
        updated_app = {
            'group_id': app.group_id,
            'profile_id': app.profile_id,
            'old_id': app.old_id
        }
        for field in orm.model._meta.get_fields():
            if field.name in self._pass_fields:
                continue
            if field.name in self._fk_fields:
                updated_app[field.name+'_id'] = app_info.get(
                    f'{field.name}_id',
                    getattr(app, f'{field.name}_id')
                )
            elif field.name == 'oo':
                if 'oo_id' in app_info and 'oo_new' in app_info:
                    if app_info.get('oo_new') != '':
                        updated_app[field.name+'_id'] = None
                        updated_app[field.name+'_new'] = app_info.get('oo_new', getattr(app, 'oo_new'))
                    else:
                        updated_app[field.name+'_id'] = app_info.get('oo_id', getattr(app, 'oo_id'))
                        updated_app[field.name+'_new'] = ''
            else:
                updated_app[field.name] = app_info.get(field.name, getattr(app, field.name))
        if 'in_work' in app_info and app_info['in_work']:
            updated_app['status'] = WORK
        orm.update_record(filter_by={'object_id': app_id}, update_object=updated_app)

    @staticmethod
    def move_application(
            orm: BaseORM,
            apps: list[uuid],
            destination_group_id: uuid
    ):
        """
        Перенос выбранных заявок из одной учебной группы в другую
        :param orm: Класс ORM для работы с заявками
        :param apps: список object_id заявок для переноса
        :param destination_group_id: object_id учебной группы назначения
        :return:
        """
        for app in apps:
            orm.update_record(dict(object_id=app), dict(group_id=destination_group_id))

    @staticmethod
    def move_group_applications(
        orm: BaseORM,
        source_group_id: uuid,
        destination_group_id: uuid
    ):
        """
        Перенос всех заявок учебной группы в другую
        :param orm: Класс ORM для работы с заявками
        :param source_group_id: object_id исходной группы
        :param destination_group_id: object_id группы назначения
        :return:
        """
        orm.update_record(
            dict(group_id=source_group_id),
            dict(group_id=destination_group_id)
        )

    @staticmethod
    def get_recipients_for_offer_pay(group_id: uuid) -> list:
        """
        Получить список получателей писем с офертой в учебной группе
        (только физлица с текущим статусом заявки "В работе")
        :param group_id: object_id учебной группы
        :return: список емэйлов
        """
        group = student_group_service.get_student_group('object_id', group_id)
        orm = event_application_orm
        base_url = f'{settings_utils.get_parameter_from_settings("AIS_ADDRESS")}student/app/'
        prefix = 'event/'
        if group.ou:
            orm = course_application_orm
            prefix = 'course/'
        recipients = []
        for app in orm.get_filter_records(filter_by=dict(group_id=group_id)):
            if app.status == WORK:
                orm.update_record(
                    filter_by=dict(object_id=app.object_id),
                    update_object={'status': WAIT_PAY}
                )
                if app.physical:
                    recipients.append({
                        'email': app.profile.django_user.email,
                        'url': f'{base_url}{prefix}{str(app.object_id)}'
                    })
        return recipients

    @staticmethod
    def get_payment_data(orm: BaseORM, application_id: uuid) -> dict:
        """
        Получение информации об оплате для заявки
        :param orm - класс ORM для работы с соответствующим типом заявки
        :param application_id: object_id заявки
        :return: словарь с данными об оплате
        """
        payment_data = {
            'pay_doc_id': None,
            'offer_id': None,
            'message': None
        }
        app = orm.get_one_record_or_none(filter_by=dict(object_id=application_id))
        if app:
            payment_data['pay_doc_id'] = app.pay_doc_id
            offer = student_group_offer_orm.get_one_record_or_none(filter_by=dict(group_id=app.group_id))
            payment_data['offer_id'] = offer.object_id
            payment_data['message'] = pay_denied_message_service.get_message(application_id)
        return payment_data

    @staticmethod
    def get_study_url(orm: BaseORM, application_id: uuid) -> Optional[dict]:
        """
        Получение ссылки на обучение
        :param orm: класс ORM для работы с заявками
        :param application_id: object_id заявки
        :return: Ссылка или None если статус заявки некорректен
        """
        app = orm.get_one_record_or_none(filter_by=dict(object_id=application_id))
        if app:
            if app.status in [PAY, STUDY, STUDY_COMPLETE]:
                return {'study_url': app.group.event_url}

    @staticmethod
    def get_group_apps(group_id: uuid, orm: BaseORM) -> QuerySet:
        """
        Получение заявок учебной группы
        :param group_id: object_id учебной группы
        :param orm: Класс ORM для работы с заявками
        :return: QuerySet с заявками
        """
        return orm.get_filter_records(filter_by=dict(group_id=group_id))

    @staticmethod
    def update_payment_type(group_id: uuid, payment_type: bool) -> None:
        """
        Смена типа оплаты у заявки
        :param orm: Класс ORM для работы с заявками (на ПК или ИКУ)
        :param group_id: object_id учебной группы, в которой необходимо изменить тип оплаты
        :param payment_type: тип оплаты (True - физ. лицо, False - юр. лицо)
        :return:
        """
        group = student_group_service.get_student_group('object_id', group_id)
        if not group:
            raise StudentGroupNotFound
        orm = course_application_orm if group.ou else event_application_orm
        apps = orm.get_filter_records(filter_by={'group_id': group_id})
        for app in apps:
            orm.update_record(filter_by={'object_id': app.object_id},update_object={'physical': payment_type})

    @staticmethod
    def remove_apps(orm: BaseORM, apps: list[uuid]):
        """
        Удаление заявок
        :param orm: Класс ORM для работы с заявками (course_application_orm или event_application_orm)
        :param apps: список object_id заявок
        :return:
        """
        for app in apps:
            orm.delete_record(filter_by=dict(object_id=app))


base_application_service = BaseApplicationService()
