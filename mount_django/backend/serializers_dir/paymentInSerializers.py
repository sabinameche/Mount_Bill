from rest_framework import serializers
from decimal import Decimal
from ..models import PaymentIn,RemainingAmount
from django.db import transaction
class PaymentInSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIn
        fields = "__all__"
        read_only_fields = ["id","created_at","company","remainings"]

    @transaction.atomic
    def create(self,validated_data):
        
        customer = validated_data["customer"]
        paymentIn = Decimal(validated_data["payment_in"])
        
        latest_remaining = RemainingAmount.objects.filter(customer=customer).order_by('-id').first()
        latest_amount = latest_remaining.remaining_amount if latest_remaining else Decimal("0.0")

        current_remaining = latest_amount - paymentIn

        new_remaining = RemainingAmount.objects.create(customer=customer,remaining_amount = current_remaining)

        payment = PaymentIn.objects.create(remainings= new_remaining,**validated_data)
        return payment
    
    @transaction.atomic
    def update(self,instance,validated_data):
        
        payment_in = validated_data["payment_in"]
        remarks = validated_data.get("remarks","")

        current_remaining = instance.remainings.remaining_amount
        current_amount = instance.payment_in

        amount_to_calculate_on = current_remaining + current_amount

        latest_remaining = amount_to_calculate_on - payment_in
        
        instance.remainings.remaining_amount = latest_remaining
        instance.payment_in = payment_in
        instance.remarks = remarks

        instance.remainings.save()
        instance.save()
        return instance

