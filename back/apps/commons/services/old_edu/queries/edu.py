import datetime

from sqlalchemy import text

from apps.commons.serializers.ad_centre import ad_centre_model
from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.commons.utils.data_types.date import DateUtils
from apps.docs.selectors.program_order import program_order_model
from apps.edu.consts.lesson_types import LECTURE, PRACTICE, TRAINEE, INDIVIDUAL
from apps.edu.consts.student_group.statuses import REGISTRATION, STATEMENT, OFFER, URL, PROCESS, COMPLETE
from apps.edu.selectors.calender_chart.calendar_chart_chapter import calendar_chart_chapter_model
from apps.edu.selectors.calender_chart.calendar_chart_theme import calendar_chart_theme_model
from apps.edu.selectors.program import program_model
from apps.edu.selectors.schedule import schedule_model
from apps.edu.selectors.services.education_service import education_service_model
from apps.edu.selectors.services.information_service import information_service_model
from apps.edu.selectors.student_group import student_group_model, student_group_orm
from apps.guides.selectors.audience_category import audience_category_model
from apps.guides.selectors.profiles.coko import coko_profile_model
from apps.guides.selectors.event_type import event_type_model
from apps.guides.selectors.profiles.student import student_profile_model


class EduData:
    """
    Класс методов для получения и сохранения данных приложения
    Учебная часть из олдовой базы edu
    """
    _date_utils = DateUtils()
    _department_qs = ad_centre_model.objects.all()

    _group_status_mapping = {
        1: REGISTRATION,
        2: STATEMENT,
        3: OFFER,
        4: URL,
        5: PROCESS,
        6: COMPLETE
    }

    def get_information_services(self):
        """
        Получение ИКУ
        """
        exists = information_service_model.objects.all()
        event_types = event_type_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_events'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for iku in data:
            if len(list(filter(lambda service: service.old_id == iku[0], exists))) > 0:
                continue
            new_iku = {
                'old_id': iku[0],
                'location': iku[4],
                'date_start': iku[5],
                'date_end': iku[6],
                'name': iku[2],
                'duration': iku[3],
                'price': iku[7]
            }
            if len(list(filter(lambda dep: dep.display_name == iku[1], self._department_qs))) != 0:
                new_iku['department_id'] = list(
                    filter(lambda dep: dep.display_name == iku[1], self._department_qs)
                )[0].object_id
            else:
                new_iku['department_id'] = None
            if len(list(filter(lambda ev_type: ev_type.old_id == iku[8], event_types))) != 0:
                new_iku['type_id'] = list(
                    filter(lambda ev_type: ev_type.old_id == iku[8], event_types)
                )[0].object_id
            else:
                new_iku['type_id'] = None
            information_service_model.objects.update_or_create(
                **new_iku
            )
            print(f'Мероприятие "{new_iku["name"]}" - добавлено')

    @staticmethod
    def get_info_service_categories():
        """
        Получение категорий слушателей для мероприятий
        """
        exists = information_service_model.objects.all()
        audience_categories = audience_category_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_events_categories'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for ev_cat in data:
            if len(list(filter(lambda ev: ev.old_id == ev_cat[1], exists))) == 0:
                continue
            event = list(filter(lambda ev: ev.old_id == ev_cat[1], exists))[0]
            try:
                aud_cat_id = list(filter(lambda cat: cat.old_id == ev_cat[2], audience_categories))[0].object_id
            except Exception:
                continue
            if event.categories.filter(object_id=aud_cat_id).exists():
                continue
            aud_cat = audience_category_model.objects.get(object_id=aud_cat_id)
            event.categories.add(aud_cat)
            print(f'Категория "{aud_cat.name}" к мероприятию "{event.name}" - добавлено')

    def get_programs(self):
        """
        Получение ДПП
        """
        exists = (program_model.objects.
                  select_related('department').
                  select_related('kug_edit').
                  prefetch_related('categories').
                  select_related('program_order').
                  all())
        program_orders = program_order_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_programs'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for program in data:
            if len(list(filter(lambda pr: pr.old_id == program[0], exists))) > 0:
                continue
            new_program = {
                'old_id': program[0],
                'name': program[2],
                'type': program[3],
                'duration': program[4],
                'annotation': program[6],
                'price': program[10],
                'kug_edit_id': None
            }
            if len(list(filter(lambda dep: dep.display_name == program[1], self._department_qs))) != 0:
                new_program['department_id'] = list(
                    filter(lambda dep: dep.display_name == program[1], self._department_qs)
                )[0].object_id
            else:
                new_program['department_id'] = None
            if len(list(filter(lambda order: order.old_id == program[0], program_orders))) != 0:
                new_program['program_order_id'] = list(
                    filter(lambda order: order.old_id == program[0], program_orders)
                )[0].object_id
            else:
                new_program['program_order_id'] = None
            program_model.objects.update_or_create(
                **new_program
            )
            print(f'ДПП "{new_program["name"]}" - добавлено')

    def get_program_calendar_chapters(self):
        """
        Получение разделов КУГ-ов ДПП
        """
        exists = calendar_chart_chapter_model.objects.select_related('program').all()
        programs = (program_model.objects.
                    select_related('department').
                    select_related('kug_edit').
                    prefetch_related('categories').
                    select_related('program_order').
                    all())
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_stschedule where parent_id is NULL'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for chapter in data:
            if len(list(filter(lambda ch: ch.old_id == chapter[0], exists))) > 0:
                continue
            try:
                program = list(filter(lambda pr: pr.old_id == chapter[13], programs))[0]
            except Exception:
                continue
            try:
                position = int(chapter[1][7])
            except ValueError:
                position = 15
            new_chapter = {
                'old_id': chapter[0],
                'position': position,
                'name': chapter[1][10:].strip(),
                'total_hours': chapter[2],
                'lecture_hours': chapter[3],
                'practice_hours': chapter[4],
                'trainee_hours': chapter[5],
                'individual_hours': chapter[6],
                'control_form': chapter[7],
                'program_id': program.object_id
            }
            calendar_chart_chapter_model.objects.update_or_create(
                **new_chapter
            )
            print(f'Раздел КУГ "{new_chapter["name"]}" ДПП "{program.name}" - добавлено')

    def get_program_calendar_themes(self):
        """
        Получение тем разделов КУГ-ов ДПП
        """
        exists = calendar_chart_theme_model.objects.select_related('chapter').all()
        chapters = calendar_chart_chapter_model.objects.select_related('program').all()
        programs = (program_model.objects.
                    select_related('department').
                    select_related('kug_edit').
                    prefetch_related('categories').
                    select_related('program_order').
                    all())
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_stschedule where parent_id is not NULL'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        print('themes data: ', data)
        for theme in data:
            if len(list(filter(lambda th: th.old_id == theme[0], exists))) > 0:
                continue
            try:
                chapter = list(filter(lambda ch: ch.old_id == theme[12], chapters))[0]
            except Exception:
                continue
            try:
                program = list(filter(lambda pr: pr.old_id == theme[13], programs))[0]
            except Exception:
                continue
            first_dot_index = theme[1].find('.')
            second_dot_index = theme[1].find('.', first_dot_index+1)
            new_theme = {
                'old_id': theme[0],
                'position': int(theme[1][first_dot_index+1]),
                'name': theme[1][second_dot_index+1:].strip(),
                'total_hours': theme[2],
                'lecture_hours': theme[3],
                'practice_hours': theme[4],
                'trainee_hours': theme[5],
                'individual_hours': theme[6],
                'control_form': theme[7],
                'chapter_id': chapter.object_id
            }
            calendar_chart_theme_model.objects.update_or_create(
                **new_theme
            )
            print(f'Тема "{new_theme["name"]}" раздела КУГ "{chapter.name}" '
                  f'ДПП "{program.name}" - добавлено')

    @staticmethod
    def get_program_categories():
        """
        Получение категорий слушателей для ДПП
        """
        exists = (program_model.objects.
                  select_related('department').
                  select_related('kug_edit').
                  prefetch_related('categories').
                  select_related('program_order').
                  all())
        audience_categories = audience_category_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_programs_categories'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for pr_cat in data:
            if len(list(filter(lambda pr: pr.old_id == pr_cat[1], exists))) == 0:
                continue
            program = list(filter(lambda pr: pr.old_id == pr_cat[1], exists))[0]
            try:
                aud_cat_id = list(filter(lambda cat: cat.old_id == pr_cat[2], audience_categories))[0].object_id
            except Exception:
                continue
            if program.categories.filter(object_id=aud_cat_id).exists():
                continue
            aud_cat = audience_category_model.objects.get(object_id=aud_cat_id)
            program.categories.add(aud_cat)
            print(f'Категория "{aud_cat.name}" к ДПП "{program.name}" - добавлено')

    @staticmethod
    def get_education_services():
        """
        Получение курсов
        """
        exists = education_service_model.objects.all()
        programs = (program_model.objects.
                    select_related('department').
                    select_related('kug_edit').
                    prefetch_related('categories').
                    select_related('program_order').
                    all())
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_courses'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for course in data:
            if len(list(filter(lambda cr: cr.old_id == course[0], exists))) > 0:
                continue
            new_course = {
                'old_id': course[0],
                'location': course[1],
                'date_start': course[2],
                'date_end': course[3]
            }
            program_name = None
            if len(list(filter(lambda pr: pr.old_id == course[4], programs))) != 0:
                program = list(
                    filter(lambda pr: pr.old_id == course[4], programs)
                )[0]
                new_course['program_id'] = program.object_id
                program_name = program.name
            else:
                new_course['program_id'] = None
            education_service_model.objects.update_or_create(
                **new_course
            )
            print(f'Курс "{program_name}" - добавлено')

    def get_student_groups(self):
        """
        Получение учебных групп
        """
        exists = (student_group_model.objects.
                  select_related('ou').
                  select_related('iku').
                  select_related('curator').
                  all())
        ou = education_service_model.objects.all()
        iku = information_service_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = 'SELECT * from dbo.centre_studentgroups'
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for group in data:
            # if len(list(filter(lambda gr: gr.old_id == group[0], exists))) > 0:
            #     update_gr = {
            #         'form': group[7],
            #     }
            #     student_group_orm.update_record(
            #         filter_by=dict(object_id=list(filter(lambda gr: gr.old_id == group[0], exists))[0].object_id),
            #         update_object=update_gr
            #     )
            #     print('Обновлена группа: ', repr(list(filter(lambda gr: gr.old_id == group[0], exists))[0]))
            if len(list(filter(lambda gr: gr.old_id == group[0], exists))) > 0:
                continue
            if len(list(filter(lambda gr: gr.code == group[1], exists))) > 0:
                continue
            course = event = None
            if group[12]:
                try:
                    course = list(filter(lambda cr: cr.old_id == group[12], ou))[0].object_id
                except Exception:
                    continue
            if group[14]:
                try:
                    event = list(filter(lambda ev: ev.old_id == group[14], iku))[0].object_id
                except Exception:
                    continue
            new_group = {
                'old_id': group[0],
                'code': group[1],
                'plan_seats_number': group[2],
                'status': self._group_status_mapping[group[15]],
                'form': group[7],
                'event_url': group[4],
                'survey_show': group[5],
                'date_enroll': group[8],
                'date_exp': group[9],
                'enroll_number': group[10],
                'exp_number': group[11],
                'iku_id': event,
                'ou_id': course
            }
            student_group_model.objects.update_or_create(
                **new_group
            )
            print(f'Учебная группа "{new_group["code"]}" - добавлено')

    @staticmethod
    def set_group_curator():
        """
        Установить учебным группам кураторов
        """
        exists = (student_group_model.objects.
                  select_related('ou').
                  select_related('iku').
                  select_related('curator').
                  all())
        curators = coko_profile_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT gr.[id] as group_id, prof.[user_id] as teacher_django_id'
                   ' from dbo.centre_studentgroups as gr inner join '
                   'dbo.authen_profiles as prof on gr.curator_id = prof.id '
                   'where gr.[curator_id] is not NULL')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for st_group in data:
            try:
                group = list(filter(lambda gr: gr.old_id == st_group[0], exists))[0]
            except Exception:
                continue
            if group.curator:
                continue
            try:
                curator = list(filter(lambda cur: cur.old_id == st_group[1], curators))[0]
            except Exception:
                continue
            group.curator_id = curator.object_id
            group.save()
            print(f'Куратор "{curator.display_name}" для группы "{group.code}" - добавлено')

    def get_course_schedule(self):
        """
        Получение расписания занятий курсов
        """
        exists = (schedule_model.objects.
                  select_related('group').
                  select_related('kug_theme').
                  all())
        groups = (student_group_model.objects.
                  select_related('ou').
                  select_related('iku').
                  select_related('curator').
                  all())
        themes = (calendar_chart_theme_model.objects.
                  select_related('chapter').
                  all())
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT *'
                   ' from dbo.centre_courselessons')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for lesson in data:
            if len(list(filter(lambda sc: sc.old_id == lesson[0], exists))) > 0:
                continue
            try:
                group = list(filter(lambda gr: gr.old_id == lesson[9], groups))[0]
            except Exception:
                print('course_group')
                continue
            time_start = (lesson[5] + datetime.timedelta(hours=8)).strftime('%H:%M')
            time_end = (lesson[6] + datetime.timedelta(hours=8)).strftime('%H:%M')
            theme = '(тема из раздела КУГ)'
            theme_id = None
            try:
                th = list(filter(lambda th: th.old_id == lesson[10], themes))[0]
                theme = th.name
                theme_id = th.object_id
            except Exception:
                theme_id = None
            les_type = LECTURE
            if lesson[2]:
                les_type = PRACTICE
            if lesson[3]:
                les_type = TRAINEE
            if lesson[4]:
                les_type = INDIVIDUAL
            new_course_lesson = {
                'old_id': lesson[0],
                'date': lesson[5].strftime('%Y-%m-%d'),
                'time_start': self._date_utils.convert_time_string_to_seconds(time_start),
                'time_end': self._date_utils.convert_time_string_to_seconds(time_end),
                'theme': theme,
                'type': les_type,
                'distance': lesson[7],
                'control': lesson[8],
                'group_id': group.object_id,
                'kug_theme_id': theme_id
            }
            schedule_model.objects.update_or_create(
                **new_course_lesson
            )
            print(f'Урок для группы "{group.code}" - добавлено')

    @staticmethod
    def set_course_schedule_theme_teacher():
        """
        Установка наименования темы и преподавателя
        """
        exists = (schedule_model.objects.
                  select_related('group').
                  select_related('kug_theme').
                  all())
        student_profiles = (student_profile_model.objects.
                            select_related('django_user').
                            select_related('state').
                            all())
        coko_profiles = coko_profile_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT lesson.[id], stsch.[name], prof.[user_id] FROM [edu-new].[dbo].[centre_courselessons] '
                   'as lesson inner join [edu-new].[dbo].[centre_stschedule] as stsch on lesson.[stschedule_id] = '
                   'stsch.[id] inner join [edu-new].[dbo].[authen_profiles] as prof on lesson.[teacher_id] = '
                   'prof.[id]')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for lesson in data:
            if len(list(filter(lambda sc: sc.old_id == lesson[0], exists))) == 0:
                continue
            les = list(filter(lambda sc: sc.old_id == lesson[0], exists))[0]
            if not lesson[2]:
                profile = {
                    'object_id': None
                }
            else:
                try:
                    profile = list(filter(lambda prof: prof.old_id == lesson[2], student_profiles))[0]
                except Exception:
                    try:
                        profile = list(filter(lambda prof: prof.old_id == lesson[2], coko_profiles))[0]
                    except Exception:
                        print(f'teacher - {lesson[2]}')
                        continue
            les.teacher = profile.object_id
            first_dot_index = lesson[1].find('.')
            les.theme = lesson[1][first_dot_index + 1:].strip()
            if lesson[1].count('.') >= 2:
                second_dot_index = lesson[1].find('.', first_dot_index + 1)
                les.theme = lesson[1][second_dot_index + 1:].strip()
            les.save()
            print(f'Преподаватель для занятий "{les.theme}" - добавлено')

    def get_event_schedule(self):
        """
        Получение расписания занятий курсов
        """
        exists = (schedule_model.objects.
                  select_related('group').
                  select_related('kug_theme').
                  all())
        groups = (student_group_model.objects.
                  select_related('ou').
                  select_related('iku').
                  select_related('curator').
                  all())
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT *'
                   ' from dbo.centre_eventslessons')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for lesson in data:
            if len(list(filter(lambda sc: sc.old_id == lesson[0], exists))) > 0:
                continue
            try:
                group = list(filter(lambda gr: gr.old_id == lesson[6], groups))[0]
            except Exception:
                print('event_group')
                continue
            time_start = (lesson[4] + datetime.timedelta(hours=8)).strftime('%H:%M')
            time_end = (lesson[5] + datetime.timedelta(hours=8)).strftime('%H:%M')
            count = 1
            les_type = None
            if lesson[2]:
                les_type = LECTURE
                if int(lesson[2]) > 1:
                    count = int(lesson[2])
            if lesson[3]:
                les_type = PRACTICE
                if int(lesson[3]) > 1:
                    count = int(lesson[3])
            new_event_lesson = {
                'old_id': lesson[0],
                'date': lesson[5].strftime('%Y-%m-%d'),
                'time_start': self._date_utils.convert_time_string_to_seconds(time_start),
                'time_end': self._date_utils.convert_time_string_to_seconds(time_end),
                'theme': lesson[1],
                'type': les_type,
                'distance': False,
                'control': '',
                'group_id': group.object_id
            }
            for _ in range(0, count):
                schedule_model.objects.update_or_create(
                    **new_event_lesson
                )
            print(f'Урок для группы "{group.code}" - добавлено')

    @staticmethod
    def set_event_schedule_teacher():
        """
        Установка преподавателя
        """
        exists = (schedule_model.objects.
                  select_related('group').
                  select_related('kug_theme').
                  all())
        student_profiles = (student_profile_model.objects.
                            select_related('django_user').
                            select_related('state').
                            all())
        coko_profiles = coko_profile_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT lesson.[id], prof.[user_id] FROM [edu-new].[dbo].[centre_eventslessons] as lesson '
                   'inner join [edu-new].[dbo].[authen_profiles] as prof on lesson.[teacher_id] = prof.[id]')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for lesson in data:
            if len(list(filter(lambda sc: sc.old_id == lesson[0], exists))) == 0:
                continue
            les = list(filter(lambda sc: sc.old_id == lesson[0], exists))[0]
            if not lesson[1]:
                profile = {
                    'object_id': None
                }
            else:
                try:
                    profile = list(filter(lambda prof: prof.old_id == lesson[1], student_profiles))[0]
                except Exception:
                    try:
                        profile = list(filter(lambda prof: prof.old_id == lesson[1], coko_profiles))[0]
                    except Exception:
                        print(f'teacher - {lesson[2]}')
                        continue
            les.teacher = profile.object_id
            les.save()
            print(f'Преподаватель для занятий "{les.theme}" - добавлено')
