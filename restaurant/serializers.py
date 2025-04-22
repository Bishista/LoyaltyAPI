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
        read_only_fields = ['expires_at','customer', 'restaurant']
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('restaurant', None)  # Hide restaurant in output
        rep['customer'] = instance.customer.id  # retain customer ID for clarity (optional)
        rep['table_number'] = instance.table_number  # Include table number in output
        return rep

# class ReviewSerializer(serializers.ModelSerializer):
#     customer_name = serializers.CharField(source='customer.name', read_only=True)
    
#     class Meta:
#         model = Review
#         fields = '__all__'
        
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         rep['customer'] = instance.customer.id  # retain customer ID for clarity (optional)
#         return rep

class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['customer']  # 💡 prevents manual setting of customer via POST

    def create(self, validated_data):
        # 🔐 Automatically assign logged-in user as customer
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['customer'] = instance.customer.id
        return rep
    
    
# serializers.py

from .models import RestaurantDetail

class RestaurantDetailSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = RestaurantDetail
        fields = '__all__'
        read_only_fields = []



