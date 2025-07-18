from rest_framework import serializers


class PaymentDataSerializer(serializers.Serializer):
    """Сериализация данных об оплате по заявке"""
    pay_doc_id = serializers.UUIDField(
        allow_null=True,
        label='object_id документа об оплате'
    )
    offer_id = serializers.UUIDField(
        allow_null=True,
        label='object_id договора оферты'
    )
    message = serializers.CharField(
        max_length=500,
        allow_null=True,
        allow_blank=False,
        label='Комментарий при отклоненной оплате (при наличии)'
    )
