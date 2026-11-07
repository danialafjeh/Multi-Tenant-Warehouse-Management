from rest_framework import serializers



class ProductInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    sku = serializers.CharField()



class InventoryInfoSerializer(serializers.Serializer):
    total_quantity = serializers.DecimalField(max_digits=14, decimal_places=1)
    is_in_stock = serializers.BooleanField()



class ProductInventorySerializer(serializers.Serializer):
    product = ProductInfoSerializer()
    inventory = InventoryInfoSerializer()
    