from rest_framework import serializers
from ..models import BalanceAdjustment

class BalanceAdjustSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id","amount","created_at","remarks","customer"]
        read_only_fields = ["id","created_at","remainings"]