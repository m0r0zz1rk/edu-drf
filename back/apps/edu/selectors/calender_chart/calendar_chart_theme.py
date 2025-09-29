from django.apps import apps

from apps.commons.orm.base_orm import BaseORM

# Модель тем раздела КУГ
calendar_chart_theme_model = apps.get_model('edu', 'CalendarChartTheme')

# Класс ORM для тем раздела КУГ
calendar_chart_theme_orm = BaseORM(
    model=calendar_chart_theme_model,
    select_related=['chapter', ]
)
