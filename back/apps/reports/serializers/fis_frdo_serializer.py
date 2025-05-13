from rest_framework import serializers


class FisFrdoSerializer(serializers.Serializer):
    """
    Сериализация параметров для отчета ФИС ФРДО
    """
    group_ids = serializers.ListSerializer(
        child=serializers.CharField(),
        label='Список object_id учебных групп'
    )
