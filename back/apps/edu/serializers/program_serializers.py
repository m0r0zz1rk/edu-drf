from django.apps import apps
from rest_framework import serializers

program_model = apps.get_model('edu', 'Program')


class ProgramBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных при обработке ДПП"""
    class Meta:
        model = program_model
        fields = ['name', 'type', 'duration']


class ProgramListSerializer(ProgramBaseSerializer):
    """Сериализация данных при получении списка/обновлении ДПП"""
    department = serializers.SerializerMethodField(
        label='Подразделение'
    )
    order_number = serializers.SerializerMethodField(
        label='Номер приказа'
    )
    date_number = serializers.SerializerMethodField(
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
        fields = ProgramBaseSerializer.Meta.fields + ['department', 'order_number', 'date_number']
