from typing import Union

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.selectors.calender_chart.calendar_chart_chapter import calendar_chart_chapter_orm
from apps.edu.selectors.calender_chart.calendar_chart_theme import calendar_chart_theme_orm
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import journal_service


class AddUpdateCalendarChartElement(MainProcessing):
    """Добавление/обновление элемента КУГ"""
    calendar_chart_required_keys = [
        'object_id',
        'position',
        'name',
        'total_hours',
        'lecture_hours',
        'practice_hours',
        'trainee_hours',
        'individual_hours',
        'control_form'
    ]
    calendar_chart_parent_keys = [
        'program_id',
        'chapter_id'
    ]

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для добавления/обновления элемента КУГ
        :return: true - данные валидны, false - данные не валидны, str - traceback
        """
        try:
            for key in self.calendar_chart_required_keys:
                if key not in self.process_data.keys():
                    return False
            check_parent = False
            for parent_key in self.calendar_chart_parent_keys:
                if parent_key in self.process_data.keys():
                    check_parent = True
            if not check_parent:
                return False
            return True
        except Exception:
            return ExceptionHandling.get_traceback()

    def _main_process(self):
        """Добавление/обновление элемента КУГ"""
        try:
            el_type = 'theme'
            if 'program_id' in self.process_data.keys():
                el_type = 'chapter'
            object_id = self.process_data['object_id']
            del self.process_data['object_id']
            orm = calendar_chart_theme_orm
            if el_type == 'chapter':
                orm = calendar_chart_chapter_orm
            orm.update_record(
                filter_by={'object_id': object_id},
                update_object=self.process_data
            )
            self.process_completed = True
        except Exception:
            journal_service.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Ошибка в процессе добавлении/удалении элемента КУГ'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном добавлении/обновлении элемента КУГ в журнале"""
        journal_service.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Элемент КУГ успешно добавлен/обновлен'
            },
            repr(self.process_data),
            None
        )
