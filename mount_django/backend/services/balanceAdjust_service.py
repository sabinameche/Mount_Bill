from ..models import BalanceAdjustment,RemainingAmount
from django.db import transaction

class BalanceAdjustService:

    @staticmethod
    @transaction.atomic
    def create_balance_adjustment(validated_data,company):
        adjust_type = validated_data.pop("adjust_btn_type")
        ajdustment_amount = validated_data["amount"]
        customer = validated_data["customer"]
        if adjust_type not in {"ADD","REDUCE"}:
            raise ValueError("Invalid ajustment type")
        
        latest_remaining = RemainingAmount.objects.filter(customer=customer).order_by('-id').first()

        amount = ajdustment_amount if adjust_type == 'ADD' else -ajdustment_amount
        current_remaining = latest_remaining.remaining_amount + amount

        new_remaining = RemainingAmount.objects.create(customer = customer,remaining_amount = current_remaining)
        balance_adjust_instance = BalanceAdjustment.objects.create(remainings = new_remaining,**validated_data)

        return balance_adjust_instance


        

