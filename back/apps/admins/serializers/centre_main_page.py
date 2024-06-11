from rest_framework import serializers


class UserInfoSerializer(serializers.Serializer):
    """Сериализация информации об администраторе"""
    display_name = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='ФИО'
    )
    first_login = serializers.DateTimeField(
        format="%d.%m.%Y %H:%M",
        allow_null=False,
        label='Первый вход в АИС'
    )


class StudyInfoSerializer(serializers.Serializer):
    """Сериализация статистики об учебном процессе в АИС"""
    user_count = serializers.IntegerField(
        min_value=0,
        allow_null=False,
        label='Количество пользователей в АИС'
    )
    app_count = serializers.IntegerField(
        min_value=0,
        allow_null=False,
        label='Количество заявок в АИС'
    )
    course_count = serializers.IntegerField(
        min_value=0,
        allow_null=False,
        label='Количество учебных курсов в АИС'
    )
    event_count = serializers.IntegerField(
        min_value=0,
        allow_null=False,
        label='Количество мероприятий в АИС'
    )


class LastAppSerializer(serializers.Serializer):
    """Сериализация данных о последней измененной заявки в АИС"""
    user = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='ФИО обучающегося'
    )
    event_name = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Наименование мероприятия/курса'
    )
    status = serializers.CharField(
        max_length=15,
        allow_null=False,
        allow_blank=False,
        label='Статус заявки'
    )


class CentreMainPageSerializer(serializers.Serializer):
    """Сериализация информации для главной страницы администратора АИС"""
    user_info = UserInfoSerializer(label='Информация о пользователе')
    study_info = StudyInfoSerializer(label='Информация по учебному процессу в АИС')
    last_apps = LastAppSerializer(label='Информация по последним заявкам', many=True)

