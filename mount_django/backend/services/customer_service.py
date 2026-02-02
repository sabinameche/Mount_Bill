from ..models import Customer,RemainingAmount
from django.db import transaction
class CustomerService:
    @staticmethod
    @transaction.atomic
    def create_customer(validated_data,company):
        opening_balance = validated_data.pop("opening_balance",0)
        customer_opening_type = validated_data.pop("customer_opening_type","TORECEIVE")

        # create customer
        customer = Customer.objects.create(**validated_data,company=company)

        amount = opening_balance
        if customer_opening_type == "TOGIVE":
            amount = -opening_balance
        elif customer_opening_type == "TORECIEVE":
            amount = opening_balance

        # creating remaining amount
        RemainingAmount.objects.create(customer=customer,remaining_amount = amount)

        return customer