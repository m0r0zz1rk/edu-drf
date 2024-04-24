from django.contrib import admin
from django.contrib.auth.models import User

from apps.authen.models.profile import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Класс для отображения профилей пользователей в административной панели"""

    list_display = (
        'state_name',
        'surname',
        'name',
        'patronymic',
        'birthday',
        'age',
        'sex_alias',
        'phone',
        'email'
    )
    search_fields = (
        'surname',
        'name',
        'patronymic',
        'phone',
        'email'
    )

    def state_name(self, obj):
        """Отображение наименования государства"""
        if obj.state is not None:
            return obj.state.name
        return '-'

    def sex_alias(self, obj):
        """Отображение пола пользователя в текстовом формате"""
        if obj.sex:
            return 'М'
        return 'Ж'

    def email(self, obj):
        """Отображение пользователського email из модели пользователей Django"""
        return User.objects.get(id=obj.django_user_id).email

    state_name.short_description = 'Государство'
    sex_alias.short_description = 'Пол'
    email.short_description = 'Email'
