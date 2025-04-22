from rest_framework import serializers
from .models import Order, OrderItem, KOT
from restaurant.models import MenuItem
from accounts.models import User

class OrderItemSerializer(serializers.ModelSerializer):
    # item_name = serializers.CharField(source='item.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['item'] = instance.item.name  # retain customer ID for clarity (optional)
        return rep

        

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    kot  = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    # restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    
    def get_kot(self, obj):
        try:
            kot = KOT.objects.get(order=obj)
            return KOTSerializer(kot).data
        except KOT.DoesNotExist:
            return None

    class Meta:
        model = Order
        fields = '__all__'
        # fields = ['id','customer_name', 'items','special_instructions', 'status','kot']  # include status
                 
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['customer_id'] = instance.customer_id.name  # retain customer ID for clarity (optional)
        return rep


# class KOTSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KOT
#         fields = '__all__'
class KOTSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    restaurant_name = serializers.CharField(source='order.restaurant.name', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    customer_name = serializers.CharField(source='order.customer.name', read_only=True)
    
    class Meta:
        model = KOT
        fields = [
            'id',
            'order',
            'order_id',
            'customer_name',
            'table_number',
            'created_at',
            'status',
            'restaurant_name',
            'order_items'
        ]
    
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj.order)
        return OrderItemSerializer(order_items, many=True).data
