from django.contrib.auth.models import User, Group
from sqlalchemy import text

from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.guides.selectors.coko import coko_profile_model
from apps.guides.selectors.state import state_model
from apps.guides.selectors.user import student_profile_model

django_user_fields = [
    'password',
    'last_login',
    'is_superuser',
    'username',
    'first_name',
    'last_name',
    'email',
    'is_staff',
    'is_active',
    'date_joined'
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
        users = User.objects.all()
        with old_edu_connect_engine.connect() as conn:
            dj_users_query = conn.execute(
                text(
                    'SELECT * from dbo.auth_user'
                )
            )
            dj_users = dj_users_query.all()
        for dj_user in dj_users:
            if len(list(filter(lambda us: us.id == dj_user[0], users))) > 0:
                continue
            new_user = {
                'id': dj_user[0]
            }
            for i in range(0, len(django_user_fields)):
                new_user[django_user_fields[i]] = dj_user[i+1]
            User.objects.update_or_create(**new_user)
            print(f'Пользователь "{dj_user[4]}" - добавлено')

    @staticmethod
    def get_student_profile_info():
        """
        Получение информации из профилей обучающихся
        """
        if student_profile_model.objects.filter(old_id=0).count() > 0:
            with old_edu_connect_engine.connect() as conn:
                user_profiles_query = conn.execute(
                    text(
                        'SELECT * from dbo.authen_profiles'
                    )
                )
                user_profiles = user_profiles_query.all()
            for profile in student_profile_model.objects.filter(old_id=0):
                profile_user = list(filter(
                    lambda prof: prof[12] == profile.django_user_id,
                    user_profiles
                ))
                if len(profile_user) == 0:
                    continue
                profile_user = profile_user[0]
                profile.old_id = profile_user[12]
                for i in range(0, len(student_profile_fields)):
                    if student_profile_fields[i] in ['id', 'date_reg']:
                        continue
                    if student_profile_fields[i] == 'state_id':
                        setattr(
                            profile,
                            student_profile_fields[i],
                            state_model.objects.filter(old_id=profile_user[i]).first().object_id
                        )
                    else:
                        setattr(profile, student_profile_fields[i], profile_user[i])
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
        for prof in student_profile_model.objects.exclude(
                django_user_id__in=User.objects.filter(
                    groups__name__in=['Обучающиеся', ]
                )
        ):
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