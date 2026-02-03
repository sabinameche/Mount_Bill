from rest_framework import serializers
from ..models import Customer,RemainingAmount
from django.db import transaction
class CustomerSerializer(serializers.ModelSerializer):
    opening_balance = serializers.DecimalField(max_digits=10,decimal_places=2,write_only = True,required=False,default =0)
    customer_opening_type = serializers.ChoiceField(
        choices=["TORECEIVE", "TOGIVE"], default="TORECEIVE", write_only = True
    )
    remaining_amount = serializers.SerializerMethodField() 
    class Meta:
        model = Customer
        fields = ["id","uid","created_at","name","phone","email","pan_id","address","customer_type","opening_balance","customer_opening_type","remaining_amount",]
        read_only_fields = ["uid","id","created_at"]
    

    
    def get_remaining_amount(self, obj):
        remaining_obj = obj.customerRemainingAmount.order_by('-id').first() 
        return remaining_obj.remaining_amount if remaining_obj else 0