from ..models import ProductCategory
from rest_framework import serializers

class ProductCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields =["id","name"]

