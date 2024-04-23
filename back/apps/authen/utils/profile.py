import datetime
import uuid
from typing import Optional

from django.contrib.auth.models import User, Group

from apps.authen.models import Profiles, States
from apps.commons.utils.data_types.dict import DictUtils


class ProfileUtils:
    """Класс методов для работы с профилями пользователей"""

    @staticmethod
    def check_profile_exists(field, value) -> Optional[bool]:
        """Проверка на существование профиля пользователя по заданному полю и значению"""
        if field in ['username', 'email']:
            filter_kwargs = {
                field: value
            }
            return User.objects.filter(**filter_kwargs).exists()
        elif field == 'phone':
            return Profiles.objects.filter(phone=value).exists()
        elif field == 'user_id':
            return User.objects.filter(id=value).exists()
        elif field == 'django_user_id':
            return Profiles.objects.filter(django_user_id=value).exists()
        elif field in ['object_id', 'profile_id']:
            return Profiles.objects.filter(object_id=value).exists()
        else:
            return None

    def get_profile_info(
            self,
            input_field: str,
            input_value: str,
            find_field: str
    ):
        """Получение нужной информации из профиля пользователя по полученному полю и его значению"""
        if self.check_profile_exists(input_field, input_value) is True:
            filter_kwargs = {}
            if input_field in ['username', 'email']:
                user_filter_kwargs = {
                    input_field: input_value
                }
                filter_kwargs = {
                    'django_user_id': User.objects.get(**user_filter_kwargs).id
                }
            elif input_field in ['phone', 'django_user_id', 'object_id']:
                filter_kwargs = {
                    input_field: input_value
                }
            else:
                pass
            if not DictUtils.dict_is_empty(filter_kwargs):
                results = Profiles.objects.filter(**filter_kwargs)
                if results.count() > 0:
                    if find_field == 'all':
                        profile = results.first()
                        return {
                            'state': profile.state.name,
                            'surname': profile.surname,
                            'name': profile.name,
                            'patronymic': profile.patronymic,
                            'sex': profile.sex,
                            'birthday': profile.birthday,
                            'age': profile.age,
                            'oo_shortname': profile.oo_shortname,
                            'oo_fullname': profile.oo_fullname,
                            'phone': profile.phone,
                            'email': profile.django_user.email
                        }
                    else:
                        return getattr(results.first(), find_field)
        return None

    def get_display_name(self, input_field, input_value) -> Optional[str]:
        """Получение ФИО пользователя по полученному полю и значению"""
        if self.check_profile_exists(input_field, input_value):
            profile_filter = {
                input_field: input_value
            }
            return Profiles.objects.filter(**profile_filter).first().get_display_name()
        return None

    @staticmethod
    def get_user_role(user_id: int) -> Optional[str]:
        """Получение роли пользователя по его ID"""
        if User.objects.filter(id=user_id).exists():
            for gr in User.objects.get(id=user_id).groups.all():
                if gr.name in ['Администраторы', 'Преподаватели', 'Участники']:
                    return gr.name
        return None

    def get_username(self, input_field, input_value) -> Optional[str]:
        """Получение имени пользователя по полученному полю"""
        if self.check_profile_exists(input_field, input_value) is True:
            if input_field == 'email':
                return User.objects.get(email=input_value).username
            if input_field == 'phone':
                user_id = self.get_profile_info('phone', input_value, 'django_user_id')
                if user_id is not None:
                    return User.objects.get(id=user_id).username
        return None

    @staticmethod
    def get_profile_by_user_id(django_user_id: int) -> Optional[Profiles]:
        """Получение профиля пользователя на основе полученного uuid пользователя Django"""
        if Profiles.objects.filter(django_user_id=django_user_id).exists():
            return Profiles.objects.get(django_user_id=django_user_id)
        else:
            return None

    @staticmethod
    def get_profile_by_object_id(profile_id: uuid) -> Optional[Profiles]:
        """Получение профиля пользователя на основе полученного object_id"""
        if Profiles.objects.filter(object_id=profile_id).exists():
            return Profiles.objects.get(object_id=profile_id)
        else:
            return None

    @staticmethod
    def check_unique_phone(phone: str, user_id=None) -> bool:
        """Проверка на уникальный номер телефона"""
        if Profiles.objects.filter(phone=phone).exists():
            if user_id is not None:
                profile = Profiles.objects.get(phone=phone)
                if profile.django_user_id == user_id:
                    return True
            return False
        return True

    @staticmethod
    def check_unique_email(email: str, user_id=None) -> bool:
        """Проверка на уникальный адрес электронной почты"""
        if User.objects.filter(email=email).exists():
            if user_id is not None:
                user = User.objects.get(email=email)
                if user.id == user_id:
                    return True
            return False
        return True

    def change_profile_info(self, user_id: int, data: dict) -> bool:
        """Изменение полученной информации в профиле пользователя по полученному ID"""
        if self.check_profile_exists('user_id', user_id):
            profile = self.get_profile_by_user_id(user_id)
            for key, value in data.items():
                if key == 'email':
                    django_user = User.objects.get(id=user_id)
                    django_user.email = value
                    django_user.save()
                elif key == 'state':
                    profile.state_id = States.objects.get(name=value).object_id
                elif key == 'birthday':
                    profile.birthday = datetime.datetime.strptime(value, "%d.%m.%Y").date()
                else:
                    setattr(profile, key, value)
            profile.save()
            return True
        return False

    def change_user_password(self, user_id: int, password: str) -> bool:
        """Изменение пароля пользователя"""
        if self.check_profile_exists('user_id', user_id):
            django_user = User.objects.get(id=user_id)
            django_user.set_password(password)
            django_user.save()
            return True
        return False

    def change_user_role(self, user_id: int, role: str) -> bool:
        """Смена роли пользователя"""
        if self.check_profile_exists('user_id', user_id) and \
                role in ['Администраторы', 'Преподаватели', 'Участники']:
            user = User.objects.get(id=user_id)
            groups = user.groups.all()
            for gr in groups:
                gr.user_set.remove(user)
            user.is_superuser = False
            user.is_staff = False
            user.save()
            Group.objects.get(name=role).user_set.add(user)
            if role == 'Администраторы':
                user.is_superuser = True
                user.is_staff = True
                user.save()
            return True
        return False

    @staticmethod
    def get_all_profiles():
        """Получение всех профилей пользователей"""
        return Profiles.objects.all().order_by('surname', 'name', 'patronymic')

    @staticmethod
    def get_profile_by_user_email(email: str) -> Optional[Profiles]:
        """Получение display name пользователя по полученному email"""
        if User.objects.filter(email=email).exists():
            if Profiles.objects.filter(django_user=User.objects.get(email=email)).exists():
                return Profiles.objects.get(django_user=User.objects.get(email=email))
        return None

    @staticmethod
    def get_user_id_by_email(email: str) -> Optional[int]:
        """Получение ID пользователя Django по его почте"""
        try:
            return User.objects.get(email=email).id
        except Exception:
            return None

