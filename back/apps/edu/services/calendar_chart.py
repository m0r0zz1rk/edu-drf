import uuid
from typing import Optional

from django.db.models import QuerySet

from apps.authen.services.profile import ProfileService
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.models.calendar_chart.calendar_chart_chapter import CalendarChartChapter
from apps.edu.operations.calendar_chart.add_update_calendar_chart_element import AddUpdateCalendarChartElement
from apps.edu.operations.calendar_chart.delete_calendar_chart_element import DeleteCalendarChartElement
from apps.edu.selectors.calender_chart.calendar_chart_chapter import calendar_chart_chapter_model
from apps.edu.selectors.calender_chart.calendar_chart_theme import calendar_chart_theme_model
from apps.edu.selectors.program import program_model
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class CalendarChartService:
    """Класс методов для работы с КУГ"""

    ju = JournalService()

    @staticmethod
    def is_chapters_exists(program_id: uuid) -> bool:
        """
        Проверка на существующие разделы КУГ для ДПП
        :param program_id: uuid ДПП
        :return: true - разделы существуют, false - разделы не найдены
        """
        return calendar_chart_chapter_model.objects.filter(program_id=program_id).exists()

    def get_chapters_for_program(self, program_id: uuid) -> Optional[QuerySet]:
        """
        Получение списка разделов КУГ для ДПП
        :param program_id: uuid ДПП
        :return: queryset - разделы КУГ для ДПП, None - разделы не найдены
        """
        if self.is_chapters_exists(program_id):
            return CalendarChartChapter.objects.filter(program_id=program_id)
        return None

    @staticmethod
    def get_themes_for_kug_chapter(chapter_id) -> Optional[QuerySet]:
        """
        Получение тема для раздела КУГ ДПП
        :param chapter_id: object_id раздела КУГ
        :return: None - темы не найдены,
        """
        if calendar_chart_chapter_model.objects.filter(object_id=chapter_id).exists():
            return calendar_chart_theme_model.objects.filter(chapter_id=chapter_id)
        return None

    @staticmethod
    def get_program_calendar_chart(program_id: uuid, user_id: int) -> Optional[dict]:
        """
        Получение КУГ для ДПП
        :param program_id: object_id ДПП
        :param user_id: ID пользователя Django
        :return: None - программа не найдена, dict - словарь с данными КУГ
        """
        if program_model.objects.filter(object_id=program_id).exists():
            program = program_model.objects.filter(object_id=program_id).first()
            kug = {
                'on_edit': None
            }
            if program.kug_edit is not None:
                if program.kug_edit.django_user_id == user_id:
                    kug['on_edit'] = 'yourself'
                else:
                    kug['on_edit'] = program.kug_edit.display_name
            chapters = []
            for chapter in (calendar_chart_chapter_model.objects.filter(
                    program_id=program_id
            ).order_by('position')):
                chapter_obj = {}
                for field in calendar_chart_chapter_model._meta.concrete_fields:
                    if field.name not in ['date_create', 'program']:
                        chapter_obj[field.name] = getattr(chapter, field.name)
                chapter_obj['program'] = chapter.program_id
                themes = []
                for theme in (calendar_chart_theme_model.objects.filter(
                        chapter_id=chapter.object_id
                ).order_by('position')):
                    theme_obj = {}
                    for field in calendar_chart_chapter_model._meta.concrete_fields:
                        if field.name not in ['date_create', 'program']:
                            theme_obj[field.name] = getattr(theme, field.name)
                    theme_obj['chapter'] = theme.chapter_id
                    themes.append(theme_obj)
                chapter_obj['themes'] = themes
                chapters.append(chapter_obj)
            kug['chapters'] = chapters
            return kug
        return None

    def update_program_calendar_chart(
        self,
        program_id: uuid,
        user_id: int,
        chart: list
    ) -> bool:
        """
        Обновление КУГ для ДПП
        :param program_id: object_id ДПП
        :param user_id: ID пользователя Django, от которого пришел запрос на обновление
        :param chart: Список разделов КУГ
        :return: true - КУГ успешно обновлен, false - Ошибка при обновлении
        """
        try:
            source = ProfileService().get_profile_or_info_by_attribute(
                'django_user_id',
                user_id,
                'display_name'
            )
            if program_model.objects.filter(object_id=program_id).exists():
                program = program_model.objects.filter(object_id=program_id).first()
                if program.kug_edit is not None:
                    if program.kug_edit.django_user_id != user_id:
                        self.ju.create_journal_rec(
                            {
                                'source': program.kug_edit.display_name,
                                'module': EDU,
                                'status': ERROR,
                                'description': 'Пользователь не может редактировать КУГ '
                                               '(уже на редактировании другим пользователем)'
                            },
                            repr({'program_id': program_id}),
                            None
                        )
                        return False
                exist_chapters = self.get_chapters_for_program(program_id)
                if exist_chapters is not None:
                    for chapter in exist_chapters:
                        DeleteCalendarChartElement({
                            'source': source,
                            'module': EDU,
                            'process_data': {
                                'object_id': chapter.object_id,
                                'program': chapter.program,
                            }
                        })
                for chapter in chart:
                    themes = chapter['themes']
                    del chapter['themes']
                    chapter['program_id'] = chapter['program']
                    del chapter['program']
                    AddUpdateCalendarChartElement({
                        'source': source,
                        'module': EDU,
                        'process_data': chapter
                    })
                    for theme in themes:
                        theme['chapter_id'] = theme['chapter']
                        del theme['chapter']
                        AddUpdateCalendarChartElement({
                            'source': source,
                            'module': EDU,
                            'process_data': theme
                        })
                program.kug_edit = None
                program.save()
                return True
            else:
                self.ju.create_journal_rec(
                    {
                        'source': 'Система',
                        'module': EDU,
                        'status': ERROR,
                        'description': 'ДПП не найдена'
                    },
                    repr({'program_id': program_id}),
                    None
                )
                return False
        except:
            self.ju.create_journal_rec(
                {
                    'source': 'Система',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при обновлении КУГ'
                },
                repr({'program_id': program_id}),
                ExceptionHandling.get_traceback()
            )
            return False
