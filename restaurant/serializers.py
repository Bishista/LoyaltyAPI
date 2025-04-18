from rest_framework import serializers
from .models import Restaurant, MenuItem, Booking, Review

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ['created_by']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['restaurant']

class BookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['expires_at','customer']
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['customer'] = instance.customer.id  # retain customer ID for clarity (optional)
        return rep

class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['customer'] = instance.customer.id  # retain customer ID for clarity (optional)
        return rep

