from rest_framework import serializers
from .models import Order, OrderItem, KOT
from restaurant.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'customer', 'items', 'special_instructions']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order

class KOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = KOT
        fields = '__all__'
