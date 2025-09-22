from sqlalchemy import text

from apps.commons.models import BaseTable
from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.guides.selectors.audience_category import audience_category_model
from apps.guides.selectors.event_type import event_type_model
from apps.guides.selectors.mo import mo_model
from apps.guides.selectors.oo import oo_model
from apps.guides.selectors.oo_type import oo_type_model
from apps.guides.selectors.position import position_model
from apps.guides.selectors.position_category import position_category_model
from apps.guides.selectors.region import region_model
from apps.guides.selectors.state import state_model


class GuidesData:
    """
    Класс методов для получения и сохранения данных приложения
    Справочники из олдовой базы edu
    """

    _oo_simple_fields = [
        'short_name',
        'full_name',
        'form',
    ]

    @staticmethod
    def one_name_process(
            guide_model: BaseTable,
            old_db_table_name: str,
            title: str
    ):
        """
        Процесс получения и сохранения записей для определенной модели справочника
        :param guide_model: модель справочника
        :param old_db_table_name: наименование таблицы в олдовой БД edu
        :param title: наименование сущности (для сообщения в консоли)
        """
        exists = list(guide_model.objects.all())
        with old_edu_connect_engine.connect() as conn:
            sql = f'SELECT * from dbo.{old_db_table_name}'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for rec in data:
            if len(list(filter(lambda ex: ex.name == rec[1], exists))) > 0:
                continue
            _, created = guide_model.objects.update_or_create(
                old_id=rec[0],
                name=rec[1]
            )
            if created:
                print(f'{title} "{rec[1]}" - добавлено')
            else:
                print(f'{title} "{rec[1]}" - обновлено')

    def get_audience_categories(self):
        """
        Получение категорий слушателей
        """
        self.one_name_process(
            audience_category_model,
            'centre_audiencecategories',
            'Категория слушателей'
        )

    def get_event_types(self):
        """
        Получение типов мероприятий
        """
        self.one_name_process(
            event_type_model,
            'centre_eventtypes',
            'Тип мероприятия'
        )

    def get_mos(self):
        """
        Получение муниципальных образований
        """
        self.one_name_process(
            mo_model,
            'centre_mos',
            'Муниципальное образование'
        )

    def get_oo_types(self):
        """
        Получение типов ОО
        """
        self.one_name_process(
            oo_type_model,
            'centre_ootypes',
            'Тип ОО'
        )

    def get_oos(self):
        """
        Получение ОО
        """
        oos = (oo_model.objects.
               select_related('mo').
               select_related('oo_type').
               all())
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_oos'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for oo in data:
            if len(list(filter(lambda rec: rec.old_id == oo[0], oos))) > 0:
                exist = list(filter(lambda rec: rec.old_id == oo[0], oos))[0]
                if exist.short_name == oo[1] and exist.full_name == oo[2] and \
                    exist.form == oo[3]:
                    continue
            new_oo = {
                'old_id': oo[0]
            }
            for i in range(0, len(self._oo_simple_fields)):
                if oo[i+1]:
                    new_oo[self._oo_simple_fields[i]] = oo[i+1]
                else:
                    new_oo[self._oo_simple_fields[i]] = ''
            new_oo['mo_id'] = mo_model.objects.filter(old_id=oo[4]).first().object_id
            new_oo['oo_type_id'] = oo_type_model.objects.filter(old_id=oo[5]).first().object_id
            _, created = oo_model.objects.update_or_create(
                **new_oo
            )
            if created:
                print(f'ОО "{new_oo["full_name"]}" - добавлено')
            else:
                print(f'ОО "{new_oo["full_name"]}" - обновлено')

    def get_positions(self):
        """
        Получение должностей
        """
        self.one_name_process(
            position_model,
            'centre_positions',
            'Должность'
        )

    def get_position_categories(self):
        """
        Получение категорий должностей
        """
        self.one_name_process(
            position_category_model,
            'centre_positioncategories',
            'Категория должностей'
        )

    def get_regions(self):
        """
        Получение регионов РФ
        """
        self.one_name_process(
            region_model,
            'students_regions',
            'Регион'
        )

    def get_states(self):
        """
        Получение государств
        """
        self.one_name_process(
            state_model,
            'authen_states',
            'Государство'
        )
