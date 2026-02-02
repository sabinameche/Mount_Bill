from rest_framework import serializers
from decimal import Decimal
from ..models import PaymentIn,RemainingAmount
from django.db import transaction
class PaymentInSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIn
        fields = "__all__"
        read_only_fields = ["id","created_at","company","remainings"]

