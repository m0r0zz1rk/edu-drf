from django.apps import apps

from apps.commons.orm.base_orm import BaseORM

# Модель разделов КУГа
calendar_chart_chapter_model = apps.get_model('edu', 'CalendarChartChapter')

# Класс ORM для работы с разделами КУГа
calendar_chart_chapter_orm = BaseORM(model=calendar_chart_chapter_model, select_related=['program',])
