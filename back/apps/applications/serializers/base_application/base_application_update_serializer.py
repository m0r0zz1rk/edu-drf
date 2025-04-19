from rest_framework import serializers

from apps.applications.selectors.course_application import course_application_model


class BaseApplicationUpdateSerializer(serializers.Serializer):
    """Базовый сериалайзер для обновления заявки обучающегося"""
    region_id = serializers.UUIDField(
        allow_null=False,
        label='object_id региона РФ'
    )
    mo_id = serializers.UUIDField(
        allow_null=True,
        label='object_id МО (для региона Иркутская область)'
    )
    oo_id = serializers.UUIDField(
        allow_null=True,
        label='object_id ОО из справочника'
    )
    position_category_id = serializers.UUIDField(
        allow_null=True,
        label='object_id категории должности'
    )
    position_id = serializers.UUIDField(
        allow_null=True,
        label='object_id должности'
    )

    class Meta:
        model = course_application_model
        fields = (
            'region_id',
            'mo_id',
            'oo_id',
            'position_category_id',
            'position_id'
        )
