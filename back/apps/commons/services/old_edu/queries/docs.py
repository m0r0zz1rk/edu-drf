from sqlalchemy import text

from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.docs.selectors.program_order import program_order_model


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
                continue
            new_order = {
                'old_id': order[0],
                'number': order[7],
                'date': order[8],
                'file': order[9]
            }
            print(new_order)
            # program_order_model.objects.update_or_create(
            #     **new_order
            # )
            # print(f'Приказ ДПП №{new_order.number} от {new_order.date.strftime("%d.%m.%Y")} '
            #       f'- добавлено')
