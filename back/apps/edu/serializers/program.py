from django.core.validators import MinValueValidator
from rest_framework import serializers

from apps.edu.selectors.program import program_model


class ProgramBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных при обработке ДПП"""

    class Meta:
        model = program_model
        fields = ['object_id', 'department', 'name', 'duration']


class ProgramListSerializer(ProgramBaseSerializer):
    """Сериализация данных при получении списка/обновлении ДПП"""
    department = serializers.SerializerMethodField(
        label='Подразделение'
    )

    order_number = serializers.SerializerMethodField(
        label='Номер приказа'
    )
    order_date = serializers.SerializerMethodField(
        label='Дата приказа'
    )

    def get_department(self, obj):
        """Получение наименования подразделения"""
        if obj.department is not None:
            return obj.department.display_name
        return '-'

    def get_order_number(self, obj):
        """Получение номера приказа об утверждении ДПП"""
        if obj.program_order is not None:
            return obj.program_order.number
        return '-'

    def get_order_date(self, obj):
        """Получение даты приказа об утверждении ДПП"""
        if obj.program_order is not None:
            return obj.program_order.date.strftime('%d.%m.%Y')
        return '-'

    class Meta:
        model = program_model
        fields = ProgramBaseSerializer.Meta.fields + ['department', 'order_number', 'order_date']


class ProgramBaseAddSerializer(ProgramBaseSerializer):
    department = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Подразделение'
    )
    categories = serializers.CharField(
        max_length=1000,
        allow_null=True,
        allow_blank=True,
        label='Категории слушателей'
    )

    class Meta:
        model = program_model
        fields = ProgramBaseSerializer.Meta.fields + [
            'categories',
            'annotation',
            'price',
        ]


class ProgramEducationServiceSerializer(ProgramBaseSerializer):
    """Сериализация данных ДПП для просмотра на форме образовательных услуг (курсов)"""
    department = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Подразделение'
    )
    categories = serializers.SerializerMethodField(
        label='Категории слушателей'
    )

    def get_categories(self, obj):
        """Получение списка имен категорий"""
        cats = ''
        for cat in obj.categories.all().order_by('name'):
            cats += cat.name + ';; '
        return cats[:-3]

    class Meta:
        model = program_model
        fields = ProgramBaseSerializer.Meta.fields + [
            'categories',
            'annotation',
            'price',
        ]


class ProgramRetrieveAddUpdateSerializer(serializers.Serializer):
    """Сериализация данных при получении объекта, добавлении или обновлении ДПП"""
    object_id = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        label='object_id ДПП (при редактировании)'
    )
    department = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Подразделение'
    )
    name = serializers.CharField(
        max_length=500,
        allow_null=False,
        allow_blank=False,
        label='Наименование программы'
    )
    type = serializers.CharField(
        max_length=35,
        allow_null=False,
        allow_blank=False,
        label='Тип программы'
    )
    duration = serializers.IntegerField(
        validators=[MinValueValidator(0),],
        label='Объем программы (часов)'
    )
    categories = serializers.CharField(
        max_length=1000,
        allow_null=True,
        allow_blank=True,
        label='Категории слушателей'
    )
    annotation = serializers.CharField(
        max_length=1500,
        allow_blank=True,
        label='Аннотация'
    )
    price = serializers.IntegerField(
        validators=[MinValueValidator(0),],
        label='Стоимость'
    )
    order_id = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        label='ID приказа (при редактировании)'
    )
    order_number = serializers.CharField(
        max_length=50,
        allow_null=True,
        allow_blank=False,
        label='Номер приказа'
    )
    order_date = serializers.DateField(
        allow_null=True,
        label='Дата приказа'
    )
    order_file = serializers.FileField(
        allow_null=True,
        required=False,
        use_url=False,
        label='Скан приказа'
    )


class ProgramGetOrderSerializer(serializers.Serializer):
    """Сериализация данных для получения приказа ДПП"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id ДПП'
    )

