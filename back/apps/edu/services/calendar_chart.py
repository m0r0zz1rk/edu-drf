import uuid
from typing import Optional

from django.db.models import QuerySet

from apps.authen.services.profile import ProfileService
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.exceptions.calendar_chart.get_kug_remains_error import GetKugRemainsError
from apps.edu.exceptions.calendar_chart.incorrect_theme_dict_format import IncorrectThemeDictFormat
from apps.edu.exceptions.calendar_chart.kug_not_found import KugNotFound
from apps.edu.exceptions.service.program_not_set import EducationServiceProgramNotSet
from apps.edu.exceptions.student_group.student_group_incorrect_service import StudentGroupIncorrectService
from apps.edu.exceptions.student_group.student_group_not_found import StudentGroupNotFound
from apps.edu.operations.calendar_chart.add_update_calendar_chart_element import AddUpdateCalendarChartElement
from apps.edu.operations.calendar_chart.delete_calendar_chart_element import DeleteCalendarChartElement
from apps.edu.selectors.calender_chart.calendar_chart_chapter import calendar_chart_chapter_model
from apps.edu.selectors.calender_chart.calendar_chart_theme import calendar_chart_theme_model
from apps.edu.services.program import ProgramService
from apps.edu.services.schedule import ScheduleService
from apps.edu.services.student_group import StudentGroupService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class CalendarChartService:
    """Класс методов для работы с КУГ"""

    ju = JournalService()
    __student_group_service = StudentGroupService()
    __program_service = ProgramService()

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
            return (calendar_chart_chapter_model.objects.
                    select_related('program').
                    filter(program_id=program_id))
        return None

    @staticmethod
    def get_themes_for_kug_chapter(chapter_id) -> Optional[QuerySet]:
        """
        Получение тема для раздела КУГ ДПП
        :param chapter_id: object_id раздела КУГ
        :return: None - темы не найдены,
        """
        if calendar_chart_chapter_model.objects.filter(object_id=chapter_id).exists():
            return calendar_chart_theme_model.objects.select_related('chapter').filter(chapter_id=chapter_id)
        return None

    def get_program_calendar_chart(self, program_id: uuid, user_id: int) -> Optional[dict]:
        """
        Получение КУГ для ДПП
        :param program_id: object_id ДПП
        :param user_id: ID пользователя Django
        :return: None - программа не найдена, dict - словарь с данными КУГ
        """
        program = self.__program_service.get_program(
            'object_id',
            program_id
        )
        if program is None:
            return None
        kug = {
            'on_edit': None
        }
        if program.kug_edit is not None:
            if program.kug_edit.django_user_id == user_id:
                kug['on_edit'] = 'yourself'
            else:
                kug['on_edit'] = program.kug_edit.display_name
        chapters = []
        for chapter in (calendar_chart_chapter_model.objects.select_related('program').filter(
                program_id=program_id
        ).order_by('position')):
            chapter_obj = {}
            for field in calendar_chart_chapter_model._meta.concrete_fields:
                if field.name not in ['date_create', 'program']:
                    chapter_obj[field.name] = getattr(chapter, field.name)
            chapter_obj['program'] = chapter.program_id
            themes = []
            for theme in (calendar_chart_theme_model.objects.select_related('chapter').filter(
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

    def copy_calendar_chart(self, curr_program_id: uuid, new_program_id: uuid):
        """
        Копирование КУГ ДПП
        :param curr_program_id: object_id существующей ДПП
        :param new_program_id: object_id новой ДПП
        :return: True - КУГ успешно скоирован, False - произошла системная ошибка
        """
        kug_chapters = self.get_chapters_for_program(curr_program_id)
        if kug_chapters:
            keys = AddUpdateCalendarChartElement.calendar_chart_required_keys
            for chapter in kug_chapters:
                new_chapter_id = uuid.uuid4()
                new_chapter = {
                    'object_id': new_chapter_id
                }
                for key in keys:
                    if key != 'object_id':
                        new_chapter[key] = getattr(chapter, key)
                new_chapter['program_id'] = new_program_id
                AddUpdateCalendarChartElement({
                    'source': 'Процесс создания копии ДПП',
                    'module': EDU,
                    'process_data': new_chapter
                })
                chapter_themes = self.get_themes_for_kug_chapter(chapter.object_id)
                for theme in chapter_themes:
                    new_theme = {}
                    for key in keys:
                        if key == 'object_id':
                            new_theme[key] = uuid.uuid4()
                        else:
                            new_theme[key] = getattr(theme, key)
                    new_theme['chapter_id'] = new_chapter_id
                    AddUpdateCalendarChartElement({
                        'source': 'Процесс создания копии ДПП',
                        'module': EDU,
                        'process_data': new_theme
                    })
        return True

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
            program = self.__program_service.get_program(
                'object_id',
                program_id
            )
            if program is None:
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
        except Exception:
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

    def get_kug_remains_for_schedule(self, group_id: uuid) -> list:
        """
        Получение возможных часов КУГ для изменения расписания занятий учебной группы
        :param group_id: object_id учебной группы
        :return: словарь с остаточными данными по часам КУГ
        """
        kug_remains = []
        group = self.__student_group_service.get_student_group(
            'object_id',
            group_id
        )
        if group is None:
            raise StudentGroupNotFound
        if group.ou is None:
            raise StudentGroupIncorrectService
        if group.ou.program is None:
            raise EducationServiceProgramNotSet
        if not self.is_chapters_exists(group.ou.program_id):
            raise KugNotFound
        kug = self.get_program_calendar_chart(group.ou.program_id, 0)
        ss = ScheduleService(group_id)
        hour_types = ('lecture', 'practice', 'trainee', 'individual')
        for number, chapter in enumerate(kug['chapters'], start=1):
            chapter_info = {
                'chapter': f'Раздел {number}. {chapter["name"]}'
            }
            themes = []
            for theme in chapter['themes']:
                theme_info = {
                    'chapter': chapter['name'],
                    'theme': theme['name'],
                    'theme_id': theme['object_id']
                }
                for ht in hour_types:
                    theme_info[ht] = theme[ht + '_hours']
                try:
                    theme_info = ss.get_remain_hours_for_kug_theme(theme_info)
                except IncorrectThemeDictFormat:
                    raise GetKugRemainsError
                themes.append(theme_info)
            chapter_info['themes'] = themes
            kug_remains.append(chapter_info)
        return kug_remains


calendar_chart_service = CalendarChartService()
