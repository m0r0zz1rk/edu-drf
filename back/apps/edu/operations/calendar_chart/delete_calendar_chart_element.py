from typing import Union

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.selectors.calender_chart.calendar_chart_chapter import calendar_chart_chapter_model
from apps.edu.selectors.calender_chart.calendar_chart_theme import calendar_chart_theme_model
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS


class DeleteCalendarChartElement(MainProcessing):
    """Удаление элемента КУГ"""
    calendar_chart_required_keys = [
        'object_id',
    ]
    calendar_chart_parent_keys = [
        'program',
        'chapter'
    ]

    @staticmethod
    def _check_element_exist(el_type, object_id) -> bool:
        """
        Проверка на существующий элемент КУГ
        :param el_type: Тип элемента (chapter, theme)
        :param object_id: uuid элемента
        :return: true - элемент существует, false - элемент не найден
        """
        if el_type == 'chapter':
            return calendar_chart_chapter_model.objects.filter(object_id=object_id).exists()
        else:
            return calendar_chart_theme_model.objects.filter(object_id=object_id).exists()

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для удаления элемента КУГ
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
        """Удаление элемента КУГ"""
        try:
            el_type = 'theme'
            if 'program' in self.process_data.keys():
                el_type = 'chapter'
            if self._check_element_exist(el_type, self.process_data['object_id']):
                if el_type == 'chapter':
                    calendar_chart_chapter_model.objects.filter(
                        object_id=self.process_data['object_id']
                    ).first().delete()
                else:
                    calendar_chart_theme_model.objects.filter(
                        object_id=self.process_data['object_id']
                    ).first().delete()
            self.process_completed = True
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Ошибка в процессе удаления элемента КУГ'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном удалении элемента КУГ в журнале"""
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Элемент КУГ успешно удален'
            },
            repr(self.process_data),
            None
        )
