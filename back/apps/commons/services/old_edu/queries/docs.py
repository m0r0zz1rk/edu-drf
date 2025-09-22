import os
from pathlib import Path
from sqlalchemy import text

from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.docs.consts.student_doc_types import DIPLOMA, CHANGE_SURNAME, TRAINING_CERTIFICATE, LICENSE_SCAN
from apps.commons.utils.django.settings import SettingsUtils
from apps.docs.selectors.pay_doc import pay_doc_model
from apps.docs.selectors.program_order import program_order_model
from apps.docs.selectors.student_doc import student_doc_model
from apps.docs.selectors.student_group_offer import student_group_offer_model
from apps.edu.selectors.student_group import student_group_model
from apps.guides.selectors.profiles.student import student_profile_model

settings_utils = SettingsUtils()

# Маппинг наименований типов документов обучающихся
_student_doc_types_mapper = {
        1: {
            'key': DIPLOMA,
            'title': 'Диплом'
        },
        2: {
            'key': CHANGE_SURNAME,
            'title': 'Документ о смене фамилии'
        },
        3: {
            'key': TRAINING_CERTIFICATE,
            'title': 'Справка об обучении'
        },
        6: {
            'key': LICENSE_SCAN,
            'title': 'Скан удостоверения'
        }
    }


class DocsData:
    """
    Класс методов для получения и сохранения данных приложения
    Документы из олдовой базы edu
    """

    @staticmethod
    def get_program_orders():
        """
        Получение приказов ДПП
        """
        exists = program_order_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_programs'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for order in data:
            if len(list(filter(lambda ord: ord.old_id == order[0], exists))) > 0:
                exist = list(filter(lambda ord: ord.old_id == order[0], exists))[0]
                if exist.date == order[8] and exist.number == order[7]:
                    continue
            file = open(
                os.path.join(settings_utils.get_parameter_from_settings('MEDIA_ROOT_OLD'), Path(order[9])),
                'rb',
            )
            new_order = {
                'old_id': order[0],
                'number': order[7],
                'date': order[8],
            }
            order_object, created = program_order_model.objects.update_or_create(
                old_id=order[0],
                defaults=new_order
            )
            order_object.file.save(
                f"dpp_order.{order[9][-3:]}",
                file
            )
            action = 'Добавлено' if created else 'Обновлено'
            print(f'Приказ ДПП №{new_order["number"]} от {new_order["date"].strftime("%d.%m.%Y")} '
                  f'- {action}')
            del file

    @staticmethod
    def get_student_docs():
        """
        Получение пользовательских документов
        """
        exists = (student_doc_model.objects.
                  select_related('profile').
                  all())
        profiles = (student_profile_model.objects.
                    select_related('django_user').
                    select_related('state').
                    all())
        with old_edu_connect_engine.connect() as conn:
            sql = ('select sd.id, sd.[file], sd.doc_type_id, sd.profile_id, p.user_id, '
                   'p.surname, p.name, p.patronymic '
                   'from dbo.students_docs as sd inner join dbo.authen_profiles as p on sd.profile_id = p.id '
                   'where sd.doc_type_id in (1, 2, 3, 6)')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for user_doc in data:
            if len(list(filter(lambda doc: doc.old_id == user_doc[0], exists))) > 0:
                continue
            try:
                file = open(
                    os.path.join(settings_utils.get_parameter_from_settings('MEDIA_ROOT_OLD'), Path(user_doc[1])),
                    'rb',
                )
            except Exception:
                continue
            try:
                profile_id = list(filter(lambda prof: prof.django_user_id == user_doc[4], profiles))[0].object_id
            except Exception:
                continue
            new_doc = {
                'old_id': user_doc[0],
                'doc_type': _student_doc_types_mapper[user_doc[2]]['key'],
                'profile_id': profile_id,
            }
            doc_object, _ = student_doc_model.objects.update_or_create(
                **new_doc
            )
            path_split = user_doc[1].split('/')
            doc_object.file.save(
                f"{path_split[-1:][0][:-5] if path_split[-1:][0].endswith('jpeg') else path_split[-1:][0][:-4]}"
                f".{user_doc[1][-3:]}",
                file
            )
            print(f'{_student_doc_types_mapper[user_doc[2]]["title"]} '
                  f'пользователя {user_doc[5]} {user_doc[6]} {user_doc[7]} '
                  f'- добавлено')
            del file

    @staticmethod
    def get_pay_docs():
        """
        Получение документов об оплате
        """
        exists = pay_doc_model.objects.all()
        profiles = (student_profile_model.objects.
                    select_related('django_user').
                    select_related('state').
                    all())
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT stdoc.[id], stdoc.[file], prof.[user_id] '
                   'from dbo.students_docs as stdoc inner join dbo.authen_profiles as prof on '
                   'stdoc.[profile_id] = prof.[id] '
                   'where stdoc.[doc_type_id] = 5')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for pay_doc in data:
            if len(list(filter(lambda pay: pay.old_id == pay_doc[0], exists))) > 0:
                continue
            try:
                profile = list(filter(lambda prof: prof.old_id == pay_doc[2], profiles))[0]
            except Exception:
                continue
            try:
                file = open(
                    os.path.join(settings_utils.get_parameter_from_settings('MEDIA_ROOT_OLD'), Path(pay_doc[1])),
                    'rb',
                )
            except Exception:
                continue
            new_pay_doc = {
                'old_id': pay_doc[0],
                'profile_id': profile.object_id,
            }
            print(new_pay_doc)
            pay_doc_object, _ = pay_doc_model.objects.update_or_create(
                **new_pay_doc
            )
            path_split = pay_doc[1].split('/')
            pay_doc_object.file.save(
                (f"{path_split[-1:][0][:-5] if path_split[-1:][0].endswith('jpeg') else path_split[-1:][0][:-4]}"
                f".{pay_doc[1][-3:]}"),
                file
            )
            print(f'Документ об оплате обучающегося "{profile.display_name}" '
                  f'- добавлено')
            del file

    @staticmethod
    def get_offers():
        """
        Получение договоров оферт
        """
        exists = (student_group_offer_model.objects.
                  select_related('group').
                  all())
        groups = (student_group_model.objects.
                  select_related('ou').
                  select_related('iku').
                  select_related('curator').
                  all())
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT [id], [offer] from dbo.centre_studentgroups'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for offer in data:
            if len(list(filter(lambda of: of.old_id == offer[0], exists))) > 0:
                continue
            try:
                group = list(filter(lambda gr: gr.old_id == offer[0], groups))[0]
            except Exception:
                print(f'group - {offer[0]}')
                continue
            try:
                file = open(
                    os.path.join(settings_utils.get_parameter_from_settings('MEDIA_ROOT_OLD'), Path(offer[1])),
                    'rb',
                )
            except Exception:
                print(f'file - {offer[1]}')
                continue
            new_offer = {
                'old_id': offer[0],
                'group_id': group.object_id,
                'file': offer[1],
            }
            offer_object, _ = student_group_offer_model.objects.update_or_create(
                **new_offer
            )
            offer_object.file.save(
                f"dpp_order.{offer[1][-3:]}",
                file
            )
            print(f'Договор оферта для группы {group.object_id} - добавлено')
            del file


