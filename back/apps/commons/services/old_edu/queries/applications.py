import datetime

from sqlalchemy import text

from apps.applications.consts.application_statuses import WORK, PAY, CHECK, WAIT_PAY, STUDY, STUDY_COMPLETE, ARCHIVE
from apps.applications.consts.education import MIDDLE_PROFESSIONAL, HIGHER, STUDENT, NONE
from apps.applications.selectors.course_application import course_application_model, course_application_orm
from apps.applications.selectors.course_certificate import course_certificate_orm
from apps.applications.selectors.event_application import event_application_model
from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.docs.selectors.pay_doc import pay_doc_model
from apps.docs.selectors.student_doc import student_doc_model
from apps.edu.selectors.student_group import student_group_model
from apps.guides.selectors.mo import mo_model
from apps.guides.selectors.oo import oo_model
from apps.guides.selectors.position import position_model
from apps.guides.selectors.position_category import position_category_model
from apps.guides.selectors.region import region_model
from apps.guides.selectors.profiles.student import student_profile_model


class ApplicationsData:
    """
    Класс методов для получения и сохранения данных приложения
    Заявки из олдовой базы edu
    """

    _groups = (student_group_model.objects.
               select_related('ou').
               select_related('iku').
               select_related('curator').
               all())
    _docs = (student_doc_model.objects.
             select_related('profile').
             all())
    _pay_docs = pay_doc_model.objects.all()
    _profiles = (student_profile_model.objects.
                 select_related('django_user').
                 select_related('state').
                 all())
    _regions = region_model.objects.all()
    _mos = mo_model.objects.all()
    _oos = (oo_model.objects.
            select_related('mo').
            select_related('oo_type').
            all())
    _position_categories = position_category_model.objects.all()
    _positions = position_model.objects.all()

    _app_status_mapping = {
        1: WORK,
        2: WAIT_PAY,
        3: CHECK,
        4: PAY,
        5: STUDY,
        6: STUDY_COMPLETE,
        7: ARCHIVE
    }

    _education_category_mapping = {
        None: NONE,
        1: MIDDLE_PROFESSIONAL,
        2: HIGHER
    }

    _education_level_mapping = {
        1: HIGHER,
        2: MIDDLE_PROFESSIONAL,
        3: STUDENT
    }

    def get_course_applications(self):
        """
        Получение заявок на курсы
        """
        exists = course_application_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = (
                "SELECT app.[id], app.[check_diploma_info], app.[check_survey], app.[certificate_id], app.[group_id],"
                "app.[pay_doc_id], prof.[user_id], app.[status_id], form.[workless], form.[region_id], form.[mo_id], "
                "form.[oo_id], form.[oo_new], form.[position_cat_id], form.[position_id], form.[type] as 'physical', "
                "form.[edu_level_id], form.[edu_cat_id], form.[edu_doc_id], form.[check_surname], "
                "form.[change_surname_id], form.[edu_serial], form.[edu_number], form.[edu_date], form.[cert_mail], "
                "form.[address] from [edu-new].[dbo].[students_apps] as app inner join "
                "[edu-new].[dbo].[students_coursesforms] as form on app.[profile_id] = form.[profile_id] and "
                "app.[group_id] = form.[group_id] inner join [edu-new].[dbo].authen_profiles as prof on "
                "app.[profile_id] = prof.[id]")
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for app in data:
            if not app[3]:
                cert_id = None
            else:
                try:
                    cert_id = list(filter(lambda doc: doc.old_id == app[3], self._docs))[0].object_id
                except Exception:
                    print(f'certificate - {app[3]}')
                    continue
            try:
                group = list(filter(lambda gr: gr.old_id == app[4], self._groups))[0]
            except Exception:
                print(f'group - {app[4]}')
                continue
            if not app[5]:
                pay_doc_id = None
            else:
                try:
                    pay_doc_id = list(filter(lambda doc: doc.old_id == app[5], self._pay_docs))[0].object_id
                except Exception:
                    print(f'pay_doc - {app[5]}')
                    continue
            try:
                profile = list(filter(lambda prof: prof.old_id == app[6], self._profiles))[0]
            except Exception:
                print(f'profile - {app[6]}')
                continue
            try:
                region_id = list(filter(lambda reg: reg.old_id == app[9], self._regions))[0].object_id
            except Exception:
                print(f'region - {app[9]}')
                continue
            if not app[10]:
                mo_id = None
            else:
                try:
                    mo_id = list(filter(lambda m: m.old_id == app[10], self._mos))[0].object_id
                except Exception:
                    print(f'mo - {app[10]}')
                    continue
            if not app[11]:
                oo_id = None
            else:
                try:
                    oo_id = list(filter(lambda o: o.old_id == app[11], self._oos))[0].object_id
                except Exception:
                    print(f'oo - {app[11]}')
                    continue
            if not app[13]:
                pos_cat_id = None
            else:
                try:
                    pos_cat_id = list(
                        filter(lambda pos_cat: pos_cat.old_id == app[13], self._position_categories)
                    )[0].object_id
                except Exception:
                    print(f'pos_cat_id - {app[13]}')
                    continue
            if not app[14]:
                pos_id = None
            else:
                try:
                    pos_id = list(
                        filter(lambda pos: pos.old_id == app[14], self._positions)
                    )[0].object_id
                except Exception:
                    print(f'pos_id - {app[14]}')
                    continue
            if not app[18]:
                edu_doc_id = None
            else:
                try:
                    edu_doc_id = list(filter(lambda doc: doc.old_id == app[18], self._docs))[0].object_id
                except Exception:
                    print(f'edu_doc_id - {app[18]}')
                    continue
            if not app[20]:
                surname_doc_id = None
            else:
                try:
                    surname_doc_id = list(filter(lambda doc: doc.old_id == app[20], self._docs))[0].object_id
                except Exception:
                    print(f'surname_doc_id - {app[20]}')
                    continue
            if not app[23]:
                edu_date = datetime.date.today()
            else:
                edu_date = app[23]
            if len(list(filter(lambda course_app: course_app.old_id == app[0], exists))) > 0:
                exist = list(filter(lambda course_app: course_app.old_id == app[0], exists))[0]
                if exist.updated_from_new:
                    continue
                oo_n = app[12] if app[12] else ''
                if exist.profile_id == profile.object_id and \
                        exist.group_id == group.object_id and \
                        exist.status == self._app_status_mapping[app[7]] and \
                        exist.pay_doc_id == pay_doc_id and \
                        exist.check_survey == app[2] and \
                        exist.work_less == app[8] and \
                        exist.region_id == region_id and \
                        exist.mo_id == mo_id and \
                        exist.oo_id == oo_id and \
                        exist.oo_new == oo_n and \
                        exist.position_category_id == pos_cat_id and \
                        exist.position_id == pos_id and \
                        exist.physical == app[15] and \
                        exist.education_level == self._education_level_mapping[app[16]] and \
                        exist.education_category == self._education_category_mapping[app[17]] and \
                        exist.education_doc_id == edu_doc_id and \
                        exist.education_check == app[1] and \
                        exist.diploma_surname == app[19] and \
                        exist.surname_doc_id == surname_doc_id and \
                        exist.education_serial == app[21] and \
                        exist.education_number == app[22] and \
                        exist.education_date == edu_date and \
                        exist.certificate_doc_id == cert_id and \
                        exist.certificate_mail == app[24] and \
                        exist.mail_address == app[25]:
                    continue
            new_course_app = {
                'old_id': app[0],
                'profile_id': profile.object_id,
                'group_id': group.object_id,
                'status': self._app_status_mapping[app[7]],
                'pay_doc_id': pay_doc_id,
                'check_survey': app[2],
                'work_less': app[8],
                'region_id': region_id,
                'mo_id': mo_id,
                'oo_id': oo_id,
                'oo_new': app[12] if app[12] else '',
                'position_category_id': pos_cat_id,
                'position_id': pos_id,
                'physical': app[15],
                'education_level': self._education_level_mapping[app[16]],
                'education_category': self._education_category_mapping[app[17]],
                'education_doc_id': edu_doc_id,
                'education_check': app[1],
                'diploma_surname': app[19],
                'surname_doc_id': surname_doc_id,
                'education_serial': app[21],
                'education_number': app[22],
                'education_date': edu_date,
                'certificate_doc_id': cert_id,
                'certificate_mail': app[24],
                'mail_address': app[25]
            }
            _, created = course_application_model.objects.update_or_create(
                old_id=app[0],
                defaults=new_course_app
            )
            action = 'добавлено' if created else 'обновлено'
            print(f'Заявка обучающегося "{profile.display_name}" в группу {group.code} - {action}')

    def get_event_applications(self):
        """
        Получение заявок на мероприятия
        """
        exists = event_application_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = ("select app.[id], prof.[user_id], app.[group_id], app.[status_id], app.[pay_doc_id], "
                   "app.[check_survey], form.[workless], form.[region_id], form.[mo_id], form.[oo_id], "
                   "form.[oo_new], form.[position_cat_id], form.[position_id], form.[type] from "
                   "[edu-new].[dbo].[students_apps] as app inner join [edu-new].[dbo].[authen_profiles] as prof "
                   "on app.[profile_id] = prof.[id] inner join [edu-new].[dbo].[students_eventsforms] as form "
                   "on app.[group_id] = form.[group_id] and app.[profile_id] = form.[profile_id]")
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for app in data:
            if len(list(filter(lambda event_app: event_app.old_id == app[0], exists))) > 0:
                continue
            try:
                profile = list(filter(lambda prof: prof.old_id == app[1], self._profiles))[0]
            except Exception:
                print(f'profile - {app[1]}')
                continue
            try:
                group = list(filter(lambda gr: gr.old_id == app[2], self._groups))[0]
            except Exception:
                print(f'group - {app[2]}')
                continue
            if not app[4]:
                pay_doc_id = None
            else:
                try:
                    pay_doc_id = list(filter(lambda doc: doc.old_id == app[4], self._pay_docs))[0].object_id
                except Exception:
                    print(f'pay_doc - {app[4]}')
                    continue
            try:
                region_id = list(filter(lambda reg: reg.old_id == app[7], self._regions))[0].object_id
            except Exception:
                print(f'region - {app[7]}')
                continue
            if not app[8]:
                mo_id = None
            else:
                try:
                    mo_id = list(filter(lambda m: m.old_id == app[8], self._mos))[0].object_id
                except Exception:
                    print(f'mo - {app[8]}')
                    continue
            if not app[9]:
                oo_id = None
            else:
                try:
                    oo_id = list(filter(lambda o: o.old_id == app[9], self._oos))[0].object_id
                except Exception:
                    print(f'oo - {app[9]}')
                    continue
            if not app[11]:
                pos_cat_id = None
            else:
                try:
                    pos_cat_id = list(
                        filter(lambda pos_cat: pos_cat.old_id == app[11], self._position_categories)
                    )[0].object_id
                except Exception:
                    print(f'pos_cat_id - {app[11]}')
                    continue
            if not app[12]:
                pos_id = None
            else:
                try:
                    pos_id = list(
                        filter(lambda pos: pos.old_id == app[12], self._positions)
                    )[0].object_id
                except Exception:
                    print(f'pos_id - {app[12]}')
                    continue
            oo_n = app[10] if app[10] else ''
            if len(list(filter(lambda event_app: event_app.old_id == app[0], exists))) > 0:
                exist = list(filter(lambda event_app: event_app.old_id == app[0], exists))[0]
                if exist.updated_from_new:
                    continue
                if exist.profile_id == profile.object_id and \
                        exist.group_id == group.object_id and \
                        exist.status == self._app_status_mapping[app[3]] and \
                        exist.pay_doc_id == pay_doc_id and \
                        exist.check_survey == app[5] and \
                        exist.work_less == app[6] and \
                        exist.region_id == region_id and \
                        exist.mo_id == mo_id and \
                        exist.oo_id == oo_id and \
                        exist.oo_new == oo_n and \
                        exist.position_category_id == pos_cat_id and \
                        exist.position_id == pos_id and \
                        exist.physical == app[13]:
                    continue
            new_course_app = {
                'old_id': app[0],
                'profile_id': profile.object_id,
                'group_id': group.object_id,
                'status': self._app_status_mapping[app[3]],
                'pay_doc_id': pay_doc_id,
                'check_survey': app[5],
                'work_less': app[6],
                'region_id': region_id,
                'mo_id': mo_id,
                'oo_id': oo_id,
                'oo_new': oo_n,
                'position_category_id': pos_cat_id,
                'position_id': pos_id,
                'physical': app[13]
            }
            _, created = event_application_model.objects.update_or_create(
                old_id=app[0],
                defaults=new_course_app
            )
            action = 'добавлено' if created else 'обновлено'
            print(f'Заявка обучающегося "{profile.display_name}" в группу {group.code} - {action}')

    @staticmethod
    def get_course_certificates():
        """
        Получение сертификатов обучающихся из олдовой базы EDU
        :return:
        """
        _course_applications = course_application_orm.get_filter_records()
        _certificates = course_certificate_orm.get_filter_records()
        with old_edu_connect_engine.connect() as conn:
            sql = ("SELECT [cert].[id] "
                   ",[cert].[reg_number]"
                   ",[cert].[blank_serial]"
                   ",[cert].[blank_number]"
                   ",[cert].[group_id]"
                   ",[student].[user_id] "
                   "FROM [edu-new].[dbo].[centre_studentscerts] as cert "
                   "inner join [edu-new].[dbo].[authen_profiles] as student "
                   "on cert.[student_id] = student.[id]")
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for certificate in data:
            try:
                application = list(
                    filter(
                        lambda app: (app.profile.old_id, app.group.old_id) == (certificate[5], certificate[4]),
                        _course_applications
                    )
                )[0]
            except Exception:
                continue
            new_course_certificate = {
                'old_id': certificate[0],
                'application_id': application.object_id,
                'registration_number': certificate[1],
                'blank_serial': certificate[2],
                'blank_number': certificate[3]
            }
            if len(list(filter(lambda cert: cert.old_id == certificate[0], _certificates))) > 0:
                exist = list(filter(lambda cert: cert.old_id == certificate[0], _certificates))[0]
                if exist.updated_from_new:
                    continue
                if (exist.registration_number, exist.blank_serial, exist.blank_number) == \
                        (certificate[1], certificate[2], certificate[3]):
                    continue
                else:
                    print('Обновлен сертификат: ', repr(new_course_certificate))
                    course_certificate_orm.update_record(
                        filter_by={'old_id': certificate[0]},
                        update_object=new_course_certificate
                    )
            else:
                course_certificate_orm.create_record(new_course_certificate)
                print('Добавлен сертификат: ', repr(new_course_certificate))
