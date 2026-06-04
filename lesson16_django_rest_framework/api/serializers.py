from rest_framework import serializers
from .models import Product

# 01.06 Smart Serializer
class ProductModelSerializer(serializers.ModelSerializer):
    productId = serializers.UUIDField(
        source='id', read_only=True, required=False
    )
    
    price_usd = serializers.SerializerMethodField()
    full_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ["productId", 'title', 'price','price_usd', 'description', 'full_info']
    
    def get_full_info(self, instance:Product):
        return f"$#{instance.id}_{instance.title}: {instance.price}"
    
    def get_price_usd(self, instance:Product):
        return round(instance.price/44.29, 2)


# 29.05 Default Serializer
class ProductSerializer(serializers.Serializer):
    productId = serializers.UUIDField(
        source='id', read_only=True, required=False
    )
    title = serializers.CharField(max_length=255, required=False)
    price = serializers.FloatField(required=False)
    description = serializers.CharField(required=False)
    
    price_usd = serializers.SerializerMethodField()
    full_info = serializers.SerializerMethodField()
    
    # def get_<method_field>
    def get_full_info(self, instance:Product):
        return f"$#{instance.id}_{instance.title}: {instance.price}"
    
    def get_price_usd(self, instance:Product):
        return round(instance.price/44.29, 2)
    
    # def validate_<field>
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price can not be lte 0")
        return value
    
    def create(self, validated_data):
        print("Validation data:", validated_data)
        return Product.objects.create(**validated_data)
    
    def update(self, instance:Product, validated_data):
        instance.title = validated_data['title']
        instance.price = validated_data['price']
        instance.description = validated_data['description']
        instance.save()
        return instance