from rest_framework import serializers
from ..models import Customer,RemainingAmount
from django.db import transaction
class CustomerSerializer(serializers.ModelSerializer):
    opening_balance = serializers.DecimalField(max_digits=10,decimal_places=2,write_only = True)
    customer_opening_type = serializers.CharField(max_length=100,write_only = True)
    remaining_amount = serializers.SerializerMethodField() 
    class Meta:
        model = Customer
        fields = ["name","phone","email","pan_id","address","customer_type","opening_balance","customer_opening_type","remaining_amount",]
    
    @transaction.atomic
    def create(self,validated_data):
        opening_balance = validated_data.pop("opening_balance",0)
        customer_opening_type = validated_data.pop("customer_opening_type")

        # create customer
        customer = Customer.objects.create(**validated_data)

        amount = opening_balance
        if customer_opening_type == "TOGIVE":
            amount = -opening_balance
        elif customer_opening_type == "TORECIEVE":
            amount = opening_balance

        # creating remaining amount
        RemainingAmount.objects.create(customer=customer,remaining_amount = amount)

        return customer
    
    def get_remaining_amount(self, obj):
        remaining_obj = obj.customerRemainingAmount.first() 
        return remaining_obj.remaining_amount if remaining_obj else 0