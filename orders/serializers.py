from rest_framework import serializers
from .models import Order, OrderItem, KOT
from restaurant.models import MenuItem
from accounts.models import User

class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'restaurant_name', 'customer', 'customer_name', 'items',
                  'special_instructions', 'status']  # include status
        
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order

# class KOTSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KOT
#         fields = '__all__'
class KOTSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    restaurant_name = serializers.CharField(source='order.restaurant.name', read_only=True)
    
    class Meta:
        model = KOT
        fields = ['id', 'order', 'table_number', 'created_at', 'status', 'order_items', 'restaurant_name']
    
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj.order)
        return OrderItemSerializer(order_items, many=True).data
