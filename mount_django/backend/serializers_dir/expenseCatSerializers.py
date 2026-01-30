from ..models import ExpenseCategory
from rest_framework import serializers

class ExpenseCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["name"]