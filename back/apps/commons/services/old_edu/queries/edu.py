import datetime

from django.db import IntegrityError
from sqlalchemy import text

from apps.commons.serializers.ad_centre import ad_centre_model
from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.commons.utils.data_types.date import date_utils
from apps.docs.selectors.program_order import program_order_model
from apps.edu.consts.lesson_types import LECTURE, PRACTICE, TRAINEE, INDIVIDUAL
from apps.edu.consts.student_group.statuses import REGISTRATION, STATEMENT, OFFER, URL, PROCESS, COMPLETE
from apps.edu.selectors.calender_chart.calendar_chart_chapter import calendar_chart_chapter_model
from apps.edu.selectors.calender_chart.calendar_chart_theme import calendar_chart_theme_model
from apps.edu.selectors.program import program_model
from apps.edu.selectors.schedule import schedule_model
from apps.edu.selectors.services.education_service import education_service_model
from apps.edu.selectors.services.information_service import information_service_model
from apps.edu.selectors.student_group import student_group_model
from apps.guides.selectors.audience_category import audience_category_model
from apps.guides.selectors.profiles.coko import coko_profile_model
from apps.guides.selectors.event_type import event_type_model
from apps.guides.selectors.profiles.student import student_profile_model


class EduData:
    """
    Класс методов для получения и сохранения данных приложения
    Учебная часть из олдовой базы edu
    """
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
                exist = list(filter(lambda service: service.old_id == iku[0], exists))[0]
                if exist.updated_from_new:
                    continue
                if exist.location == iku[4] and \
                        exist.date_start == iku[5] and \
                        exist.date_end == iku[6] and \
                        exist.name == iku[2] and \
                        exist.duration == iku[3] and \
                        exist.price == iku[7]:
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
            _, created = information_service_model.objects.update_or_create(
                old_id=iku[0],
                defaults=new_iku
            )
            action = 'добавлено' if created else 'обновлено'
            print(f'Мероприятие "{new_iku["name"]}" - {action}')

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
            if event.updated_from_new:
                continue
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
                exist = list(filter(lambda pr: pr.old_id == program[0], exists))[0]
                if exist.updated_from_new:
                    continue
                if exist.name == program[2] and \
                        exist.type == program[3] and \
                        exist.duration == program[4] and \
                        exist.annotation == program[6] and \
                        exist.price == program[10]:
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
            _, created = program_model.objects.update_or_create(
                old_id=program[0],
                defaults=new_program
            )
            action = 'добавлено' if created else 'обновлено'
            print(f'ДПП "{new_program["name"]}" - {action}')

    @staticmethod
    def get_program_calendar_chapters():
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
            try:
                program = list(filter(lambda pr: pr.old_id == chapter[13], programs))[0]
            except Exception:
                continue
            try:
                position = int(chapter[1][7])
            except ValueError:
                position = 15
            if len(list(filter(lambda ch: ch.old_id == chapter[0], exists))) > 0:
                exist = list(filter(lambda ch: ch.old_id == chapter[0], exists))[0]
                if exist.updated_from_new:
                    continue
                if exist.position == position and \
                        exist.name == chapter[1][10:].strip() and \
                        exist.total_hours == chapter[2] and \
                        exist.lecture_hours == chapter[3] and \
                        exist.practice_hours == chapter[4] and \
                        exist.trainee_hours == chapter[5] and \
                        exist.individual_hours == chapter[6] and \
                        exist.control_form == chapter[7] and \
                        exist.program_id == program.object_id:
                    continue
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
            _, created = calendar_chart_chapter_model.objects.update_or_create(
                old_id=chapter[0],
                defaults=new_chapter
            )
            action = 'добавлено' if created else 'обновлено'
            print(f'Раздел КУГ "{new_chapter["name"]}" ДПП "{program.name}" - {action}')

    @staticmethod
    def get_program_calendar_themes():
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
            try:
                chapter = list(filter(lambda ch: ch.old_id == theme[12], chapters))[0]
            except Exception:
                continue
            try:
                program = list(filter(lambda pr: pr.old_id == theme[13], programs))[0]
            except Exception:
                continue
            first_dot_index = theme[1].find('.')
            second_dot_index = theme[1].find('.', first_dot_index + 1)
            if len(list(filter(lambda th: th.old_id == theme[0], exists))) > 0:
                exist = list(filter(lambda th: th.old_id == theme[0], exists))[0]
                if exist.updated_from_new:
                    continue
                if exist.position == int(theme[1][first_dot_index + 1]) and \
                        exist.name == theme[1][second_dot_index + 1:].strip() and \
                        exist.total_hours == theme[2] and \
                        exist.lecture_hours == theme[3] and \
                        exist.practice_hours == theme[4] and \
                        exist.trainee_hours == theme[5] and \
                        exist.individual_hours == theme[6] and \
                        exist.control_form == theme[7] and \
                        exist.chapter_id == chapter.object_id:
                    continue
            new_theme = {
                'old_id': theme[0],
                'position': int(theme[1][first_dot_index + 1]),
                'name': theme[1][second_dot_index + 1:].strip(),
                'total_hours': theme[2],
                'lecture_hours': theme[3],
                'practice_hours': theme[4],
                'trainee_hours': theme[5],
                'individual_hours': theme[6],
                'control_form': theme[7],
                'chapter_id': chapter.object_id
            }
            _, created = calendar_chart_theme_model.objects.update_or_create(
                old_id=theme[0],
                defaults=new_theme
            )
            action = 'добавлено' if created else 'обновлено'
            print(f'Тема "{new_theme["name"]}" раздела КУГ "{chapter.name}" '
                  f'ДПП "{program.name}" - {action}')

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
            if program.updated_from_new:
                continue
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
                exist = list(filter(lambda cr: cr.old_id == course[0], exists))[0]
                if exist.updated_from_new:
                    continue
                if exist.location == course[1] and \
                        exist.date_start == course[2] and \
                        exist.date_end == course[3]:
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
            _, created = education_service_model.objects.update_or_create(
                old_id=course[0],
                defaults=new_course
            )
            action = 'добавлено' if created else 'обновлено'
            print(f'Курс "{program_name}" - {action}')

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
            if len(list(filter(lambda gr: gr.old_id == group[0], exists))) > 0:
                exist = list(filter(lambda gr: gr.old_id == group[0], exists))[0]
                print(f'code: {group[1]} --- status: {group[15]}')
                if exist.updated_from_new:
                    continue
                if exist.code == group[1] and \
                        exist.plan_seats_number == group[2] and \
                        exist.status == self._group_status_mapping[group[15]] and \
                        exist.form == group[7] and \
                        exist.event_url == group[4] and \
                        exist.survey_show == group[5] and \
                        exist.date_enroll == group[8] and \
                        exist.date_exp == group[9] and \
                        exist.enroll_number == group[10] and \
                        exist.exp_number == group[11]:
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
            try:
                _, created = student_group_model.objects.update_or_create(
                    old_id=group[0],
                    defaults=new_group
                )
            except IntegrityError:
                continue
            action = 'добавлено' if created else 'обновлено'
            print(f'Учебная группа "{new_group["code"]}" - {action}')

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
            sql = ('SELECT id, curator_id from dbo.centre_studentgroups')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for st_group in data:
            try:
                group = list(filter(lambda gr: gr.old_id == st_group[0], exists))[0]
            except Exception:
                continue
            if group.updated_from_new:
                continue
            try:
                curator = list(filter(lambda cur: cur.old_id == st_group[1], curators))[0]
            except Exception:
                continue
            if group.curator_id == curator.object_id:
                continue
            group.curator_id = curator.object_id
            group.save()
            print(f'Куратор "{curator.display_name}" для группы "{group.code}" - обновлено')

    def get_course_schedule(self):
        """
        Получение расписания занятий курсов
        """
        exists = (schedule_model.objects.
                  select_related('group').
                  all())
        groups = (student_group_model.objects.
                  select_related('ou').
                  select_related('iku').
                  select_related('curator').
                  all())
        themes = (calendar_chart_theme_model.objects.
                  select_related('chapter').
                  all())
        chapters = calendar_chart_chapter_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT *'
                   ' from dbo.centre_courselessons')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for lesson in data:
            try:
                group = list(filter(lambda gr: gr.old_id == lesson[9], groups))[0]
            except Exception:
                print('course_group')
                continue
            time_start = (lesson[5] + datetime.timedelta(hours=8)).strftime('%H:%M')
            time_end = (lesson[6] + datetime.timedelta(hours=8)).strftime('%H:%M')
            theme = '(тема из раздела КУГ)'
            try:
                th = list(filter(lambda th: th.old_id == lesson[10], themes))[0]
                theme = th.name
                theme_id = th.object_id
            except Exception:
                try:
                    th = list(filter(lambda th: th.old_id == lesson[10], chapters))[0]
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
            if len(list(filter(lambda sc: sc.old_id == lesson[0], exists))) > 0:
                exist = list(filter(lambda sc: sc.old_id == lesson[0], exists))[0]
                if exist.updated_from_new:
                    continue
                if str(exist.date) == lesson[5].strftime('%Y-%m-%d') and \
                        exist.time_start == date_utils.convert_time_string_to_seconds(time_start) and \
                        exist.time_end == date_utils.convert_time_string_to_seconds(time_end) and \
                        exist.theme == theme and \
                        exist.type == les_type and \
                        exist.distance == lesson[7] and \
                        exist.control == lesson[8] and \
                        exist.group_id == group.object_id and \
                        exist.kug_theme_id == theme_id:
                    continue
            new_course_lesson = {
                'old_id': lesson[0],
                'date': lesson[5].strftime('%Y-%m-%d'),
                'time_start': date_utils.convert_time_string_to_seconds(time_start),
                'time_end': date_utils.convert_time_string_to_seconds(time_end),
                'theme': theme,
                'type': les_type,
                'distance': lesson[7],
                'control': lesson[8],
                'group_id': group.object_id,
                'kug_theme_id': theme_id
            }
            _, created = schedule_model.objects.update_or_create(
                old_id=lesson[0],
                defaults=new_course_lesson
            )
            action = 'добавлено' if created else 'обновлено'
            print(f'Урок для группы "{group.code}" - {action}')

    @staticmethod
    def set_course_schedule_theme_teacher():
        """
        Установка наименования темы и преподавателя
        """
        exists = (schedule_model.objects.
                  select_related('group').
                  all())
        student_profiles = (student_profile_model.objects.
                            select_related('django_user').
                            select_related('state').
                            all())
        coko_profiles = coko_profile_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT lesson.[id], stsch.[name], prof.[id] FROM [edu-new].[dbo].[centre_courselessons] '
                   'as lesson inner join [edu-new].[dbo].[centre_stschedule] as stsch on lesson.[stschedule_id] = '
                   'stsch.[id] inner join [edu-new].[dbo].[authen_profiles] as prof on lesson.[teacher_id] = '
                   'prof.[id]')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for lesson in data:
            if len(list(filter(lambda sc: sc.old_id == lesson[0], exists))) == 0:
                continue
            les = list(filter(lambda sc: sc.old_id == lesson[0], exists))[0]
            if les.updated_from_new:
                continue
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
            first_dot_index = lesson[1].find('.')
            th = lesson[1][first_dot_index + 1:].strip()
            if lesson[1].count('.') >= 2:
                second_dot_index = lesson[1].find('.', first_dot_index + 1)
                th = lesson[1][second_dot_index + 1:].strip()
            if les.theme == th and les.teacher == profile.object_id:
                continue
            les.teacher = profile.object_id
            les.theme = th
            les.save()
            print(f'Преподаватель для занятий "{les.theme}" - обновлено')

    @staticmethod
    def get_event_schedule():
        """
        Получение расписания занятий курсов
        """
        exists = (schedule_model.objects.
                  select_related('group').
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
            if len(list(filter(lambda sc: sc.old_id == lesson[0], exists))) > 0:
                exist = list(filter(lambda sc: sc.old_id == lesson[0], exists))[0]
                if exist.updated_from_new:
                    continue
                if str(exist.date) == lesson[5].strftime('%Y-%m-%d') and \
                        exist.time_start == date_utils.convert_time_string_to_seconds(time_start) and \
                        exist.time_end == date_utils.convert_time_string_to_seconds(time_end) and \
                        exist.theme == lesson[1] and \
                        exist.type == les_type and \
                        exist.control == '' and \
                        exist.group_id == group.object_id:
                    continue
            new_event_lesson = {
                'old_id': lesson[0],
                'date': lesson[5].strftime('%Y-%m-%d'),
                'time_start': date_utils.convert_time_string_to_seconds(time_start),
                'time_end': date_utils.convert_time_string_to_seconds(time_end),
                'theme': lesson[1],
                'type': les_type,
                'distance': False,
                'control': '',
                'group_id': group.object_id
            }
            for _ in range(0, count):
                _, created = schedule_model.objects.update_or_create(
                    old_id=lesson[0],
                    defaults=new_event_lesson
                )
                action = 'добавлено' if created else 'обновлено'
                print(f'Урок для группы "{group.code}" - {action}')

    @staticmethod
    def set_event_schedule_teacher():
        """
        Установка преподавателя
        """
        exists = (schedule_model.objects.
                  select_related('group').
                  all())
        student_profiles = (student_profile_model.objects.
                            select_related('django_user').
                            select_related('state').
                            all())
        coko_profiles = coko_profile_model.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT lesson.[id], prof.[id] FROM [edu-new].[dbo].[centre_eventslessons] as lesson '
                   'inner join [edu-new].[dbo].[authen_profiles] as prof on lesson.[teacher_id] = prof.[id]')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for lesson in data:
            if len(list(filter(lambda sc: sc.old_id == lesson[0], exists))) == 0:
                continue
            les = list(filter(lambda sc: sc.old_id == lesson[0], exists))[0]
            if les.updated_from_new:
                continue
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
            if les.teacher == profile.object_id:
                continue
            les.teacher = profile.object_id
            les.save()
            print(f'Преподаватель для занятий "{les.theme}" - обновлено')
