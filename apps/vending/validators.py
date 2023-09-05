from rest_framework import serializers
from decimal import Decimal


class ListSlotsValidator(serializers.Serializer):
    quantity = serializers.IntegerField(required=False, min_value=0, default=None)


class AuthValidator(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)


class UserValidator(serializers.Serializer):
    credit = serializers.DecimalField(
        required=True, max_digits=6, decimal_places=2, min_value=Decimal("0.00")
    )


class OrderValidator(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)
    slot_id = serializers.UUIDField(required=True)
    product_id = serializers.UUIDField(required=True)
