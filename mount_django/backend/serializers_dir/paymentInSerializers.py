from rest_framework import serializers
from ..models import PaymentIn
class PaymentInSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIn
        fields = "__all__"
        read_only_fields = ["id","created_at","company","remainings"]