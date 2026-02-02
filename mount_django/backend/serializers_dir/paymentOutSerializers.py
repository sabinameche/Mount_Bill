from rest_framework import serializers
from ..models import PaymentOut

class PaymentOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOut
        fields = "__all__"
        read_only_fields = ["id","created_at","company","remainings"]
