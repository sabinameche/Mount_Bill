from rest_framework import serializers
from decimal import Decimal
from ..models import PaymentOut,RemainingAmount
from django.db import transaction

class PaymentOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOut
        fields = "__all__"
        read_only_fields = ["id","created_at","company","remainings"]

    @transaction.atomic
    def create(self,validated_data):
        customer = validated_data["customer"]
        payment_out = Decimal(validated_data["payment_out"])
        

        latest_remaining = RemainingAmount.objects.filter(customer=customer).order_by('-id').first()
            
        latest_remaining_amount = latest_remaining.remaining_amount if latest_remaining else Decimal("0.0")

        new_remaining_amount = latest_remaining_amount + payment_out
        new_remaining = RemainingAmount.objects.create(customer=customer,remaining_amount = new_remaining_amount)

        paymentOut = PaymentOut.objects.create(remainings = new_remaining,**validated_data)           
        return paymentOut

    @transaction.atomic
    def update(self,instance,validated_data):
        payment_out = validated_data["payment_out"]
        remarks = validated_data.get("remarks","")

        current_remainig_amount = instance.remainings.remaining_amount
        current_paymentOut = instance.payment_out

        amount_to_calculate_on = current_remainig_amount - current_paymentOut
        latest_remaining_amount = amount_to_calculate_on + payment_out

        instance.remainings.remaining_amount = latest_remaining_amount
        instance.remainings.save()

        instance.payment_out = payment_out
        instance.remarks = remarks
        instance.save()

        return instance  
        
