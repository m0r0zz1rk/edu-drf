from rest_framework import serializers


class UploadLicenses(serializers.Serializer):
    """Сериализация данных при подгрузке сканов удостоверений обучающихся"""
    file = serializers.FileField(
        label='Архив RAR со сканами удостоверений в формате .pdf'
    )
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )
