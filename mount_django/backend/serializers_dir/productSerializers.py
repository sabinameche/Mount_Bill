from ..models import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","uid","name","cost_price","selling_price","product_quantity","category","low_stock","created_at"]
        read_only_fields = ["id","uid","created_at","company","created_at"]
