from django.contrib.auth.models import User, Group
from sqlalchemy import text

from apps.authen.selectors.user import user_orm
from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.commons.utils.django.exception import exception_handling
from apps.guides.selectors.profiles.coko import coko_profile_model
from apps.guides.selectors.state import state_model
from apps.guides.selectors.profiles.student import student_profile_model

django_user_fields = [
    'password',
    '',
    'is_superuser',
    'username',
    'first_name',
    'last_name',
    'email',
    'is_staff',
    'is_active'
]

student_profile_fields = [
    'id',
    'phone',
    'surname',
    'name',
    'patronymic',
    'sex',
    'birthday',
    'snils',
    'date_reg',
    'teacher',
    'health',
    'state_id'
]


class AuthenData:
    """
    Класс методов для получения и сохранения данных приложения
    авторизации/аутентификации из олдовой базы edu
    """

    @staticmethod
    def get_django_users():
        """
        Получение пользователей Django
        """
        users = user_orm.get_filter_records()
        with old_edu_connect_engine.connect() as conn:
            dj_users_query = conn.execute(text('SELECT * from dbo.auth_user'))
            dj_users = dj_users_query.all()
        for dj_user in dj_users:
            try:
                exist = None
                if len(list(filter(lambda us: us.id == dj_user[0], users))) > 0:
                    exist = list(filter(lambda us: us.id == dj_user[0], users))[0]
                    if exist.password == dj_user[1]:
                        continue
                if len(list(filter(lambda us: us.username == dj_user[4], users))) > 0:
                    continue
                new_user = {}
                for i in range(0, len(django_user_fields)):
                    if django_user_fields[i] != '':
                        new_user[django_user_fields[i]] = dj_user[i+1]
                if exist:
                    user = User(id=exist.id)
                    for key, value in new_user:
                        setattr(user, key, value)
                    user.save()
                    print(f'Пользователь "{dj_user[4]}" - обновлено')
                    continue
                User.objects.create_user(**new_user)
                print(f'Пользователь "{dj_user[4]}" - добавлено')
            except Exception:
                print('django_users error:', exception_handling.get_traceback())

    @staticmethod
    def get_student_profile_info():
        """
        Получение информации из профилей обучающихся
        """
        if (student_profile_model.objects.
                select_related('django_user').
                select_related('state').
                filter(old_id=0).count() > 0):
            with old_edu_connect_engine.connect() as conn:
                user_profiles_query = conn.execute(text('SELECT * from dbo.authen_profiles'))
                user_profiles = user_profiles_query.all()
            profiles = student_profile_model.objects.select_related('django_user').select_related('state')
            for profile in profiles:
                profile_user = list(filter(lambda prof: prof[12] == profile.django_user_id, user_profiles))
                if len(profile_user) == 0:
                    continue
                exist = profile_user[0]
                if profile.updated_from_new:
                    continue
                if profile.phone == exist[1] and \
                        profile.surname == exist[2] and \
                        profile.name == exist[3] and \
                        profile.patronymic == exist[4] and \
                        profile.sex == exist[5] and \
                        profile.birthday == exist[6] and \
                        profile.snils == exist[7] and \
                        profile.teacher == exist[9] and \
                        profile.health == exist[10]:
                    continue
                profile.old_id = exist[12]
                for i in range(0, len(student_profile_fields)):
                    if student_profile_fields[i] in ['id', 'date_reg']:
                        continue
                    if student_profile_fields[i] == 'state_id':
                        setattr(
                            profile,
                            student_profile_fields[i],
                            state_model.objects.filter(old_id=exist[i]).first().object_id
                        )
                    else:
                        setattr(profile, student_profile_fields[i], exist[i])
                profile.save()
                print(f'Профиль "{profile.surname} {profile.name} '
                      f'{profile.patronymic}" - сохранено')

    @staticmethod
    def add_student_to_group():
        """
        Добавление пользователей-студентов в группу "Обучающиеся"
        """
        dj_group = Group.objects.get(name='Обучающиеся')
        users = User.objects.all()
        for prof in (student_profile_model.objects.
                     select_related('django_user').
                     select_related('state').
                     exclude(
                     django_user_id__in=User.objects.filter(
                         groups__name__in=['Обучающиеся', ]
                     )
        )):
            user = list(filter(lambda us: us.id == prof.django_user_id, users))[0]
            dj_group.user_set.add(user)
            print(f'Пользователь "{user.username}" добавлен в группу "Обучающиеся"')

    @staticmethod
    def get_coko_profile_info():
        """
        Получение информации из профилей работников ЦОКО
        """
        if coko_profile_model.objects.filter(old_id=0).count() > 0:
            with old_edu_connect_engine.connect() as conn:
                user_profiles_query = conn.execute(
                    text(
                        'SELECT * from dbo.authen_profiles'
                    )
                )
                user_profiles = user_profiles_query.all()
            for profile in coko_profile_model.objects.filter(old_id=0):
                profile_user = list(filter(
                    lambda prof: prof[12] == profile.django_user_id,
                    user_profiles
                ))
                if len(profile_user) == 0:
                    continue
                profile_user = profile_user[0]
                profile.old_id = profile_user[12]
                profile.surname = profile_user[2]
                profile.name = profile_user[3]
                profile.patronymic = profile_user[4]
                profile.curator_groups = profile_user[13]
                profile.save()
                print(f'Профиль ЦОКО "{profile.surname} {profile.name} {profile.patronymic}" '
                      f'- сохранено')

    @staticmethod
    def add_coko_to_group():
        """
        Добавление пользователей-студентов в группу "Обучающиеся"
        """
        centre_group = Group.objects.get(name='Сотрудники')
        admin_group = Group.objects.get(name='Администраторы')
        users = User.objects.all()
        for prof in coko_profile_model.objects.filter(
                django_user_id__in=User.objects.filter(
                    is_superuser=False
                )
        ):
            user = list(filter(lambda us: us.id == prof.django_user_id, users))[0]
            centre_group.user_set.add(user)
            print(f'Пользователь "{user.username}" добавлен в группу "Сотрудники"')
        for prof in coko_profile_model.objects.filter(
                django_user_id__in=User.objects.filter(
                    is_superuser=True
                )
        ):
            user = list(filter(lambda us: us.id == prof.django_user_id, users))[0]
            admin_group.user_set.add(user)
            print(f'Пользователь "{user.username}" добавлен в группу "Администраторы"')